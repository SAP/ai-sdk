import time
import json
import uuid
import os
from pathlib import PurePosixPath
from typing import List, Union, Any, Optional, Callable, Dict
from ai_core_sdk.ai_core_v2_client import AICoreV2Client
from ai_core_sdk.models.object_store_secret import ObjectStoreSecret
from ai_api_client_sdk.models.configuration import Configuration
from ai_api_client_sdk.models.deployment import Deployment
from ai_api_client_sdk.models.status import Status
from ai_api_client_sdk.models.artifact import Artifact
from ai_api_client_sdk.models.input_artifact_binding import InputArtifactBinding
from ai_api_client_sdk.models.parameter_binding import ParameterBinding
from gen_ai_hub.evaluations.constants import (
    ORCHESTRATION_GLOBAL_SCENARIO_NAME,
    AI_PROTOCOL_PREFIX,
    AWS_OSS_BUCKET_URL_KEY,
    AWS_OSS_REGION_URL_KEY,
    AWS_OSS_PATH_PREFIX_URL_KEY,
    CSV_FILE_TYPE,
    JSON_FILE_TYPE,
    EVALUATIONS_SCENARIO_ID,
    EVALUATIONS_CONFIG_PREFIX_KEY,
    EVALUATIONS_ARTIFACT_PREFIX_KEY,
    DATASET_FOLDER_KEY,
    EVAL_ORCHESTRATION_CONFIG_PREFIX_NAME,
    EVALUATIONS_ARTIFACT_DESCRIPTION,
    ORCHESTRATION_REGISTRY_ENDPOINT,
    SYSTEM_DEFINED_METRIC_MAPPING,
)
from gen_ai_hub.evaluations.models.artifact_source import ArtifactSource
from gen_ai_hub.evaluations.helpers.collector import ValidationCollector
from gen_ai_hub.evaluations.exceptions.error_codes import ErrorCode
from gen_ai_hub.evaluations.utils.oss_secret_utils import (
    fetch_object_store_secret_by_name,
)
from gen_ai_hub.evaluations.helpers.s3_file_client import S3FileClient
from gen_ai_hub.evaluations._internal._models import _AWSObjectStoreData
from gen_ai_hub.evaluations._internal._models import _EvaluationConfigData
from gen_ai_hub.evaluations.utils.metric_client_utils import (
    get_metric_template_info_from_server,
    get_metric_version_history,
    get_custom_metric_by_id,
)
from gen_ai_hub.evaluations.models.metric_config import MetricConfig
from gen_ai_hub.evaluations.helpers.logging import get_logger
from gen_ai_hub.orchestration_v2.service import OrchestrationService
from gen_ai_hub.orchestration_v2.models.config import OrchestrationConfig


logger = get_logger()


def generate_random_id():
    """generates and returns a random uuid everytime"""
    return uuid.uuid4().hex


def find_configuration_id_by_name(
    configurations_list: List[Configuration], target_name: str
):
    response = next(
        (
            configuration.id
            for configuration in configurations_list
            if configuration.name == target_name
        ),
        None,
    )
    logger.info("value of id fetched for configuration is %s", response)
    return response


def get_all_configurations(
    ai_core_client: AICoreV2Client, resource_group: str, scenario_id: str
) -> List[Configuration]:
    try:
        response = ai_core_client.configuration.query(
            scenario_id=scenario_id, resource_group=resource_group
        )
        return response.resources  # direct list of resources
    except Exception as e:
        raise ValueError(
            f"Could not fetch all configurations with the error of {e}"
        ) from e


def get_running_deployments_by_configuration_id(
    ai_core_client: AICoreV2Client, configuration_id: str, resource_group: str
) -> List[Deployment]:
    try:
        response = ai_core_client.deployment.query(
            scenario_id=ORCHESTRATION_GLOBAL_SCENARIO_NAME,
            configuration_id=configuration_id,
            status=Status.RUNNING,
            resource_group=resource_group,
        )
        return response.resources
    except Exception as e:
        raise ValueError(
            f"Could not fetch all deployments with the error of {e}"
        ) from e


