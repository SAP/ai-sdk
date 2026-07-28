from typing import List

from ai_api_client_sdk.models.status import Status
from ai_core_sdk.ai_core_v2_client import AICoreV2Client
from gen_ai_hub.evaluations.exceptions.error_codes import ErrorCode
from gen_ai_hub.evaluations.helpers.collector import ValidationCollector
from gen_ai_hub.evaluations._internal._models import _EvaluationConfigData
from gen_ai_hub.evaluations.utils.aicore_utils import (
    fetch_deployment_config,
    fetch_configuration_by_id,
    call_orchestration_service_with_v2_config,
)
from gen_ai_hub.evaluations.utils.gen_utils import (
    create_model_versions_map_from_orch_configs,
    create_model_versions_map_from_configuration_param_bindings,
    select_model_details_randomly,
    validate_metrics,
    remove_filter_metrics_if_provider_not_supported,
    validate_variable_mapping_of_prompts,
    validate_variable_mapping_of_metrics,
    handle_missing_dependent_variables_in_dataset,
    handle_json_schema_match,
    handle_language_match,
    handle_reference_missing_rows,
    update_test_orch_config,
)

from gen_ai_hub.evaluations.utils.orch_config_utils import (
    validate_orch_config_mandatory_modules,
    validate_model_name_in_llm_module_config,
    validate_template_ref_absent_in_config,
    validate_if_template_list_is_empty_in_templating_module_config,
    validate_if_content_inside_template_is_empty_in_templating_module_config,
    validate_if_image_url_is_provided_in_content_type_inside_templating_module_config,
    validate_if_grounding_output_present_in_prompt_variables,
    validate_if_all_grounding_input_params_present_in_prompt_variables,
)


from gen_ai_hub.evaluations.helpers.logging import get_logger

logger = get_logger()


def validate_filtered_models(
    configuration_param_bindings,
    orchestration_config_data: List[dict],
    error_collector: ValidationCollector,
):
    run_config_model_versions_map = create_model_versions_map_from_orch_configs(
        orchestration_config_data, error_collector
    )
    orch_config_model_versions_map, model_filter_type = (
        create_model_versions_map_from_configuration_param_bindings(
            configuration_param_bindings, error_collector
        )
    )

    if not orch_config_model_versions_map:
        logger.info(
            "No model filter list provided — skipping model filtering.",
        )
        return

    if model_filter_type not in {"allow", "deny"}:
        error_collector.add_error(
            ErrorCode.INVALID_FILTER_TYPE_ERROR,
            f"Unsupported model filter type: {model_filter_type}. Expected 'allow' or 'deny'.",
        )
        return

    if model_filter_type == "allow":
        _validate_allowed_models(
            run_config_model_versions_map,
            orch_config_model_versions_map,
            error_collector,
        )
    else:  # deny
        _validate_denied_models(
            run_config_model_versions_map,
            orch_config_model_versions_map,
            error_collector,
        )


def _validate_allowed_models(
    run_models_map, allowed_models_map, error_collector: ValidationCollector
):
    for model_name, versions in run_models_map.items():
        for version in versions:
            if not _is_model_version_allowed(model_name, version, allowed_models_map):
                error_collector.add_error(
                    ErrorCode.MODEL_NOT_ALLOWED_ERROR.value,
                    f"Model '{model_name}' with version '{version}' from run/custom metric configuration, is not in the allowlist.",
                )


def _validate_denied_models(
    run_models_map, denied_models_map, error_collector: ValidationCollector
):
    for model_name, versions in run_models_map.items():
        for version in versions:
            if _is_model_version_denied(model_name, version, denied_models_map):
                error_collector.add_error(
                    ErrorCode.MODEL_NOT_ALLOWED_ERROR.value,
                    f"Model '{model_name}' with version '{version}' from run/custom metric configuration, is explicitly denied.",
                )


def _is_model_version_allowed(model_name, version, allowed_models_map):
    return (
        model_name in allowed_models_map and version in allowed_models_map[model_name]
    )


def _is_model_version_denied(model_name, version, denied_models_map):
    return model_name in denied_models_map and version in denied_models_map[model_name]


def fetch_and_validate_orchestration_config(
    ai_core_client: AICoreV2Client,
    configuration_id: str,
    orchestration_config_data: List[dict],
    resource_group: str,
    error_collector: ValidationCollector,
):
    configuration_response = fetch_configuration_by_id(
        configuration_id, ai_core_client, resource_group, error_collector
    )
    configuration_param_bindings = configuration_response.parameter_bindings
    validate_filtered_models(
        configuration_param_bindings,
        orchestration_config_data,
        error_collector,
    )


def validate_orchestration_url_across_configs(
    accumulated_config_data: List[_EvaluationConfigData] | _EvaluationConfigData,
    orchestration_url: str,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
    proxy_client=None,
):
    """wrapper function to perform validation of fetched config data in case of single vs multiple executions flow"""
    items = (
        accumulated_config_data
        if isinstance(accumulated_config_data, list)
        else [accumulated_config_data]
    )

    for current_config_data in items:
        validate_orchestration_url(
            current_config_data,
            orchestration_url,
            ai_core_client,
            resource_group,
            error_collector,
            proxy_client,
        )

def extract_deployment_id(orch_url) -> str:
    return orch_url.rstrip("/").split("/")[-1]

