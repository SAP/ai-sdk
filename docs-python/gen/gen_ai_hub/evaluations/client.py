from typing import List
from ai_core_sdk.ai_core_v2_client import AICoreV2Client
from ai_api_client_sdk.models.model import Model
from gen_ai_hub.proxy.core.proxy_clients import get_proxy_client
from gen_ai_hub.evaluations.models.evaluation_config import EvaluationConfig
from gen_ai_hub.evaluations.constants import (
    DEFAULT_KEY,
    AWS_PROVIDER_KEY,
    INPUT_SECRET_SETUP_KEY,
    DEFAULT_SECRET_SETUP_KEY,
    ORCHESTRATION_URL_SETUP_KEY,
    AWS_S3_OSS_TYPE_KEY,
    SUPPORTED_OSS_TYPES,
    OBJECT_STORE_SECRET_EXISTS_MESSAGE,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
)
from gen_ai_hub.evaluations.utils.oss_secret_utils import (
    create_aws_object_store_secret,
    fetch_object_store_secret_by_name,
    delete_object_store_secret,
)
from gen_ai_hub.evaluations.utils.aicore_utils import (
    create_llm_orchestration_deployment_url,
    list_available_llm_models,
)
from gen_ai_hub.evaluations.exceptions.error_codes import ErrorCode
from gen_ai_hub.evaluations.helpers.collector import ValidationCollector
from gen_ai_hub.evaluations._internal._models import (
    _EvaluationConfigData,
    _AWSObjectStoreData,
)
from gen_ai_hub.evaluations.helpers.config_data import (
    extract_config_data,
    build_accumulated_config,
)
from gen_ai_hub.proxy import get_proxy_client
from gen_ai_hub.evaluations.utils.validation_utils import (
    validate_config_data_collection,
    validate_orchestration_url_across_configs,
)
from gen_ai_hub.evaluations.credentials import fetch_credentials
from gen_ai_hub.evaluations.models.evaluation_run import EvaluationRun
from gen_ai_hub.evaluations.helpers.evaluation_optimization_flow import (
    single_evaluation_job_flow,
    multiple_evaluation_jobs_flow,
)

from gen_ai_hub.evaluations.utils.orch_config_utils import (
    validate_orchestration_params_from_evaluation_config,
)

from gen_ai_hub.evaluations.utils.metric_client_utils import (
    fetch_all_system_predefined_metrics,
)

from gen_ai_hub.evaluations.helpers.logging import get_logger
from gen_ai_hub.orchestration_v2.service import get_orchestration_api_url

logger = get_logger()


def _has_mixed_config_types(evaluation_configs: List[EvaluationConfig]) -> bool:
    """Check if evaluation configs have mixed types (llm+template and orchestration_registry).

    A single execution cannot handle both types together, so this detection is used
    to determine if multiple executions are required.

    :param evaluation_configs: List of evaluation configuration objects
    :type evaluation_configs: List[EvaluationConfig]
    :return: True if configs contain both llm and orchestration_registry types
    :rtype: bool
    """
    if len(evaluation_configs) <= 1:
        return False

    has_llm = any(config.llm is not None for config in evaluation_configs)
    has_registry = any(config.orchestration_registry_reference is not None for config in evaluation_configs)

    return has_llm and has_registry


