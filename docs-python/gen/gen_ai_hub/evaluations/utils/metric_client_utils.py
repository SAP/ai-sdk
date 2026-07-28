import requests
from ai_core_sdk.ai_core_v2_client import AICoreV2Client
from gen_ai_hub.evaluations.constants import (
    CONTENT_TYPE,
    METRIC_SERVER_ENDPOINT,
    EVALUATION_METRICS_ENDPOINT,
)
from gen_ai_hub.evaluations.helpers.collector import ValidationCollector
from gen_ai_hub.evaluations.exceptions.error_codes import ErrorCode

from gen_ai_hub.evaluations.helpers.logging import get_logger

logger = get_logger()


def _get_custom_metric_details(
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
) -> dict | None:
    """
    Fetches custom metric details from the given GenAI metrics server endpoint via a GET request.

    Note: Not using rest_client.get() because it converts camelCase to snake_case,
    but the Metric Management Service requires exact camelCase field names.

    :param ai_core_client: AI Core client instance for API access.
    :type ai_core_client: AICoreV2Client
    :param resource_group: The resource group name.
    :type resource_group: str
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: Parsed JSON response as a dictionary, or None if request fails.
    :rtype: dict | None
    """
    try:
        url_built = f"{ai_core_client.base_url}{METRIC_SERVER_ENDPOINT}"
        token = ai_core_client.rest_client.get_token()
        headers = {
            "Content-Type": CONTENT_TYPE,
            "Authorization": token,  # already sends token in Bearer token format
            "AI-Resource-Group": resource_group,
        }
        response = requests.get(
            url=url_built,
            headers=headers,
        )
        response = response.json()
        return response

    except Exception as e:
        error_collector.add_error(
            ErrorCode.METRIC_SERVER_RESOLVE_ERROR,
            f"GenAI metrics server GET request encountered an exception. Error: {e}",
        )
        return None


def get_custom_metric_by_id(
    metric_id: str,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
) -> dict | None:
    """
    Fetches a specific custom metric by its ID from the GenAI metrics server.

    Note: Not using rest_client.get() because it converts camelCase to snake_case,
    but the Metric Management Service requires exact camelCase field names like
    'additionalProperties' (would become 'additional_properties' if using rest_client).

    :param metric_id: The unique ID of the metric to retrieve.
    :type metric_id: str
    :param ai_core_client: AI Core client instance for API access.
    :type ai_core_client: AICoreV2Client
    :param resource_group: The resource group name.
    :type resource_group: str
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: Parsed JSON response as a dictionary, or None if not found.
    :rtype: dict | None
    """
    path = f"{METRIC_SERVER_ENDPOINT}/{metric_id}"
    logger.debug(
        f"Sending GET request to {path} for metric ID: {metric_id}",
    )
    try:
        # Not using rest_client of aicore as fields are getting snake cased by the rest client while all keys in schema of metric client uses camelCase like additionalProperties. if used via rest client its returning additional_properties whereas we need additionalProperties
        url_built = f"{ai_core_client.base_url}{path}"
        token = ai_core_client.rest_client.get_token()
        headers = {
            "Content-Type": CONTENT_TYPE,
            "Authorization": token,  # already sends token in Bearer token format
            "AI-Resource-Group": resource_group,
        }
        # response = requests.post(completion_url, json=test_orch_config, headers=headers)

        response = requests.get(
            url=url_built,
            headers=headers,
        )
        response = response.json()
        return response
    except Exception as e:
        error_collector.add_error(
            ErrorCode.METRIC_SERVER_RESOLVE_ERROR,
            f"GenAI metrics server GET request encountered an exception. Error: {e}",
        )
        return None


