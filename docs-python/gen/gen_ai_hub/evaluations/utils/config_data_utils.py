from ai_core_sdk.ai_core_v2_client import AICoreV2Client
from gen_ai_hub.evaluations.helpers.collector import ValidationCollector
from gen_ai_hub.orchestration_v2.models.template_ref import TemplateRef
from gen_ai_hub.evaluations.models.evaluation_config import EvaluationConfig
from gen_ai_hub.evaluations.models.artifact_source import ArtifactSource
from gen_ai_hub.evaluations.models.dataset_config import Dataset
from gen_ai_hub.evaluations.exceptions.error_codes import ErrorCode
from gen_ai_hub.evaluations._internal._models import _AWSObjectStoreData
from gen_ai_hub.evaluations.constants import (
    PROMPT_TEMPLATE_METADATA_FIELDS,
    PROMPT_TEMPLATE_ID_KEY,
    TEST_PROMPT_TEMPLATE_NAME,
    TEST_PROMPT_TEMPLATE_VERSION,
    EVALUATIONS_SCENARIO_ID,
)
from gen_ai_hub.evaluations.utils.aicore_utils import (
    resolve_artifact_path,
    fetch_orchestration_config_from_registry,
    generate_random_id,
)
from gen_ai_hub.evaluations.utils.file_utils import (
    load_config_file,
)
from gen_ai_hub.evaluations.utils.gen_utils import resolve_orchestration_config_v2
from gen_ai_hub.proxy.gen_ai_hub_proxy.client import GenAIHubProxyClient
from gen_ai_hub.prompt_registry.client import PromptTemplateClient
from gen_ai_hub.prompt_registry.models.prompt_template import (
    PromptTemplateSpec,
    PromptTemplate,
)
from gen_ai_hub.evaluations.helpers.logging import get_logger

logger = get_logger()


def _fetch_template_by_guid(
    prompt_template_client: PromptTemplateClient,
    prompt_template_id: str,
    error_collector: ValidationCollector,
):
    try:
        response = prompt_template_client.get_prompt_template_by_id(prompt_template_id)
        return response.spec.template
    except Exception as e:
        error_collector.add_error(
            ErrorCode.PROMPT_TEMPLATE_GET_ERROR,
            f"Error: {e} while fetching the prompt template from this uuid: {prompt_template_id} from the prompt registry.",
        )
        return None


def _register_prompt_template(
    template_data,
    prompt_template_client: PromptTemplateClient,
    error_collector: ValidationCollector,
):
    try:
        if not isinstance(template_data, PromptTemplateSpec):
            # handling for the case when just a prompt template str is passed.
            template_data = PromptTemplateSpec(template=template_data)

        random_id = generate_random_id()[:7]
        prompt_template_name = TEST_PROMPT_TEMPLATE_NAME + random_id

        response = prompt_template_client.create_prompt_template(
            name=prompt_template_name,
            version=TEST_PROMPT_TEMPLATE_VERSION,
            scenario=EVALUATIONS_SCENARIO_ID,
            prompt_template_spec=template_data,
        )
        return response.id
    except Exception as e:
        error_collector.add_error(
            ErrorCode.REGISTER_PROMPT_TEMPLATE_ERROR,
            f"Registering Prompt template to Prompt registry failed with this error of:{e}",
        )
        return None


def _get_prompt_template_uuid_by_metadata(
    prompt_template_client: PromptTemplateClient,
    template_ref: TemplateRef,
    error_collector: ValidationCollector,
):
    """Fetch template using metadata parameters and return uuid"""
    try:
        # Convert TemplateRef to dict (using model_dump for Pydantic v2)
        template_ref_dict = template_ref.model_dump() if hasattr(template_ref, 'model_dump') else template_ref.to_dict()
        template_ref_data = template_ref_dict["template_ref"]
        response = prompt_template_client.get_prompt_templates(
            scenario=template_ref_data["scenario"],
            name=template_ref_data["name"],
            version=template_ref_data["version"],
        )
        prompt_template_id = response.resources[0].id
        return prompt_template_id
    except Exception as e:
        error_collector.add_error(
            ErrorCode.GENERIC_ERROR,
            f"Prompt template fetch failed for the provided matching of the metadata for the provided {template_ref}, failed with the error of {e}",
        )


