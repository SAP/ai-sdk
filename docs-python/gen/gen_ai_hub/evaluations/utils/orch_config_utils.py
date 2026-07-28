from typing import List, Any
from gen_ai_hub.evaluations.models.evaluation_config import EvaluationConfig
from gen_ai_hub.evaluations.constants import (
    TEMPLATE_REF_KEY,
    TEMPLATE_KEY,
    IMAGE_URL_KEY,
    CONTENT_KEY,
    ROLE_KEY,
    TYPE_KEY,
    MODULES_KEY,
    PROMPT_TEMPLATING_KEY,
    PROMPT_KEY,
    MODEL_KEY,
)
from gen_ai_hub.evaluations.utils.gen_utils import (
    list_prompt_variables,
)
from gen_ai_hub.evaluations.exceptions.error_codes import ErrorCode
from gen_ai_hub.evaluations.helpers.collector import ValidationCollector
from gen_ai_hub.orchestration_v2.models.config import OrchestrationConfig


def validate_mandatory_modules(
    orch_config: dict,
    error_collector: ValidationCollector,
    module_key: str,
    required_keys: list[str],
    config_keys: list[str],
) -> None:
    """
    Validates the presence of mandatory modules and their structure.

    :param orch_config: The orchestration configuration dictionary.
    :type orch_config: dict
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :param module_key: The key of the module to validate.
    :type module_key: str
    :param required_keys: List of required keys in the module.
    :type required_keys: list[str]
    :param config_keys: List of configuration keys to validate as dictionaries.
    :type config_keys: list[str]
    :return: None
    :rtype: None
    """
    if module_key not in orch_config:
        error_collector.add_error(
            ErrorCode.INVALID_ORCHESTRATION_CONFIG_ERROR.value,
            f"{module_key} is mandatory in the orchestration config of {orch_config}",
        )
        return

    # Check if required keys exist in the module
    module_config = orch_config[module_key]
    temp_config = module_config
    for key in required_keys:
        if key not in module_config:
            error_collector.add_error(
                ErrorCode.INVALID_ORCHESTRATION_CONFIG_ERROR.value,
                f"{', '.join(required_keys)} is mandatory in the {module_key} field of the orchestration config of {orch_config}",
            )
            return
        temp_config = temp_config[key]

    # Validate if the required configurations are dictionaries
    for key in config_keys:
        try:
            config = temp_config[key]
        except KeyError:
            error_collector.add_error(
                ErrorCode.INVALID_ORCHESTRATION_CONFIG_ERROR.value,
                f"Missing inside here configuration for {key} in the orchestration config {temp_config}",
            )
            continue
        if not isinstance(config, dict):
            error_collector.add_error(
                ErrorCode.INVALID_ORCHESTRATION_CONFIG_ERROR.value,
                f"{key} should be a valid dictionary in the provided orchestration config of {orch_config}",
            )


def validate_orch_config_mandatory_modules(
    orch_config: dict, error_collector: ValidationCollector
) -> None:
    """
    Validates if the outer structure of the orchestration config is valid and exists.

    :param orch_config: The orchestration configuration dictionary.
    :type orch_config: dict
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: None
    :rtype: None
    """
    validate_mandatory_modules(
        orch_config,
        error_collector,
        module_key=MODULES_KEY,
        required_keys=[PROMPT_TEMPLATING_KEY],
        config_keys=[PROMPT_KEY, MODEL_KEY],
    )


def get_model_name(
    orch_config: dict, keys: list[str], error_collector: ValidationCollector
) -> Any:
    """
    Retrieves the value from orch_config using the list of keys provided.
    If any key in the path is missing, logs an error and returns None.

    Args:
        orch_config (dict): The orchestration configuration JSON object.
        keys (list): List of keys representing the path to the desired field.
        error_collector (ValidationCollector): The error collector to log errors.

    Returns:
        The value at the specified path in orch_config, or None if any key is missing.
    """
    try:
        for key in keys:
            orch_config = orch_config[key]
        return orch_config
    except KeyError:
        error_collector.add_error(
            ErrorCode.INVALID_ORCHESTRATION_CONFIG_ERROR.value,
            f"Missing configuration for {' -> '.join(keys)} in the orchestration config of {orch_config}",
        )
        return None


