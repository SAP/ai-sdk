import uuid
from typing import List
from ai_core_sdk.ai_core_v2_client import AICoreV2Client
from ai_api_client_sdk.models.artifact import Artifact
from gen_ai_hub.evaluations.models.evaluation_config import EvaluationConfig
from gen_ai_hub.evaluations._internal._models import (
    _EvaluationConfigData,
    _AWSObjectStoreData,
)
from gen_ai_hub.evaluations.models.artifact_source import ArtifactSource
from gen_ai_hub.evaluations.utils.aicore_utils import (
    upload_evaluation_dataset_data,
    register_aicore_artifact,
    register_aicore_configuration,
    register_aicore_execution,
)
from gen_ai_hub.evaluations.constants import DEFAULT_KEY
from gen_ai_hub.evaluations.helpers.collector import ValidationCollector
from gen_ai_hub.evaluations.exceptions.error_codes import ErrorCode
from gen_ai_hub.evaluations.models.evaluation_run import EvaluationRun
from gen_ai_hub.evaluations.helpers.logging import get_logger

logger = get_logger()


def upload_dataset_data_and_register_aicore_artifact(
    input_object_store_secret_name: str,
    accumulated_config_data: _EvaluationConfigData,
    object_store_credentials: _AWSObjectStoreData,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
):
    current_object_store_secret_name = (
        input_object_store_secret_name
        if input_object_store_secret_name
        else DEFAULT_KEY
    )
    (
        artifact_folder_path,
        aicore_configuration_dataset_path,
    ) = upload_evaluation_dataset_data(
        accumulated_config_data,
        object_store_credentials,
        current_object_store_secret_name,
        ai_core_client,
        resource_group,
        error_collector,
    )
    if artifact_folder_path == "":
        error_collector.add_error(
            ErrorCode.FILE_UPLOAD_ERROR,
            "Error while uploading the files to the provided object store secret, so terminating the evaluate function. Please look into the error and try again",
        )

    logger.info(
        "After uploading the data to the hyperscaler, the root folder path is %s. The dataset path is %s",
        artifact_folder_path,
        aicore_configuration_dataset_path,
    )

    error_collector.raise_if_errors()
    # STEP3: artifact creation
    aicore_artifact_id = register_aicore_artifact(
        artifact_folder_path,
        ai_core_client,
        resource_group,
        current_object_store_secret_name,
        error_collector,
    )

    if aicore_artifact_id == "":
        error_collector.add_error(
            ErrorCode.ARTIFACT_CREATION_FAILURE,
            "Error while registering the artifact with the provided config files, so terminating the evaluate function. Please look into the error and try again",
        )
    logger.info("AI Core artifact ID created: %s", aicore_artifact_id)
    error_collector.raise_if_errors()

    return (aicore_artifact_id, aicore_configuration_dataset_path)


def configure_dataset_artifact(
    evaluation_configs: List[EvaluationConfig],
    accumulated_config_data: _EvaluationConfigData,  # single execution so config is accumulated
    input_object_store_secret_name: str,
    object_store_credentials: _AWSObjectStoreData,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
):
    dataset_config_instance = evaluation_configs[0].dataset_config
    dataset_folder_artifact_path = ""
    aicore_artifact_id = ""

    if isinstance(dataset_config_instance.source, ArtifactSource):
        # Single artifact and it's the same artifact instance across the entire config list.
        artifact_instance = dataset_config_instance.source.artifact
        if isinstance(artifact_instance, Artifact):
            dataset_folder_artifact_path = artifact_instance.id
        else:
            dataset_folder_artifact_path = artifact_instance  # direct string instance.

    if dataset_folder_artifact_path != "":
        aicore_artifact_id = dataset_folder_artifact_path
        aicore_configuration_dataset_path = dataset_config_instance.source.path
        logger.info(
            "Dataset artifact fetched: %s, dataset config path: %s",
            aicore_artifact_id,
            aicore_configuration_dataset_path,
        )
        logger.info(
            "AI Core artifact ID being reused for AI Core configuration: %s",
            aicore_artifact_id,
        )

    else:
        (aicore_artifact_id, aicore_configuration_dataset_path) = (
            upload_dataset_data_and_register_aicore_artifact(
                input_object_store_secret_name,
                accumulated_config_data,
                object_store_credentials,
                ai_core_client,
                resource_group,
                error_collector,
            )
        )

    return (aicore_artifact_id, aicore_configuration_dataset_path)


