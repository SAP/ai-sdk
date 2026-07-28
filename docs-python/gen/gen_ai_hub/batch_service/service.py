"""
Client for the LLM Batch Service API.

Provides synchronous and asynchronous methods to create, list, inspect,
cancel, and delete batch processing jobs via SAP AI Core.
"""

from typing import Optional, Union

import httpx

from gen_ai_hub import GenAIHubProxyClient
from gen_ai_hub.proxy import get_proxy_client
from gen_ai_hub.batch_service.exceptions import BatchServiceError
from gen_ai_hub.batch_service.models.request import BatchCreateRequest, BatchInput, BatchOutput, BatchSpec
from gen_ai_hub.batch_service.models.response import (
    BatchCreateResponse,
    BatchListResponse,
    BatchDetailResponse,
    BatchStatusResponse,
    BatchCancelResponse,
    BatchDeleteResponse,
)

_BASE_PATH = "/llm-batch-service/v1/batches"


def _handle_http_error(response: httpx.Response) -> None:
    """Raises BatchServiceError from a non-2xx httpx response."""
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        try:
            payload = response.json()
            request_id = payload.get('request_id', '')
            error_message = payload.get('message', response.text)
        except Exception as exc:
            raise error from exc
        raise BatchServiceError(
            request_id=request_id,
            message=error_message,
            status_code=response.status_code,
            headers=response.headers,
        )