def validate_model_name(
    orch_config: dict, keys: list[str], error_collector: ValidationCollector
) -> None:
    """
    Validates if llm_module_config is a dict and the model name exists.

    :param orch_config: The orchestration configuration dictionary.
    :type orch_config: dict
    :param keys: List of keys representing the path to the model name.
    :type keys: list[str]
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: None
    :rtype: None
    """
    if error_collector.has_error_code(
        ErrorCode.INVALID_ORCHESTRATION_CONFIG_ERROR.value
    ):
        # Skip further validation for this run
        return
    get_model_name(orch_config, keys, error_collector)


def validate_model_name_in_llm_module_config(
    orch_config: dict, error_collector: ValidationCollector
) -> None:
    """
    Validates if the model configuration in llm_module_config is a dict and the model name exists.

    :param orch_config: The orchestration configuration dictionary.
    :type orch_config: dict
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: None
    :rtype: None
    """
    validate_model_name(
        orch_config,
        [MODULES_KEY, PROMPT_TEMPLATING_KEY, MODEL_KEY, "name"],
        error_collector,
    )


def get_prompt_templating_config(
    orch_config: dict, error_collector: ValidationCollector
) -> None:
    """
    Returns the prompt_templating configuration from the orchestration config.

    :param orch_config: The orchestration configuration dictionary.
    :type orch_config: dict
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: None
    :rtype: None
    """
    prompt_templating_config = orch_config.get(MODULES_KEY, {}).get(
        PROMPT_TEMPLATING_KEY, {}
    )
    if TEMPLATE_REF_KEY in prompt_templating_config[PROMPT_KEY]:
        error_collector.add_error(
            ErrorCode.INVALID_TEMPLATE_MODULE_CONFIG_ERROR.value,
            f"template_ref inside prompt is not yet supported in the genai-evaluation service in the orchestration config of {orch_config}",
        )


def validate_template_ref_absent_in_config(
    orch_config: dict, error_collector: ValidationCollector
) -> None:
    """
    Validates if template_ref is given in templating module config and raises an error.

    :param orch_config: The orchestration configuration dictionary.
    :type orch_config: dict
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: None
    :rtype: None
    """
    if error_collector.has_error_code(
        ErrorCode.INVALID_ORCHESTRATION_CONFIG_ERROR.value
    ):
        # Skip further validation for this run
        return
    get_prompt_templating_config(orch_config, error_collector)


def get_template_key(
    orch_config: dict, keys: list[str], error_collector: ValidationCollector
) -> Any:
    """
    Retrieves the value from orch_config using the list of keys provided.

    If any key in the path is missing, logs an error and returns None.

    :param orch_config: The orchestration configuration dictionary.
    :type orch_config: dict
    :param keys: List of keys representing the path to the desired field.
    :type keys: list[str]
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: The value at the specified path in orch_config, or None if any key is missing.
    :rtype: Any | None
    """
    try:
        for key in keys:
            orch_config = orch_config[key]
        return orch_config
    except KeyError:
        error_collector.add_error(
            ErrorCode.INVALID_ORCHESTRATION_CONFIG_ERROR.value,
            f"Missing 'template' key in the orchestration config of {orch_config}",
        )
        return None


def validate_if_template_list_is_empty(
    orch_config: dict, keys: list[str], error_collector: ValidationCollector
) -> None:
    """
    Validates if template list exists and is not empty.

    :param orch_config: The orchestration configuration dictionary.
    :type orch_config: dict
    :param keys: List of keys representing the path to the template list.
    :type keys: list[str]
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: None
    :rtype: None
    """
    if error_collector.has_error_code(
        ErrorCode.INVALID_ORCHESTRATION_CONFIG_ERROR.value
    ) or error_collector.has_error_code(
        ErrorCode.INVALID_TEMPLATE_MODULE_CONFIG_ERROR.value
    ):
        # Skip further validation for this run
        return
    template_list = get_template_key(orch_config, keys, error_collector)

    if not isinstance(template_list, list) or len(template_list) == 0:
        error_collector.add_error(
            ErrorCode.EMPTY_TEMPLATE_LIST_ERROR.value,
            f"template list cannot be empty in prompt field inside the orchestration config of {orch_config}",
        )


def validate_if_template_list_is_empty_in_templating_module_config(
    orch_config: dict, error_collector: ValidationCollector
) -> None:
    """
    Validates if template list exists and is not empty in the templating module config.

    :param orch_config: The orchestration configuration dictionary.
    :type orch_config: dict
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: None
    :rtype: None
    """
    validate_if_template_list_is_empty(
        orch_config,
        [MODULES_KEY, PROMPT_TEMPLATING_KEY, PROMPT_KEY, TEMPLATE_KEY],
        error_collector,
    )