def configure_orchestration_config_for_simplified_executable(
    evaluation_configs: List[EvaluationConfig],
):
    # Logic to generate the uuids required for llm,prompt combination or orchestration_registry list of uuids
    llm_model_config = None
    template_config = None
    orchestration_registry_config = None
    template_config_list = []
    model_config_list = []
    orchestration_registry_config_list = []
    current_config = evaluation_configs[0]
    if (
        current_config.llm is not None
    ):  # JUST TO check whether user provided llm,template combination or orchestration_regostry_combination
        # user provided llm and template combination
        for config in evaluation_configs:
            llm_model_name = config.llm.name
            llm_model_version = config.llm.version
            model_config = f"{llm_model_name}:{llm_model_version}"
            model_config_list.append(model_config)
            template_config_list.append(config.template)
        # building the actual config object needed for underlying executable
        llm_model_config = ",".join(model_config_list)
        template_config = template_config_list
    else:
        # user provided orchestration registry uuids
        for config in evaluation_configs:
            orchestration_registry_config_list.append(
                config.orchestration_registry_reference
            )
        # building the actual config object needed for underlying executable
        orchestration_registry_config = ",".join(orchestration_registry_config_list)

    return llm_model_config, template_config, orchestration_registry_config


def single_evaluation_job_flow(
    evaluation_configs: List[EvaluationConfig],
    accumulated_config_data: _EvaluationConfigData,  # single execution so config is accumulated
    input_object_store_secret_name: str,
    object_store_credentials: _AWSObjectStoreData,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    orchestration_url: str,
    error_collector: ValidationCollector,
):
    aicore_artifact_id, aicore_configuration_dataset_path = configure_dataset_artifact(
        evaluation_configs,
        accumulated_config_data,
        input_object_store_secret_name,
        object_store_credentials,
        ai_core_client,
        resource_group,
        error_collector,
    )
    # STEP4: config creation
    # generates the list of run_ids to be attached to the execution executable based on length of orchestration_configs provoded by user
    run_ids_list = [
        uuid.uuid4().hex for _ in range(len(accumulated_config_data.orch_config_data))
    ]

    llm_model_config, template_config, orchestration_registry_config = (
        configure_orchestration_config_for_simplified_executable(evaluation_configs)
    )

    aicore_configuration_id = register_aicore_configuration(
        aicore_artifact_id,
        ai_core_client,
        resource_group,
        accumulated_config_data,
        orchestration_url,
        aicore_configuration_dataset_path,
        run_ids_list,
        llm_model_config,
        template_config,
        orchestration_registry_config,
        error_collector,
    )
    logger.info("AI Core configuration ID: %s", aicore_configuration_id)

    if aicore_configuration_id == "":
        error_collector.add_error(
            ErrorCode.CONFIGURATION_CREATION_FAILURE,
            "Error while creating the aicore configuration with the provided config files, so terminating the evaluate function. Please look into the error and try again",
        )

    error_collector.raise_if_errors()

    # STEP5: execution creation

    aicore_execution_id = register_aicore_execution(
        ai_core_client,
        aicore_configuration_id,
        resource_group,
        error_collector,
    )

    logger.info("AI Core execution ID: %s", aicore_execution_id)

    if aicore_execution_id == "":
        error_collector.add_error(
            ErrorCode.EXECUTION_CREATION_FAILURE,
            "Error while creating the aicore execution with the provided config files, so terminating the evaluate function. Please look into the error and try again",
        )

    evaluation_runs: List[EvaluationRun] = []
    for run_id in run_ids_list:
        run = EvaluationRun(
            run_id=run_id,
            execution_id=aicore_execution_id,
            configuration_id=aicore_configuration_id,
            artifact_id=aicore_artifact_id,
            ai_core_client=ai_core_client,
            resource_group=resource_group,
            object_store_credentials=object_store_credentials,  # credentials object mapped to get the results based on run id.
            metrics_list=accumulated_config_data.metrics_list,  # passing the specific metric ids list to the run for parsing results.
        )
        evaluation_runs.append(run)
    return evaluation_runs