def get_orch_config_data(
    evaluation_config: EvaluationConfig,
    ai_core_client: AICoreV2Client,
    gen_ai_hub_proxy_client: GenAIHubProxyClient,
    error_collector: ValidationCollector,
):
    orchestration_config_data = []
    prompt_template_client = PromptTemplateClient(gen_ai_hub_proxy_client)
    llm = evaluation_config.llm
    template_info = evaluation_config.template
    orchestration_registry_reference = (
        evaluation_config.orchestration_registry_reference
    )

    # check if one of the llm and template is provided, then it is invalid config
    if (llm is None) != (template_info is None):
        error_collector.add_error(
            ErrorCode.INVALID_ORCHESTRATION_CONFIG_ERROR,
            "Only llm or only template cannot be provided for a orchestration config, please provide both or a different way of EvaluationConfig",
        )

    if llm is not None and template_info is not None:
        template_data = []
        prompt_template_uuid = ""
        if isinstance(template_info, str):
            # template just as str-> so convert to the required dict
            template_data = [PromptTemplate(role="user", content=template_info)]

            # get the corresponding uuid by uploading this prompt to prompt registry.
            prompt_template_uuid = _register_prompt_template(
                template_data, prompt_template_client, error_collector
            )

        elif isinstance(template_info, PromptTemplateSpec):
            # no need to convert as provided is already a template dict
            template_data = template_info.template
            # get the corresponding uuid by uploading this prompt to prompt registry.
            prompt_template_uuid = _register_prompt_template(
                template_info, prompt_template_client, error_collector
            )

        elif isinstance(template_info, TemplateRef):
            # orchestration_v2 has nested structure: template_info.template_ref contains TemplateRefByID or TemplateRefByScenarioNameVersion
            template_ref_inner = template_info.template_ref

            if hasattr(template_ref_inner, PROMPT_TEMPLATE_ID_KEY):
                # to load data from uuid
                prompt_template_uuid = template_ref_inner.id
                template_data = _fetch_template_by_guid(
                    prompt_template_client, prompt_template_uuid, error_collector
                )

            elif all(
                hasattr(template_ref_inner, key) for key in PROMPT_TEMPLATE_METADATA_FIELDS
            ):
                prompt_template_uuid = _get_prompt_template_uuid_by_metadata(
                    prompt_template_client, template_info, error_collector
                )
                template_data = _fetch_template_by_guid(
                    prompt_template_client, prompt_template_uuid, error_collector
                )

            else:
                error_collector.add_error(
                    ErrorCode.INVALID_TEMPLATE_REFERENCE_KEY,
                    "Invalid template reference format, either use uuid or scenario/name/version format",
                )
        # converting all template formats given back to uuid to be used for simplified executable
        evaluation_config.template = prompt_template_uuid
        orchestration_config_data = resolve_orchestration_config_v2(template_data, llm)
    elif orchestration_registry_reference is not None:
        # To handle both uuid and scenario/name/version
        orchestration_config_data = fetch_orchestration_config_from_registry(
            orchestration_registry_reference, ai_core_client, error_collector
        )
    logger.info(
        "The orchestration config that is being generated from the provided config is %s",
        orchestration_config_data,
    )

    return orchestration_config_data


def get_dataset_data(
    dataset_config: Dataset,
    ai_core_client: AICoreV2Client,
    object_store_credentials: _AWSObjectStoreData,
    resource_group: str,
    error_collector: ValidationCollector,
):
    if isinstance(dataset_config.source, ArtifactSource):
        # needs to resolve loading via artifact
        return resolve_artifact_path(
            dataset_config.source,
            ai_core_client,
            object_store_credentials,
            resource_group,
            error_collector,
        )
    return load_config_file(dataset_config.source, error_collector)