def validate_orchestration_url(
    evaluation_config_data: _EvaluationConfigData,
    orchestration_url: str,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
    proxy_client=None,
):
    """
    Validates if the orchestration deployment url provided via config resides in same
    resourceGroup as workload or not. Also validates if url is valid
    and orchestration deployment is not in terminal state
    """
    logger.info(
        "Validating the user provided Orchestration Deployment URL with a test orch config"
    )

    deployment_id = extract_deployment_id(orchestration_url)

    deployment_config = fetch_deployment_config(
        deployment_id, ai_core_client, resource_group, error_collector
    )

    deployment_status = deployment_config.status
    config_id = deployment_config.configuration_id
    orch_configs_data = evaluation_config_data.orch_config_data

    if deployment_status != Status.RUNNING:
        error_collector.add_error(
            ErrorCode.INVALID_DEPLOYMENT_STATUS,
            f"Deployment status is '{deployment_status}', expected 'RUNNING'.",
        )
        return

    fetch_and_validate_orchestration_config(
        ai_core_client, config_id, orch_configs_data, resource_group, error_collector
    )
    model_name, model_version = select_model_details_randomly(
        orch_configs_data, error_collector
    )
    test_orch_config = update_test_orch_config(
        model_name, model_version, error_collector
    )
    call_orchestration_service_with_v2_config(
        test_orch_config,
        ai_core_client,
        orchestration_url,
        resource_group,
        error_collector,
        proxy_client,
    )


def validate_orchestration_configuration(
    orchestration_config_data: List[dict],
    error_collector: ValidationCollector,
):
    """Validates the Orchestration configuration provided by user"""
    for orch_config in orchestration_config_data:
        validate_orch_config_mandatory_modules(orch_config, error_collector)
        validate_model_name_in_llm_module_config(orch_config, error_collector)
        validate_template_ref_absent_in_config(orch_config, error_collector)
        validate_if_template_list_is_empty_in_templating_module_config(
            orch_config, error_collector
        )
        validate_if_content_inside_template_is_empty_in_templating_module_config(
            orch_config, error_collector
        )
        validate_if_image_url_is_provided_in_content_type_inside_templating_module_config(
            orch_config, error_collector
        )
        validate_if_grounding_output_present_in_prompt_variables(
            orch_config, error_collector
        )
        validate_if_all_grounding_input_params_present_in_prompt_variables(
            orch_config, error_collector
        )


def validate_input_config(
    orchestration_config_data: List[dict],
    metrics: List[str],
    metric_templates: List[dict],
    error_collector: ValidationCollector,
):
    """Validates the input parameters of run data and metrics"""
    # Validates the metrics of the run data
    validate_metrics(
        metrics, metric_templates, orchestration_config_data, error_collector
    )
    # Validates the Orchestration configuration provided by user
    validate_orchestration_configuration(orchestration_config_data, error_collector)

    remove_filter_metrics_if_provider_not_supported(
        orchestration_config_data, metrics, error_collector
    )


def validate_variable_mapping_with_input_config(
    orchestration_config_data: List[dict],
    dataset_data: dict,
    variable_mapping: dict,
    metrics: List[str],
    metric_templates: List[dict],
    error_collector: ValidationCollector,
):
    """
    Validates all the required variable mappings provided in input config with a zero-tolerance failure threshold.

    Args:
        orchestration_config_data(list): Orchestration run configuration
        dataset_data (dict): Dataset rows to validate
        variable_mapping (dict): The variable mapping provided in the input configuration.
        metrics (list[str]): List of metrics provided in the input configuration.
        metric_templates (list[dict]): Metric templates information resolved from Metric Management Service
        error_collector (ValidationCollector): To accumulate the errors occurred during the process
    Raises:
        ValidationError: If any required variable mapping is invalid or the default column does not exist in the dataset.
    """
    validate_variable_mapping_of_prompts(
        orchestration_config_data, dataset_data, variable_mapping, error_collector
    )
    validate_variable_mapping_of_metrics(
        metrics, metric_templates, dataset_data, variable_mapping, error_collector
    )


def validate_config_data_collection(
    accumulated_config_data: List[_EvaluationConfigData] | _EvaluationConfigData,
    error_collector: ValidationCollector,
):
    """wrapper function to perform validation of fetched config data in case of single vs multiple executions flow"""
    items = (
        accumulated_config_data
        if isinstance(accumulated_config_data, list)
        else [accumulated_config_data]
    )

    for current_config_data in items:
        validate_merged_config_data(current_config_data, error_collector)


def validate_merged_config_data(
    evaluation_config_data: _EvaluationConfigData,
    error_collector: ValidationCollector,
):
    """handles the validation of config provided from the user"""

    orchestration_config_data = evaluation_config_data.orch_config_data
    metrics = evaluation_config_data.metrics_list
    dataset_data = evaluation_config_data.dataset_data
    variable_mapping = evaluation_config_data.variable_mapping
    metric_templates = evaluation_config_data.metric_templates
    validate_input_config(
        orchestration_config_data, metrics, metric_templates, error_collector
    )
    # validates the variable mapping provided in the input config
    validate_variable_mapping_with_input_config(
        orchestration_config_data,
        dataset_data,
        variable_mapping,
        metrics,
        metric_templates,
        error_collector,
    )
    # validates whether the dependent variables for the metrics provided exist in the datset
    handle_missing_dependent_variables_in_dataset(
        dataset_data, metrics, metric_templates, variable_mapping, error_collector
    )
    # validates whether the json_schema_match metric is provided in input config, then a valid schema needs to be provided
    handle_json_schema_match(metrics, dataset_data, variable_mapping, error_collector)
    # validates whether the language_match metric is provided in input config, then a valid schema needs to be provided
    handle_language_match(metrics, dataset_data, variable_mapping, error_collector)
    # handles the case where a single reference is provided in the input config, treats it as a golden reference and populates all the rows of test data
    handle_reference_missing_rows(
        dataset_data, variable_mapping, metrics, error_collector
    )
    return