class EvaluationClient:
    """
    Base Client for the Evaluations service
    """

    def __init__(
        self,
        base_url: str,
        auth_url: str = None,
        client_id: str = None,
        client_secret: str = None,
        cert_str: str = None,
        key_str: str = None,
        cert_file_path: str = None,
        key_file_path: str = None,
        resource_group: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        ai_core_client: AICoreV2Client = None,
        orchestration_url: str = None,
        input_object_store_secret_name: str = None,
        provider_name: str = AWS_PROVIDER_KEY,  # later will be a mandatory param with no default value
    ):
        """
        EvaluationsClient root object to be used for Evaluations.

        :param base_url: Base URL of the AI Core instance (must include `/v2` suffix).
        :type base_url: str
        :param auth_url: Authentication URL used to retrieve access tokens.
        :type auth_url: str, optional
        :param client_id: OAuth client ID.
        :type client_id: str, optional
        :param client_secret: OAuth client secret.
        :type client_secret: str, optional
        :param cert_str: X.509 certificate content as a string.
        :type cert_str: str, optional
        :param key_str: X.509 private key content as a string.
        :type key_str: str, optional
        :param cert_file_path: File path to X.509 certificate.
        :type cert_file_path: str, optional
        :param key_file_path: File path to X.509 private key.
        :type key_file_path: str, optional
        :param resource_group: Resource group name within the AI Core instance.
        :type resource_group: str, optional
        :param aws_access_key_id: AWS access key ID.
        :type aws_access_key_id: str, optional
        :param aws_secret_access_key: AWS secret access key.
        :type aws_secret_access_key: str, optional
        :param ai_core_client: Pre-configured AI Core client instance.
        :type ai_core_client: AICoreV2Client, optional
        :param orchestration_url: Pre-existing orchestration deployment URL.
        :type orchestration_url: str, optional
        :param input_object_store_secret_name: Name of input object store secret.
        :type input_object_store_secret_name: str, optional
        :param provider_name: Hyperscaler provider name (e.g., "aws").
        :type provider_name: str, optional
        :raises ValueError: If required hyperscaler provider parameters are missing.
        """

        logger.info("Initializing the Evaluations client")
        self.base_url = base_url
        self.resource_group = resource_group
        self.ai_core_client = (
            ai_core_client
            if ai_core_client is not None
            else AICoreV2Client(
                base_url=base_url,
                auth_url=auth_url,
                client_id=client_id,
                client_secret=client_secret,
                cert_str=cert_str,
                key_str=key_str,
                cert_file_path=cert_file_path,
                key_file_path=key_file_path,
                resource_group=resource_group,
            )
        )

        self.__gen_ai_hub_proxy_client = get_proxy_client(
            proxy_version="gen-ai-hub",
            base_url=base_url,
            auth_url=auth_url,
            client_id=client_id,
            client_secret=client_secret,
            resource_group=resource_group,
        )
        self.__gen_ai_hub_proxy_client.ai_core_client = self.ai_core_client

        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.orchestration_url = orchestration_url
        self.user_provided_orchestration_url = (
            True if self.orchestration_url is not None else False
        )  # using this flag to figure out whether url has been passed from user to only validate in that case
        self.default_object_store_secret_name = None
        self.input_object_store_secret_name = input_object_store_secret_name
        self.provider_name = provider_name
        logger.info("Validating whether all the required params have been passed")
        self._validate_provider_params()
        logger.info("Initialization of the client completed!")

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{self.__class__.__name__}({attrs})"

    def _validate_provider_params(self):
        """
        Validate required hyperscaler provider parameters.
        :raises ValueError: If required provider parameters are missing.
        """
        # params related to aicore will fail if not provided when tried to initialise the AICOREV2 client
        errors = []
        provider_name = self.provider_name
        required_provider_params = []
        if provider_name == AWS_PROVIDER_KEY:
            required_provider_params = {
                AWS_ACCESS_KEY_ID.lower(): self.aws_access_key_id,
                AWS_SECRET_ACCESS_KEY.lower(): self.aws_secret_access_key,
            }
        # add support for other providers

        for key, value in required_provider_params.items():
            if value is None:
                errors.append(key)

        if errors:
            raise ValueError(
                f"Missing required hyperscalar provider params: {', '.join(errors)}"
            )

    @staticmethod
    def from_env(profile_name: str = None, **kwargs):
        """
        Alternative way to create an EvaluationClient object.

        Parameter resolution precedence:
        1. Explicit keyword arguments
        2. Environment variables
        3. Configuration file
        4. VCAP_SERVICES environment variable

        :param profile_name: Profile name defined in configuration.
        :type profile_name: str, optional
        :param kwargs: Additional parameters passed to constructor.
        :return: Configured EvaluationClient instance.
        :rtype: EvaluationClient
        """
        env_credentials = fetch_credentials(profile=profile_name, **kwargs)

        # if cert_url is present in the fetched credentials, rename it to auth_url
        if "cert_url" in env_credentials:
            env_credentials["auth_url"] = env_credentials.pop("cert_url")

        kwargs.update(env_credentials)
        return EvaluationClient(**kwargs)


    def validate_secret_type(self, secret_type: str, creator_mapping: dict):
        if secret_type not in creator_mapping:
            raise ValueError(
                f"Invalid object store secret type, please use one among the supported types: {SUPPORTED_OSS_TYPES}"
            )


    def create_or_update_object_store_secret(
        self,
        *,
        context,
        secret_body: dict,
        is_default: bool,
        result_key: str,
        attr_name: str,
        creator_mapping: dict,
        replace_existing: bool,
        result: dict,
    ):
        secret_type = secret_body.get("type") or AWS_S3_OSS_TYPE_KEY
        secret_name = secret_body.get("name") or DEFAULT_KEY

        self.validate_secret_type(secret_type, creator_mapping)

        try:
            response = creator_mapping[secret_type](
                context.aws_access_key_id,
                context.aws_secret_access_key,
                context.ai_core_client,
                context.resource_group,
                secret_body,
                is_default,
            )

            if response.message.lower() == OBJECT_STORE_SECRET_EXISTS_MESSAGE.lower():
                if not replace_existing:
                    raise ValueError(
                        f"{secret_name} Object store secret already exists. "
                        "Use replace_existing=True to overwrite."
                    )

                # delete and recreate
                delete_object_store_secret(
                    context.ai_core_client,
                    secret_name,
                    context.resource_group,
                )

                return self.create_or_update_object_store_secret(
                    context=context,
                    secret_body=secret_body,
                    is_default=is_default,
                    result_key=result_key,
                    attr_name=attr_name,
                    creator_mapping=creator_mapping,
                    replace_existing=False,
                    result=result,
                )

        except Exception as e:
            logger.exception(e)
            raise RuntimeError(
                f"Creation of {secret_name} object store secret failed with error: {e}"
            ) from e

        setattr(context, attr_name, secret_name)
        result[result_key] = secret_name


    def resolve_orchestration_deployment_url(self) -> str:
        """
        Resolves the orchestration deployment URL.

        For non-default resource groups, creates a new deployment.
        For default resource group, attempts to discover existing deployment
        with the default config name using the orchestration service,
        or creates one if not found.

        :return: The orchestration deployment URL.
        :rtype: str
        """
        # For non-default resource groups, create deployment directly
        if self.resource_group != DEFAULT_KEY:
            return create_llm_orchestration_deployment_url(
                self.ai_core_client,
                self.resource_group,
            )

        # For default resource group, try to discover existing deployment
        # using the orchestration service's get_orchestration_api_url function
        try:
            orchestration_url = get_orchestration_api_url(
                self.__gen_ai_hub_proxy_client,
            )
            logger.info("Found existing orchestration deployment: %s", orchestration_url)
            return orchestration_url
        except ValueError:
            # No deployment found, create a new one
            logger.info("No existing orchestration deployment found, creating new deployment")
            return create_llm_orchestration_deployment_url(
                self.ai_core_client,
                self.resource_group,
            )


    def setup(
        self,
        input_secret_body: dict | None = None,
        default_secret_body: dict | None = None,
        replace_existing: bool = False,
    ):
        """
        One time setup function which does object store secrets creation
        and orchestration deployment url creation if not provided.
        """

        secret_creator_mapping = {
            AWS_S3_OSS_TYPE_KEY: create_aws_object_store_secret,
        }

        result: dict = {}

        if input_secret_body:
            if not input_secret_body.get("name"):
                raise ValueError(
                    "name field is mandatory for creating input ObjectStore Secret"
                )

            self.create_or_update_object_store_secret(
                context=self,
                secret_body=input_secret_body,
                is_default=False,
                result_key=INPUT_SECRET_SETUP_KEY,
                attr_name="input_object_store_secret_name",
                creator_mapping=secret_creator_mapping,
                replace_existing=replace_existing,
                result=result,
            )

        if default_secret_body:
            self.create_or_update_object_store_secret(
                context=self,
                secret_body=default_secret_body,
                is_default=True,
                result_key=DEFAULT_SECRET_SETUP_KEY,
                attr_name="default_object_store_secret_name",
                creator_mapping=secret_creator_mapping,
                replace_existing=replace_existing,
                result=result,
            )

        if self.user_provided_orchestration_url:
            result[ORCHESTRATION_URL_SETUP_KEY] = self.orchestration_url
            return result

        orchestration_url = self.resolve_orchestration_deployment_url()
        self.orchestration_url = orchestration_url
        result[ORCHESTRATION_URL_SETUP_KEY] = orchestration_url

        logger.info("One time Setup complete with the created details %s!", result)
        return result
        
    def evaluate(
        self, evaluation_configs: List[EvaluationConfig]
    ) -> List[EvaluationRun]:
        """
        Main evaluate function to create the Evaluation job

        Parameters:
            evaluation_configs(List[EvaluationConfig]): A list of one or more of the EvaluationConfig objects
        Returns:
            List[EvaluationRun]: A list of EvaluationRun objects, one for each EvaluationConfig provided.

        """
        error_collector = ValidationCollector()
        # If is instance of one instance convert it to List
        if isinstance(evaluation_configs, EvaluationConfig):
            evaluation_configs = [evaluation_configs]
        try:
            # PRE STEP checking if setup is needed and missed
            if self.default_object_store_secret_name is None:
                # see if default secret exists in the rg
                response = fetch_object_store_secret_by_name(
                    self.ai_core_client,
                    DEFAULT_KEY,
                    self.resource_group,
                    error_collector,
                )

                if response is None:
                    error_collector.add_error(
                        ErrorCode.MISSING_DEFAULT_OBJECT_STORE_SECRET_ERROR.value,
                        "Default Object Store secret is required to run evaluate function. Please use setup() function to create one!",
                    )
                    self.default_object_store_secret_name = DEFAULT_KEY

            if self.orchestration_url is None:
                error_collector.add_error(
                    ErrorCode.MISSING_ORCHESTRATION_URL_ERROR.value,
                    "Orchestration deployment url is required to run evaluate function. Please use setup() function to create one or pass the value during initialization if already created",
                )

            # raises errors if any collected and missed for setup stage
            error_collector.raise_if_errors()

            # STEP0: getting data from files or config provided from the user.
            # For now the data object with only AWS creds-> need to extend further for other hyperscalers
            # can add a mapper her based on the provider type to incorporate other hyperscalers.
            object_store_credentials = {}
            if self.provider_name == AWS_PROVIDER_KEY:
                object_store_credentials = _AWSObjectStoreData(
                    aws_access_key_id=self.aws_access_key_id,
                    aws_secret_access_key=self.aws_secret_access_key,
                )

            # Pre-validation to validate if user provided both orchestration registry and (llm, template) combination
            validate_orchestration_params_from_evaluation_config(
                evaluation_configs, error_collector
            )

            error_collector.raise_if_errors()

            evaluation_configs_data: List[_EvaluationConfigData] = extract_config_data(
                evaluation_configs,
                self.ai_core_client,
                object_store_credentials,
                self.resource_group,
                self.__gen_ai_hub_proxy_client,
                error_collector,
            )
            # to catch any errors while trying to read the files and report
            error_collector.raise_if_errors()

            accumulated_config_data, single_execution_flow, reusable_artifact = (
                build_accumulated_config(
                    evaluation_configs_data,
                    _has_mixed_config_types(evaluation_configs)
                )
            )

            # validates the orchestration url for each run data along with custom metric config data
            if self.user_provided_orchestration_url:
                logger.info(
                    "Validating the orchestration Deployment URL, as it was explicitly passed during initialization and not set up automatically."
                )
                # only validate when the user provided the url
                validate_orchestration_url_across_configs(
                    accumulated_config_data,
                    self.orchestration_url,
                    self.ai_core_client,
                    self.resource_group,
                    error_collector,
                    self.__gen_ai_hub_proxy_client,
                )
                error_collector.raise_if_errors()

            validate_config_data_collection(
                accumulated_config_data,
                error_collector,
            )
            # raise any current errors and stop evaluate if any issues found in validation of the config provided
            error_collector.raise_if_errors()

            # Single Execution flow
            if single_execution_flow:
                evaluation_runs_list = single_evaluation_job_flow(
                    evaluation_configs,
                    accumulated_config_data,
                    self.input_object_store_secret_name,
                    object_store_credentials,
                    self.ai_core_client,
                    self.resource_group,
                    self.orchestration_url,
                    error_collector,
                )
                return evaluation_runs_list

            # Multiple Executions flow
            evaluation_runs_list = multiple_evaluation_jobs_flow(
                evaluation_configs,
                accumulated_config_data,
                self.input_object_store_secret_name,
                object_store_credentials,
                self.ai_core_client,
                self.resource_group,
                self.orchestration_url,
                reusable_artifact,
                error_collector,
            )
            return evaluation_runs_list
        except Exception as exc:
            # If validation errors were collected, raise them with details
            # Otherwise, re-raise the original exception
            error_collector.raise_if_errors()
            raise RuntimeError("Evaluate function failed!") from exc

    # UTIL functions in client
    def list_available_models(self):
        """
        Method to list all the available llm models
        """
        models_info: List[Model] = list_available_llm_models(
            self.ai_core_client, self.resource_group
        )
        parsed_models_info = []
        for current_model in models_info:
            model_extracted_details = current_model.__dict__
            allowed_scenarios_list = model_extracted_details["allowed_scenarios"]
            if any(
                scenario.get("scenario_id") == "orchestration"
                for scenario in allowed_scenarios_list
            ):
                version_details = [item.__dict__ for item in current_model.versions]
                filtered_details = {
                    k: model_extracted_details[k] for k in ["model", "provider"]
                }
                filtered_details["versions"] = version_details
                parsed_models_info.append(filtered_details)
        return parsed_models_info

    def get_system_supported_metrics(self) -> List[str]:
        """helper method to get the list of all supported metric ids"""
        error_collector = ValidationCollector()
        predefined_metric_templates = fetch_all_system_predefined_metrics(
            self.ai_core_client, self.resource_group, error_collector
        )
        return predefined_metric_templates

__all__ = ["EvaluationClient", "_has_mixed_config_types"]
