import json
import re
import random
import pandas as pd
from collections import defaultdict
from typing import List, Any, Dict, Optional, Set, Tuple
from gen_ai_hub.orchestration_v2.models.llm_model_details import LLMModelDetails as LLM
from gen_ai_hub.prompt_registry.models.prompt_template import PromptTemplate
from gen_ai_hub.evaluations.constants import (
    VARIABLE_MAPPING_DATA_PREFIX_KEY,
    MODEL_NAME_KEY,
    MODEL_VERSION_KEY,
    MODEL_CONFIGURATION_KEY,
    LATEST_MODEL_VERSION_KEY,
    MODEL_FILTER_LIST_KEY,
    MODEL_FILTER_LIST_TYPE_KEY,
    TEMPLATE_KEY,
    CONTENT_FILTER_ON_INPUT_METRIC_ID,
    CONTENT_FILTER_ON_OUTPUT_METRIC_ID,
    INPUT_VARIABLE_REGEX_PATTERN,
    VALIDATION_REGEX_PATTERN_FOR_INPUT_VARIABLES,
    PREDEFINED_SYSTEM_VARIABLES_LIST,
    AICORE_LLM_PROMPT_TEMPLATE_KEY,
    AICORE_LLM_COMPLETION_KEY,
    PROMPT_KEY,
    ALL_METRICS_COLUMN_MAPPING_KEY,
    COLUMN_MAPPING_DEFAULT_KEYS,
    JSON_SCHEMA_MATCH_METRIC_ID,
    JSON_SCHEMA_KEY,
    LANGUAGE_MATCH_METRIC_ID,
    LANGUAGE_KEY,
    REFERENCE_KEY,
    AZURE_CONTENT_SAFETY_KEY,
    FILTERS_KEY,
    LLAMA_GUARD_CONTENT_SAFETY_KEY,
    TYPE_KEY,
    MODEL_KEY,
    MODULES_KEY,
    PROMPT_TEMPLATING_KEY,
    ORCHESTRATION_CONFIGURATION_V2,
    CONFIG_KEY,
    ORCHESTRATION_CONFIG_TEMPLATE_V2,
    LLM_MODULE_V2_NAME_KEY,
    LLM_MODULE_V2_PARAMETERS_KEY,
    LLM_MODULE_V2_VERSION_KEY,
    PROMPT_REGISTRY_ROLE_KEY,
    PROMPT_REGISTRY_CONTENT_KEY,
    SYSTEM_DEFINED_METRIC_MAPPING,
    LLM_AS_A_JUDGE,
    ID,
    VARIABLES_KEY,
    NAME_KEY,
)
from gen_ai_hub.evaluations._internal._models import _EvaluationConfigData
from gen_ai_hub.evaluations.helpers.collector import ValidationCollector
from gen_ai_hub.evaluations.exceptions.error_codes import ErrorCode
from gen_ai_hub.evaluations.utils.language_match_utils import LanguageMapper
from gen_ai_hub.evaluations.models.artifact_source import ArtifactSource
from gen_ai_hub.evaluations.helpers.logging import get_logger

logger = get_logger()


def update_variable_mapping(
    variable_mapping: dict, prefix_key: str, variable_mapping_dict: dict
) -> dict:
    for key, value in variable_mapping.items():
        key = prefix_key + key
        value = VARIABLE_MAPPING_DATA_PREFIX_KEY + value
        variable_mapping_dict[key] = value

    return variable_mapping_dict


def get_accumulated_config_data(evaluation_configs_data: List[_EvaluationConfigData]) -> _EvaluationConfigData:
    # case when all dataset data and all metrics across all evaluation configs are the same.
    accumulated_orchestration_config_data: List[dict] = []
    accumulated_metrics_list: List[str] = evaluation_configs_data[0].metrics_list
    accumulated_variable_mapping: dict = {}
    accumulated_dataset_data: Any = evaluation_configs_data[0].dataset_data
    dataset_file_type: str = evaluation_configs_data[0].dataset_type
    accumulated_metric_templates: List[dict] = evaluation_configs_data[
        0
    ].metric_templates
    try:
        for evaluation_config_data in evaluation_configs_data:
            # accumulating only orchestration config data and variable mapping
            accumulated_orchestration_config_data.extend(  # we already get the data as a list
                evaluation_config_data.orch_config_data
            )
            if evaluation_config_data.variable_mapping is not None:
                accumulated_variable_mapping.update(
                    evaluation_config_data.variable_mapping
                )

        result = _EvaluationConfigData(
            orch_config_data=accumulated_orchestration_config_data,
            metrics_list=accumulated_metrics_list,
            metric_templates=accumulated_metric_templates,
            variable_mapping=accumulated_variable_mapping,
            dataset_data=accumulated_dataset_data,
            dataset_type=dataset_file_type,
        )

        return result
    except Exception as e:
        raise RuntimeError(
            f"Failed to accumulate data across multiple evaluation configs provided with error of {e}"
        ) from e


def set_model_details_from_run_configs(orch_config) -> Optional[Tuple[str, str]]:
    """
    Sets the model name and version from the run data if available.
    If not available, it returns None.
    """
    try:
        llm_module = orch_config[MODULES_KEY][PROMPT_TEMPLATING_KEY][MODEL_KEY]
        llm_model = llm_module.get("name")
        if not llm_model:
            return None
        llm_version = llm_module.get("version") or "latest"
        return llm_model, llm_version
    except (KeyError, TypeError):
        return None


