import uuid
import re
import pandas as pd
from typing import Optional, Any, List
from dataclasses import dataclass
from ai_api_client_sdk.models.status import Status
from ai_core_sdk.ai_core_v2_client import AICoreV2Client
from ai_core_sdk.tracking.tracking import Tracking
from gen_ai_hub.evaluations.utils.aicore_utils import wait_for_target_status
from gen_ai_hub.evaluations.constants import (
    ADDITIONAL_INFO_KEY,
    DEFAULT_KEY,
    AWS_OSS_PATH_PREFIX_URL_KEY,
    DEFAULT_TIMEOUT,
    RESULTS_FILE_KEY,
    AWS_OSS_BUCKET_URL_KEY,
    AWS_OSS_REGION_URL_KEY,
    COMPLETIONS_TABLE_KEY,
    METRICS_TABLE_KEY,
)
from gen_ai_hub.evaluations.helpers.s3_file_client import S3FileClient
from gen_ai_hub.evaluations._internal._models import (
    _AWSObjectStoreData,
)


@dataclass
class ExecutionStatusDetails:
    """Dataclass for execution status details.

    :param details: Detailed information about the execution status
    :type details: Any
    :param status: Current status of the execution
    :type status: Any
    """
    details: Any
    status: Any


class _RunContext:
    """Holds the metadata context information of the EvaluationRun object.

    :param execution_id: ID of the AI Core execution
    :param configuration_id: ID of the configuration
    :param artifact_id: ID of the artifact
    :param ai_core_client: AI Core client instance
    :param resource_group: Resource group name
    :param object_store_credentials: Object store credentials
    :param metrics_list: List of metrics to evaluate
    :param cached_results_data: Cached results data, defaults to None
    """

    def __init__(
        self,
        execution_id,
        configuration_id,
        artifact_id,
        ai_core_client,
        resource_group,
        object_store_credentials,
        metrics_list,
        cached_results_data=None,
    ):
        self.execution_id = execution_id
        self.configuration_id = configuration_id
        self.artifact_id = artifact_id
        self.ai_core_client = ai_core_client
        self.resource_group = resource_group
        self.object_store_credentials = object_store_credentials
        self.metrics_list = metrics_list
        self.cached_results_data = cached_results_data