def get_metric_template_info_from_server(
    metric: str,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
):
    """
    Retrieves metric template information from the server by metric name.

    :param metric: The name of the metric to retrieve.
    :type metric: str
    :param ai_core_client: AI Core client instance for API access.
    :type ai_core_client: AICoreV2Client
    :param resource_group: The resource group name.
    :type resource_group: str
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: Metric information dictionary, or None if not found.
    :rtype: dict | None
    """
    all_metric = _get_custom_metric_details(
        ai_core_client, resource_group, error_collector
    )
    metric_id = None
    for current_metric in all_metric.get("resources", []):
        if current_metric["name"] == metric:
            metric_id = current_metric["id"]
    if metric_id:
        metric_info = get_custom_metric_by_id(
            metric_id, ai_core_client, resource_group, error_collector
        )
        return metric_info
    return None


def get_metric_version_history(
    scenario: str,
    metric_id: str,
    version: str,
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
) -> dict | None:
    """
    Fetches the version history for a specific evaluation metric in a scenario.

    Note: Not using rest_client.get() because it converts camelCase to snake_case,
    but the Metric Management Service requires exact camelCase field names.

    :param scenario: The name of the scenario.
    :type scenario: str
    :param metric_id: The unique ID of the evaluation metric.
    :type metric_id: str
    :param version: The version of the metric.
    :type version: str
    :param ai_core_client: AI Core client instance for API access.
    :type ai_core_client: AICoreV2Client
    :param resource_group: The resource group name.
    :type resource_group: str
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: Parsed JSON response as a dictionary, or None if not found.
    :rtype: dict | None
    """
    path = f"/lm/scenarios/{scenario}{EVALUATION_METRICS_ENDPOINT}/{metric_id}/versions/{version}/history"
    logger.debug(
        f"Sending GET request to {path} for scenario: {scenario}, metric: {metric_id}, version: {version}",
    )

    try:
        # removed other valiations of Http status code being not found and other checks from the prompt eval repo as here it is being handled from the rest_client and not a seperate metric_management_service client

        url_built = f"{ai_core_client.base_url}{path}"
        token = ai_core_client.rest_client.get_token()
        headers = {
            "Content-Type": CONTENT_TYPE,
            "Authorization": token,  # already sends token in Bearer token format
            "AI-Resource-Group": resource_group,
        }
        response = requests.get(
            url=url_built,
            headers=headers,
        )
        response = response.json()
        resources = response.get("resources", [])
        if resources:
            return resources[0]  # return the latest metric version
        else:
            error_collector.add_error(
                ErrorCode.METRIC_SERVER_RESOLVE_ERROR,
                f"No version history resources found for scenario: {scenario}, metric: {metric_id}, version: {version}",
            )
            return None

    except Exception as e:
        error_collector.add_error(
            ErrorCode.METRIC_SERVER_RESOLVE_ERROR,
            f"GenAI metrics server GET request encountered an exception for metric version history. Scenario: {scenario}, metric: {metric_id}, version: {version}. Error: {e}",
        )
        return None


def fetch_all_system_predefined_metrics(
    ai_core_client: AICoreV2Client,
    resource_group: str,
    error_collector: ValidationCollector,
):
    """
    Fetches all system-predefined metrics from the GenAI metrics server.

    :param ai_core_client: AI Core client instance for API access.
    :type ai_core_client: AICoreV2Client
    :param resource_group: The resource group name.
    :type resource_group: str
    :param error_collector: ValidationCollector instance for collecting validation errors.
    :type error_collector: ValidationCollector
    :return: List of system-predefined metric templates.
    :rtype: list
    :raises RuntimeError: If fetching system predefined metrics fails.
    """
    try:
        all_metrics_info = _get_custom_metric_details(
            ai_core_client, resource_group, error_collector
        )
        all_metric_templates = all_metrics_info.get("resources", [])

        predefined_metric_templates = [
            item
            for item in all_metric_templates
            if item.get("systemPredefined")
            is True  # filtering metric templates based on systemPredefined flag from metric management service
        ]

        return predefined_metric_templates
    except Exception as e:
        raise RuntimeError(
            f"System Predefined metrics obtained from Metric Management service failed with error of {e}"
        )