def create_model_versions_map_from_orch_configs(
    orchestration_configs_data: List[dict], error_collector: ValidationCollector
) -> Optional[Dict[str, List[str]]]:
    model_versions_map = defaultdict(list)
    for orch_config in orchestration_configs_data:
        model_details = set_model_details_from_run_configs(orch_config)

        if model_details:
            llm_model, llm_version = model_details
            model_versions_map[llm_model].append(llm_version)

    if not model_versions_map:
        error_collector.add_error(
            ErrorCode.EMPTY_FIELD_NAME_ERROR, "No models found in run data."
        )
        return None

    return model_versions_map


def parse_model_filter_list(param, error_collector: ValidationCollector) -> List:
    """Parse and return model filter list from a param."""
    try:
        model_list = param.value

        if model_list == "null":
            model_list = None

        if model_list is None:
            return []

        if isinstance(model_list, str):
            model_list = json.loads(model_list)

        if not isinstance(model_list, list):
            error_collector.add_error(
                ErrorCode.GENERIC_ERROR, "modelFilterList must be a list"
            )
            return []

        return model_list

    except (json.JSONDecodeError, TypeError) as e:
        error_collector.add_error(
            ErrorCode.GENERIC_ERROR,
            f"Failed to parse modelFilterList, Invalid modelFilterList format in parameterBindings with error of {e}",
        )
        return []


def build_model_versions_map(model_list) -> Dict[str, List[str]]:
    """Builds a map of model names to their versions."""
    model_versions_map = defaultdict(list)
    if not model_list:
        return model_versions_map
    for model_entry in model_list:
        model_name = model_entry.get("modelName")
        versions = model_entry.get("modelVersions", [])
        if model_name:
            model_versions_map[model_name].extend(versions)
    return model_versions_map


def create_model_versions_map_from_configuration_param_bindings(
    param_bindings, error_collector: ValidationCollector
) -> Tuple[Dict[str, List[str]], Optional[str]]:
    model_versions_map = defaultdict[Any, list](list)
    model_filter_type = None

    for param in param_bindings:
        if param.key == MODEL_FILTER_LIST_KEY:
            model_list = parse_model_filter_list(param, error_collector)
            model_versions_map = build_model_versions_map(model_list)
        elif param.key == MODEL_FILTER_LIST_TYPE_KEY:
            model_filter_type = param.value

    return model_versions_map, model_filter_type


def create_model_versions_map_from_custom_metric_config(custom_metric_config_data) -> Dict[str, List[str]]:
    model_versions_map = defaultdict(list)
    if not custom_metric_config_data:
        return model_versions_map

    for metric in custom_metric_config_data:
        model_config = metric.get(MODEL_CONFIGURATION_KEY, {})
        model_name = model_config.get(MODEL_NAME_KEY)
        model_version = model_config.get(MODEL_VERSION_KEY) or LATEST_MODEL_VERSION_KEY

        if model_name and model_version:
            model_versions_map[model_name].append(model_version)

    return model_versions_map


def select_model_details_randomly(
    orchestration_config_data: List[dict],
    error_collector: ValidationCollector,
) -> Optional[Tuple[str, str]]:
    """
    Selects at random, model name and version from the list of model names and versions provided by the users run data.
    """
    model_versions_map = create_model_versions_map_from_orch_configs(
        orchestration_config_data, error_collector
    )

    if not model_versions_map:
        return None

    model_name = random.choice(list(model_versions_map))
    model_version = random.choice(model_versions_map[model_name])
    logger.info(
        f"Randomly chosen model and version is: {model_name} & {model_version}",
    )
    return model_name, model_version


def update_test_orch_config(
    model_name, model_version, error_collector: ValidationCollector
) -> Optional[dict]:
    try:
        ORCHESTRATION_CONFIGURATION_V2[CONFIG_KEY][MODULES_KEY][PROMPT_TEMPLATING_KEY][
            MODEL_KEY
        ].update(
            {
                "name": model_name,
                "version": model_version,
            }
        )
        return ORCHESTRATION_CONFIGURATION_V2[CONFIG_KEY]
    except Exception as e:
        error_collector.add_error(
            ErrorCode.ORCHESTRATION_URL_VALIDATION_ERROR,
            f"Error updating model name and version in TEST_ORCH_CONFIG: Key Error: {e}",
        )
        return None


def has_filter_key(orch_config: dict) -> bool:
    """
    Check if the 'filtering' key is present in the orchestration config.

    :param orch_config: Orchestration configuration dictionary.
    :type orch_config: dict
    :return: True if filtering key is present, False otherwise.
    :rtype: bool
    """
    return "filtering" in orch_config.get(MODULES_KEY, {})


def get_filter_config(orch_config: dict) -> dict:
    """
    Extract the filtering configuration from the orchestration config.

    :param orch_config: Orchestration configuration dictionary.
    :type orch_config: dict
    :return: Filtering configuration dictionary, or empty dict if not present.
    :rtype: dict
    """
    return orch_config.get(MODULES_KEY, {}).get("filtering", {})


def check_if_content_filter_provider_supported(
    orch_config: dict, error_collector: ValidationCollector
) -> bool:
    """
    Validates if all filters in the filtering module configuration are of supported types.

    :param orch_config: Orchestration configuration dictionary.
    :type orch_config: dict
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: True if all filters are supported or no filtering is configured, False otherwise.
    :rtype: bool
    """
    if not has_filter_key(orch_config):
        return True
    filter_config = get_filter_config(orch_config)

    for section_name, section in filter_config.items():
        for filter_obj in section[FILTERS_KEY]:
            if filter_obj.get(TYPE_KEY) not in {
                AZURE_CONTENT_SAFETY_KEY,
                LLAMA_GUARD_CONTENT_SAFETY_KEY,
            }:
                error_collector.add_error(
                    ErrorCode.UNSUPPORTED_FILTER_TYPE_ERROR,
                    f"In provided orch config of {orch_config}, found unsupported filter type '{filter_obj[TYPE_KEY]}' "
                    f"in section '{section_name}'. Only '{AZURE_CONTENT_SAFETY_KEY}' is supported.",
                )
                return False

    return True


