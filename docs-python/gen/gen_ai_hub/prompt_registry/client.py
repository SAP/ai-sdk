from typing import Optional
from abc import ABC
from gen_ai_hub import GenAIHubProxyClient
from gen_ai_hub.proxy import get_proxy_client
from gen_ai_hub.proxy.gen_ai_hub_proxy.client import GenAIHubRestClient
from .models.prompt_template import (
    PromptTemplatePostRequest,
    PromptTemplatePostResponse,
    PromptTemplateGetResponse,
    PromptTemplateListResponse,
    PromptTemplateDeleteResponse,
    PromptTemplateSubstitutionRequest,
    PromptTemplateSubstitutionResponse,
    PromptTemplateSpec
)
from .models.orchestration_config import (
    OrchestrationConfigPostRequest,
    OrchestrationConfigPostResponse,
    OrchestrationConfigGetResponse,
    OrchestrationConfigListResponse,
    OrchestrationConfigDeleteResponse,
    OrchestrationConfig)

# Constants
PATH_SCENARIOS = "/lm/scenarios"
PATH_PROMPT_TEMPLATES = "/lm/promptTemplates"
CONTENT_TYPE_JSON_ = "application/json"
PATH_REGISTRY_CONFIG = "/registry/v2/orchestrationConfigs"
PATH_REGISTRY_SCENARIOS = "/registry/v2/scenarios"

class PromptRegistryClient(ABC):
    """
    Client for interacting with the Prompt Registry API.

    https://api.sap.com/api/PROMPT_REGISTRY_API/overview
    """
    def __init__(self, proxy_client: Optional[GenAIHubProxyClient] = None):
        """Initializes the PromptRegistryClient.

        :param proxy_client: Optional proxy client to use for requests.
        :type proxy_client: Optional[GenAIHubProxyClient], optional
        """
        self.proxy_client = proxy_client or get_proxy_client(proxy_version="gen-ai-hub")
        self.rest_client = GenAIHubRestClient(self.proxy_client)