def create_deployment_by_configuration_id(
    ai_core_client: AICoreV2Client, configuration_id: str, resource_group: str
):
    try:
        # create deployment
        deployment_response = ai_core_client.deployment.create(
            configuration_id=configuration_id,
            resource_group=resource_group,
        )

        # wait till the deployment is up and running
        def deployment_status_fetcher():
            return ai_core_client.deployment.get(
                deployment_id=deployment_response.id,
                resource_group=resource_group,
            )

        def extract_deployment_url(response):
            return response.deployment_url

        deployment_url = wait_for_target_status(
            status_fetcher=deployment_status_fetcher,
            target_status=Status.RUNNING,
            extract_url=extract_deployment_url,
        )
        if (
            deployment_url is None
        ):  # when the value is returned after waiting till its running
            raise ValueError(
                "Deployment URL could not reach the target status of Running, so failing the setup!"
            )

        return deployment_url
    except Exception as e:
        raise RuntimeError(
            f"Creation of orchestration deployment failed with the error of {e}"
        ) from e


def create_llm_orchestration_deployment_url(
    ai_core_client: AICoreV2Client, resource_group: str
):
    """creates the llm-orchestration configuration based on orchestration global scenario and then creates a deployment using that configuration"""
    try:
        # create config.
        configuration_name = (
            EVAL_ORCHESTRATION_CONFIG_PREFIX_NAME + generate_random_id()[:5]
        )
        logger.info(
            "Using the configuration name of %s to create the AICore configuration",
            configuration_name,
        )
        configuration_response = ai_core_client.configuration.create(
            name=configuration_name,  # some randomization maybe here.
            scenario_id=ORCHESTRATION_GLOBAL_SCENARIO_NAME,
            executable_id=ORCHESTRATION_GLOBAL_SCENARIO_NAME,
        )
        logger.info(
            "Response after creating the configuration is %s", configuration_response
        )

        # positive case gets id
        configuration_id = configuration_response.id
        return create_deployment_by_configuration_id(
            ai_core_client, configuration_id, resource_group
        )

    except Exception as e:
        raise RuntimeError(
            f"Creation of orchestration deployment url failed with the error of {e}"
        ) from e


def wait_for_target_status(
    status_fetcher: Callable[[], Any],
    target_status: Status,
    extract_url: Optional[Callable[[Any], str]] = None,
    timeout: int = 1200,
    initial_interval: int = 120,
    pending_interval: int = 40,
) -> Optional[str]:
    """Reusable polling function to wait until a resource reaches target_status.

    :param status_fetcher: Function to get current status response
    :type status_fetcher: Callable[[], Any]
    :param target_status: Target status to wait for (Status enum)
    :type target_status: Status
    :param extract_url: Optional function to extract URL from response, defaults to None
    :type extract_url: Optional[Callable[[Any], str]]
    :param timeout: Maximum time to wait in seconds, defaults to 1200
    :type timeout: int
    :param initial_interval: Initial polling interval in seconds, defaults to 120
    :type initial_interval: int
    :param pending_interval: Polling interval for pending/running status in seconds, defaults to 40
    :type pending_interval: int
    :return: Extracted URL if extract_url is provided and status reached, None otherwise
    :rtype: Optional[str]
    """
    logger.info("Waiting for the target end status of %s", target_status)
    try:
        start = time.time()
        current_interval = initial_interval

        while time.time() - start < timeout:
            response = status_fetcher()
            status = response.status
            logger.info("Current status is : %s", status)

            if status == target_status:
                end = time.time()
                logger.info(
                    "Time in wait till it reached target_status of %s is %s seconds",
                    target_status,
                    end - start,
                )
                if extract_url:
                    return extract_url(response)
                return None  # or return success indication

            elif status == Status.UNKNOWN:
                current_interval = initial_interval
            elif (
                status == Status.PENDING or status == Status.RUNNING
            ):  # Running status is also intermediate status to be reused for executions
                current_interval = pending_interval
            elif (
                status == Status.DEAD
                or status == Status.STOPPED
                or status == Status.STOPPING
            ):
                logger.error(
                    "Could not reach the target status. Please use debug_info function to get the info regarding failures"
                )
                return None

            time.sleep(current_interval)

    except Exception as e:
        raise KeyError(
            f"Failed to reach the target status of {target_status} because of {e}"
        ) from e

    logger.error("Timeout reached without success status.")
    return None