def remove_filter_metrics_if_provider_not_supported(
    orchestration_config_data: List[dict],
    metrics: List[str],
    error_collector: ValidationCollector,
) -> None:
    """Removes content filter-related metric IDs from the metrics list if the content filter
    provider is not supported for any of the runs in orchestration_config_data."""
    is_content_filter_provider_supported = True
    for orch_config in orchestration_config_data:
        if is_content_filter_provider_supported:
            is_content_filter_provider_supported = (
                check_if_content_filter_provider_supported(orch_config, error_collector)
            )
    if not is_content_filter_provider_supported:
        metrics[:] = [
            metric
            for metric in metrics
            if metric
            not in {
                CONTENT_FILTER_ON_INPUT_METRIC_ID,
                CONTENT_FILTER_ON_OUTPUT_METRIC_ID,
            }
        ]


def create_custom_metric_name(
    custom_metric_config: dict, error_collector: ValidationCollector
) -> str:
    """
    Creates a custom metric name based on the provided custom metric configuration.

    :param custom_metric_config: Dictionary containing metric configuration.
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :return: A string representing the custom metric name.
    :raises ValidationError: If required fields are missing or invalid.
    """

    # Extract required fields
    metric_id = custom_metric_config.get("metricId")
    scenario = custom_metric_config.get("scenario")
    metric_name = custom_metric_config.get("metricName")
    version = custom_metric_config.get("version")

    # Validate inputs
    if not metric_id:
        if not scenario:
            error_collector.add_error(
                ErrorCode.GENERIC_ERROR,
                "Missing 'scenario' field in custom metric configuration.",
            )
        if not metric_name:
            error_collector.add_error(
                ErrorCode.GENERIC_ERROR,
                "Missing 'metricName' field in custom metric configuration.",
            )
    elif metric_id and (scenario or metric_name):
        error_collector.add_error(
            ErrorCode.GENERIC_ERROR,
            "Both 'metricId' and 'scenario/metricName' cannot be provided at the same time in the custom metric configuration.",
        )

    # Generate custom metric name
    if metric_id:
        return metric_id.strip()
    # Only proceed if scenario and metric_name are not None/empty (errors already added above)
    if not scenario or not metric_name:
        return ""  # Return empty string if required fields are missing
    custom_metric_name = f"{scenario.strip()}/{metric_name.strip()}"
    if version:
        custom_metric_name += f"/{version.strip()}"
    return custom_metric_name


def validate_metric_name(
    metric: str, all_supported_metrics: List, error_collector: ValidationCollector
) -> None:
    """Validates if metrics name is not empty and the value actually exists in the list of supported metrics"""
    if metric == "":
        error_collector.add_error(
            ErrorCode.EMPTY_METRIC_NAME_ERROR,
            "Metric name cannot be empty. Please provide a valid metric name",
        )
    if metric not in all_supported_metrics:
        error_collector.add_error(
            ErrorCode.UNSUPPORTED_METRIC_ERROR,
            f"{metric} is neither a system supported metric nor provided in custom metric configuration",
        )


def count_user_prompts_from_template_list(template_list) -> int:
    user_prompts = []
    for item in template_list:
        if item["role"] == "user":
            user_prompts.append(item)
    return len(user_prompts)


def get_template_list_from_orch_config(orch_config) -> List:
    return orch_config[MODULES_KEY][PROMPT_TEMPLATING_KEY][PROMPT_KEY][TEMPLATE_KEY]


def validate_prompts_in_templating_module(
    orchestration_config_data: List[dict],
    metric: str,
    error_collector: ValidationCollector,
) -> None:
    """Checks whether the templating config provided in the Orchestration Config has exactly one user prompt"""
    for orch_config in orchestration_config_data:
        prompt_list = get_template_list_from_orch_config(orch_config)
        user_prompt_count = count_user_prompts_from_template_list(prompt_list)
        if user_prompt_count < 1:
            error_collector.add_error(
                ErrorCode.MISSING_USER_PROMPT_ERROR.value,
                f"Missing user prompt in template list. Please provide exactly one user prompt for "
                f"{orch_config} to evaluate {metric} metric",
            )
        elif user_prompt_count > 1:
            error_collector.add_error(
                ErrorCode.MORE_THAN_ONE_USER_PROMPT_PROVIDED_ERROR.value,
                f"More than one user prompts provided in template list. Please provide exactly one user prompt for "
                f"{orch_config} to evaluate {metric} metric",
            )


def get_custom_metric_ids_from_input(
    custom_metric_config_data: List[dict], error_collector: ValidationCollector
) -> list[str]:
    """
    Retrieve custom metric ids from the file data provided by the user.

    :param custom_metric_config_data: List of dictionaries containing custom metric definitions.
    :type custom_metric_config_data: List[dict]
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: List of custom metric ids.
    :rtype: list[str]
    """
    custom_metrics_ids = []
    if not custom_metric_config_data:
        return custom_metrics_ids
    for custom_metric_config in custom_metric_config_data:
        custom_metric_name = create_custom_metric_name(
            custom_metric_config, error_collector
        )
        custom_metrics_ids.append(custom_metric_name)
    return custom_metrics_ids


