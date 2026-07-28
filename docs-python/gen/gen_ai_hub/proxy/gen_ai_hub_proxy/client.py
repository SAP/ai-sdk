from __future__ import annotations

import os

import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy
from datetime import datetime
from enum import Enum
from fnmatch import fnmatch
from typing import Any, ClassVar, Dict, List, Optional, Tuple, Type, Union

from ai_api_client_sdk.models.status import Status
from ai_core_sdk.ai_core_v2_client import AICoreV2Client
from pydantic import BaseModel, PrivateAttr, model_validator, Field, ConfigDict, ValidationError

from gen_ai_hub.proxy.core.base import BaseDeployment, BaseProxyClient
from gen_ai_hub.proxy.core.proxy_clients import proxy_clients
from gen_ai_hub.proxy.core.utils import warn_once

_temporary_headers_addition = ContextVar('temporary_headers_addition', default={})


class GenAIHubRestClient:
    """REST client with automatic header injection.

    This client wraps the AI Core rest_client and ensures that all requests include:
    - Instance-level headers (set via proxy_client.set_headers_addition)
    - Request-level headers (set via temporary_headers_addition context manager)

    :param proxy_client: The GenAIHubProxyClient instance to get the rest_client and headers from.
    """

    def __init__(self, proxy_client: 'GenAIHubProxyClient'):
        """Initialize the GenAIHubRestClient.

        :param proxy_client: The GenAIHubProxyClient instance to get the rest_client and headers from.
        """
        self._rest_client = proxy_client.ai_core_client.rest_client
        self._proxy_client = proxy_client

    def _inject_headers(self, kwargs: dict) -> dict:
        """Inject additional headers into the request kwargs.

        Only injects headers if there are additional headers to add.
        Base headers (AI-Client-Type, AI-Resource-Group) and Authorization
        are handled by the underlying RestClient.

        :param kwargs: The keyword arguments passed to the request method.
        :return: Updated kwargs with injected headers.
        """
        additional = self._proxy_client.get_additional_headers()
        if not additional:
            return kwargs  # No additional headers to inject

        headers = dict(additional)
        if kwargs.get('headers'):
            headers.update(kwargs['headers'])  # Explicit headers take precedence
        kwargs['headers'] = headers
        return kwargs

    def get(self, path: str, **kwargs):
        """Send a GET request with injected headers.

        :param path: The API path.
        :param kwargs: Additional arguments to pass to the underlying rest_client.
        :return: The response from the rest_client.
        """
        return self._rest_client.get(path=path, **self._inject_headers(kwargs))

    def post(self, path: str, **kwargs):
        """Send a POST request with injected headers.

        :param path: The API path.
        :param kwargs: Additional arguments to pass to the underlying rest_client.
        :return: The response from the rest_client.
        """
        return self._rest_client.post(path=path, **self._inject_headers(kwargs))

    def delete(self, path: str, **kwargs):
        """Send a DELETE request with injected headers.

        :param path: The API path.
        :param kwargs: Additional arguments to pass to the underlying rest_client.
        :return: The response from the rest_client.
        """
        return self._rest_client.delete(path=path, **self._inject_headers(kwargs))

    def patch(self, path: str, **kwargs):
        """Send a PATCH request with injected headers.

        :param path: The API path.
        :param kwargs: Additional arguments to pass to the underlying rest_client.
        :return: The response from the rest_client.
        """
        return self._rest_client.patch(path=path, **self._inject_headers(kwargs))


@contextmanager
def temporary_headers_addition(headers: Dict[str, str]):
    """Context manager to temporarily add headers to requests made by the GenAIHubProxyClient.

    :param headers: Headers to add temporarily.
    :type headers: Dict[str, str]
    """
    previous_temporary_headers = _temporary_headers_addition.set(headers)

    try:
        yield
    finally:
        _temporary_headers_addition.reset(previous_temporary_headers)