def read_data_from_artifact(
    object_store_credentials: Union[
        _AWSObjectStoreData
    ],  # can be later extend to other providers
    object_store_secret_metadata_details: Dict[str, str],
    s3_file_key: str,
    file_type: str,
    error_collector: ValidationCollector,
):
    file_data = []
    if isinstance(object_store_credentials, _AWSObjectStoreData):
        s3_file_client = S3FileClient(
            object_store_secret_metadata_details.get(AWS_OSS_BUCKET_URL_KEY),
            object_store_secret_metadata_details.get(AWS_OSS_REGION_URL_KEY),
            object_store_credentials.aws_access_key_id,
            object_store_credentials.aws_secret_access_key,
            error_collector=error_collector,
        )
        if file_type == CSV_FILE_TYPE:
            file_data = s3_file_client.read_csv(s3_file_key)
        elif file_type == JSON_FILE_TYPE:
            file_data = s3_file_client.read_json(s3_file_key)
        else:
            file_data = s3_file_client.read_jsonl(s3_file_key)

    return file_data


def build_s3_file_key(
    object_store_secret_metadata_details: Dict[str, str],
    artifact_url_relative_path: str,
    artifact_source: ArtifactSource,
):
    path_prefix = object_store_secret_metadata_details.get(AWS_OSS_PATH_PREFIX_URL_KEY)
    final_path = []

    if path_prefix:
        final_path.append(path_prefix)

    if artifact_url_relative_path:
        final_path.append(artifact_url_relative_path)

    if artifact_source.path is not None:
        final_path.append(artifact_source.path)

    if not final_path:
        return ""

    # PurePosixPath ensures forward slashes (S3-compatible)
    return str(PurePosixPath(*final_path))


# Assumption is the provided artifact is the same as what creds are provided and url is of type ai://secret_name/pathPRefix
def resolve_artifact_path(
    artifact_source: ArtifactSource,
    ai_core_client: AICoreV2Client,
    object_store_credentials: Union[_AWSObjectStoreData],
    resource_group: str,
    error_collector: ValidationCollector,
):
    file_type = artifact_source.file_type
    artifact = artifact_source.artifact
    if isinstance(artifact, str):
        artifact = ai_core_client.artifact.get(artifact_id=artifact)
    artifact_url = artifact.url
    if artifact_url.startswith(AI_PROTOCOL_PREFIX):
        url_part = artifact_url[len(AI_PROTOCOL_PREFIX) :]

        sep = url_part.find("/")
        if sep == -1:  # "/" does not exist in url_part
            error_collector.add_error(
                ErrorCode.INVALID_ARTIFACT_URL_ERROR,
                f"Artifact URL '{artifact_url}' has invalid format. Valid format is {AI_PROTOCOL_PREFIX}<object store name>/<data path>",
            )
            return []

        object_store_secret_name = url_part[:sep]
        artifact_url_relative_path = url_part[sep + 1 :]
        object_store_secret_details: ObjectStoreSecret = (
            fetch_object_store_secret_by_name(
                ai_core_client, object_store_secret_name, resource_group, error_collector
            )
        )
        if object_store_secret_details is None:
            error_collector.add_error(
                ErrorCode.INVALID_OBJECT_STORE_SECRET_ERROR,
                f"The provided artifact url's object store secret {object_store_secret_name} is invalid. Please provide a valid url",
            )
            return []

        # building the key of where the file is present based on artifact url and path_prefix given in secret
        # order of resolution is secret pathprefix + artifact url continuation after secret name + relative path inside ArtifactSource object
        s3_file_key = build_s3_file_key(
            object_store_secret_details.metadata,
            artifact_url_relative_path,
            artifact_source,
        )

        file_data = read_data_from_artifact(
            object_store_credentials,
            object_store_secret_details.metadata,
            s3_file_key,
            file_type,
            error_collector,
        )
        return file_data
    return []