def check_if_metric_is_defined(
    metrics: List[str],
    metric_templates: List[dict],
    error_collector: ValidationCollector,
) -> None:
    for metric in metrics:
        if metric in SYSTEM_DEFINED_METRIC_MAPPING.values():
            continue

        found = False
        for template in metric_templates:
            if metric == template.get("id"):
                found = True
                break

            if "/" in metric and metric == template.get(
                "scenario"
            ) + "/" + template.get("name") + "/" + template.get("version"):
                found = True
                break

        if not found:
            error_collector.add_error(
                ErrorCode.EMPTY_METRIC_ERROR.value,
                f"{metric} is neither a system supported metric nor provided in metric templates",
            )


def is_value_in_json(value, name, data: dict[str, str]) -> bool:
    """
    Check if a value matches a name or exists in a mapping dictionary.

    :param value: The value to search for.
    :type value: Any
    :param name: The name to compare against.
    :type name: str
    :param data: Dictionary to search in (keys or values).
    :type data: dict[str, str]
    :return: True if value matches name or is found in data, False otherwise.
    :rtype: bool
    """
    value_str = str(value)
    if value_str == name:
        return True
    return any(value_str == key or value_str == str(item) for key, item in data.items())


def validate_metrics(
    metrics: List[str],
    metric_templates: List[dict],
    orchestration_config_data: List[dict],
    error_collector: ValidationCollector,
) -> None:
    """Validates if metrics list is empty or metric name is invalid"""
    if not metrics:
        error_collector.add_error(
            ErrorCode.EMPTY_METRIC_ERROR.value,
            "Metrics list cannot be empty. Atleast one metric needs to be provided",
        )

    check_if_metric_is_defined(metrics, metric_templates, error_collector)

    for metric in metrics:
        if metric == "":
            error_collector.add_error(
                ErrorCode.EMPTY_METRIC_ERROR.value,
                "Metric name cannot be empty. Please provide a valid metric name",
            )
        for template in metric_templates:
            if (
                is_value_in_json(metric, template["id"], SYSTEM_DEFINED_METRIC_MAPPING)
                and template.get("evaluationMethod", "") == LLM_AS_A_JUDGE
            ):
                validate_prompts_in_templating_module(
                    orchestration_config_data, metric, error_collector
                )


def _is_field_name_valid(field_name: str) -> bool:
    """
    Validates the parameter field name that is specified in the prompt template variables.
    """
    if not field_name:
        raise ValueError(
            ErrorCode.EMPTY_FIELD_NAME_ERROR, "Parameter names cannot be empty."
        )
    # field_names must start with a character and end with a character or number
    # only special characters allowed are _ and - and multiple consecutive - and _ are disallowed
    validation_pattern = re.compile(VALIDATION_REGEX_PATTERN_FOR_INPUT_VARIABLES)
    if not validation_pattern.match(field_name):
        raise ValueError(
            ErrorCode.GENERIC_ERROR,
            "Parameter names in templates must be of the form {{ ?parameter_name }}. They must start with a character and end with a character or number. Only special characters allowed are _ and - . Multiple consecutive - and _ are disallowed.",
        )
    return True


def list_prompt_variables(format_string: str) -> list[str]:
    """
    Get all fields (parameters) of the form {{ ?param_name }} from the template.
    Optionally return the raw field names without stripping spaces and '?'.
    """
    field_names = re.findall(INPUT_VARIABLE_REGEX_PATTERN, format_string)
    field_names = [
        (field_name.strip()[1:])
        for field_name in field_names
        if field_name.strip().startswith("?")
    ]
    field_names = [
        (field_name)
        for field_name in field_names
        if _is_field_name_valid(field_name=field_name)
    ]
    return field_names


def extract_dataset_columns(template_variables) -> List[str]:
    """Extracts column names from the template variables provided. If the value is a list, extracts column names from the first rows; else, extracts from the template_variables directly."""
    if isinstance(template_variables, list) and template_variables:
        return list(template_variables[0].keys())
    elif isinstance(template_variables, dict):
        return list(template_variables.keys())
    return []


def get_prompt_variables_from_orch_config(orch_config: dict) -> Set[str]:
    var_set = set()
    template_list = get_template_list_from_orch_config(orch_config)
    for template in template_list:
        template_data = template["content"]
        variables = []
        if isinstance(template_data, list):
            for data in template_data:
                variables.extend(list_prompt_variables(data["text"]))
        elif isinstance(template_data, str):
            variables = list_prompt_variables(template["content"])

        var_set.update(variables)
    # removes 'output_param' if it exists in the set
    return _remove_output_param_if_present(var_set, orch_config)


def get_grounding_config_from_orch_config(orch_config) -> dict:
    """
    Extracts the grounding configuration from the orchestration configuration.
    Args:
        orch_config (dict): Orchestration configuration.
    Returns:
        dict: Grounding configuration if present, otherwise an empty dictionary.
    """
    return orch_config[MODULES_KEY].get("grounding", {})


def get_grounding_output_param_key(orch_config: dict) -> str:
    """
    Determines the correct key to extract the grounding output parameter based on the API version.
    Args:
        orch_config (dict): Orchestration configuration.
    Returns:
        str: The key to extract the grounding output parameter.
    """
    return (
        orch_config.get(MODULES_KEY, {})
        .get("grounding", {})
        .get("placeholders", {})
        .get("output")
    )