def multiple_evaluation_jobs_flow(
    evaluation_configs: List[EvaluationConfig],
    accumulated_config_data: List[_EvaluationConfigData],
    input_object_store_secret_name: str,
    object_store_credentials: _AWSObjectStoreData,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    orchestration_url: str,
    reusable_artifact: bool,
    error_collector: ValidationCollector,
):
    artifact_ids_list = []
    aicore_configuration_dataset_paths_list = []
    if reusable_artifact:
        aicore_artifact_id, aicore_configuration_dataset_path = (
            configure_dataset_artifact(
                evaluation_configs,
                accumulated_config_data[
                    0
                ],  # as data across all datasets are the same, using the first config object
                input_object_store_secret_name,
                object_store_credentials,
                ai_core_client,
                resource_group,
                error_collector,
            )
        )
        artifact_ids_list = [aicore_artifact_id]
        aicore_configuration_dataset_paths_list = [aicore_configuration_dataset_path]
    else:
        # create multiple artifacts for each of config data provided.
        for current_accumulated_config in accumulated_config_data:
            (aicore_artifact_id, aicore_configuration_dataset_path) = (
                upload_dataset_data_and_register_aicore_artifact(
                    input_object_store_secret_name,
                    current_accumulated_config,
                    object_store_credentials,
                    ai_core_client,
                    resource_group,
                    error_collector,
                )
            )

            artifact_ids_list.append(aicore_artifact_id)
            aicore_configuration_dataset_paths_list.append(
                aicore_configuration_dataset_path
            )

    evaluation_runs: List[EvaluationRun] = []

    for index, current_accumulated_config in enumerate(accumulated_config_data):
        aicore_artifact_id = (
            artifact_ids_list[index]
            if index < len(artifact_ids_list)
            else artifact_ids_list[0]
        )
        # STEP4: config creation
        # generates the list of run_ids to be attached to the execution executable based on length of orchestration_configs provoded by user
        run_ids_list = [
            uuid.uuid4().hex
            for _ in range(len(current_accumulated_config.orch_config_data))
        ]
        
        llm_model_config, template_config, orchestration_registry_config = (
            configure_orchestration_config_for_simplified_executable(
                [
                    evaluation_configs[index]
                ]  # using that particular configs data of llm and template
            )
        )
        aicore_configuration_id = register_aicore_configuration(
            aicore_artifact_id,
            ai_core_client,
            resource_group,
            current_accumulated_config,
            orchestration_url,
            aicore_configuration_dataset_path,
            run_ids_list,
            llm_model_config,
            template_config,
            orchestration_registry_config,
            error_collector,
        )
        if aicore_configuration_id == "":
            error_collector.add_error(
                ErrorCode.CONFIGURATION_CREATION_FAILURE,
                "Error while creating the aicore configuration with the provided config files, so terminating the evaluate function. Please look into the error and try again",
            )
        error_collector.raise_if_errors()
        logger.info("AI Core configuration ID: %s", aicore_configuration_id)

        # STEP5: execution creation
        aicore_execution_id = register_aicore_execution(
            ai_core_client,
            aicore_configuration_id,
            resource_group,
            error_collector,
        )

        if aicore_execution_id == "":
            error_collector.add_error(
                ErrorCode.EXECUTION_CREATION_FAILURE,
                "Error while creating the aicore execution with the provided config files, so terminating the evaluate function. Please look into the error and try again",
            )
        error_collector.raise_if_errors()
        logger.info("AI Core execution ID: %s", aicore_execution_id)

        for run_id in run_ids_list:
            evaluation_run = EvaluationRun(
                run_id=run_id,
                execution_id=aicore_execution_id,
                configuration_id=aicore_configuration_id,
                artifact_id=aicore_artifact_id,
                ai_core_client=ai_core_client,
                resource_group=resource_group,
                object_store_credentials=object_store_credentials,
                metrics_list=current_accumulated_config.metrics_list,
            )
            evaluation_runs.append(evaluation_run)
    return evaluation_runs
