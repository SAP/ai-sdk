# pylint: disable=duplicate-code
"""
Module for orchestration service handling requests and responses.

Provides synchronous and asynchronous methods to run orchestration pipelines.
"""

from copy import deepcopy
import random
import time
import logging
import asyncio
from functools import wraps
from typing import List, Optional, Iterable, Union

import httpx
from ai_api_client_sdk.models.status import Status

from gen_ai_hub import GenAIHubProxyClient
from gen_ai_hub.orchestration_v2.models.orchestration_request import CompletionPostRequest
from gen_ai_hub.orchestration_v2.models.config import OrchestrationConfig, OrchestrationConfigReference
from gen_ai_hub.orchestration_v2.models.message import ChatMessage
from gen_ai_hub.orchestration_v2.models.response import (CompletionPostResponse, StreamCompletionPostResponse,
                                                         OrchestrationResponseWithRetries)
from gen_ai_hub.orchestration_v2.models.embeddings import (
    EmbeddingsOrchestrationConfig,
    EmbeddingsInput,
    EmbeddingsRequest,
    EmbeddingsPostResponse,
)
from gen_ai_hub.orchestration_v2.sse_client import SSEClient, AsyncSSEClient, _handle_http_error
from gen_ai_hub.orchestration_v2.exceptions import OrchestrationError
from gen_ai_hub.proxy import get_proxy_client

V2_COMPLETION_SUFFIX = "/v2/completion"
V2_EMBEDDINGS_SUFFIX = "/v2/embeddings"
CONFIG_AND_CONFIG_REF_ERROR_TEXT = "Cannot provide both a configuration and a configuration reference."

def cache_if_not_none(func):
    """Custom cache decorator that only caches non-None results"""
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
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
    :return: the orchestration API URL or None if no deployment is found.
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
        sorted_deployments = sorted(deployments.resources, key=lambda x: x.start_time, reverse=True)
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

    :param proxy_client: the GenAIHubProxyClient instance.
    :type proxy_client: GenAIHubProxyClient
    :param deployment_id: the deployment ID, defaults to None
    :type deployment_id: Optional[str], optional
    :param config_name: the configuration name, defaults to None
    :type config_name: Optional[str], optional
    :param config_id: the configuration ID, defaults to None
    :type config_id: Optional[str], optional
    :raises ValueError: throws if no orchestration deployment is found.
    :return: the orchestration API URL.
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
    return f"{url.rstrip('/')}"