class EvaluationRun:
    """Represents an individual EvaluationRun object and its associated context.

    :param run_id: Unique identifier for the evaluation run
    :type run_id: str
    :param execution_id: ID of the AI Core execution
    :type execution_id: str
    :param ai_core_client: AI Core client instance
    :type ai_core_client: AICoreV2Client
    :param configuration_id: ID of the configuration, defaults to None
    :type configuration_id: str
    :param artifact_id: ID of the artifact, defaults to None
    :type artifact_id: str
    :param resource_group: Resource group name, defaults to None
    :type resource_group: str
    :param object_store_credentials: Object store credentials, defaults to None
    :type object_store_credentials: _AWSObjectStoreData
    :param metrics_list: List of metrics to evaluate, defaults to None
    :type metrics_list: List[str]
    """

    # Step-level error messages for failed pods
    _STEP_ERROR_MESSAGES = {
        "combine": "Evaluation job failed in Aggregating Results step.",
        "completion": "Evaluation job failed in generating Completion Responses step.",
        "config": "Evaluation job failed in Config Validation step.",
    }

    def __init__(
        self,
        run_id: str,
        execution_id: str,
        ai_core_client: AICoreV2Client,
        configuration_id: str = None,
        artifact_id: str = None,
        resource_group: str = None,
        object_store_credentials: _AWSObjectStoreData = None,
        metrics_list: List[str] = None,
    ):
        self.id = run_id
        self.status = Status.UNKNOWN
        self._run_context = _RunContext(
            # RUNTIME_INFO OBJECT ISOLATION
            execution_id=execution_id,
            configuration_id=configuration_id,
            artifact_id=artifact_id,
            ai_core_client=ai_core_client,
            resource_group=resource_group,
            object_store_credentials=object_store_credentials,
            metrics_list=metrics_list,
            cached_results_data=None,
        )

    def set_cached_results_data(self, data):
        """Set the cached results data from the child results class.

        :param data: Results data to cache
        :type data: Any
        """
        self._cached_results_data = data

    def _execution_status_fetcher(self):
        return self._run_context.ai_core_client.execution.get(
            execution_id=self._run_context.execution_id,
            resource_group=self._run_context.resource_group,
            select="status",
        )

    def wait_for_completion(self, timeout: Optional[int] = None):
        """Wait for the evaluation run to complete by polling status.

        :param timeout: Maximum time to wait in seconds, defaults to 3600 (1 hour)
        :type timeout: Optional[int]
        """

        wait_for_target_status(
            status_fetcher=self._execution_status_fetcher,
            target_status=Status.COMPLETED,
            timeout=timeout or DEFAULT_TIMEOUT,  # one hour
        )
        return

    def get_current_status(self):
        """Get the current status of the evaluation run.

        :return: Current status of the run
        :rtype: Status
        :raises ValueError: If failed to retrieve the current status
        """
        try:
            response = self._execution_status_fetcher()
            return response.status

        except Exception as e:
            raise ValueError(
                f"Failed to get the current status of the run with the error of {e}"
            )

    # for now mention that everything is run_id not specific and will come up in future.
    # User might be interested in run_id specific logs.
    def get_debug_info(self) -> ExecutionStatusDetails:
        """Provide debug information when execution status is FAILED or DEAD.

        :return: Execution status details including failed pod information
        :rtype: ExecutionStatusDetails
        """
        execution_status_response = self._execution_status_fetcher()
        current_status = execution_status_response.status
        status_details = getattr(execution_status_response, "status_details", None)

        if not status_details:
            return ExecutionStatusDetails(
                details=(
                    "No specific details found. Please use get_debug_logs() "
                    "function to get more information!"
                ),
                status=current_status,
            )

        failed_pod_details = self._extract_failed_pods(status_details)
        workflow_lookup = self._build_workflow_lookup(status_details)

        self._enrich_failed_pods(
            failed_pod_details,
            workflow_lookup,
        )

        return ExecutionStatusDetails(
            details=failed_pod_details,
            status=current_status,
        )

    def _extract_failed_pods(self, status_details: dict) -> list[dict]:
        details = status_details.get("details", [])

        return [
            {
                "name": c["pod_name"],
                "last_log_message": c["last_log_messages"],
            }
            for c in details
            if c.get("exit_code", 0) > 0
        ]

    def _build_workflow_lookup(self, status_details: dict) -> dict:
        workflow_lookup = {}

        for workflow in status_details.get("workflow_info", []):
            workflow_id = workflow.get("id", "")
            suffix = workflow_id.split("-")[-1]
            workflow_lookup[suffix] = workflow

        return workflow_lookup

    def _enrich_failed_pods(
        self,
        failed_pods: list[dict],
        workflow_lookup: dict,
    ) -> None:
        for pod in failed_pods:
            pod_name = pod.get("name", "")

            if self._apply_step_level_message(pod, pod_name):
                continue

            self._apply_metric_level_message(
                pod,
                pod_name,
                workflow_lookup,
            )

    def _apply_step_level_message(
        self,
        pod: dict,
        pod_name: str,
    ) -> bool:
        for key, message in self._STEP_ERROR_MESSAGES.items():
            if key in pod_name:
                pod[ADDITIONAL_INFO_KEY] = message
                return True
        return False

    def _apply_metric_level_message(
        self,
        pod: dict,
        pod_name: str,
        workflow_lookup: dict,
    ) -> None:
        suffix = pod_name.split("-")[-1]
        workflow = workflow_lookup.get(suffix)

        if not workflow:
            return

        metric_name = self._extract_metric_name(workflow.get("name", ""))
        message = workflow.get("message", "Unknown error")

        pod[ADDITIONAL_INFO_KEY] = (
            f"Evaluation job failed in metric evaluation for "
            f"'{metric_name}' with error: {message}"
        )

    def _extract_metric_name(self, name: str) -> str | None:
        match = re.search(r"metric_name:([^,)\s]+(?: [^,)\s]+)*)", name)
        return match.group(1) if match else None


    def get_debug_logs(self):
        """Get the complete trace of execution logs.

        :return: List of log entries as dictionaries
        :rtype: list
        """
        execution_logs = self._run_context.ai_core_client.execution.query_logs(
            execution_id=self._run_context.execution_id
        )
        log_items = execution_logs.data.result
        log_values = [item.__dict__ for item in log_items]
        return log_values

    def results(self):
        """Get the results of the evaluation run.

        :return: Results object for accessing completion and metric results
        :rtype: Results
        :raises ValueError: If execution is not completed
        """
        # validate if execution is actually completed
        execution_status = self._execution_status_fetcher().status
        if execution_status != Status.COMPLETED:
            if execution_status == Status.RUNNING:
                raise ValueError(
                    "status of the run is Running, Use wait_for_completion() to wait until completed and then see the results"
                )
            else:
                raise ValueError(
                    f"Cannot call results as the status of run is not yet completed. The current status is {execution_status}"
                )

        return Results(self)

    def load_results_tables(self):
        """Download results from S3 and load the required table data.

        :return: Dictionary containing completions and metrics table data
        :rtype: dict
        :raises RuntimeError: If failed to download results
        """
        try:
            if self._run_context.cached_results_data:
                return self._run_context.cached_results_data

            secret_response = self._run_context.ai_core_client.object_store_secrets.get(
                name=DEFAULT_KEY, resource_group=self._run_context.resource_group
            )
            metadata_details = secret_response.metadata

            if isinstance(
                self._run_context.object_store_credentials, _AWSObjectStoreData
            ):
                secret_path_prefix = metadata_details.get(AWS_OSS_PATH_PREFIX_URL_KEY)
                aws_bucket_name = metadata_details.get(AWS_OSS_BUCKET_URL_KEY)
                aws_region = metadata_details.get(AWS_OSS_REGION_URL_KEY)
                s3_file_client = S3FileClient(
                    aws_bucket_name,
                    aws_region,
                    self._run_context.object_store_credentials.aws_access_key_id,
                    self._run_context.object_store_credentials.aws_secret_access_key,
                )
                results_db_file_key = f"{secret_path_prefix}/{self._run_context.execution_id}/tmp/{RESULTS_FILE_KEY}"
                tables_to_load = [
                    COMPLETIONS_TABLE_KEY,
                    METRICS_TABLE_KEY,
                ]
                data = s3_file_client.get_sqlitedb_tables_data_from_s3(
                    results_db_file_key, tables_to_load
                )
                return data
        except Exception as e:
            raise RuntimeError(
                f"Could not download the results for the run id :{self.id} failing with: ",
                e,
            ) from e