class BatchService:
    """
    Client for the LLM Batch Service API.

    Supports synchronous and asynchronous variants of all five operations:
    create, list, get, cancel, and delete batch jobs.

    The ``AI-Resource-Group`` header is injected automatically from
    ``proxy_client.request_header`` on every request.


    :param api_url: Base URL of the SAP AI Core API
                 (e.g. ``https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com/v2``).
                 Defaults to the URL resolved from ``proxy_client``.
    :type api_url: str, Optional
    :param proxy_client: A ``GenAIHubProxyClient`` instance. Defaults to the
                      result of ``get_proxy_client(proxy_version="gen-ai-hub")``.
    :type proxy_client: :class:`GenAIHubProxyClient`
    :param resource_group: Value for the ``AI-Resource-Group`` header. Falls back
                        to the resource group on ``proxy_client`` when omitted.
    :type resource_group: str, Optional
    :param timeout: Default HTTP request timeout passed to httpx.
    :type timeout: Union[int, float, httpx.Timeout], Optional
    """

    def __init__(
        self,
        api_url: Optional[str] = None,
        proxy_client: Optional[GenAIHubProxyClient] = None,
        resource_group: Optional[str] = None,
        timeout: Union[int, float, httpx.Timeout, None] = None,
    ):
        self.proxy_client = proxy_client or get_proxy_client(proxy_version="gen-ai-hub")
        if api_url:
            self.api_url = api_url.rstrip("/")
        else:
            base = self.proxy_client.ai_core_client.base_url.rstrip("/")
            self.api_url = base
        self.resource_group = resource_group
        self.timeout = timeout
        self.client = httpx.Client(timeout=self.timeout)
        self.async_client = httpx.AsyncClient(timeout=self.timeout)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _headers(self) -> dict:
        headers = dict(self.proxy_client.request_header)
        if self.resource_group:
            headers["AI-Resource-Group"] = self.resource_group
        return headers

    def _determine_timeout(
        self, timeout: Union[int, float, httpx.Timeout, None]
    ) -> Union[int, float, httpx.Timeout]:
        if timeout is not None:
            return timeout
        if self.timeout is not None:
            return self.timeout
        return httpx.USE_CLIENT_DEFAULT

    def _batches_url(self, *segments: str) -> str:
        parts = [self.api_url + _BASE_PATH] + list(segments)
        return "/".join(p.strip("/") for p in parts if p)

    # ------------------------------------------------------------------
    # Sync API
    # ------------------------------------------------------------------

    def create(
        self,
        *,
        type: str,
        input_uri: str,
        output_uri: str,
        provider: str,
        model: str,
        timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> BatchCreateResponse:
        """Create a new batch processing job.

        :param type: Batch processing type (only ``"llm-native"`` is supported).
        :type type: str
        :param input_uri: URI of the input ``.jsonl`` file in the object store.
        :type input_uri: str
        :param output_uri: URI of the output directory in the object store.
        :type output_uri: str
        :param provider: LLM provider name (e.g. ``"azure-openai"``).
        :type provider: str
        :param model: Model name (e.g. ``"gpt-4.1-mini"``).
        :type model: str
        :param timeout: Per-request timeout override.
        :type timeout: Union[int, float, httpx.Timeout], Optional
        :returns: :class:`BatchCreateResponse` with the job ID and initial status.
        """
        body = BatchCreateRequest(
            type=type,
            input=BatchInput(uri=input_uri),
            output=BatchOutput(uri=output_uri),
            spec=BatchSpec(provider=provider, model=model),
        )
        response = self.client.post(
            self._batches_url(),
            headers=self._headers(),
            json=body.model_dump(),
            timeout=self._determine_timeout(timeout),
        )
        if not response.is_success:
            _handle_http_error(response)
        return BatchCreateResponse(**response.json())

    def list(
        self,
        timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> BatchListResponse:
        """List all batch jobs for the current resource group.

        :param timeout: Per-request timeout override.
        :type timeout: Union[int, float, httpx.Timeout], Optional
        :returns: :class:`BatchListResponse` containing the batch summaries.
        """
        response = self.client.get(
            self._batches_url(),
            headers=self._headers(),
            timeout=self._determine_timeout(timeout),
        )
        if not response.is_success:
            _handle_http_error(response)
        return BatchListResponse(**response.json())

    def get(
        self,
        batch_id: str,
        timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> BatchDetailResponse:
        """Retrieve details of a specific batch job.

        :param batch_id: UUID of the batch job.
        :type batch_id: str
        :param timeout: Per-request timeout override.
        :type timeout: Union[int, float, httpx.Timeout], Optional
        :returns: :class:`BatchDetailResponse` with full job details.
        """
        response = self.client.get(
            self._batches_url(batch_id),
            headers=self._headers(),
            timeout=self._determine_timeout(timeout),
        )
        if not response.is_success:
            _handle_http_error(response)
        return BatchDetailResponse(**response.json())

    def get_status(
        self,
        batch_id: str,
        timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> BatchStatusResponse:
        """Retrieve the current status of a batch job.

        :param batch_id: UUID of the batch job.
        :type batch_id: str
        :param timeout: Per-request timeout override.
        :type timeout: Union[int, float, httpx.Timeout], Optional
        :returns: :class:`BatchStatusResponse` with current and target status.
        """
        response = self.client.get(
            self._batches_url(batch_id, "status"),
            headers=self._headers(),
            timeout=self._determine_timeout(timeout),
        )
        if not response.is_success:
            _handle_http_error(response)
        return BatchStatusResponse(**response.json())

    def cancel(
        self,
        batch_id: str,
        timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> BatchCancelResponse:
        """Schedule a batch job for cancellation.

        :param batch_id: UUID of the batch job.
        :type batch_id: str
        :param timeout: Per-request timeout override.
        :type timeout: Union[int, float, httpx.Timeout], Optional
        :returns: :class:`BatchCancelResponse` confirming the cancellation request.
        """
        response = self.client.patch(
            self._batches_url(batch_id, "cancel"),
            headers=self._headers(),
            timeout=self._determine_timeout(timeout),
        )
        if not response.is_success:
            _handle_http_error(response)
        return BatchCancelResponse(**response.json())

    def delete(
        self,
        batch_id: str,
        timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> BatchDeleteResponse:
        """Delete a batch job (only allowed for terminal states: COMPLETED, FAILED, CANCELLED).

        :param batch_id: UUID of the batch job.
        :type batch_id: str
        :param timeout: Per-request timeout override.
        :type timeout: Union[int, float, httpx.Timeout], Optional
        :returns: :class:`BatchDeleteResponse` confirming the deletion.
        """
        response = self.client.delete(
            self._batches_url(batch_id),
            headers=self._headers(),
            timeout=self._determine_timeout(timeout),
        )
        if not response.is_success:
            _handle_http_error(response)
        return BatchDeleteResponse(**response.json())

    # ------------------------------------------------------------------
    # Async API
    # ------------------------------------------------------------------

    async def acreate(
        self,
        *,
        type: str = "llm-native",
        input_uri: str,
        output_uri: str,
        provider: str,
        model: str,
        timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> BatchCreateResponse:
        """Async variant of :meth:`create`.

        :param type: Batch processing type (only ``"llm-native"`` is supported).
        :type type: str
        :param input_uri: URI of the input ``.jsonl`` file in the object store.
        :type input_uri: str
        :param output_uri: URI of the output directory in the object store.
        :type output_uri: str
        :param provider: LLM provider name (e.g. ``"azure-openai"``).
        :type provider: str
        :param model: Model name (e.g. ``"gpt-4.1-mini"``).
        :type model: str
        :param timeout: Per-request timeout override.
        :type timeout: Union[int, float, httpx.Timeout], Optional
        :returns: :class:`BatchCreateResponse` with the job ID and initial status.
        """
        body = BatchCreateRequest(
            type=type,
            input=BatchInput(uri=input_uri),
            output=BatchOutput(uri=output_uri),
            spec=BatchSpec(provider=provider, model=model),
        )
        response = await self.async_client.post(
            self._batches_url(),
            headers=self._headers(),
            json=body.model_dump(),
            timeout=self._determine_timeout(timeout),
        )
        if not response.is_success:
            _handle_http_error(response)
        return BatchCreateResponse(**response.json())

    async def alist(
        self,
        timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> BatchListResponse:
        """Async variant of :meth:`list`.

        :param timeout: Per-request timeout override.
        :type timeout: Union[int, float, httpx.Timeout], Optional
        :returns: :class:`BatchListResponse` containing the batch summaries.
        """
        response = await self.async_client.get(
            self._batches_url(),
            headers=self._headers(),
            timeout=self._determine_timeout(timeout),
        )
        if not response.is_success:
            _handle_http_error(response)
        return BatchListResponse(**response.json())

    async def aget(
        self,
        batch_id: str,
        timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> BatchDetailResponse:
        """Async variant of :meth:`get`.

        :param batch_id: UUID of the batch job.
        :type batch_id: str
        :param timeout: Per-request timeout override.
        :type timeout: Union[int, float, httpx.Timeout], Optional
        :returns: :class:`BatchDetailResponse` with full job details.
        """
        response = await self.async_client.get(
            self._batches_url(batch_id),
            headers=self._headers(),
            timeout=self._determine_timeout(timeout),
        )
        if not response.is_success:
            _handle_http_error(response)
        return BatchDetailResponse(**response.json())

    async def aget_status(
        self,
        batch_id: str,
        timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> BatchStatusResponse:
        """Async variant of :meth:`get_status`.

        :param batch_id: UUID of the batch job.
        :type batch_id: str
        :param timeout: Per-request timeout override.
        :type timeout: Union[int, float, httpx.Timeout], Optional
        :returns: :class:`BatchStatusResponse` with current and target status.
        """
        response = await self.async_client.get(
            self._batches_url(batch_id, "status"),
            headers=self._headers(),
            timeout=self._determine_timeout(timeout),
        )
        if not response.is_success:
            _handle_http_error(response)
        return BatchStatusResponse(**response.json())

    async def acancel(
        self,
        batch_id: str,
        timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> BatchCancelResponse:
        """Async variant of :meth:`cancel`.

        :param batch_id: UUID of the batch job.
        :type batch_id: str
        :param timeout: Per-request timeout override.
        :type timeout: Union[int, float, httpx.Timeout], Optional
        :returns: :class:`BatchCancelResponse` confirming the cancellation request.
        """
        response = await self.async_client.patch(
            self._batches_url(batch_id, "cancel"),
            headers=self._headers(),
            timeout=self._determine_timeout(timeout),
        )
        if not response.is_success:
            _handle_http_error(response)
        return BatchCancelResponse(**response.json())

    async def adelete(
        self,
        batch_id: str,
        timeout: Union[int, float, httpx.Timeout, None] = None,
    ) -> BatchDeleteResponse:
        """Async variant of :meth:`delete`.

        :param batch_id: UUID of the batch job.
        :type batch_id: str
        :param timeout: Per-request timeout override.
        :type timeout: Union[int, float, httpx.Timeout], Optional
        :returns: :class:`BatchDeleteResponse` confirming the deletion.
        """
        response = await self.async_client.delete(
            self._batches_url(batch_id),
            headers=self._headers(),
            timeout=self._determine_timeout(timeout),
        )
        if not response.is_success:
            _handle_http_error(response)
        return BatchDeleteResponse(**response.json())

    # ------------------------------------------------------------------
    # Resource management
    # ------------------------------------------------------------------

    def close_http_connection(self) -> None:
        """Close the underlying synchronous httpx client."""
        self.client.close()

    async def aclose_http_connection(self) -> None:
        """Close the underlying asynchronous httpx client."""
        await self.async_client.aclose()