class OrchestrationService:
    """
    A service for executing orchestration requests, allowing for the generation of LLM-generated content
    through a pipeline of configured modules.

    This service supports both synchronous and asynchronous request execution. For streaming responses,
    special care is taken to not close the underlying HTTP stream prematurely.

    See https://api.sap.com/api/ORCHESTRATION_API_v2/overview

    Args:

    api_url: The base URL for the orchestration API.

    config: The default orchestration configuration.

    config_ref: The reference to default orchestration configuration.

    proxy_client: A GenAIHubProxyClient instance.

    deployment_id: Optional deployment ID.

    config_name: Optional configuration name.

    config_id: Optional configuration ID.

    timeout: Optional timeout for HTTP requests.

    
    """

    def __init__(self,
                 api_url: Optional[str] = None,
                 config: Optional[OrchestrationConfig] = None,
                 config_ref: Optional[OrchestrationConfigReference] = None,
                 proxy_client: Optional[GenAIHubProxyClient] = None,
                 deployment_id: Optional[str] = None,
                 config_name: Optional[str] = None,
                 config_id: Optional[str] = None,
                 timeout: Union[int, float, httpx.Timeout, None] = None):
        """Initializes the OrchestrationService.

        :param api_url: the base URL for the orchestration API, defaults to None
        :type api_url: Optional[str], optional
        :param config: the orchestration configuration, defaults to None
        :type config: Optional[OrchestrationConfig], optional
        :param config_ref: the orchestration configuration reference, defaults to None
        :type config_ref: Optional[OrchestrationConfigReference], optional
        :param proxy_client: the GenAIHubProxyClient instance, defaults to None
        :type proxy_client: Optional[GenAIHubProxyClient], optional
        :param deployment_id: the deployment ID, defaults to None
        :type deployment_id: Optional[str], optional
        :param config_name: the configuration name, defaults to None
        :type config_name: Optional[str], optional
        :param config_id: the configuration ID, defaults to None
        :type config_id: Optional[str], optional
        :param timeout: the timeout for HTTP requests, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :raises ValueError: if both config and config_ref are provided.
        """
        self.proxy_client = proxy_client or get_proxy_client(proxy_version="gen-ai-hub")
        if api_url:
            self.api_url = api_url
        else:
            self.api_url = get_orchestration_api_url(self.proxy_client, deployment_id, config_name, config_id)
        self.config = config
        self.config_ref = config_ref
        if self.config_ref and self.config:
            raise ValueError(CONFIG_AND_CONFIG_REF_ERROR_TEXT)
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
        """
        Determines if a request should be retried based on the error type.

        Args:
            error: The exception that occurred.

        Returns:
            True if the error is retryable (only 429 rate limit errors), False otherwise.
        """
        if isinstance(error, httpx.HTTPStatusError):
            return error.response.status_code == 429
        return False

    def _get_retry_after(self, error: Exception) -> Optional[float]:
        """
        Extracts the Retry-After header value from a 429 response if available.

        Args:
            error: The exception that occurred.

        Returns:
            Number of seconds to wait before retrying, or None if not specified.
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
        """
        Calculates exponential backoff delay with jitter.

        Uses exponential backoff capped at max_delay, with uniform random jitter
        to prevent thundering herd problem when multiple clients retry simultaneously.

        Args:
            retry_count: Current retry attempt number.
            base_delay: Initial delay in seconds.
            max_delay: Maximum delay in seconds (e.g., 60s for rate limit resets).
            min_delay: Minimum delay in seconds (default: 0.0).

        Returns:
            Delay in seconds before next retry, within [min_delay, max_delay] range.
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
            config: Optional[OrchestrationConfig] = None,
            config_ref: Optional[OrchestrationConfigReference] = None,
            placeholder_values: Optional[dict] = None,
            history: Optional[List[ChatMessage]] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
            stream: bool = False,
    ) -> Union[CompletionPostResponse | Iterable[StreamCompletionPostResponse]]:
        """
        Executes an orchestration request synchronously.

        For streaming requests, this method creates a single HTTP stream. It manually enters the stream's
        context to obtain the response, checks for HTTP errors, and then passes both the open response and
        a custom close function to the SSE client. The SSEClient will then yield streaming events and
        close the HTTP stream upon completion.

        Args:
            config: The orchestration configuration.
            config_ref: The orchestration configuration reference.
            placeholder_values: Template values for the request.
            history: History of chat messages. Can be used to provide system and assistant messages
                     to set the context of the conversation. Will be merged with the template message.
            timeout: Optional timeout overwrite per request.
            stream: Whether to stream the response.

        Returns:
            A CompletionPostResponse if not streaming, or an iterable of StreamCompletionPostResponse
            objects if streaming.

        Raises:
            ValueError: If no configuration is provided.
            OrchestrationError: If the HTTP request fails.
        """
        if config is None and config_ref is None:
            raise ValueError("A configuration is required to invoke the orchestration service.")
        if config and config_ref:
            raise ValueError(CONFIG_AND_CONFIG_REF_ERROR_TEXT)
        if config and config.stream:
            if config.stream.enabled != stream:
                raise ValueError("Config stream setting must match used function. "
                                 "Use stream function with config with enabled stream "
                                 "and run function with config without enabled stream.")

        config_copy = deepcopy(config)
        config_ref_copy = deepcopy(config_ref)

        request_obj = CompletionPostRequest(
            config=config_copy,
            config_ref=config_ref_copy,
            placeholder_values=placeholder_values,
            messages_history=history
        )

        if stream:
            # Create the streaming response context manager.
            response_cm = self.client.stream(
                "POST",
                self.api_url + V2_COMPLETION_SUFFIX,
                headers=self.proxy_client.request_header,
                json=request_obj.model_dump(),
                timeout=self._determine_timeout(timeout)
            )
            return SSEClient(response_cm, prefix="data: ", final_message="[DONE]")

        response = self.client.post(
            self.api_url + V2_COMPLETION_SUFFIX,
            headers=self.proxy_client.request_header,
            json=request_obj.model_dump(),
            timeout=self._determine_timeout(timeout)
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            _handle_http_error(error, response)

        data = response.json()
        return CompletionPostResponse(**data)

    async def _a_execute_request(
            self,
            config: Optional[OrchestrationConfig] = None,
            config_ref: Optional[OrchestrationConfigReference] = None,
            placeholder_values: Optional[dict] = None,
            history: Optional[List[ChatMessage]] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
            stream: bool = False,
    ) -> Union[CompletionPostResponse | AsyncSSEClient]:
        """
        Executes an orchestration request asynchronously.

        For streaming requests, this method creates a single HTTP stream and returns an AsyncSSEClient.
        The AsyncSSEClient manages the stream's lifecycle (opening it via __aenter__ and closing it via __aexit__)
        and performs error checking upon entering the stream.

        Args:
            config: The orchestration configuration.
            config_ref: The orchestration configuration reference.
            placeholder_values: Template values for the request.
            history: Message history.
            timeout: Optional timeout overwrite per request.
            stream: Whether to stream the response.

        Returns:
            A CompletionPostResponse if not streaming, or an AsyncSSEClient for iterating over the streaming response.

        Raises:
            ValueError: If no configuration is provided.
            OrchestrationError: If the HTTP request fails.
        """
        if config is None and config_ref is None:
            raise ValueError("A configuration is required to invoke the orchestration service.")
        if config and config_ref:
            raise ValueError(CONFIG_AND_CONFIG_REF_ERROR_TEXT)
        if config and config.stream:
            if config.stream.enabled != stream:
                raise ValueError("Config stream setting must match used function. "
                                 "Use astream function with config with enabled stream "
                                 "and arun function with config without enabled stream.")

        config_copy = deepcopy(config)
        config_ref_copy = deepcopy(config_ref)

        request_obj = CompletionPostRequest(
            config=config_copy,
            config_ref=config_ref_copy,
            placeholder_values=placeholder_values,
            messages_history=history,
        )

        if stream:
            response_cm = self.async_client.stream(
                "POST",
                self.api_url + V2_COMPLETION_SUFFIX,
                headers=self.proxy_client.request_header,
                json=request_obj.model_dump(),
                timeout=self._determine_timeout(timeout)
            )
            return AsyncSSEClient(response_cm, prefix="data: ", final_message="[DONE]")

        response = await self.async_client.post(
            self.api_url + V2_COMPLETION_SUFFIX,
            headers=self.proxy_client.request_header,
            json=request_obj.model_dump(),
            timeout=self._determine_timeout(timeout)
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            _handle_http_error(error, response)

        data = response.json()
        return CompletionPostResponse(**data)

    def run(
            self,
            config: Optional[OrchestrationConfig] = None,
            config_ref: Optional[OrchestrationConfigReference] = None,
            placeholder_values: Optional[dict] = None,
            history: Optional[List[ChatMessage]] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> CompletionPostResponse:
        """Executes an orchestration request synchronously (non-streaming).

        :param config: the orchestration configuration, defaults to None
        :type config: Optional[OrchestrationConfig], optional
        :param config_ref: the orchestration configuration reference, defaults to None
            if not provided, the default configuration is used.
        :type config_ref: Optional[OrchestrationConfigReference], optional
        :param placeholder_values: the template values, defaults to None
        :type placeholder_values: Optional[dict], optional
        :param history: the message history, defaults to None
        :type history: Optional[List[ChatMessage]], optional
        :param timeout: the timeout overwrite per request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :return: the CompletionPostResponse object
        :rtype: CompletionPostResponse
        """        

        return self._execute_request(
            config=config or self.config,
            config_ref=config_ref or self.config_ref,
            placeholder_values=placeholder_values,
            history=history,
            timeout=timeout,
        )

    def stream(
            self,
            config: Optional[OrchestrationConfig] = None,
            config_ref: Optional[OrchestrationConfigReference] = None,
            placeholder_values: Optional[dict] = None,
            history: Optional[List[ChatMessage]] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> Iterable[StreamCompletionPostResponse]:
        """Executes an orchestration streaming request synchronously.

        :param config: the orchestration configuration, defaults to None
        :type config: Optional[OrchestrationConfig], optional
        :param config_ref: the orchestration configuration reference, defaults to None
        :type config_ref: Optional[OrchestrationConfigReference], optional
            if not provided, the default configuration is used.
        :param placeholder_values: the template values, defaults to None
        :type placeholder_values: Optional[dict], optional
        :param history: the message history, defaults to None
        :type history: Optional[List[ChatMessage]], optional
        :param timeout: the timeout overwrite per request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :return: An Iterable[StreamCompletionPostResponse] object
        :rtype: Iterable[StreamCompletionPostResponse]
        """

        return self._execute_request(
            config=config or self.config,
            config_ref=config_ref or self.config_ref,
            placeholder_values=placeholder_values,
            history=history,
            timeout=timeout,
            stream=True
        )

    async def arun(
            self,
            config: Optional[OrchestrationConfig] = None,
            config_ref: Optional[OrchestrationConfigReference] = None,
            placeholder_values: Optional[dict] = None,
            history: Optional[List[ChatMessage]] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> CompletionPostResponse:
        """Executes an orchestration request asynchronously (non-streaming).

        :param config: the orchestration configuration, defaults to None
        :type config: Optional[OrchestrationConfig], optional
        :param config_ref: the orchestration configuration reference, defaults to None
        :type config_ref: Optional[OrchestrationConfigReference], optional
        :param placeholder_values: the template values, defaults to None
        :type placeholder_values: Optional[dict], optional
        :param history: the message history, defaults to None
        :type history: Optional[List[ChatMessage]], optional
        :param timeout: the timeout overwrite per request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :return: the CompletionPostResponse object
        :rtype: CompletionPostResponse
        """

        return await self._a_execute_request(
            config=config or self.config,
            config_ref=config_ref or self.config_ref,
            placeholder_values=placeholder_values,
            history=history,
            timeout=timeout,
        )

    async def astream(
            self,
            config: Optional[OrchestrationConfig] = None,
            config_ref: Optional[OrchestrationConfigReference] = None,
            placeholder_values: Optional[dict] = None,
            history: Optional[List[ChatMessage]] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> AsyncSSEClient:
        """Executes an orchestration streaming request asynchronously.

        :param config: the orchestration configuration, defaults to None
        :type config: Optional[OrchestrationConfig], optional
        :param config_ref: the orchestration configuration reference, defaults to None
        :type config_ref: Optional[OrchestrationConfigReference], optional
        :param placeholder_values: the template values, defaults to None
        :type placeholder_values: Optional[dict], optional
        :param history: the message history, defaults to None
        :type history: Optional[List[ChatMessage]], optional
        :param timeout: the timeout overwrite per request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :return: the AsyncSSEClient object
        :rtype: AsyncSSEClient
        """        

        return await self._a_execute_request(
            config=config or self.config,
            config_ref=config_ref or self.config_ref,
            placeholder_values=placeholder_values,
            history=history,
            timeout=timeout,
            stream=True
        )

    def run_with_retries(
            self,
            config: Optional[OrchestrationConfig] = None,
            config_ref: Optional[OrchestrationConfigReference] = None,
            placeholder_values: Optional[dict] = None,
            history: Optional[List[ChatMessage]] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
            max_retries: int = 10,
            base_delay: float = 1.0,
    ) -> OrchestrationResponseWithRetries | None:
        """Executes an orchestration request with automatic retry on rate limits (429) and server errors.

        :param config: the orchestration configuration, defaults to None
        :type config: Optional[OrchestrationConfig], optional
        :param config_ref: the orchestration configuration reference, defaults to None
        :type config_ref: Optional[OrchestrationConfigReference], optional
        :param placeholder_values: the template values, defaults to None
        :type placeholder_values: Optional[dict], optional
        :param history: the message history, defaults to None
        :type history: Optional[List[ChatMessage]], optional
        :param timeout: the timeout overwrite per request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :param max_retries: the maximum number of retry attempts, defaults to 10
        :type max_retries: int, optional
        :param base_delay: the initial delay between retries in seconds, defaults to 1.0
        :type base_delay: float, optional
        :return: the OrchestrationResponseWithRetries with retry count information
        :rtype: OrchestrationResponseWithRetries | None
        :raises ValueError: if no configuration is provided.
        :raises OrchestrationError: if request fails after all retries (includes retry count).
        """

        for retry_count in range(max_retries + 1):
            try:
                # Execute the request
                response: CompletionPostResponse = self.run(
                    config=config or self.config,
                    config_ref=config_ref or self.config_ref,
                    placeholder_values=placeholder_values,
                    history=history,
                    timeout=timeout,
                )

                # Success, response with retry count
                return OrchestrationResponseWithRetries(
                    request_id=response.request_id,  # pylint: disable=no-member
                    intermediate_results=response.intermediate_results,  # pylint: disable=no-member
                    final_result=response.final_result,  # pylint: disable=no-member
                    intermediate_failures=response.intermediate_failures,
                    retries=retry_count,
                )

            except (OrchestrationError, httpx.HTTPStatusError, httpx.ConnectError, httpx.TimeoutException) as error:
                time.sleep(self.handle_retry(retry_count, base_delay, error, max_retries))
        return None

    def handle_retry(self, retry_count: int, base_delay: float, error: OrchestrationError, max_retries: int) -> float:
        """ Handles retry logic with exponential backoff and jitter.
        If Retry-After header exists, use it as min_delay to add jitter on top

        :param retry_count: the incremented retry attempt number
        :type retry_count: int
        :param base_delay: the initial delay between retries in seconds
        :type base_delay: float
        :param error: the exception that occurred
        :type error: OrchestrationError
        :param max_retries: the maximum number of retry attempts
        :type max_retries: int
        :raises error: throws the original error if no retry should be attempted
        :return: the number of seconds to wait before next retry
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
            config_ref: Optional[OrchestrationConfigReference] = None,
            placeholder_values: Optional[dict] = None,
            history: Optional[List[ChatMessage]] = None,
            timeout: Union[int, float, httpx.Timeout, None] = None,
            max_retries: int = 10,
            base_delay: float = 1.0,
    ) -> OrchestrationResponseWithRetries | None:
        """Executes an orchestration request asynchronously with automatic retry on rate limits (429) and server errors.
        Uses exponential backoff with jitter to handle rate limiting gracefully.

        :param config: the orchestration configuration, defaults to None
        :type config: Optional[OrchestrationConfig], optional
        :param config_ref: the orchestration configuration reference, defaults to None
        :type config_ref: Optional[OrchestrationConfigReference], optional
        :param placeholder_values: the template values, defaults to None
        :type placeholder_values: Optional[dict], optional
        :param history: the message history, defaults to None
        :type history: Optional[List[ChatMessage]], optional
        :param timeout: the timeout overwrite per request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :param max_retries: the maximum number of retry attempts, defaults to 10
        :type max_retries: int, optional
        :param base_delay: the initial delay between retries in seconds, defaults to 1.0
        :type base_delay: float, optional
        :return: the OrchestrationResponseWithRetries with retry count information
        :rtype: OrchestrationResponseWithRetries | None
        :raises ValueError: if no configuration is provided.
        :raises OrchestrationError: if request fails after all retries (includes retry count).
        """        

        for retry_count in range(max_retries + 1):
            try:
                # Execute the request
                response: CompletionPostResponse = await self.arun(
                    config=config or self.config,
                    config_ref=config_ref or self.config_ref,
                    placeholder_values=placeholder_values,
                    history=history,
                    timeout=timeout,
                )

                return OrchestrationResponseWithRetries(
                    request_id=response.request_id,
                    intermediate_results=response.intermediate_results,
                    final_result=response.final_result,
                    intermediate_failures=response.intermediate_failures,
                    retries=retry_count,
                )

            except (OrchestrationError, httpx.HTTPStatusError, httpx.ConnectError, httpx.TimeoutException) as error:
                await asyncio.sleep(self.handle_retry(retry_count, base_delay, error, max_retries))
        return None

    def embed(
            self,
            config: EmbeddingsOrchestrationConfig,
            input: EmbeddingsInput,  # pylint: disable=redefined-builtin
            timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> EmbeddingsPostResponse:
        """Executes an embeddings request synchronously.

        :param config: the embeddings orchestration configuration
        :type config: EmbeddingsOrchestrationConfig
        :param input: the input text to embed
        :type input: EmbeddingsInput
        :param timeout: the timeout overwrite per request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :return: the EmbeddingsPostResponse object
        :rtype: EmbeddingsPostResponse
        """
        request_obj = EmbeddingsRequest(
            config=deepcopy(config),
            input=deepcopy(input),
        )

        response = self.client.post(
            self.api_url + V2_EMBEDDINGS_SUFFIX,
            headers=self.proxy_client.request_header,
            json=request_obj.model_dump(),
            timeout=self._determine_timeout(timeout)
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            _handle_http_error(error, response)

        data = response.json()
        return EmbeddingsPostResponse(**data)

    async def aembed(
            self,
            config: EmbeddingsOrchestrationConfig,
            input: EmbeddingsInput,  # pylint: disable=redefined-builtin
            timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> EmbeddingsPostResponse:
        """Executes an embeddings request asynchronously.

        :param config: the embeddings orchestration configuration
        :type config: EmbeddingsOrchestrationConfig
        :param input: the input text to embed
        :type input: EmbeddingsInput
        :param timeout: the timeout overwrite per request, defaults to None
        :type timeout: Union[int, float, httpx.Timeout, None], optional
        :return: the EmbeddingsPostResponse object
        :rtype: EmbeddingsPostResponse
        """
        request_obj = EmbeddingsRequest(
            config=deepcopy(config),
            input=deepcopy(input),
        )

        response = await self.async_client.post(
            self.api_url + V2_EMBEDDINGS_SUFFIX,
            headers=self.proxy_client.request_header,
            json=request_obj.model_dump(),
            timeout=self._determine_timeout(timeout)
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            _handle_http_error(error, response)

        data = response.json()
        return EmbeddingsPostResponse(**data)

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


__all__ = ["OrchestrationService"]