def get_template_list_from_orch_config(orch_config: dict) -> list:
    """
    Returns the template list from the orchestration config.

    :param orch_config: The orchestration configuration dictionary.
    :type orch_config: dict
    :return: The template list from the orchestration config.
    :rtype: list
    """
    return (
        orch_config.get(MODULES_KEY, {})
        .get(PROMPT_TEMPLATING_KEY, {})
        .get(PROMPT_KEY, {})
        .get(TEMPLATE_KEY, [])
    )


def validate_if_content_inside_template_is_empty_in_templating_module_config(
    orch_config: dict, error_collector: ValidationCollector
) -> None:
    """
    Validates if the template list is an array and is a valid dict and content exists in template.

    :param orch_config: The orchestration configuration dictionary.
    :type orch_config: dict
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: None
    :rtype: None
    """
    if error_collector.has_error_code(
        ErrorCode.INVALID_ORCHESTRATION_CONFIG_ERROR.value
    ) or error_collector.has_error_code(
        ErrorCode.INVALID_TEMPLATE_MODULE_CONFIG_ERROR.value
    ):
        return

    template_list = get_template_list_from_orch_config(orch_config)
    for template in template_list:
        if (
            not isinstance(template, dict)
            or CONTENT_KEY not in template
            or ROLE_KEY not in template
        ):
            error_collector.add_error(
                ErrorCode.EMPTY_TEMPLATE_LIST_ERROR.value,
                f"Each template must be a dictionary containing 'content' and 'role' in {orch_config}",
            )


def validate_if_image_url_is_provided_in_content_type_inside_templating_module_config(
    orch_config: dict, error_collector: ValidationCollector
) -> None:
    """
    Validates if inside the template list of templating_module_config if it has image_url type inside the content.

    :param orch_config: The orchestration configuration dictionary.
    :type orch_config: dict
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: None
    :rtype: None
    """
    if error_collector.has_error_code(
        ErrorCode.INVALID_ORCHESTRATION_CONFIG_ERROR.value
    ) or error_collector.has_error_code(
        ErrorCode.INVALID_TEMPLATE_MODULE_CONFIG_ERROR.value
    ):
        return

    template_list = get_template_list_from_orch_config(orch_config)

    for template in template_list:
        content = template.get(CONTENT_KEY)
        if isinstance(content, list):  # Only apply image_url check if content is list
            for item in content:
                if isinstance(item, dict) and item.get(TYPE_KEY) == IMAGE_URL_KEY:
                    error_collector.add_error(
                        ErrorCode.EMPTY_TEMPLATE_LIST_URL_ERROR.value,
                        f"image_url is not supported in the content of template in the orchestration config of {orch_config}",
                    )


def _validate_grounding_output_param_in_prompt_variables(
    orch_config: dict,
    error_collector: ValidationCollector,
    module_key: str,
    grounding_key: str,
    output_param_path: list[str],
    template_path: list[str],
    content_key: str,
):
    # Check if module_key and grounding_key exist
    if module_key not in orch_config:
        return
    module_section = orch_config[module_key]
    if grounding_key not in module_section:
        return

    # Get grounding config and output_param
    grounding_config = module_section[grounding_key]
    output_param = grounding_config
    for key in output_param_path:
        output_param = output_param.get(key, {})
    # If the last key doesn't exist, output_param will be {}, so check for str
    if not isinstance(output_param, str) or not output_param:
        return

    # Get template list
    template_section = module_section
    for key in template_path:
        template_section = template_section.get(key, {})
    template_list = template_section if isinstance(template_section, list) else []

    # Collect all variables from templates
    all_variables = set()
    for template in template_list:
        content = template.get(content_key)
        if isinstance(content, str):
            variables = list_prompt_variables(content)
            all_variables.update(variables)

    # Validate if output_param exists in prompt variables
    if output_param not in all_variables:
        error_collector.add_error(
            ErrorCode.INVALID_GROUNDING_CONFIGURATION.value,
            f"Grounding response '{output_param}' is not being used in the template in orch config of: {orch_config}",
        )