def configure_pandas_display():
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.expand_frame_repr", False)


class Results:
    """Represents the Results handler for an EvaluationRun object.

    This class provides methods to access completion results, metric results,
    and aggregated results for a specific evaluation run.

    :param run: The parent EvaluationRun object
    :type run: EvaluationRun
    """

    def __init__(self, run: EvaluationRun):
        self.run = run
        self._data_store = None
        self._run_context = self.run._run_context
        self._tracking_client = Tracking(
            base_url=self._run_context.ai_core_client.base_url,
            token_creator=self._run_context.ai_core_client.rest_client.get_token,
            resource_group=self._run_context.resource_group,
        )
        configure_pandas_display()

    def _ensure_loaded(self):
        """Fetch and store results data if not already loaded.

        Lazy-loads the table data only when results are accessed.
        """
        if self._data_store is None:
            self._data_store = self.run.load_results_tables()
            self.run.set_cached_results_data(self._data_store)

    def _filter_by_run_id(self, data: List[dict], run_id):
        """Filter data to return only rows for the specified run_id.

        :param data: List of data dictionaries to filter
        :type data: List[dict]
        :param run_id: Run ID to filter by
        :type run_id: str
        :return: Filtered list containing only rows matching the run_id
        :rtype: list
        """
        run_id = uuid.UUID(
            run_id
        ).hex
        filtered_store = [
            current_row for current_row in data if current_row.get("run_id") == run_id
        ]
        return filtered_store

    def completions(self):
        """Get the completion results for the run.

        :return: DataFrame containing completion results for the run
        :rtype: pd.DataFrame
        :raises ValueError: If error occurs while fetching completions
        """
        try:
            self._ensure_loaded()
            filtered_data = self._filter_by_run_id(
                self._data_store[COMPLETIONS_TABLE_KEY], self.run.id
            )
            df = pd.DataFrame(filtered_data)
            return df
        except Exception as e:
            raise ValueError("Error while trying to fetch completions: ", e) from e

    def metrics(self):
        """Get the metric-level results for the run.

        :return: DataFrame containing metric results for the run
        :rtype: pd.DataFrame
        :raises ValueError: If error occurs while fetching metric results
        """
        try:
            self._ensure_loaded()
            run_id_filtered_rows = self._filter_by_run_id(
                self._data_store[METRICS_TABLE_KEY], self.run.id
            )
            df = pd.DataFrame(run_id_filtered_rows)
            return df
        except Exception as e:
            raise ValueError("Error while trying to fetch metric results: ", e) from e

    def aggregations(self):
        """Get the aggregated results for the run from the tracking service.

        :return: JSON response containing aggregated metric results
        :rtype: dict
        :raises ValueError: If error occurs while fetching aggregation results
        """
        try:
            run_id = self.run.id
            run_id = uuid.UUID(run_id).hex

            response = self._tracking_client.query(execution_ids=[run_id])
            return response
        except Exception as e:
            raise ValueError(
                "Error while trying to fetch aggregation results from tracking service with error of: ",
                e,
            ) from e

__all__ = ["EvaluationRun", "Results"]