def fetch_deployment_config(
    deployment_id: str,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
):
    try:
        deployment_config = ai_core_client.deployment.get(deployment_id, resource_group)
        return deployment_config
    except Exception as e:
        error_collector.add_error(
            ErrorCode.GENERIC_ERROR,
            f"Could not fetch configuration of the deployment id {deployment_id} failing with the error of {e}",
        )
        return []


def fetch_configuration_by_id(
    configuration_id: str,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
):
    try:
        configuration_response = ai_core_client.configuration.get(
            configuration_id, resource_group=resource_group
        )
        return configuration_response
    except Exception as e:
        error_collector.add_error(
            ErrorCode.GENERIC_ERROR,
            f"Could not fetch configuration of the configuration id {configuration_id} failing with the error of {e}",
        )
        return []


def call_orchestration_service_with_v2_config(
    test_orch_config: dict,
    ai_core_client: AICoreV2Client,
    orchestration_deployment_url: str,
    resource_group: str,
    error_collector: ValidationCollector,
    proxy_client=None,
):
    try:
        # Create the orchestration service with the deployment URL
        orchestration_service = OrchestrationService(
            api_url=orchestration_deployment_url,
            proxy_client=proxy_client,
        )

        # Convert the dict config to OrchestrationConfig object
        orch_config = OrchestrationConfig(**test_orch_config)

        # Make the completion call using the orchestration_v2 client
        response = orchestration_service.run(config=orch_config)

        # If we get here, the call succeeded
        return response

    except Exception as e:
        error_collector.add_error(
            ErrorCode.INVALID_ORCHESTRATION_CONFIG_ERROR,
            f"Error occurred: {e} while trying to run the test orchestration config endpoint call with this user provided deployment url of {orchestration_deployment_url}",
        )


def upload_file_to_aws_s3(
    object_store_credentials: Union[_AWSObjectStoreData],
    object_store_secret_metadata_details: Dict[str, str],
    file_data: Any,
    file_key: str,
    file_type: str,
    error_collector: ValidationCollector,
):
    s3_file_client = S3FileClient(
        object_store_secret_metadata_details.get(AWS_OSS_BUCKET_URL_KEY),
        object_store_secret_metadata_details.get(AWS_OSS_REGION_URL_KEY),
        object_store_credentials.aws_access_key_id,
        object_store_credentials.aws_secret_access_key,
        error_collector=error_collector,
    )

    if file_type == CSV_FILE_TYPE:
        return s3_file_client.upload_csv(file_data, file_key)

    elif file_type == JSON_FILE_TYPE:
        return s3_file_client.upload_json(file_data, file_key)
    # not csv and json trying jsonl
    return s3_file_client.upload_jsonl(file_data, file_key)