def get_defaults(orchestration_configuration: dict) -> dict:
    """Returns the default field from the orchestration configuration."""
    templating_config = orchestration_configuration.get(MODULES_KEY, {}).get(
        PROMPT_TEMPLATING_KEY, {}
    )
    return templating_config.get(PROMPT_KEY, {}).get("defaults", {})


def _remove_output_param_if_present(var_set: set[str], orch_config: dict) -> set[str]:
    """Removes the 'output_param' from variable set if present in the grounding config."""
    grounding_config = get_grounding_config_from_orch_config(orch_config)
    if grounding_config:
        output_param = get_grounding_output_param_key(orch_config)
        if output_param and output_param in var_set:
            var_set.remove(output_param)
    return var_set


def get_mapped_value_if_exists(key, mapping_keys, variable_mapping, dataset_columns) -> str:
    """Gets the first valid mapped value from the list of keys if it exists in variable mapping, else returns the first key"""
    # Ensure mapping_keys is a list, even if it's a single string
    if isinstance(mapping_keys, str):
        mapping_keys = [mapping_keys]
    for mapping_key in mapping_keys:
        if mapping_key in variable_mapping:
            key_value = variable_mapping[mapping_key]
            prefix, field = key_value.split("/")

            # If mapped value exists in dataset, use it
            if prefix == "data" and field in dataset_columns:
                return field

    # If no mapping exists, return the key
    return key


def validate_variable_mapping_of_prompts(
    orchestration_config_data: list,
    dataset_data: List[dict],
    variable_mapping: dict,
    error_collector: ValidationCollector,
) -> None:
    """
    Validates the variable mapping for prompts with a zero-tolerance failure threshold.

    Args:
        orchestration_config_data (list): Orchestration run configuration
        dataset_data (dict): Dataset rows to validate
        variable_mapping (dict): The variable mapping provided in the input configuration.

    Raises:
        ValidationError: If any prompts variable mapping is invalid or does not exist in the dataset.
    """

    # Get list of variables from each orch config and validate
    dataset_columns = extract_dataset_columns(dataset_data)
    for orch_config in orchestration_config_data:
        prompt_variables = get_prompt_variables_from_orch_config(orch_config)
        # Extract default values from templating_module_config
        defaults = get_defaults(orch_config)
        # adding a validation check to see if system defined variables exits in the list of variables
        if set(prompt_variables) & set(PREDEFINED_SYSTEM_VARIABLES_LIST):
            error_collector.add_error(
                ErrorCode.INVALID_METRIC_MAPPING_ERROR.value,
                f"System defined variables {AICORE_LLM_PROMPT_TEMPLATE_KEY} or {AICORE_LLM_COMPLETION_KEY} cannot be used as prompt variables inside the Run Configuration.",
            )

        for var in prompt_variables:
            # Skip validation for variables that have default values
            if defaults is not None and var in defaults:
                continue
            key_name = f"prompt/{var}"
            key_value = get_mapped_value_if_exists(
                var, key_name, variable_mapping, dataset_columns
            )
            if key_value not in dataset_columns:
                error_collector.add_error(
                    ErrorCode.INVALID_METRIC_MAPPING_ERROR.value,
                    f"The provided prompt variable :{var} in Orch config does not match with any variable mapping provided or the actual dataset rows for this orch config of: {orch_config}",
                )


def validate_all_metrics_mapping(
    variable_mapping: dict, dataset_columns: list, error_collector: ValidationCollector
) -> None:
    """
    Validates the variable mapping for 'all_metrics' with a zero-tolerance failure threshold.

    Args:
        variable_mapping (dict): The variable mapping provided in the input configuration.
        dataset_columns (list): List of column names in the dataset.

    Raises:
        ValidationError: If any 'all_metrics' mapping is invalid or the direct column does not exist in the dataset.
    """
    all_metrics_keys = [
        key for key in variable_mapping.keys() if ALL_METRICS_COLUMN_MAPPING_KEY in key
    ]

    for all_metric_key in all_metrics_keys:
        all_metric_variable_value = variable_mapping[all_metric_key]
        default_column_values = all_metric_key.split("/")
        default_column_value = "/".join(default_column_values[:-1])
        dataset_column_name = all_metric_variable_value.split("/")[1]

        if (
            dataset_column_name not in dataset_columns
            and default_column_value not in dataset_columns
        ):
            error_collector.add_error(
                ErrorCode.GENERIC_ERROR.value,
                f"The provided column mapping for all_metrics of {all_metric_key}:{all_metric_variable_value} "
                f"in the variable mapping does not exist in the dataset provided nor the actual variable column.",
            )


def extract_metrics_variables(metric_templates, metric_name: str = None) -> Set:
    """Extracts unique set of variables from the 'variables' key."""
    variables_list = set()  # Use a set to store unique values
    for current_metric in metric_templates:
        if metric_name in (current_metric[ID], current_metric[NAME_KEY]):
            return current_metric.get("additionalProperties", {}).get(VARIABLES_KEY, [])
        variables_list.update(
            current_metric.get("additionalProperties", {}).get(VARIABLES_KEY, [])
        )

    return variables_list


