"""
Module for orchestration service handling requests and responses.

Provides synchronous and asynchronous methods to run orchestration pipelines.
"""

from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from functools import wraps
import asyncio
import random
import time
import logging
from typing import List, Optional, Iterable, Union

import dacite
from gen_ai_hub.orchestration.exceptions import OrchestrationError
import httpx
from ai_api_client_sdk.models.status import Status

from gen_ai_hub import GenAIHubProxyClient
from gen_ai_hub.orchestration.models.base import JSONSerializable
from gen_ai_hub.orchestration.models.config import OrchestrationConfig
from gen_ai_hub.orchestration.models.message import Message
from gen_ai_hub.orchestration.models.response import OrchestrationResponse, OrchestrationResponseStreaming, \
    OrchestrationResponseWithRetries
from gen_ai_hub.orchestration.models.template import TemplateValue
from gen_ai_hub.orchestration.sse_client import SSEClient, AsyncSSEClient, _handle_http_error
from gen_ai_hub.proxy import get_proxy_client

COMPLETION_SUFFIX = "/completion"


@dataclass
class OrchestrationRequest(JSONSerializable):
    """
    Represents a request for the orchestration process, including configuration,
    template values, and message history.
    """
    config: OrchestrationConfig
    """The orchestration configuration for the request.

    :return: OrchestrationConfig
    :rtype: OrchestrationConfig
    """
    template_values: List[TemplateValue]
    """List of template values to be used in the orchestration."""
    history: List[Message]
    """List of messages representing the conversation history."""

    def to_dict(self):
        """Converts the OrchestrationRequest instance to a dictionary.

        :return: Dictionary representation of the OrchestrationRequest
        :rtype: dict
        """
        return {
            "orchestration_config": self.config.to_dict(),
            "input_params": {value.name: str(value.value) for value in self.template_values},
            "messages_history": [message.to_dict() for message in self.history],
        }