def validate_if_grounding_output_present_in_prompt_variables(
    orch_config: dict, error_collector: ValidationCollector
) -> None:
    """
    Validates if the grounding output parameter is present in prompt variables.

    :param orch_config: The orchestration configuration dictionary.
    :type orch_config: dict
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: None
    :rtype: None
    """
    module_key = MODULES_KEY
    grounding_key = "grounding"
    output_param_path = ["config", "placeholders", "output"]
    template_path = [PROMPT_TEMPLATING_KEY, PROMPT_KEY, TEMPLATE_KEY]
    content_key = "content"

    _validate_grounding_output_param_in_prompt_variables(
        orch_config,
        error_collector,
        module_key,
        grounding_key,
        output_param_path,
        template_path,
        content_key,
    )


def validate_if_all_grounding_input_params_present_in_prompt_variables(
    orch_config: dict, error_collector: ValidationCollector
) -> None:
    """
    Validates if all the input params of the grounding module exist in the prompt variables for v2 configuration.

    :param orch_config: The orchestration configuration dictionary.
    :type orch_config: dict
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: None
    :rtype: None
    """
    if MODULES_KEY not in orch_config:
        return

    if "grounding" in orch_config[MODULES_KEY]:
        grounding_config = orch_config[MODULES_KEY]["grounding"]
        input_params_list = (
            grounding_config.get("config", {}).get("placeholders", {}).get("input")
        )
        template_list = orch_config[MODULES_KEY][PROMPT_TEMPLATING_KEY][PROMPT_KEY].get(
            TEMPLATE_KEY, []
        )

        if input_params_list:
            all_variables = _get_variables_from_template_list(template_list)
            _validate_if_input_param_exists_in_prompt_variables(
                all_variables, error_collector, input_params_list, orch_config
            )


def _get_variables_from_template_list(template_list):
    all_variables = set()
    for template in template_list:
        content = template[CONTENT_KEY]
        if isinstance(content, str):
            variables = list_prompt_variables(content)
            all_variables.update(variables)
    return all_variables


def _validate_if_input_param_exists_in_prompt_variables(
    all_variables,
    error_collector: ValidationCollector,
    input_params_list: list[str],
    orch_config: OrchestrationConfig,
):
    # Validate if each of the input_param exists in prompt variables
    for input_param in input_params_list:
        # Validate if input_param exists in prompt variables
        if input_param not in all_variables:
            error_collector.add_error(
                ErrorCode.INVALID_GROUNDING_CONFIGURATION.value,
                f"Grounding input '{input_param}' is not being used in the template in run: {orch_config}",
            )


def validate_orchestration_params_from_evaluation_config(
    evaluation_configs: List[EvaluationConfig], error_collector: ValidationCollector
) -> None:
    """
    Validates orchestration parameters from evaluation configuration.

    Ensures that either orchestration_registry_reference is provided alone,
    or both template and llm are provided together.

    :param evaluation_configs: List of evaluation configuration objects.
    :type evaluation_configs: List[EvaluationConfig]
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: None
    :rtype: None
    """
    template_configs_list = []
    for current_evaluation_config in evaluation_configs:
        template_configs_list.append(current_evaluation_config.template)
        has_prompt = current_evaluation_config.template is not None
        has_models = current_evaluation_config.llm is not None
        has_orch_registry = (
            current_evaluation_config.orchestration_registry_reference is not None
        )
        if has_orch_registry:
            if has_prompt or has_models:
                error_collector.add_error(
                    ErrorCode.INVALID_PARAMETER_VALUE_ERROR.value,
                    "When providing orchestration_registry_uuids, do not provide prompt_template or models",
                )
            continue  # to cover for all other configs before returning the error

        if not (has_prompt and has_models):
            error_collector.add_error(
                ErrorCode.INVALID_PARAMETER_VALUE_ERROR.value,
                "When orchestration_registry_uuids is absent, both prompt_template and models are required.",
            )


def to_comparable(x) -> dict | Any:
    """
    Converts an object to a comparable format (dict or primitive).

    Handles Pydantic v1, Pydantic v2, custom classes, and primitives.

    :param x: The object to convert.
    :type x: Any
    :return: Dictionary representation or the primitive value.
    :rtype: dict | Any
    """
    if hasattr(x, "model_dump"):  # Pydantic v2
        return x.model_dump()
    if hasattr(x, "dict"):  # Pydantic v1
        return x.dict()
    if hasattr(x, "__dict__"):  # Custom classes like TemplateRef
        return vars(x)
    return x  # primitives like string

