from typing import Optional, Union
import httpx

from gen_ai_hub import GenAIHubProxyClient
from gen_ai_hub.proxy import get_proxy_client
from gen_ai_hub.proxy.native.sap.models import RPTResponse, RPTException, RPTRequest

PREDICTION_SUFFIX = "/predict"

def _handle_http_error(error, response: httpx.Response):

    if not response.content:
        raise error
    try:
        error_status = response.json().get("status", {})
        error_detail = response.json().get("detail", None)
    except ValueError as exc:
        raise error from exc
    raise RPTException(
            status=error_status,
            detail=error_detail,
        ) from error


class RPTClient:
    """
    Handles interaction with RPT models for making predictions.

    This class acts as a client for executing prediction requests using RPT
    models deployed via the Gen AI Hub. It retrieves deployment information,
    handles timeouts, and processes request and response data.

    :param proxy_client: Proxy client for interacting with the Gen AI Hub API.
                         If not provided, a default implementation is used.
    :type proxy_client: Optional[GenAIHubProxyClient]

    :param timeout: Default timeout value for the HTTP client used for requests.
    :type timeout: Union[int, float, httpx.Timeout, None]
    """

    def __init__(
            self,
            proxy_client: Optional[GenAIHubProxyClient] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
    ):
        self.proxy_client = proxy_client or get_proxy_client(proxy_version="gen-ai-hub")
        self.timeout = timeout
        self.client = httpx.Client(timeout=self.timeout)
        self.async_client = httpx.AsyncClient(timeout=self.timeout)

    def _determine_timeout(self, timeout: httpx.Timeout) -> httpx.Timeout:
        # Determine the timeout to use for this request
        if timeout is not None:
            # Overwrite default timeout for this request
            request_timeout = timeout
        elif self.timeout is not None:
            # Use the  default timeout is set
            request_timeout = self.timeout
        else:
            # If timeout is not set, use httpx client's default behavior, rather than "None" (disables timeout)
            request_timeout = httpx.USE_CLIENT_DEFAULT
        return request_timeout

    def _execute_request(
            self,
            body: RPTRequest,
            api_url: str,
            timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> RPTResponse:
        """
        Executes an HTTP POST request to a prediction API endpoint with the given
        body, headers, URL, and timeout configuration.

        This method serializes the given request body to JSON and sends it to the
        constructed API endpoint.

        :param body: The request object containing the necessary data to be sent
                     to the prediction API.
        :type body: RPTRequest

        :param api_url: The base URL of the API to which the request is made.
        :type api_url: str

        :param timeout: The timeout configuration for the HTTP request. Can be an
                        integer, float, httpx.Timeout object, or None.
        :type timeout: Union[int, float, httpx.Timeout, None]

        :returns: A response object representing the data returned from the API
                  after successful execution.
        :rtype: RPTResponse

        :raises RPTException: If the response contains any HTTP status errors.
        """

        response = self.client.post(
            api_url + PREDICTION_SUFFIX,
            headers=self.proxy_client.request_header,
            json=body.model_dump(),
            timeout=self._determine_timeout(timeout)
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            _handle_http_error(error, response)

        data = response.json()
        return RPTResponse(**data)

    async def _a_execute_request(
            self,
            body: RPTRequest,
            api_url: str,
            timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> RPTResponse:
        """
        Asynchronously executes an HTTP POST request to a prediction API endpoint
        with the given body, headers, URL, and timeout configuration.

        This method serializes the given request body to JSON and sends it to the
        constructed API endpoint.

        :param body: The request object containing the necessary data to be sent
                     to the prediction API.
        :type body: RPTRequest

        :param api_url: The base URL of the API to which the request is made.
        :type api_url: str

        :param timeout: The timeout configuration for the HTTP request. Can be an
                        integer, float, httpx.Timeout object, or None.
        :type timeout: Union[int, float, httpx.Timeout, None]

        :returns: A response object representing the data returned from the API
                  after successful execution.
        :rtype: RPTResponse

        :raises RPTException: If the response contains any HTTP status errors.
        """

        response = await self.async_client.post(
            api_url + PREDICTION_SUFFIX,
            headers=self.proxy_client.request_header,
            json=body.model_dump(),
            timeout=self._determine_timeout(timeout)
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            _handle_http_error(error, response)

        data = response.json()
        return RPTResponse(**data)

    def _get_url(self, model_name: Optional[str] = None, model_version: Optional[str] = None, **kwargs) -> str:
        """
        Builds a URL for the selected deployment based on the provided model
        name and/or deployment ID.

        This function queries a proxy client to select a deployment that matches
        the specified criteria (model name and/or deployment ID) and retrieves
        the deployment's URL. If no matching deployment is found, an exception
        is raised.

        :param model_name: The name of the model to filter deployments.
        :type model_name: Optional[str]
        :param model_version: The version of the model to filter deployments.
        :type model_version: Optional[str]

        :param kwargs: Additional keyword arguments for identifying the deployment.
        :type kwargs: dict

        :returns: The URL of the selected deployment.
        :rtype: str

        :raises ValueError: If no deployment matches the provided parameters.
        """
        filters = kwargs.copy()
        if model_name:
            filters["model_name"] = model_name
        if model_version:
            filters["model_version"] = model_version
        try:
            url = self.proxy_client.select_deployment(**filters).url
        except ValueError:
            raise ValueError(f"No deployment found for the given parameters:{filters}.")
        return url

    def _validate_request_body(self, body: Union[dict, RPTRequest]):
        if isinstance(body, dict):
            return RPTRequest(**body)
        return body

    def _validate_parameters(self, model_name: Optional[str] = None, model_version: Optional[str] = None,
                             deployment_url: Optional[str] = None, **kwargs):
        if not model_name and not deployment_url and not kwargs:
            raise ValueError("Deployment URL or model_name or other deployment parameters must be provided.")
        if model_version and not model_name:
            raise ValueError("model_version can be provided only if model_name is provided.")

    def predict(self,
                body: Union[dict, RPTRequest],
                deployment_url: Optional[str] = None,
                model_name: Optional[str] = None,
                model_version: Optional[str] = None,
                timeout: Union[int, float, httpx.Timeout, None] = None,
                **kwargs) -> RPTResponse:
        """
        Executes a prediction request by sending the provided data and deployment parameters.

        The `body` parameter can be supplied either as a dictionary or as an instance of `RPTRequest`.

        :param body: The input data for the prediction request, represented either as a
                     dictionary or an `RPTRequest` object.
        :type body: Union[dict, RPTRequest]

        :param deployment_url: The URL of the deployment to use for prediction. If not provided,
                        `model_name` or other deployment parameters must be specified.
        :type deployment_url: Optional[str]

        :param model_name: The name of the model to use for prediction. If not provided,
                           `api_url` or other deployment parameters must be specified.
        :type model_name: Optional[str]
        :param model_version: The version of the model to use for prediction.
                              Could be provided only if `model_name` is provided.
        :type model_version: Optional[str]
        :param timeout: The time duration to wait for the prediction request to complete.
                        Can be an integer, float, or an instance of `httpx.Timeout`.
        :type timeout: Union[int, float, httpx.Timeout, None]

        :returns: The response received from the prediction endpoint, represented as an
                  `RPTResponse` object.
        :rtype: RPTResponse

        :raises ValueError: If no deployment is found for the given parameters.
        """
        body = self._validate_request_body(body)
        self._validate_parameters(model_name, model_version, deployment_url, **kwargs)
        return self._execute_request(body=body,
                                     api_url = deployment_url if deployment_url else self._get_url(
                                         model_name, model_version, **kwargs),
                                     timeout=timeout)

    async def apredict(self,
                       body: Union[dict, RPTRequest],
                       deployment_url: Optional[str] = None,
                       model_name: Optional[str] = None,
                       model_version: Optional[str] = None,
                       timeout: Union[int, float, httpx.Timeout, None] = None,
                       **kwargs) -> RPTResponse:
        """
        Asynchronously executes a prediction request by sending the provided data and deployment parameters.

        The `body` parameter can be supplied either as a dictionary or as an instance of `RPTRequest`.

        :param body: The input data for the prediction request, represented either as a
                     dictionary or an `RPTRequest` object.
        :type body: Union[dict, RPTRequest]

        :param deployment_url: The URL of the deployment to use for prediction. If not provided,
                        `model_name` or other deployment parameters must be specified.
        :type deployment_url: Optional[str]

        :param model_name: The name of the model to use for prediction. If not provided,
                           `api_url` or other deployment parameters must be specified.
        :type model_name: Optional[str]

        :param model_version: The version of the model to use for prediction.
                              Could be provided only if `model_name` is provided.
        :type model_version: Optional[str]

        :param timeout: The time duration to wait for the prediction request to complete.
                        Can be an integer, float, or an instance of `httpx.Timeout`.
        :type timeout: Union[int, float, httpx.Timeout, None]

        :returns: The response received from the prediction endpoint, represented as an
                  `RPTResponse` object.
        :rtype: RPTResponse

        :raises ValueError: If no deployment is found for the given parameters.
        """
        body = self._validate_request_body(body)
        self._validate_parameters(model_name, model_version, deployment_url, **kwargs)
        return await self._a_execute_request(body=body,
                                             api_url = deployment_url if deployment_url else self._get_url(
                                                 model_name, model_version, **kwargs),
                                             timeout=timeout)