class Deployment(BaseDeployment):
    """Deployment class represents a deployment of a foundational model in the GenAI Hub."""
    url: str
    config_id: str
    config_name: str
    deployment_id: str
    model_name: str
    model_version: Optional[str] = None
    created_at: datetime
    additonal_parameters: Dict[str, str] = Field(default_factory=dict)
    custom_prediction_suffix: Optional[str] = None

    def __getattr__(self, name):
        """Get attribute from additional parameters if not found in the Deployment instance.

        :param name: Attribute name to get.
        :type name: str
        :raises err: If attribute not found in both Deployment instance and additional parameters.
        :return: Attribute value.
        :rtype: Any
        """
        try:
            super().__getattr__(name)
        except AttributeError as err:
            self.additonal_parameters: Dict[str, str]
            value = self.additonal_parameters.get(name, None)
            if value:
                return value
            raise err

    # abstractmethod implementations
    def additional_request_body_kwargs(self) -> Dict[str, Any]:
        return {}

    @classmethod
    def get_model_identification_kwargs(cls) -> Tuple[str]:
        """Get model identification keywords.

        :return: Tuple of model identification keywords.
        :rtype: Tuple[str]
        """
        return ('model_name', 'model_version', 'config_id', 'config_name', 'deployment_id')

    @property
    def prediction_url(self):
        if self.model_name.startswith("cohere"):
            return self.url.rstrip('/?') + '/chat' if self.url else ''
        return None


class FoundationalModelScenario(BaseModel):
    """Represents a foundational model scenario in the GenAI Hub."""
    model_config = ConfigDict(
        protected_namespaces=()
    )

    scenario_id: str
    config_names: Optional[Union[List[str], str]] = None
    model_name_parameter: str = 'model_name'
    prediction_url_suffix: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def adjust(cls, data: Any) -> Any:
        """Adjust input data before model initialization.

        :param data: Input data to adjust.
        :type data: Any
        :return: Adjusted data.
        :rtype: Any
        """
        if isinstance(data, dict):
            config_names = data.get('config_names', None)
            if isinstance(config_names, str):
                data['config_names'] = [config_names]
            elif config_names is None:
                data['config_names'] = ['*']
            prediction_url_suffix = data.get('prediction_url_suffix', None)
            if prediction_url_suffix is not None:
                data['prediction_url_suffix'] = '/' + prediction_url_suffix.lstrip('/')
        return data


def _deployment_matches(deployment: BaseDeployment, **search_key_value: Dict[str, str]):
    match = False
    for key, value in search_key_value.items():
        if value is None:
            continue
        deployment_value = getattr(deployment, key, None)
        if deployment_value is None:
            continue
        elif deployment_value != value:
            match = False
            break
        elif deployment_value == value and not match:
            match = True
    return match


class InvalidDeploymentBehavior(str, Enum):
    warn = 'warn'
    raise_error = 'raise_error'
    ignore = 'ignore'