def validate_individual_metrics(
    metrics: list[str],
    variable_mapping: dict,
    dataset_columns: list,
    metric_dependent_variables: set,
    error_collector: ValidationCollector,
) -> None:
    """
    Validates the variable mapping for any metric mapping with a zero-tolerance failure threshold.

    Args:
        metrics (list): List of metrics provided in the input configuration.
        variable_mapping (dict): The variable mapping provided in the input configuration.
        dataset_columns (list): List of column names in the dataset.
        metric_dependent_variables (set): Set of dependent variables for all metrics

    Raises:
        ValidationError: If any metric mapping is invalid or the direct column does not exist in the dataset.
    """
    temp_metrics = metrics

    for key, value in variable_mapping.items():
        key_parts = key.split("/")
        mapping_key = "/".join(key_parts[:-1])
        default_mapping_value = key_parts[-1]
        _, dataset_value = value.split("/")

        # Skip if not a metric or not in the metrics list
        if (
            mapping_key in COLUMN_MAPPING_DEFAULT_KEYS
            or mapping_key not in temp_metrics
        ):
            continue

        if default_mapping_value not in metric_dependent_variables:
            error_collector.add_error(
                ErrorCode.INVALID_METRIC_MAPPING_ERROR.value,
                f"Invalid mapping value provided: {key}:{value} in the variable mapping. "
                f"For system defined metrics, the list of dependent variables are {metric_dependent_variables}",
            )

        if (
            dataset_value not in dataset_columns
            and default_mapping_value not in dataset_columns
        ):
            error_collector.add_error(
                ErrorCode.INVALID_METRIC_MAPPING_ERROR.value,
                f"The provided mapping of {key}:{value} in the variable mapping is not valid as the dataset "
                f"does not neither contains the column values provided in the mapping or the direct column name",
            )


def validate_variable_mapping_of_metrics(
    metrics: list[str],
    metric_templates: list[dict],
    dataset_data: List[dict],
    variable_mapping: dict,
    error_collector: ValidationCollector,
) -> None:
    """
    Validates variable mapping of metrics with tolerance to zero failure threshold

    Args:
        metrics: List of metrics provided in the input config
        metric_templates (list[dict]): Metric templates information resolved from Metric Management Service
        dataset_data: Dataset rows to validate
        variable_mapping: variable mapping provided in input config

    Returns:
        Validates and throws validation error even if one variable mapping related to metrics is invalid.
    """
    dataset_columns = extract_dataset_columns(dataset_data)

    # Validate all_metrics mappings
    validate_all_metrics_mapping(variable_mapping, dataset_columns, error_collector)
    # Validate individual metrics mappings

    metric_dependent_variables = extract_metrics_variables(metric_templates)
    validate_individual_metrics(
        metrics,
        variable_mapping,
        dataset_columns,
        metric_dependent_variables,
        error_collector,
    )


def flatten_prompt_configuration(prompt_config: dict) -> str:
    """
    Flatten a nested prompt configuration dictionary into a readable string.
    """

    def format_value(val):
        if isinstance(val, dict):
            return ", ".join(f"{k}: {format_value(v)}" for k, v in val.items())
        elif isinstance(val, list):
            return "; ".join(format_value(item) for item in val)
        else:
            return str(val)

    parts = [f"{k}: {format_value(v)}" for k, v in prompt_config.items()]
    return "\n".join(parts)


def validate_individual_custom_metrics(
    variable_mapping: dict,
    dataset_columns: list,
    custom_metric_ids: list,
    custom_metric_variables: set,
    error_collector: ValidationCollector,
) -> None:
    """
    Validates the variable mapping for any metric mapping with a zero-tolerance failure threshold.
    """
    custom_metric_variables -= set(PREDEFINED_SYSTEM_VARIABLES_LIST)

    _validate_empty_mapping_with_custom_vars(
        variable_mapping, dataset_columns, custom_metric_variables, error_collector
    )

    for key, value in variable_mapping.items():
        _validate_mapping_entry(
            key,
            value,
            custom_metric_ids,
            custom_metric_variables,
            dataset_columns,
            error_collector,
        )


def _validate_empty_mapping_with_custom_vars(
    variable_mapping: dict,
    dataset_columns: List,
    custom_metric_variables: set,
    error_collector: ValidationCollector,
) -> None:
    if not variable_mapping and custom_metric_variables:
        unmapped_vars = {
            var for var in custom_metric_variables if var not in dataset_columns
        }
        if unmapped_vars:
            error_collector.add_error(
                ErrorCode.GENERIC_ERROR.value,
                "Variable mapping is empty, and the following custom metric variables are not found in the dataset: "
                f"{unmapped_vars}. Either map them or ensure they are present in the dataset columns.",
            )


def _validate_mapping_entry(
    key,
    value,
    custom_metric_ids,
    custom_metric_variables,
    dataset_columns,
    error_collector: ValidationCollector,
) -> None:
    key_parts = key.split("/")
    if len(key_parts) < 3:
        return

    mapping_key = "/".join(key_parts[:-1])
    mapping_value = key_parts[-1]

    try:
        _, dataset_value = value.split("/")
    except ValueError:
        dataset_value = value

    if (
        mapping_key in COLUMN_MAPPING_DEFAULT_KEYS
        or mapping_key not in custom_metric_ids
    ):
        return

    if (
        mapping_value not in custom_metric_variables
        and mapping_value not in dataset_columns
    ):
        error_collector.add_error(
            ErrorCode.GENERIC_ERROR.value,
            f"Invalid mapping value provided: {key}:{value} in the variable mapping. "
            f"For custom metrics, the list of dependent variables are {custom_metric_variables} "
            f"and the available dataset columns are {dataset_columns}",
        )

    if dataset_value not in dataset_columns:
        error_collector.add_error(
            ErrorCode.GENERIC_ERROR.value,
            f"The provided mapping of {key}:{value} in the variable mapping is not valid, as the dataset "
            f"does not contain the column values provided in the mapping or the direct column name.",
        )