def upload_evaluation_dataset_data(
    evaluation_config_data: _EvaluationConfigData,
    object_store_credentials: Union[_AWSObjectStoreData],
    object_store_secret_name: str,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
):
    """Method to upload the evaluation config data using the object store secrets data passed"""
    # creating a unique uuid name for the rootfolder.
    artifact_folder_path = generate_random_id()
    root_folder_id = artifact_folder_path
    logger.info("Randomly created root folder id created is %s", artifact_folder_path)
    logger.info(
        "Using Object Store Secret %s to upload the files from the config provided",
        object_store_secret_name,
    )
    object_store_secret_details: ObjectStoreSecret = fetch_object_store_secret_by_name(
        ai_core_client, object_store_secret_name, resource_group, error_collector
    )

    aicore_configuration_dataset_file_path = ""

    if isinstance(object_store_credentials, _AWSObjectStoreData):
        path_prefix_key = object_store_secret_details.metadata.get(
            AWS_OSS_PATH_PREFIX_URL_KEY
        )
        if path_prefix_key:
            root_folder_id = os.path.join(path_prefix_key, root_folder_id)
            logger.info(
                "Updated rootfolder after incorporating pathPrefix value from secret is %s",
                root_folder_id,
            )

        # uploading the testdataset to testdataset folder
        dataset_folder = os.path.join(root_folder_id, DATASET_FOLDER_KEY)
        dataset_data = evaluation_config_data.dataset_data
        dataset_type = evaluation_config_data.dataset_type
        dataset_file_name = f"{generate_random_id()[:7]}.{dataset_type}"  # taking only 7chars from the generated random id.

        dataset_file_key = os.path.join(dataset_folder, dataset_file_name)
        aicore_configuration_dataset_file_path = os.path.join(
            DATASET_FOLDER_KEY, dataset_file_name
        )

        dataset_file_uploaded = upload_file_to_aws_s3(
            object_store_credentials,
            object_store_secret_details.metadata,
            dataset_data,
            dataset_file_key,
            dataset_type,
            error_collector,
        )
        if not dataset_file_uploaded:
            # stop uploading files if any of the file is not uploaded so to not waste the compute resources
            error_collector.add_error(
                ErrorCode.FILE_UPLOAD_ERROR,
                f"Error uploading testdataset to the object store secret with the folder path of {dataset_file_key}",
            )
            return "", ""

    return (
        artifact_folder_path,
        aicore_configuration_dataset_file_path,
    )


def register_aicore_artifact(
    artifact_folder_path: str,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    object_store_secret_name: str,
    error_collector: ValidationCollector,
):
    input_artifact_path = os.path.join(
        AI_PROTOCOL_PREFIX, object_store_secret_name, artifact_folder_path
    )
    random_id = generate_random_id()
    artifact_name = EVALUATIONS_ARTIFACT_PREFIX_KEY + random_id[:7]
    logger.info("Artifact path of upload is %s", input_artifact_path)
    logger.info("Artifact file name is %s", artifact_name)

    try:
        response = ai_core_client.artifact.create(
            name=artifact_name,
            kind=Artifact.Kind.OTHER,
            url=input_artifact_path,
            scenario_id=EVALUATIONS_SCENARIO_ID,
            resource_group=resource_group,
            description=EVALUATIONS_ARTIFACT_DESCRIPTION,
        )
        artifact_id = response.id
        logger.info("result of artifact creation is %s", artifact_id)
        return artifact_id
    except Exception as e:
        error_collector.add_error(
            ErrorCode.ARTIFACT_CREATION_FAILURE,
            f"Error occurred while attempting to create an artifact with error of {e}",
        )
        return ""