@proxy_clients.register('gen-ai-hub')
class GenAIHubProxyClient(BaseProxyClient, extra='allow'):
    """GenAIHubProxyClient is a proxy client for interacting with the GenAI Hub."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    base_url: Optional[str] = None
    auth_url: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    resource_group: Optional[str] = None
    ai_core_client: Optional[AICoreV2Client] = None

    AI_CLIENT_TYPE_VAL: ClassVar[str] = 'GenAI Hub SDK (Python)' 

    # class attributes
    foundational_model_scenarios: ClassVar[List[FoundationalModelScenario]] = [
        FoundationalModelScenario(scenario_id='foundation-models', config_names='*', model_name_parameter='model_name'),
    ]
    default_values: ClassVar[Dict[str, Any]] = {}
    on_invalid_deployments: ClassVar[InvalidDeploymentBehavior] = InvalidDeploymentBehavior.warn

    # private_attributes
    _headers_addition: Dict[str, str] = PrivateAttr(default={})
    _deployments: List[Deployment] = PrivateAttr(default_factory=list)

    @model_validator(mode='before')
    @classmethod
    def init_client(cls, data: Any) -> Any:
        """Initialize the client with the provided data.

        :param data: Input data for client initialization.
        :type data: Any
        :return: Initialized data.
        :rtype: Any
        """
        if isinstance(data, dict):
            if data.get('ai_core_client', None) is not None:
                return data
            kwargs = {}
            for name in ['base_url', 'auth_url', 'client_id', 'client_secret', 'resource_group']:
                value = data.get(name, cls.default_values.get(name, None))
                if value is not None:
                    kwargs[name] = value
            # Set AI-Client-Type header specific to generated AI Hub SDK.
            # Is overwritten by environment variable AI_CLIENT_TYPE if set.
            kwargs['client_type'] = cls.AI_CLIENT_TYPE_VAL
            data['ai_core_client'] = AICoreV2Client.from_env(**kwargs)


        return data

    # abstract method implementations
    @property
    def request_header(self) -> Dict[str, Any]:
        return self.get_request_header()

    @property
    def deployments(self) -> List[Deployment]:
        return self.get_deployments()

    @property
    def deployment_class(self) -> Type[Deployment]:
        return Deployment

    def _get_matched_deployments(self, **search_key_value):
        return [deployment for deployment in self.deployments if _deployment_matches(deployment, **search_key_value)]

    def select_deployment(self, raise_on_multiple: bool = False, **search_key_value):
        if not search_key_value:
            raise ValueError('No key-value pairs provided for model discovery')

        if "model_version" in search_key_value and "model_name" not in search_key_value:
            raise ValueError('If a model version is specified for search, the model name must also be provided.')

        matched_deployments = self._get_matched_deployments(**search_key_value)
        if len(matched_deployments) == 0:
            self.update_deployments()
            matched_deployments = self._get_matched_deployments(**search_key_value)

        num_matches = len(matched_deployments)
        if num_matches == 1:
            return matched_deployments[0]
        elif num_matches > 1:
            if raise_on_multiple:
                raise ValueError(
                    "Multiple deployments match the query. Use 'raise_on_multiple=False' to return the first matching "
                    "deployment."
                )
            return matched_deployments[0]
        else:
            raise ValueError('No deployment found with: ' + ', '.join(
                [f'deployment.{k} == {v}' for k, v in search_key_value.items()]
            ))

    # public methods
    def get_additional_headers(self) -> Dict[str, str]:
        """Get only the additional headers (instance-level and request-level).

        :return: Additional headers.
        :rtype: Dict[str, str]
        """
        headers = dict(self._headers_addition)
        headers.update(_temporary_headers_addition.get())
        return headers

    def set_headers_addition(self, headers: Dict[str, str]):
        """Set additional headers for requests made by the client.

        :param headers: Headers to add.
        :type headers: Dict[str, str]
        """
        self._headers_addition = headers

    def get_request_header(self):
        """Get the request headers for requests made by the client.

        :return: Request headers.
        :rtype: Dict[str, str]
        """
        headers = deepcopy(self.ai_core_client.rest_client.headers)
        headers.update(self.get_additional_headers())
        if os.environ.get('SKIP_AUTHORIZATION', '').lower() != 'true':
            headers.update({'Authorization': self.get_ai_core_token()})

        return headers

    def get_deployments(self):
        """Get the list of deployments.

        :return: List of deployments.
        :rtype: List[Deployment]
        """
        if len(self._deployments) == 0:
            self.update_deployments()
        return self._deployments

    def _create_deployment(self, deployment, scenario_info):
        try:
            details = deployment.details["resources"]["backend_details"]["model"]
            additional_parameters = {
                "model_name": details["name"],
                "model_version": details["version"]
            }
        except KeyError:
            additional_parameters = config_parameters(scenario_info.model_name_parameter, self.ai_core_client, deployment)
        return Deployment(url=deployment.deployment_url,
                          deployment_id=deployment.id,
                          created_at=deployment.created_at,
                          config_id=deployment.configuration_id,
                          config_name=deployment.configuration_name,
                          custom_prediction_suffix=scenario_info.prediction_url_suffix,
                          **additional_parameters)

    def _handle_deployment_error(self, deployment, scenario_info, err):
        if self.on_invalid_deployments in [InvalidDeploymentBehavior.raise_error,
                                           InvalidDeploymentBehavior.warn]:
            msg = f'Failed to get all relevant information for deployment {deployment.id} ' + \
                  f'[scenario: {scenario_info.scenario_id}; config: {deployment.configuration_name}]! ' + \
                  'If this deployment is an LLM deployment make sure to set the model_name_parameter ' + \
                  'when registring the foundation model scenario or use a more rigorous ' + \
                  'config name filter. If the deployment is in the default foundation model scenario ' + \
                  'consider using a different scenario for you deployments.'
            if self.on_invalid_deployments == InvalidDeploymentBehavior.raise_error:
                raise RuntimeError(msg) from err
            else:
                warn_once(msg)
        elif self.on_invalid_deployments == InvalidDeploymentBehavior.ignore:
            pass
        else:
            raise ValueError(f'Invalid value for on_invalid_deployments: {self.on_invalid_deployments}')

    def _get_scenario_deployments(self, scenario_info: FoundationalModelScenario):
        deployments = {}
        query = self.ai_core_client.deployment.query(status=Status.RUNNING, scenario_id=scenario_info.scenario_id)

        resources_to_process = [
            deployment
            for deployment in query.resources
            if any(
                fnmatch(deployment.configuration_name, n)
                for n in scenario_info.config_names
            )
        ]

        with ThreadPoolExecutor() as executor:
            future_to_deployment = {
                executor.submit(
                    self._create_deployment, deployment, scenario_info
                ): deployment
                for deployment in resources_to_process
            }
            for future in as_completed(future_to_deployment):
                deployment = future_to_deployment[future]
                try:
                    deployments[deployment.id] = future.result()
                except ValidationError as err:
                    self._handle_deployment_error(deployment, scenario_info, err)

        return deployments

    def update_deployments(self):
        """Update the list of deployments from the GenAI Hub.

        :return: List of updated deployments.
        :rtype: List[Deployment]
        """
        deployment_set = {}  # use dict to remove duplicates based on deployment id
        # self.select_deployment.cache_clear()  # pylint: disable=no-member
        for scenario_info in self.foundational_model_scenarios:
            deployment_set.update(self._get_scenario_deployments(scenario_info))
        self._deployments = [*deployment_set.values()]
        self._deployments = sorted(self._deployments, key=lambda d: d.created_at, reverse=True)
        return self._deployments

    @classmethod
    def add_foundation_model_scenario(cls,
                                      scenario_id,
                                      config_names: Optional[List[str]] = None,
                                      prediction_url_suffix: Optional[str] = None,
                                      model_name_parameter: str = 'model_name'):
        """Add a foundational model scenario to the client.

        :param scenario_id: the scenario ID.
        :type scenario_id: str
        :param config_names: list of configuration names, defaults to None
        :type config_names: Optional[List[str]], optional
        :param prediction_url_suffix: prediction URL suffix, defaults to None
        :type prediction_url_suffix: Optional[str], optional
        :param model_name_parameter: model name parameter, defaults to 'model_name'
        :type model_name_parameter: str, optional
        """
        cls.foundational_model_scenarios.append(
            FoundationalModelScenario(scenario_id=scenario_id,
                                      config_names=config_names,
                                      model_name_parameter=model_name_parameter,
                                      prediction_url_suffix=prediction_url_suffix))
        for client in cls._instances.values():
            client._deployments = []

    def get_ai_core_token(self):
        """Get the AI core token for authentication.

        :return: AI core token.
        :rtype: str
        """
        return self.ai_core_client.rest_client.get_token()

    @classmethod
    def set_default_values(cls, **kwargs):
        """Set default values for the client."""
        cls.default_values.update(kwargs)

    @classmethod
    def for_profile(cls, profile: str = None):
        """Create a GenAIHubProxyClient instance for the given profile.

        :param profile: Profile name, defaults to None
        :type profile: str, optional
        :return: GenAIHubProxyClient instance.
        :rtype: GenAIHubProxyClient
        """
        return cls(ai_core_client=AICoreV2Client.from_env(profile_name=profile))


def camel_to_snake(name):
    """Convert camelCase or PascalCase string to snake_case.

    :param name: Input string in camelCase or PascalCase.
    :type name: str
    :return: String converted to snake_case.
    :rtype: str
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def config_parameters(model_name_parameter, ai_core_client, deployment):
    """Get configuration parameters for a deployment.

    :param model_name_parameter: the model name parameter.
    :type model_name_parameter: str
    :param ai_core_client: the AI core client.
    :type ai_core_client: AICoreV2Client
    :param deployment: the deployment.
    :type deployment: Deployment
    :return: Dictionary with model name and additional parameters.
    :rtype: Dict[str, Any]
    """
    model_parameters = {}
    config = ai_core_client.configuration.get(deployment.configuration_id)
    model_parameters['executable_id'] = config.executable_id
    for param in config.parameter_bindings:
        model_parameters[camel_to_snake(param.key)] = param.value
    return {'model_name': model_parameters.pop(model_name_parameter, None), 'additonal_parameters': model_parameters}