def handle_missing_dependent_variables_in_dataset(
    dataset_data: List[dict],
    metrics: list[str],
    metric_templates: list[dict],
    variable_mapping: dict,
    error_collector: ValidationCollector,
) -> None:
    """validates whether all the dependent variables for the metrics list are either directly present as columns in dataset or a variable mapping is provided
    Args:
        dataset_data (List[dict]): Dataset rows to validate (list of row dictionaries)
        metrics (list[str]): List of metrics provided in the input configuration.
        metric_templates (list[dict]): Metric templates information resolved from Metric Management Service
        variable_mapping (dict): The variable mapping provided in the input configuration.
    Raises:
        ValidationError: If any dependent variable is missing in the dataset and the variable mapping is invalid for that metric.
    """

    dataset_columns = extract_dataset_columns(dataset_data)
    for metric in metrics:
        dependent_variables = extract_metrics_variables(metric_templates, metric)
        # when no dependent variables are present for the metric -  can be the case of custom metric or system defined metric with no dependent variables
        if not dependent_variables:
            continue

        for variable in dependent_variables:
            # checking if variable mapping exists of some kind
            first_mapping_key = f"{metric}/{variable}"
            second_mapping_key = f"{ALL_METRICS_COLUMN_MAPPING_KEY}/{variable}"
            if (
                first_mapping_key not in variable_mapping
                and second_mapping_key not in variable_mapping
                and variable not in dataset_columns
            ):
                error_collector.add_error(
                    ErrorCode.INVALID_METRIC_MAPPING_ERROR,
                    f"Invalid mapping: The dependent variable '{variable}' for the metric '{metric}' is neither mapped correctly nor found as a direct column in the dataset.",
                )


def populate_dataset_data_if_data_missing(
    dataset_data: list, variable_mapped_key, error_collector: ValidationCollector
) -> None:
    """Validates and Populates the dataset_data with missing data fields if golden truth is present and throws error if dataset is partially filled"""
    count_pre_filled_values_with_data = sum(
        1
        for row in dataset_data
        if variable_mapped_key in row and row.get(variable_mapped_key) not in [None, ""]
    )

    if count_pre_filled_values_with_data == len(dataset_data):
        # as populating is done across all rows we just return as populating is not required.
        return

    if count_pre_filled_values_with_data != 1:
        # raise an error saying only one or all can be provided it cannot be partial
        error_collector.add_error(
            ErrorCode.INVALID_METRIC_MAPPING_ERROR.value,
            f"Only one or all rows can be provided with '{variable_mapped_key}' in the dataset. Partial rows count is not allowed",
        )
    # Find the value of the key in the first occurrence be it any row
    first_data_value = next(
        (
            row.get(variable_mapped_key)
            for row in dataset_data
            if variable_mapped_key in row
            and row.get(variable_mapped_key) not in [None, ""]
        ),
        None,
    )

    if first_data_value is None:
        error_collector.add_error(
            ErrorCode.INVALID_METRIC_MAPPING_ERROR.value,
            f"At least one valid data entry needs to be provided for '{variable_mapped_key}' in the dataset.",
        )

    # If the value exists, replicate it across all rows if any row does not have this column value
    for row in dataset_data:
        if (
            variable_mapped_key not in row
            or pd.isna(row[variable_mapped_key])
            or row[variable_mapped_key] == ""
        ):  # if key is not present or value is None or null then populate
            row[variable_mapped_key] = first_data_value


def populate_dataset_data_if_single_schema_provided(
    dataset_data, variable_mapping, collector
) -> None:
    """Populates the dataset_data with missing json schema column entries across rows of dataset_data"""
    default_column_name = JSON_SCHEMA_KEY
    mapping_key = f"{JSON_SCHEMA_MATCH_METRIC_ID}/{default_column_name}"
    dataset_columns = extract_dataset_columns(dataset_data)
    variable_mapped_key = get_mapped_value_if_exists(
        default_column_name, mapping_key, variable_mapping, dataset_columns
    )
    populate_dataset_data_if_data_missing(dataset_data, variable_mapped_key, collector)


def handle_json_schema_match(
    metrics: list[str],
    dataset_data: list,
    variable_mapping: dict,
    error_collector: ValidationCollector,
) -> None:
    if JSON_SCHEMA_MATCH_METRIC_ID in metrics:
        # populates all the rows of test data if golden instance is provided.
        populate_dataset_data_if_single_schema_provided(
            dataset_data, variable_mapping, error_collector
        )
        logger.info(
            "template vars data after modifying incase of missing rows and %s is %s ",
            JSON_SCHEMA_MATCH_METRIC_ID,
            dataset_data,
        )


def validate_language_code_and_data_population(
    dataset_data: list, variable_mapping: dict, error_collector: ValidationCollector
) -> None:
    """Populates the dataset_data with missing language column entries across rows of dataset_data"""
    mapping_key = f"{LANGUAGE_MATCH_METRIC_ID}/{LANGUAGE_KEY}"
    dataset_columns = extract_dataset_columns(dataset_data)
    variable_mapped_key = get_mapped_value_if_exists(
        LANGUAGE_KEY, mapping_key, variable_mapping, dataset_columns
    )
    populate_dataset_data_if_data_missing(
        dataset_data, variable_mapped_key, error_collector
    )

    for row in dataset_data:
        if variable_mapped_key in row and row.get(variable_mapped_key) in (None, ""):
            error_collector.add_error(
                ErrorCode.INVALID_DATASET_DATA_ERROR.value,
                f"All rows must be provided with '{variable_mapped_key}' in the dataset. Partial rows count is not allowed",
            )

        code = row.get(variable_mapped_key)
        target_iso_code = LanguageMapper.get_iso_code_639_1(code)
        if target_iso_code is None:
            error_collector.add_error(
                ErrorCode.UNSUPPORTED_LANGUAGE_MATCH_ERROR.value,
                f"{code} is not supported by the language match metric",
            )