def cache_if_not_none(func):
    """Custom cache decorator that only caches non-None results

    :param func: The function to be decorated.
    :type func: callable
    :return: The decorated function with caching behavior.
    :rtype: callable
    """
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function that implements caching logic.

        :return: The result of the decorated function, either from cache or freshly computed.
        :rtype: Any
        """
        key = (args, frozenset(kwargs.items()))  # Create hashable key for cache
        if key not in cache:
            result = func(*args, **kwargs)
            if result is not None:  # Only cache if result is not None
                cache[key] = result
            return result
        return cache[key]

    def cache_clear():
        cache.clear()

    wrapper.cache_clear = cache_clear
    return wrapper


# pylint: disable=too-many-arguments,too-many-positional-arguments
@cache_if_not_none
def discover_orchestration_api_url(base_url: str,
                                   auth_url: str,
                                   client_id: str,
                                   client_secret: str,
                                   resource_group: str,
                                   config_id: Optional[str] = None,
                                   config_name: Optional[str] = None,
                                   orchestration_scenario: str = "orchestration",
                                   executable_id: str = "orchestration") -> Optional[str]:
    """Discovers the orchestration API URL based on provided configuration details.

    :param base_url: the base URL for the AI Core API.
    :type base_url: str
    :param auth_url: the URL for the AI Core authentication service.
    :type auth_url: str
    :param client_id: the client ID for the AI Core API.
    :type client_id: str
    :param client_secret: the client secret for the AI Core API.
    :type client_secret: str
    :param resource_group: the resource group for the AI Core API.
    :type resource_group: str
    :param config_id: the configuration ID, defaults to None
    :type config_id: Optional[str], optional
    :param config_name: the configuration name, defaults to None
    :type config_name: Optional[str], optional
    :param orchestration_scenario: the orchestration scenario ID, defaults to "orchestration"
    :type orchestration_scenario: str, optional
    :param executable_id: the orchestration executable ID, defaults to "orchestration"
    :type executable_id: str, optional
    :return: The orchestration API URL or None if no deployment is found.
    :rtype: Optional[str]
    """
    proxy_client = GenAIHubProxyClient(
        base_url=base_url,
        auth_url=auth_url,
        client_id=client_id,
        client_secret=client_secret,
        resource_group=resource_group
    )
    deployments = proxy_client.ai_core_client.deployment.query(
        scenario_id=orchestration_scenario,
        executable_ids=[executable_id],
        status=Status.RUNNING
    )
    if deployments.count > 0:
        sorted_deployments = sorted(deployments.resources, key=lambda x: x.start_time)[::-1]
        check_for = {}
        if config_name:
            check_for["configuration_name"] = config_name
        if config_id:
            check_for["configuration_id"] = config_id
        if not check_for:
            return sorted_deployments[0].deployment_url
        for deployment in sorted_deployments:
            if all(getattr(deployment, key) == value for key, value in check_for.items()):
                return deployment.deployment_url
    return None


def get_orchestration_api_url(proxy_client: GenAIHubProxyClient,
                              deployment_id: Optional[str] = None,
                              config_name: Optional[str] = None,
                              config_id: Optional[str] = None) -> str:
    """Retrieves the orchestration API URL based on provided deployment or configuration details.

    :param proxy_client: The GenAIHubProxyClient instance.
    :type proxy_client: GenAIHubProxyClient
    :param deployment_id: the deployment ID, defaults to None
    :type deployment_id: Optional[str], optional
    :param config_name: the configuration name, defaults to None
    :type config_name: Optional[str], optional
    :param config_id: the configuration ID, defaults to None
    :type config_id: Optional[str], optional
    :raises ValueError: If no orchestration deployment is found.
    :return: The orchestration API URL.
    :rtype: str
    """

    if deployment_id:
        return f"{proxy_client.ai_core_client.base_url.rstrip('/')}/inference/deployments/{deployment_id}"
    url = discover_orchestration_api_url(
        **proxy_client.model_dump(exclude='ai_core_client'),
        config_name=config_name,
        config_id=config_id
    )
    if url is None:
        raise ValueError('No Orchestration deployment found!')
    return url


class OrchestrationService:
    """A service for executing orchestration requests, allowing for the generation of 
    LLM-generated content through a pipeline of configured modules. This service supports both synchronous and
    asynchronous request execution. For streaming responses, special care is taken to not close the underlying 
    HTTP stream prematurely.

    https://api.sap.com/api/ORCHESTRATION_API/overview
    """

    def __init__(self,
                 api_url: Optional[str] = None,
                 config: Optional[OrchestrationConfig] = None,
                 proxy_client: Optional[GenAIHubProxyClient] = None,
                 deployment_id: Optional[str] = None,
                 config_name: Optional[str] = None,
                 config_id: Optional[str] = None,
                 timeout: Union[int, float, httpx.Timeout, None] = None):
        """Initializes the OrchestrationService with the provided parameters.

        :param api_url: The base URL for the orchestration API, defaults to None
        :type api_url: Optional[str], optional
        :param config: The default orchestration configuration, defaults to None
        :type config: Optional[OrchestrationConfig], optional
        :param proxy_client: The GenAIHubProxyClient instance, defaults to None
        :type proxy_client: Optional[GenAIHubProxyClient], optional
        :param deployment_id: the deployment ID, defaults to None
        :type deployment_id: Optional[str], optional
        :param config_name: the configuration name, defaults to None
        :type config_name: Optional[str], optional
        :param config_id: the configuration ID, defaults to None
        :type config_id: Optional[str], optional
        :param timeout: the timeout for HTTP requests, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        """
        self.proxy_client = proxy_client or get_proxy_client(proxy_version="gen-ai-hub")    
        if api_url:
            self.api_url = api_url
        else:
            self.api_url = get_orchestration_api_url(self.proxy_client, deployment_id, config_name, config_id)
        self.config = config
        self.timeout = timeout
        # create reusable httpx client to improve performance
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

    def _should_retry(self, error: Exception) -> bool:
        """Determines if a request should be retried based on the error type.

        :param error: The exception that occurred.
        :type error: Exception
        :return: True if the error is retryable (only 429 rate limit errors), False otherwise.
        :rtype: bool
        """
        if isinstance(error, httpx.HTTPStatusError):
            return error.response.status_code == 429
        return False

    def _get_retry_after(self, error: Exception) -> Optional[float]:
        """Extracts the Retry-After header value from a 429 response if available.

        :param error: The exception that occurred.
        :type error: Exception
        :return: Number of seconds to wait before retrying, or None if not specified.
        :rtype: Optional[float]
        """
        if isinstance(error, httpx.HTTPStatusError) and error.response.status_code == 429:
            retry_after = error.response.headers.get('Retry-After')
            if retry_after:
                try:
                    # Retry-After can be in seconds (integer) or HTTP date format
                    return float(retry_after)
                except ValueError:
                    # If it's a date format, we'll fall back to exponential backoff
                    return None
        return None

    def _calculate_backoff(self, retry_count: int, base_delay: float = 1.0, max_delay: float = 60.0,
                           min_delay: float = 0.0) -> float:
        """Calculates exponential backoff delay with jitter.

        :param retry_count: The current retry attempt number.
        :type retry_count: int
        :param base_delay: the initial delay in seconds, defaults to 1.0
        :type base_delay: float, optional
        :param max_delay: the maximum delay in seconds, defaults to 60.0
        :type max_delay: float, optional
        :param min_delay: the minimum delay in seconds, defaults to 0.0
        :type min_delay: float, optional
        :return: Delay in seconds before the next retry.
        :rtype: float
        """
        # Calculate exponential delay: base_delay * 2^retry_count
        exp_delay = base_delay * (2 ** retry_count)

        # Cap at max_delay
        capped = min(exp_delay, max_delay)

        # Ensure the lower bound doesn't exceed the cap
        lower = max(0.0, min_delay)
        if lower >= capped:
            return capped

        # Return random value in range [lower, capped] for jitter
        return random.uniform(lower, capped)

    def _execute_request(
            self,
            config: OrchestrationConfig,
            template_values: List[TemplateValue],
            history: List[Message],
            stream: bool,
            stream_options: Optional[dict] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> Union[OrchestrationResponse, Iterable[OrchestrationResponseStreaming]]:
        """Executes an orchestration request synchronously.
        For streaming requests, this method creates a single HTTP stream. It manually enters the stream's
        context to obtain the response, checks for HTTP errors, and then passes both the open response and
        a custom close function to the SSE client. The SSEClient will then yield streaming events and
        close the HTTP stream upon completion.

        :param config: the orchestration configuration.
        :type config: OrchestrationConfig
        :param template_values: the template values for the request.
        :type template_values: List[TemplateValue]
        :param history: the message history.
        :type history: List[Message]
        :param stream: whether to stream the response.
        :type stream: bool
        :param stream_options: additional streaming options, defaults to None
        :type stream_options: Optional[dict], optional
        :param timeout: the timeout for the request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :raises ValueError: If no configuration is provided.
        :raises OrchestrationError: If the HTTP request fails.
        :return: An OrchestrationResponse if not streaming, or an iterable of OrchestrationResponseStreaming
        :rtype: Union[OrchestrationResponse, Iterable[OrchestrationResponseStreaming]]
        :yield: OrchestrationResponseStreaming objects if streaming.
        :rtype: Iterator[Union[OrchestrationResponse, Iterable[OrchestrationResponseStreaming]]]
        """
        if config is None:
            raise ValueError("A configuration is required to invoke the orchestration service.")
        config_copy = deepcopy(config)
        config_copy._stream = stream
        if stream_options:
            config_copy.stream_options = stream_options
        request_obj = OrchestrationRequest(
            config=config_copy,
            template_values=template_values or [],
            history=history or [],
        )

        if stream:
            # Create the streaming response context manager.
            response_cm = self.client.stream(
                "POST",
                self.api_url + COMPLETION_SUFFIX,
                headers=self.proxy_client.request_header,
                json=request_obj.to_dict(),
                timeout=self._determine_timeout(timeout)
            )
            return SSEClient(response_cm, prefix="data: ", final_message="[DONE]")

        response = self.client.post(
            self.api_url + COMPLETION_SUFFIX,
            headers=self.proxy_client.request_header,
            json=request_obj.to_dict(),
            timeout=self._determine_timeout(timeout)
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            _handle_http_error(error, response)

        data = response.json()
        return dacite.from_dict(
            data_class=OrchestrationResponse,
            data=data,
            config=dacite.Config(cast=[Enum]),
        )

    async def _a_execute_request(
            self,
            config: OrchestrationConfig,
            template_values: List[TemplateValue],
            history: List[Message],
            stream: bool,
            stream_options: Optional[dict] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> Union[OrchestrationResponse, AsyncSSEClient]:
        """Executes an orchestration request asynchronously.

        :param config: the orchestration configuration.
        :type config: OrchestrationConfig
        :param template_values: the template values for the request.
        :type template_values: List[TemplateValue]
        :param history: the message history.
        :type history: List[Message]
        :param stream: whether to stream the response.
        :type stream: bool
        :param stream_options: additional streaming options, defaults to None
        :type stream_options: Optional[dict], optional
        :param timeout: the timeout for the request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :raises ValueError: If no configuration is provided.
        :raises OrchestrationError: If the HTTP request fails.
        :return: An OrchestrationResponse if not streaming, or an AsyncSSEClient for iterating over 
        the streaming response.
        :rtype: Union[OrchestrationResponse, AsyncSSEClient]
        """
        if config is None:
            raise ValueError("A configuration is required to invoke the orchestration service.")
        config_copy = deepcopy(config)
        config_copy._stream = stream
        if stream_options:
            config_copy.stream_options = stream_options
        request_obj = OrchestrationRequest(
            config=config_copy,
            template_values=template_values or [],
            history=history or [],
        )

        if stream:
            response_cm = self.async_client.stream(
                "POST",
                self.api_url + COMPLETION_SUFFIX,
                headers=self.proxy_client.request_header,
                json=request_obj.to_dict(),
                timeout=self._determine_timeout(timeout)
            )
            return AsyncSSEClient(response_cm, prefix="data: ", final_message="[DONE]")

        response = await self.async_client.post(
            self.api_url + COMPLETION_SUFFIX,
            headers=self.proxy_client.request_header,
            json=request_obj.to_dict(),
            timeout=self._determine_timeout(timeout)
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            _handle_http_error(error, response)

        data = response.json()
        return dacite.from_dict(
            data_class=OrchestrationResponse,
            data=data,
            config=dacite.Config(cast=[Enum]),
        )

    def run(
            self,
            config: Optional[OrchestrationConfig] = None,
            template_values: Optional[List[TemplateValue]] = None,
            history: Optional[List[Message]] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> OrchestrationResponse:
        """Executes an orchestration request synchronously (non-streaming).

        :param config: the orchestration configuration, defaults to None
        :type config: Optional[OrchestrationConfig], optional
        :param template_values: the template values for the request, defaults to None
        :type template_values: Optional[List[TemplateValue]], optional
        :param history: the message history, defaults to None
        :type history: Optional[List[Message]], optional
        :param timeout: the timeout for the request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :return: An OrchestrationResponse object.
        :rtype: OrchestrationResponse
        """
        return self._execute_request(
            config=config or self.config,
            template_values=template_values,
            history=history,
            stream=False,
            timeout=timeout,
        )

    def stream(
            self,
            config: Optional[OrchestrationConfig] = None,
            template_values: Optional[List[TemplateValue]] = None,
            history: Optional[List[Message]] = None,
            stream_options: Optional[dict] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> SSEClient:
        """Executes an orchestration request in streaming mode (synchronously).

        :param config: the orchestration configuration, defaults to None
        :type config: Optional[OrchestrationConfig], optional
        :param template_values: the template values for the request, defaults to None
        :type template_values: Optional[List[TemplateValue]], optional
        :param history: the message history, defaults to None
        :type history: Optional[List[Message]], optional
        :param stream_options: the additional streaming options, defaults to None
        :type stream_options: Optional[dict], optional
        :param timeout: the timeout for the request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :return: An SSEClient instance for iterating over the streaming response.
        :rtype: SSEClient
        """
        return self._execute_request(
            config=config or self.config,
            template_values=template_values,
            history=history,
            stream=True,
            stream_options=stream_options,
            timeout=timeout,
        )

    async def arun(
            self,
            config: Optional[OrchestrationConfig] = None,
            template_values: Optional[List[TemplateValue]] = None,
            history: Optional[List[Message]] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> OrchestrationResponse:
        """Executes an orchestration request asynchronously (non-streaming).

        :param config: the orchestration configuration, defaults to None
        :type config: Optional[OrchestrationConfig], optional
        :param template_values: the template values for the request, defaults to None
        :type template_values: Optional[List[TemplateValue]], optional
        :param history: the message history, defaults to None
        :type history: Optional[List[Message]], optional
        :param timeout: the timeout for the request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :return: An OrchestrationResponse object.
        :rtype: OrchestrationResponse
        """
        return await self._a_execute_request(
            config=config or self.config,
            template_values=template_values,
            history=history,
            stream=False,
            timeout=timeout,
        )

    async def astream(
            self,
            config: Optional[OrchestrationConfig] = None,
            template_values: Optional[List[TemplateValue]] = None,
            history: Optional[List[Message]] = None,
            stream_options: Optional[dict] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> AsyncSSEClient:
        """Executes an orchestration request asynchronously in streaming mode.

        :param config: the orchestration configuration, defaults to None
        :type config: Optional[OrchestrationConfig], optional
        :param template_values: the template values for the request, defaults to None
        :type template_values: Optional[List[TemplateValue]], optional
        :param history: the message history, defaults to None
        :type history: Optional[List[Message]], optional
        :param stream_options: the additional streaming options, defaults to None
        :type stream_options: Optional[dict], optional
        :param timeout: the timeout for the request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :return: An AsyncSSEClient instance for iterating over the streaming response.
        :rtype: AsyncSSEClient
        """
        return await self._a_execute_request(
            config=config or self.config,
            template_values=template_values,
            history=history,
            stream=True,
            stream_options=stream_options,
            timeout=timeout,
        )

    def close_http_connection(self):   
        """
        Closes the httpx synchronous client.
        """
        self.client.close()

    async def aclose_http_connection(self):
        """
        Closes the httpx asynchronous client.
        """
        await self.async_client.aclose()

    def run_with_retries(
            self,
            config: Optional[OrchestrationConfig] = None,
            template_values: Optional[List[TemplateValue]] = None,
            history: Optional[List[Message]] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
            max_retries: int = 10,
            base_delay: float = 1.0,
    ) -> OrchestrationResponseWithRetries | None:
        """Executes an orchestration request with automatic retry on rate limits (429) and server errors.

        :param config: the orchestration configuration, defaults to None
        :type config: Optional[OrchestrationConfig], optional
        :param template_values: the template values for the request, defaults to None
        :type template_values: Optional[List[TemplateValue]], optional
        :param history: the message history, defaults to None
        :type history: Optional[List[Message]], optional
        :param timeout: the timeout for the request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :param max_retries: the maximum number of retry attempts, defaults to 10
        :type max_retries: int, optional
        :param base_delay: the initial delay between retries in seconds, defaults to 1.0
        :type base_delay: float, optional
        :return: An OrchestrationResponseWithRetries with retry count information.
        :rtype: OrchestrationResponseWithRetries | None
        :raises OrchestrationError: If the request fails after all retries (includes retry count).
        :raises ValueError: If no configuration is provided.
        """
        for retry_count in range(max_retries + 1):
            try:
                # Execute the request
                response = self.run(
                    config=config,
                    template_values=template_values,
                    history=history,
                    timeout=timeout,
                )

                # Success, response with retry count
                return OrchestrationResponseWithRetries(
                    request_id=response.request_id,
                    module_results=response.module_results,
                    orchestration_result=response.orchestration_result,
                    retries=retry_count,
                )

            except (OrchestrationError, httpx.HTTPStatusError, httpx.ConnectError, httpx.TimeoutException) as error:
                time.sleep(self.handle_retry(retry_count, base_delay, error, max_retries))
        return None

    def handle_retry(self, retry_count: int, base_delay: float, error: OrchestrationError, max_retries: int) -> float:
        """Handles retry logic with exponential backoff and jitter.
        If Retry-After header exists, use it as min_delay to add jitter on top

        :param retry_count: the current retry attempt number
        :type retry_count: int
        :param base_delay: the initial delay between retries in seconds
        :type base_delay: float
        :param error: the exception that occurred
        :type error: OrchestrationError
        :param max_retries: the maximum number of retry attempts
        :type max_retries: int
        :raises error: Raises the original error if no more retries should be attempted
        :return: number of seconds to wait before next retry
        :rtype: float
        """
        if not self._should_retry(error) or retry_count >= max_retries:
            error.retries = retry_count
            raise error

        retry_after = self._get_retry_after(error)
        delay = self._calculate_backoff(retry_count, base_delay,
                                        min_delay=0.0 if retry_after is None else retry_after)
        logging.info("Retry no. %d, due to rate limiting", retry_count)
        return delay

    async def arun_with_retries(
            self,
            config: Optional[OrchestrationConfig] = None,
            template_values: Optional[List[TemplateValue]] = None,
            history: Optional[List[Message]] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
            max_retries: int = 10,
            base_delay: float = 1.0,
    ) -> OrchestrationResponseWithRetries | None:
        """Executes an orchestration request asynchronously with automatic retry on rate limits (429) and 
        server errors. Uses exponential backoff with jitter to handle rate limiting gracefully.

        :param config: the orchestration configuration, defaults to None
        :type config: Optional[OrchestrationConfig], optional
        :param template_values: the template values for the request, defaults to None
        :type template_values: Optional[List[TemplateValue]], optional
        :param history: the message history, defaults to None
        :type history: Optional[List[Message]], optional
        :param timeout: the timeout for the request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :param max_retries: the maximum number of retry attempts, defaults to 10
        :type max_retries: int, optional
        :param base_delay: the initial delay between retries in seconds, defaults to 1.0
        :type base_delay: float, optional
        :return: An OrchestrationResponseWithRetries with retry count information.
        :rtype: OrchestrationResponseWithRetries | None
        :raises OrchestrationError: If the request fails after all retries (includes retry count).
        :raises ValueError: If no configuration is provided.
        """
        for retry_count in range(max_retries + 1):
            try:
                # Execute the request
                response = await self.arun(
                    config=config,
                    template_values=template_values,
                    history=history,
                    timeout=timeout,
                )

                # Success! Return response with retry count
                return OrchestrationResponseWithRetries(
                    request_id=response.request_id,
                    module_results=response.module_results,
                    orchestration_result=response.orchestration_result,
                    retries=retry_count,
                )

            except (OrchestrationError, httpx.HTTPStatusError, httpx.ConnectError, httpx.TimeoutException) as error:
                await asyncio.sleep(self.handle_retry(retry_count, base_delay, error, max_retries))
        return None