class PromptTemplateClient(PromptRegistryClient):
    """
    Client for interacting with the Prompt Registry Prompt Template API.

    https://api.sap.com/api/PROMPT_REGISTRY_API/overview
    """

    def create_prompt_template(self, name: str, version: str, scenario: str,
                               prompt_template_spec: PromptTemplateSpec) -> PromptTemplatePostResponse:
        """Create or update a prompt template.

        :param name: the name of the prompt template.
        :type name: str
        :param version: the version of the prompt template.
        :type version: str
        :param scenario: the scenario name of the prompt template.
        :type scenario: str
        :param prompt_template_spec: the specification of the prompt template.
        :type prompt_template_spec: PromptTemplateSpec
        :return: A PromptTemplatePostResponse object.
        :rtype: PromptTemplatePostResponse
        """
        request = PromptTemplatePostRequest(scenario=scenario, name=name, version=version, spec=prompt_template_spec)
        response = self.rest_client.post(path=PATH_PROMPT_TEMPLATES,
                                         body=request.model_dump(by_alias=True, exclude_none=True),
                                         convert_body_to_camel_case=False)

        return PromptTemplatePostResponse(**response)

    def get_prompt_templates(self, scenario: str, name: str, version: str, retrieve: str = None,
                             include_spec: bool = None) -> PromptTemplateListResponse:
        """Retrieve the latest version of every prompt template based on the filters.

        :param scenario: the scenario name of the prompt template.
        :type scenario: str
        :param name: the name of the prompt template.
        :type name: str
        :param version: the version of the prompt template.
        :type version: str
        :param retrieve: both(default), imperative, declarative
        :type retrieve: str, optional
        :param include_spec: false(default), true
        :type include_spec: bool, optional
        :return: A PromptTemplateListResponse object.
        :rtype: PromptTemplateListResponse
        """
        query_params = {
            "scenario": scenario,
            "name": name,
            "version": version,
            "retrieve": retrieve,
            "include_spec": include_spec
        }

        response = self.rest_client.get(path=PATH_PROMPT_TEMPLATES, params=query_params)

        return PromptTemplateListResponse(**response)

    def get_prompt_template_by_id(self, template_id: str) -> PromptTemplateGetResponse:
        """Retrieve a specific version of the prompt template by ID.

        :param template_id: The ID of the prompt template to retrieve.
        :type template_id: str
        :return: A PromptTemplateGetResponse object.
        :rtype: PromptTemplateGetResponse
        """

        response = self.rest_client.get(path=f"{PATH_PROMPT_TEMPLATES}/{template_id}")

        return PromptTemplateGetResponse(**response)

    def get_prompt_template_history(self, scenario: str, name: str, version: str) -> PromptTemplateListResponse:
        """Retrieve the history of edits to the prompt template. Only for imperative managed prompt templates.

        :param scenario: The scenario name of the prompt template.
        :type scenario: str
        :param name: The name of the prompt template.
        :type name: str
        :param version: The version ID of the prompt template.
        :type version: str
        :return: A PromptTemplateListResponse object.
        :rtype: PromptTemplateListResponse
        """

        response = self.rest_client.get(f"{PATH_SCENARIOS}/{scenario}/promptTemplates/{name}/versions/{version}/history")

        return PromptTemplateListResponse(**response)

    def delete_prompt_template_by_id(self, template_id: str) -> PromptTemplateDeleteResponse:
        """Delete a specific version of the prompt template by ID.

        :param template_id: The ID of the prompt template to delete.
        :type template_id: str
        :return: A PromptTemplateDeleteResponse object.
        :rtype: PromptTemplateDeleteResponse
        """

        response = self.rest_client.delete(f"{PATH_PROMPT_TEMPLATES}/{template_id}")

        return PromptTemplateDeleteResponse(**response)

    def import_prompt_template(self, file: bytes) -> PromptTemplatePostResponse:
        """Import a runtime/declarative prompt template into the design time environment.

        :param file: binary file content
        :type file: bytes
        :return: A PromptTemplatePostResponse object.
        :rtype: PromptTemplatePostResponse
        """

        # Content-Type: multipart/form-data is added automatically by requests when a file is passed in the request.
        kwargs = {"files": {"file": file}}
        response = self.rest_client.post(path=f"{PATH_PROMPT_TEMPLATES}/import", **kwargs)
        return PromptTemplatePostResponse(**response)

    def export_prompt_template(self, template_id: str) -> bytes:
        """Export a design time template in a declarative compatible yaml file. Supports only single file export.

        :param template_id: The id of the prompt template to export.
        :type template_id: str
        :return: bytes: The content of the exported file
        :rtype: bytes
        """

        response = self.rest_client.get(path=f"{PATH_PROMPT_TEMPLATES}/{template_id}/export", return_bytes_content=True)

        return response

    def fill_prompt_template(self, scenario: str, name: str, version: str, input_params: dict,
                             metadata: bool = False) -> PromptTemplateSubstitutionResponse:
        """Replace the placeholders of the prompt template referenced via scenario-name-version 
        with user provided values.

        :param scenario: the scenario name of the prompt template.
        :type scenario: str
        :param name: the name of the prompt template.
        :type name: str
        :param version: the version of the prompt template.
        :type version: str
        :param input_params: User provided values to replace the placeholders of the prompt template.
        :type input_params: dict
        :param metadata: False(default), True return resource object with all details.
        :type metadata: bool, optional
        :return: A PromptTemplateSubstitutionResponse object.
        :rtype: PromptTemplateSubstitutionResponse
        """

        request =PromptTemplateSubstitutionRequest(input_params=input_params)
        kwargs = {'convert_body_to_camel_case': False}
        if metadata:
            kwargs.update({'params': {"metadata": metadata}})
        response = self.rest_client.post(path=(f"{PATH_SCENARIOS}/{scenario}/promptTemplates/{name}/versions/"
                                               f"{version}/substitution"),
                                         headers={"Content-Type": CONTENT_TYPE_JSON_},
                                         body=request.model_dump(by_alias=True),
                                         **kwargs)

        return PromptTemplateSubstitutionResponse(**response)

    def fill_prompt_template_by_id(self,
                                   template_id: str,
                                   input_params: dict,
                                   metadata: bool = False, ) -> PromptTemplateSubstitutionResponse:
        """Replace the placeholders of the prompt template referenced via template_id with user provided values.

        :param template_id: The ID of the prompt template.
        :type template_id: str
        :param input_params: User provided values to replace the placeholders of the prompt template.
        :type input_params: dict
        :param metadata: False(default), True return resource object with all details.
        :type metadata: bool, optional
        :return: A PromptTemplateSubstitutionResponse object.
        :rtype: PromptTemplateSubstitutionResponse
        """

        request =PromptTemplateSubstitutionRequest(input_params=input_params)
        kwargs = {'params': {"metadata": metadata}, 'convert_body_to_camel_case': False}
        response = self.rest_client.post(path=f"{PATH_PROMPT_TEMPLATES}/{template_id}/substitution",
                                         headers={"Content-Type": CONTENT_TYPE_JSON_},
                                         body=request.model_dump(by_alias=True),
                                         **kwargs)

        return PromptTemplateSubstitutionResponse(**response)