def handle_language_match(
    metrics: list,
    dataset_data: list,
    variable_mapping: dict,
    error_collector: ValidationCollector,
) -> None:
    if LANGUAGE_MATCH_METRIC_ID in metrics:
        validate_language_code_and_data_population(
            dataset_data, variable_mapping, error_collector
        )
        logger.info(
            "template vars data after modifying in case of missing rows and %s is %s",
            LANGUAGE_MATCH_METRIC_ID,
            dataset_data,
        )


def populate_dataset_data_if_single_reference_provided(
    dataset_data: List[dict], variable_mapping: dict, collector
) -> None:
    """Populates the dataset_data with missing reference column entries across rows of
        dataset_data for only all metrics case where a golden reference is present
    Args:
        dataset_data (List[dict]): Dataset rows to validate (list of row dictionaries)
        variable_mapping (dict): The variable mapping provided in the input configuration.
    """
    default_column_name = REFERENCE_KEY
    mapping_key = f"{ALL_METRICS_COLUMN_MAPPING_KEY}/{default_column_name}"  # as reference needs to be there across all predefined system defined metrics
    dataset_columns = extract_dataset_columns(dataset_data)
    if mapping_key in variable_mapping or default_column_name in dataset_columns:
        # only populate when a mapping exists for all metrics reference or directly the reference column exists in the dataset
        variable_mapped_key = get_mapped_value_if_exists(
            default_column_name, mapping_key, variable_mapping, dataset_columns
        )
        populate_dataset_data_if_data_missing(
            dataset_data, variable_mapped_key, collector
        )


def populate_dataset_data_if_individual_metric_reference_provided(
    dataset_data: List[dict],
    variable_mapping: dict,
    metrics: list,
    error_collector: ValidationCollector,
) -> None:
    """populates reference value across all rows of dataset_data if individual metric reference is provided
    and is different than all metrics reference provided. This population happens if the provided reference is a golden instance

    Args:
        dataset_data (List[dict]): Dataset rows to validate (list of row dictionaries)
        variable_mapping (dict): The variable mapping provided in the input configuration.
        metrics (list): List of metrics provided in the input configuration.
    """
    dataset_columns = extract_dataset_columns(dataset_data)
    for metric in metrics:
        default_column_name = REFERENCE_KEY
        mapping_key = f"{metric}/{REFERENCE_KEY}"
        # if a valid mapping exists for the metric with reference, then populate the data for that column
        if mapping_key in variable_mapping:
            variable_mapped_key = get_mapped_value_if_exists(
                default_column_name, mapping_key, variable_mapping, dataset_columns
            )
            # populates if mapped key exists and that mapping column is a single entry
            populate_dataset_data_if_data_missing(
                dataset_data, variable_mapped_key, error_collector
            )


def handle_reference_missing_rows(
    dataset_data: List[dict],
    variable_mapping: dict,
    metrics: list,
    error_collector: ValidationCollector,
) -> None:
    """validates whether the reference columns in the rows are missing in the dataset for all metrics and for each individual metrics

    Args:
        dataset_data (List[dict]): Dataset rows to validate (list of row dictionaries)
        variable_mapping (dict): The variable mapping provided in the input configuration.
        metrics (list): List of metrics provided in the input configuration.

    Raises:
        ValidationError: If any required variable mapping is invalid or the default column does not exist in the dataset.
    """

    populate_dataset_data_if_single_reference_provided(
        dataset_data, variable_mapping, error_collector
    )
    populate_dataset_data_if_individual_metric_reference_provided(
        dataset_data, variable_mapping, metrics, error_collector
    )


def update_artifact_dict(artifact_reference: ArtifactSource, artifact_dict_count: dict) -> None:
    artifact_instance = artifact_reference.artifact
    if isinstance(artifact_instance, str):
        artifact_dict_count[artifact_instance] = (
            artifact_dict_count.get(artifact_instance, 0) + 1
        )
    else:
        artifact_dict_count[artifact_instance.id] = (
            artifact_dict_count.get(artifact_instance.id, 0) + 1
        )


def resolve_orchestration_config_v2(template_data: List[PromptTemplate], llm: LLM) -> dict:
    orchestration_config_data = ORCHESTRATION_CONFIG_TEMPLATE_V2
    template_list_data = []
    for data in template_data:
        current_template_data = {}
        current_template_data[PROMPT_REGISTRY_ROLE_KEY] = data.role
        current_template_data[PROMPT_REGISTRY_CONTENT_KEY] = data.content
        template_list_data.append(current_template_data)
    orchestration_config_data[MODULES_KEY][PROMPT_TEMPLATING_KEY][PROMPT_KEY][
        TEMPLATE_KEY
    ] = template_list_data
    llm_module = {}
    llm_module[LLM_MODULE_V2_NAME_KEY] = llm.name
    llm_module[LLM_MODULE_V2_VERSION_KEY] = llm.version
    # Support both old (parameters) and new (params) attribute names
    llm_module[LLM_MODULE_V2_PARAMETERS_KEY] = getattr(llm, 'params', None) or getattr(llm, 'parameters', {})
    orchestration_config_data[MODULES_KEY][PROMPT_TEMPLATING_KEY][MODEL_KEY] = (
        llm_module
    )

    return orchestration_config_data