def register_aicore_configuration(
    aicore_artifact_id: str,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    accumulated_config_data: _EvaluationConfigData,
    orchestration_url: str,
    dataset_file_key: str,
    run_ids_list: List[str],
    llm_model_config: str,
    template_config: List,
    orchestration_registry_config: str,
    error_collector: ValidationCollector,
):
    try:
        # logic to generate the uuids for templates or orchestration registry
        dataset_type = accumulated_config_data.dataset_type
        test_datasets = f'{{"path": "{dataset_file_key}", "type": "{dataset_type}"}}'
        test_row_count = accumulated_config_data.test_row_count
        distinct_metrics_list = list(set(accumulated_config_data.metrics_list))
        metrics_list = ",".join(distinct_metrics_list)
        variable_mapping = json.dumps(
            accumulated_config_data.variable_mapping
        )  # to validate if this generates the right escaped string

        logger.info(
            "The generated variable mapping is %s",
            variable_mapping,
        )
        tags = accumulated_config_data.tags
        run_ids = ",".join(
            run_ids_list
        )  # underlying executable expects string as a parameter

        repetitions = accumulated_config_data.repetitions
        random_id = generate_random_id()[:7]
        configuration_name = EVALUATIONS_CONFIG_PREFIX_KEY + random_id
        parameter_bindings_list = [
            ParameterBinding(key="repetitions", value=str(repetitions)),
            ParameterBinding(key="orchestrationDeploymentURL", value=orchestration_url),
            ParameterBinding(key="tags", value=str(tags)),
            ParameterBinding(key="variableMapping", value=variable_mapping),
            ParameterBinding(key="metrics", value=metrics_list),
            ParameterBinding(key="testDataset", value=test_datasets),
            ParameterBinding(key="testRowCount", value=str(test_row_count)),
            ParameterBinding(
                key="runIds", value=run_ids
            ),  # explicilty passing created run ids to the executable to map or create runs with the same id's
        ]
        if not accumulated_config_data.debug_mode:
            parameter_bindings_list.append(
                ParameterBinding(key="debugMode", value="OFF")
            )

        if llm_model_config is not None:
            parameter_bindings_list.append(
                ParameterBinding(key="models", value=llm_model_config)
            )
            parameter_bindings_list.append(
                ParameterBinding(key="promptTemplate", value=template_config[0])
            )
        else:
            parameter_bindings_list.append(
                ParameterBinding(
                    key="orchestrationRegistryIds", value=orchestration_registry_config
                )
            )

        response = ai_core_client.configuration.create(
            name=configuration_name,
            scenario_id=EVALUATIONS_SCENARIO_ID,
            # executable_id=EVALUATIONS_SCENARIO_ID,
            executable_id="genai-evaluations-simplified",  # to replace with main simplified executable once changes are merged, till then testing with locally built executable
            parameter_bindings=parameter_bindings_list,
            input_artifact_bindings=[
                InputArtifactBinding(
                    key="datasetFolder", artifact_id=aicore_artifact_id
                )
            ],
            resource_group=resource_group,
        )

        configuration_id = response.id
        logger.info("configuration id created is %s", configuration_id)
        return configuration_id
    except Exception as e:
        error_collector.add_error(
            ErrorCode.CONFIGURATION_CREATION_FAILURE,
            f"Error occurred while attempting to create aicore configuration with error of {e}",
        )
        return None


def register_aicore_execution(
    ai_core_client: AICoreV2Client,
    configuration_id: str,
    resource_group: str,
    error_collector: ValidationCollector,
):
    try:
        response = ai_core_client.execution.create(configuration_id, resource_group)
        execution_id = response.id
        logger.info("result of execution creation is %s", execution_id)
        return execution_id
    except Exception as e:
        error_collector.add_error(
            ErrorCode.EXECUTION_CREATION_FAILURE,
            f"Error occurred while attempting to create an execution with error of {e}",
        )
        return None


def list_available_llm_models(ai_core_client: AICoreV2Client, resource_group: str):
    try:
        return ai_core_client.model.query(resource_group).resources
    except Exception as e:
        raise RuntimeError(
            f"Failed to list the available models with the error of {e}"
        ) from e


def fetch_orchestration_config_from_registry(
    orchestration_registry_reference: str,
    ai_core_client: AICoreV2Client,
    error_collector: ValidationCollector,
):
    # using restClient as the prompt registry haven't added orchestration registry endpoint yet in the sdk
    # curl -X GET "{{apiurl}}/v2/registry/v2/orchestrationConfigs?name=example-orchestration-config&scenario=customer-support&version=0.0.1" \
    try:
        orch_registry_url_path = (
            f"{ORCHESTRATION_REGISTRY_ENDPOINT}/{orchestration_registry_reference}"
        )
        response = ai_core_client.rest_client.get(path=orch_registry_url_path)
        return response["spec"]

    except Exception as e:
        error_collector.add_error(
            ErrorCode.GENERIC_ERROR,
            f"Orchestration config GET request from Orchestration regsitry failed with error of {e}",
        )
    return None

