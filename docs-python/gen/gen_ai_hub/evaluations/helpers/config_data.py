from typing import List, Union, Tuple
from ai_core_sdk.ai_core_v2_client import AICoreV2Client
from gen_ai_hub.evaluations.models.evaluation_config import EvaluationConfig
from gen_ai_hub.evaluations._internal._models import (
    _EvaluationConfigData,
    _AWSObjectStoreData,
)
from gen_ai_hub.evaluations.helpers.collector import ValidationCollector
from gen_ai_hub.evaluations.utils.config_data_utils import (
    get_orch_config_data,
    get_dataset_data,
)
from gen_ai_hub.evaluations.utils.gen_utils import (
    get_accumulated_config_data,
    update_variable_mapping,
)
from gen_ai_hub.evaluations.constants import VARIABLE_MAPPING_PROMPT_PREFIX_KEY
from gen_ai_hub.proxy.gen_ai_hub_proxy.client import GenAIHubProxyClient
from gen_ai_hub.evaluations.exceptions.error_codes import ErrorCode
from gen_ai_hub.evaluations.helpers.logging import get_logger
from gen_ai_hub.evaluations.utils.aicore_utils import (
    resolve_metric_identifiers,
    resolve_metric_names,
)

logger = get_logger()


def extract_config_data(
    evaluation_configs: List[EvaluationConfig],
    ai_core_client: AICoreV2Client,
    object_store_credentials: _AWSObjectStoreData,
    resource_group: str,
    gen_ai_hub_proxy_client: GenAIHubProxyClient,
    error_collector: ValidationCollector,
) -> List[_EvaluationConfigData]:
    """Extract configuration data from user-provided evaluation configs.

    This function processes evaluation configurations to extract orchestration config,
    dataset data, metric templates, and variable mappings for each configuration.

    :param evaluation_configs: List of evaluation configuration objects to process
    :type evaluation_configs: List[EvaluationConfig]
    :param ai_core_client: AI Core V2 client for API interactions
    :type ai_core_client: AICoreV2Client
    :param object_store_credentials: Credentials for accessing object storage (AWS S3)
    :type object_store_credentials: _AWSObjectStoreData
    :param resource_group: AI Core resource group name
    :type resource_group: str
    :param gen_ai_hub_proxy_client: GenAI Hub proxy client for orchestration operations
    :type gen_ai_hub_proxy_client: GenAIHubProxyClient
    :param error_collector: Collector for validation errors
    :type error_collector: ValidationCollector
    :return: List of extracted evaluation configuration data objects
    :rtype: List[_EvaluationConfigData]
    """
    result: List[_EvaluationConfigData] = []
    logger.info("Extracting data from the Configuration provided!")
    try:
        # builds the variable mapping
        for evaluation_config in evaluation_configs:
            variable_mapping_dict = {}  # individual variable_mapping for each of the config object provided by user
            logger.info(
                "For the current evaluation config of %s", evaluation_config.__dict__
            )
            orch_config_data = get_orch_config_data(
                evaluation_config,
                ai_core_client,
                gen_ai_hub_proxy_client,
                error_collector,
            )
            dataset_type = evaluation_config.dataset_config.file_type
            dataset_data = get_dataset_data(
                evaluation_config.dataset_config,
                ai_core_client,
                object_store_credentials,
                resource_group,
                error_collector,
            )
            # handling the template variable mapping for prompt and dataset
            if evaluation_config.template_variable_mapping is not None:
                variable_mapping_dict = update_variable_mapping(
                    evaluation_config.template_variable_mapping,
                    VARIABLE_MAPPING_PROMPT_PREFIX_KEY,
                    variable_mapping_dict,
                )

            # fetch the data and store in resolved_metrics_data
            metric_templates_data = resolve_metric_identifiers(
                evaluation_config.metrics,
                ai_core_client,
                resource_group,
                error_collector,
            )


            # stores resolved metric names provided via metricConfig
            metrics_list = resolve_metric_names(
                evaluation_config.metrics, error_collector
            )

            for index, metric in enumerate(evaluation_config.metrics):
                # handling the variable mapping for metrics
                if metric.variable_mapping is not None:
                    prefix_key = metrics_list[index] + "/"
                    variable_mapping_dict = update_variable_mapping(
                        metric.variable_mapping,
                        prefix_key,
                        variable_mapping_dict,
                    )

            current_config_data = _EvaluationConfigData(
                orch_config_data=[orch_config_data],
                dataset_type=dataset_type,
                dataset_data=dataset_data,
                metrics_list=metrics_list,
                metric_templates=metric_templates_data,
                variable_mapping=variable_mapping_dict,
                test_row_count=evaluation_config.test_row_count,
                tags=evaluation_config.tags,
                repetitions=evaluation_config.repetitions,
                debug_mode=evaluation_config.debug_mode,
            )

            if not orch_config_data:
                error_collector.add_error(
                    ErrorCode.INVALID_ORCHESTRATION_CONFIG_ERROR,
                    f"Orchestration config data provided from the evaluation configuration is empty. Please provide a valid combination of (llm and template) or orchestration_registry reference for this config: {evaluation_config.__dict__}",
                )

            if not dataset_data:
                error_collector.add_error(
                    ErrorCode.EMPTY_FILE_DATA_ERROR,
                    f"Dataset config file data is empty, please provide a valid path or artifact for this datasetConfig: {evaluation_config.dataset_config}",
                )

            # all configs from user mapping to jsonl type as there can be multiple metrics and reading data already in the array
            logger.info(
                "Extracted data for the current evaluation config is %s",
                current_config_data,
            )
            result.append(current_config_data)

        return result
    except Exception as e:
        error_collector.add_error(
            ErrorCode.GENERIC_ERROR,
            f"Data extraction of the evaluation config provided failed with error of {e}",
        )
        return result  # empty result which just obeys the config data dict