class OrchestrationConfigClient(PromptRegistryClient):
    """
    Client for interacting with the Prompt Registry Orchestration Config API.

    https://api.sap.com/api/PROMPT_REGISTRY_API/overview
    """
    def create_orchestration_config(self, name: str, version: str, scenario: str,
                                    spec: OrchestrationConfig | dict) -> OrchestrationConfigPostResponse:
        """Create an orchestration config.

        :param name: the name of the orchestration config.
        :type name: str
        :param version: the version of the orchestration config.
        :type version: str
        :param scenario: the scenario name of the orchestration config.
        :type scenario: str
        :param spec: the specification of the orchestration config.
        :type spec: Union[dict, OrchestrationConfig]

        :return: An OrchestrationConfigPostResponse object.
        :rtype: OrchestrationConfigPostResponse
        """
        request = OrchestrationConfigPostRequest(name=name, version=version, scenario=scenario, spec=spec)
        response = self.rest_client.post(path=PATH_REGISTRY_CONFIG,
                                         body=request.model_dump(by_alias=True, exclude_none=True),
                                         convert_body_to_camel_case=False)

        return OrchestrationConfigPostResponse(**response)

    def get_orchestration_configs(
            self, scenario: str, name: str, version: str, retrieve: str = None, include_spec: bool = None,
            resolve_template_ref:bool = None) -> OrchestrationConfigListResponse:
        """Retrieve the latest version of every orchestration config based on the filters.

        :param scenario: the scenario name of the orchestration config.
        :type scenario: str
        :param name: the name of the orchestration config.
        :type name: str
        :param version: the version of the orchestration config.
        :type version: str
        :param retrieve: both(default), imperative, declarative
        :type retrieve: str, optional
        :param include_spec: false(default), true
        :type include_spec: bool, optional
        :param resolve_template_ref: false(default), true
        :type resolve_template_ref: bool, optional

        :return: An OrchestrationConfigListResponse object.
        :rtype: OrchestrationConfigListResponse
        """
        query_params = {
            "scenario": scenario,
            "name": name,
            "version": version,
            "retrieve": retrieve,
            "include_spec": include_spec,
            "resolve_template_ref": resolve_template_ref
        }

        response = self.rest_client.get(path=PATH_REGISTRY_CONFIG, params=query_params,
                                        convert_params_to_camel_case=False)

        return OrchestrationConfigListResponse(**response)

    def get_orchestration_config_by_id(self, config_id: str, resolve_template_ref: bool = None
                                       ) -> OrchestrationConfigGetResponse:
        """Retrieve a specific version of the orchestration config by ID.

        :param config_id: The ID of the orchestration config to retrieve.
        :type config_id: str
        :param resolve_template_ref: false(default), true
        :type resolve_template_ref: bool, optional

        :return: An OrchestrationConfigGetResponse object.
        :rtype: OrchestrationConfigGetResponse"""

        query_params = {"resolve_template_ref": resolve_template_ref}
        response = self.rest_client.get(path=f"{PATH_REGISTRY_CONFIG}/{config_id}", params=query_params,
                                        convert_params_to_camel_case=False)
        return OrchestrationConfigGetResponse(**response)

    def get_orchestration_config_history(self, scenario: str, name: str, version: str, include_spec: bool = None,
                                         resolve_template_ref:bool = None) -> OrchestrationConfigListResponse:
        """Retrieve the history of edits to the orchestration config.

         :param scenario: The scenario name of the orchestration config.
         :type scenario: str
         :param name: The name of the orchestration config.
         :type name: str
         :param version: The version ID of the orchestration config.
         :type version: str
         :param include_spec: false(default), true
         :type include_spec: bool, optional
         :param resolve_template_ref: false(default), true
         :type resolve_template_ref: bool, optional

         :return: An OrchestrationConfigListResponse object.
         :rtype: OrchestrationConfigListResponse
         """
        response = self.rest_client.get(
            path=f"{PATH_REGISTRY_SCENARIOS}/{scenario}/orchestrationConfigs/{name}/versions/{version}/history",
            params={"include_spec": include_spec, "resolve_template_ref": resolve_template_ref},
            convert_params_to_camel_case=False
        )
        return OrchestrationConfigListResponse(**response)

    def delete_orchestration_config_by_id(self, config_id: str) -> OrchestrationConfigDeleteResponse:
        """Delete a specific version of the orchestration config by ID.

        :param config_id: The ID of the orchestration config.
        :type config_id: str

        :return: An OrchestrationConfigDeleteResponse object.
        :rtype: OrchestrationConfigDeleteResponse
        """

        response = self.rest_client.delete(f"{PATH_REGISTRY_CONFIG}/{config_id}")
        return OrchestrationConfigDeleteResponse(**response)

    def import_orchestration_config(self, file: bytes) -> OrchestrationConfigPostResponse:
        """Import a runtime/declarative orchestration config into the design time environment.

        :param file: binary file content
        :type file: bytes
        :return: A OrchestrationConfigPostResponse object.
        :rtype: OrchestrationConfigPostResponse
        """

        # Content-Type: multipart/form-data is added automatically by requests when a file is passed in the request.
        kwargs = {"files": {"file": file}}
        response = self.rest_client.post(path=f"{PATH_REGISTRY_CONFIG}/import", **kwargs)
        return OrchestrationConfigPostResponse(**response)

    def export_orchestration_config(self, config_id: str) -> bytes:
        """Export a design orchestration config  in a declarative compatible yaml file.
        Supports only single file export.

        :param config_id: The id of the orchestration config to export.
        :type config_id: str
        :return: bytes: The content of the exported file
        :rtype: bytes
        """

        response = self.rest_client.get(path=f"{PATH_REGISTRY_CONFIG}/{config_id}/export", return_bytes_content=True)

        return response

__all__ = ["PromptTemplateClient", "OrchestrationConfigClient"]