def resolve_metric_identifiers(
    metrics: List[MetricConfig],
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
) -> List[Dict]:
    """
    Resolves metric identifiers to metric template metadata.
    """
    metric_templates: List[Dict] = []

    for metric in metrics:
        metric_info = _resolve_single_metric(
            metric,
            ai_core_client,
            resource_group,
            error_collector,
        )

        if metric_info:
            metric_templates.append(metric_info)

    return metric_templates

def _resolve_single_metric(
    metric: MetricConfig,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
) -> Dict | None:
    metric_reference = metric.reference

    if metric_reference.id is not None:
        return _resolve_metric_by_id(
            metric_reference.id,
            ai_core_client,
            resource_group,
            error_collector,
        )

    if _has_scenario_name_version(metric_reference):
        return _resolve_metric_by_metadata(
            metric_reference,
            ai_core_client,
            resource_group,
            error_collector,
        )

    if _is_system_defined_metric(metric_reference):
        return _resolve_system_metric(
            metric_reference.name,
            ai_core_client,
            resource_group,
            error_collector,
        )

    error_collector.add_error(
        ErrorCode.METRIC_CONFIG_ERROR,
        (
            "Could not resolve metric config from Metric Management Service. "
            "Please provide one of id or name or (scenario,name,version) "
            f"combination for this metric reference of {metric.reference}"
        ),
    )
    return None

def _has_scenario_name_version(metric_reference) -> bool:
    return all(
        [
            metric_reference.scenario,
            metric_reference.name,
            metric_reference.version,
        ]
    )

def _is_system_defined_metric(metric_reference) -> bool:
    return (
        metric_reference.name is not None
        and metric_reference.name in SYSTEM_DEFINED_METRIC_MAPPING.values()
    )


def _resolve_metric_by_id(
    metric_id: str,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
) -> Dict | None:
    metric_info = get_custom_metric_by_id(
        metric_id,
        ai_core_client,
        resource_group,
        error_collector,
    )

    if not metric_info:
        error_collector.add_error(
            ErrorCode.METRIC_SERVER_RESOLVE_ERROR,
            f"Could not resolve metric with ID {metric_id}",
        )
        return None

    return metric_info

def _resolve_metric_by_metadata(
    metric_reference,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
) -> Dict | None:
    metric_info = get_metric_version_history(
        metric_reference.scenario,
        metric_reference.name,
        metric_reference.version,
        ai_core_client,
        resource_group,
        error_collector,
    )

    if not metric_info:
        error_collector.add_error(
            ErrorCode.METRIC_SERVER_RESOLVE_ERROR,
            f"Could not resolve metric {metric_reference} — no version history found",
        )
        return None

    return metric_info

def _resolve_system_metric(
    metric_name: str,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
) -> Dict | None:
    metric_info = get_metric_template_info_from_server(
        metric_name,
        ai_core_client,
        resource_group,
        error_collector,
    )

    if not metric_info:
        error_collector.add_error(
            ErrorCode.METRIC_SERVER_RESOLVE_ERROR,
            f"Could not resolve metric {metric_name} — not found in Metric Server",
        )
        return None

    return metric_info



def resolve_metric_names(
    metric_configs_list: List[MetricConfig], error_collector: ValidationCollector
):
    resolved_metrics_list = []

    for metric_config in metric_configs_list:
        metric_reference = metric_config.reference
        if metric_reference.id is not None:
            resolved_metrics_list.append(metric_reference.id)
        elif all(
            [metric_reference.scenario, metric_reference.name, metric_reference.version]
        ):
            resolved_metrics_list.append(
                "/".join(
                    [
                        metric_reference.scenario,
                        metric_reference.name,
                        metric_reference.version,
                    ]
                )
            )
        elif metric_reference.name is not None:
            resolved_metrics_list.append(metric_reference.name)
        else:
            error_collector.add_error(
                ErrorCode.METRIC_CONFIG_ERROR,
                f"Could not identify metric name. Please provide one of id or name or (scenario,name,version) combination for this metric config of {metric_reference}",
            )

    return resolved_metrics_list