def build_accumulated_config(
    evaluation_configs_data: List[_EvaluationConfigData],
    has_mixed_config_types: bool = False,
) -> Tuple[Union[List[_EvaluationConfigData], _EvaluationConfigData], bool, bool]:
    """Build accumulated configuration data and determine execution flow strategy.

    Analyzes evaluation configurations to determine whether they can be executed
    as a single job (if datasets and metrics match) or require multiple executions.
    Also determines if artifacts can be reused across executions.

    :param evaluation_configs_data: List of extracted evaluation configuration data objects
    :type evaluation_configs_data: List[_EvaluationConfigData]
    :param has_mixed_config_types: Whether evaluation configs have mixed types (llm+template and orchestration_registry)
    :type has_mixed_config_types: bool
    :return: Tuple containing:
        - accumulated_config_data: Either a single accumulated config or list of configs
        - single_execution_flow: True if all configs can be executed as one job
        - reusable_artifact: True if dataset artifact can be reused across executions
    :rtype: Tuple[Union[List[_EvaluationConfigData], _EvaluationConfigData], bool, bool]
    """
    single_execution_flow = False
    reusable_artifact = False
    accumulated_config_data: List[_EvaluationConfigData] | _EvaluationConfigData = None
    fetched_dataset_data = evaluation_configs_data[0].dataset_data
    fetched_metrics_list = evaluation_configs_data[0].metrics_list
    all_datasets_data_same = all(
        current_eval_config_data.dataset_data == fetched_dataset_data
        for current_eval_config_data in evaluation_configs_data
    )
    all_metrics_list_same = all(
        set(current_eval_config_data.metrics_list) == set(fetched_metrics_list)
        for current_eval_config_data in evaluation_configs_data
    )

    # A single execution cannot handle both llm+template and orchestration_registry types together
    if all_datasets_data_same and all_metrics_list_same and not has_mixed_config_types:
        # to create one artifact and one execution
        # As decided now all config will be mapped to one single execution so one single config
        accumulated_config_data = get_accumulated_config_data(evaluation_configs_data)
        single_execution_flow = (
            True  # as we are accumulating the data, only one single execution
        )
    elif all_datasets_data_same:
        # to create one artifact in case of multiple executions
        reusable_artifact = True

    if not accumulated_config_data:
        # Not a single execution flow so re-create multiple executions
        accumulated_config_data = evaluation_configs_data


    return (accumulated_config_data, single_execution_flow, reusable_artifact)
