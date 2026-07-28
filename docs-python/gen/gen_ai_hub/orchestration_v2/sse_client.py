# pylint: disable=duplicate-code
"""
Module for Server-Sent Events (SSE) clients for orchestration responses.

This module provides both synchronous and asynchronous SSE clients for iterating over streaming responses.
Each client is responsible for handling HTTP errors and for closing the underlying HTTP stream
when iteration is complete.
"""

import json
from typing import Iterable, Iterator, AsyncIterator

import httpx

from gen_ai_hub.orchestration_v2.exceptions import OrchestrationError, OrchestrationErrorList
from gen_ai_hub.orchestration_v2.models.response import StreamCompletionPostResponse


def _parse_event_data(event_data: str, final_message: str) -> "StreamCompletionPostResponse":
    """
    Parses the event data JSON string into a StreamCompletionPostResponse object.

    Args:
        event_data: The JSON string containing event data.
        final_message: A message indicating the end of the stream.

    Returns:
        An OStreamCompletionPostResponse object parsed from the event data.
        Returns None if the event_data equals the final_message.

    Raises:
        OrchestrationError: If the event data contains an error code.
    """
    if event_data == final_message:
        return None
    event = json.loads(event_data)
    if "error" in event:
        error_event = event["error"]
        if isinstance(error_event, dict):
            raise OrchestrationError(
                request_id=error_event.get("request_id"),
                headers=httpx.Headers({}),
                message=error_event.get("message"),
                code=error_event.get("code"),
                location=error_event.get("location"),
                intermediate_results=error_event.get("intermediate_results", {}),
            )
        if isinstance(error_event, list):
            errors = [
                OrchestrationError(
                    request_id=e.get("request_id"),
                    headers=httpx.Headers({}),
                    message=e.get("message"),
                    code=e.get("code"),
                    location=e.get("location"),
                    intermediate_results=e.get("intermediate_results", {}),
                )
                for e in error_event
                if isinstance(e, dict)
            ]
            raise OrchestrationErrorList(errors=errors)
    return StreamCompletionPostResponse(**event)


class SSEClient:
    """
    A synchronous Server-Sent Events (SSE) client that wraps an httpx.Response for iterating
    over streaming responses.

    This client reads data chunks from the HTTP stream and parses each SSE event.
    For performance reasons the underlying HTTP stream is reused for subsequent calls.
    """

    def __init__(self, response_cm, prefix: str = "data: ", final_message: str = "[DONE]"):
        """Initializes the SSEClient.

        :param response_cm: An httpx.Response context manager for the streaming response.
        :type response_cm: httpx.Response
        :param prefix: The prefix string that identifies SSE event data, defaults to data:
        :type prefix: str, optional
        :param final_message: The message that indicates the end of the stream, defaults to [DONE]
        :type final_message: str, optional
        """

        self.response_cm = response_cm
        self.event_prefix = prefix
        self.final_message = final_message
        self._response = None
        self._iterator = None

    def __enter__(self):
        """Synchronously enters the context for the streaming response.

        It awaits the response, checks for HTTP errors, and if an error occurs,
        reads the content and raises an OrchestrationError.

        :return: Self, with the streaming response stored.
        :rtype: SSEClient
        """

        self._response = self.response_cm.__enter__()
        try:
            self._response.raise_for_status()
        except httpx.HTTPStatusError as error:
            content = self._response.read()
            error_response = httpx.Response(
                status_code=self._response.status_code,
                headers=self._response.headers,
                content=content,
                request=self._response.request,
            )
            self.response_cm.__exit__(None, None, None)
            _handle_http_error(error, error_response)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Synchronously exits the context, ensuring that the context manager is properly closed.
        """
        self.response_cm.__exit__(exc_type, exc_val, exc_tb)

    def iter_lines(self) -> Iterable[str]:
        """Reads data chunks from the HTTP stream and yields complete lines.

        This method accumulates incoming chunks until a newline is encountered, yielding one complete
        line at a time.

        :return: Complete lines of text from the streaming response.
        :rtype: Iterable[str]
        :yield: Complete lines of text from the streaming response.
        :rtype: Iterator[Iterable[str]]
        """

        buffer = ""
        for chunk in self._response.iter_text():
            buffer += chunk
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                yield line.strip()
        if buffer:
            yield buffer.strip()

    def __iter__(self) -> Iterator:
        """
        Returns self as an iterator. Opens the HTTP stream and initializes the internal iterator.
        """
        return self

    def __next__(self):
        """
        Retrieves the next parsed SSE event from the stream.
        It skips any lines that do not start with the expected prefix. When the final message is encountered
        or the stream is exhausted, it closes the stream and raises StopIteration.
        """
        if self._iterator is None:
            self.__enter__()
            self._iterator = self.iter_lines()
        while True:
            try:
                line = next(self._iterator)
            except StopIteration:
                # End of stream; ensure resources are cleaned up.
                self.__exit__(None, None, None)
                raise StopIteration

            if not line or not line.startswith(self.event_prefix):
                continue

            event_data = line[len(self.event_prefix):]
            result = _parse_event_data(event_data, self.final_message)
            if result is None:
                # Final message encountered; close the stream.
                self.__exit__(None, None, None)
                raise StopIteration
            return result


class AsyncSSEClient:
    """
    An asynchronous SSE client for iterating over streaming responses.

    This client wraps an asynchronous HTTP stream (provided as a context manager) and ensures
    that the stream is properly opened and closed. It also checks for HTTP errors upon entering the stream.
    """

    def __init__(self, response_cm, prefix: str = "data: ", final_message: str = "[DONE]"):
        """Initializes the AsyncSSEClient.

        :param response_cm: An asynchronous context manager for the HTTP streaming response.
        :type response_cm: typing.AsyncContextManager[httpx.Response]
        :param prefix: the SSE data prefix, defaults to "data: "
        :type prefix: str, optional
        :param final_message: the message indicating the end of the stream, defaults to "[DONE]"
        :type final_message: str, optional
        """

        self.response_cm = response_cm
        self.event_prefix = prefix
        self.final_message = final_message
        self._response = None
        self._iterator = None

    async def __aenter__(self):
        """
        Asynchronously enters the context for the streaming response.

        It awaits the response, checks for HTTP errors, and if an error occurs,
        reads the content and raises an OrchestrationError.

        Returns:
            Self, with the streaming response stored.
        """
        self._response = await self.response_cm.__aenter__()
        try:
            self._response.raise_for_status()
        except httpx.HTTPStatusError as error:
            content = await self._response.aread()
            error_response = httpx.Response(
                status_code=self._response.status_code,
                headers=self._response.headers,
                content=content,
                request=self._response.request,
            )
            await self.response_cm.__aexit__(None, None, None)
            _handle_http_error(error, error_response)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Asynchronously exits the context, ensuring that the context manager is properly closed.
        """
        await self.response_cm.__aexit__(exc_type, exc_val, exc_tb)

    def _process_line(self, line: str) -> "StreamCompletionPostResponse":
        """
        Process a single line and return parsed event data if valid.

        :param line: The line to process
        :type line: str
        :return: Parsed event data or None if line is invalid or end of stream
        :rtype: StreamCompletionPostResponse or None
        """
        line = line.strip()
        if not line or not line.startswith(self.event_prefix):
            return None
        event_data = line[len(self.event_prefix):]
        return _parse_event_data(event_data, self.final_message)

    async def _internal_iterator(self) -> AsyncIterator:
        """
        Internal asynchronous generator that yields parsed events from the HTTP stream.
        """
        buffer = ""
        async for chunk in self._response.aiter_text():
            buffer += chunk
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                result = self._process_line(line)
                if result is None:
                    if line.strip() == self.final_message or line.strip().endswith(self.final_message):
                        return
                    continue
                yield result
        # Process any remaining data in the buffer
        if buffer:
            result = self._process_line(buffer)
            if result is not None:
                yield result

    def __aiter__(self):
        """
        Returns the async iterator (self). The initialization of the stream is deferred until the first
        call to __anext__.
        """
        return self

    async def __anext__(self):
        """
        Asynchronously retrieves the next event from the stream. On the first call, it enters the asynchronous
        context to start the stream. When the stream is exhausted or the final message is received, it properly
        exits the context.

        Returns:
            The next parsed event from the stream.

        Raises:
            StopAsyncIteration: When the stream is exhausted.
        """
        if self._iterator is None:
            # Lazily initialize the stream.
            await self.__aenter__()
            self._iterator = self._internal_iterator().__aiter__()
        try:
            return await self._iterator.__anext__()
        except StopAsyncIteration:
            await self.__aexit__(None, None, None)
            raise StopAsyncIteration


def _handle_http_error(error, response: httpx.Response):
    """
    Handles HTTP errors by raising an OrchestrationError with details from the response.

    Args:
        error: The original HTTP error.
        response: The httpx.Response object containing error details incl. headers.

    Raises:
        OrchestrationError with information extracted from the response.
    """
    if not response.content:
        raise error
    try:
        error_content = response.json().get("error", None)
    except ValueError as exc:
        raise error from exc
    if isinstance(error_content, dict):
        raise OrchestrationError(
            request_id=error_content.get("request_id"),
            headers=response.headers,
            message=error_content.get("message"),
            code=error_content.get("code"),
            location=error_content.get("location"),
            intermediate_results=error_content.get("intermediate_results", {}),
        ) from error
    if isinstance(error_content, list):
        errors = [
            OrchestrationError(
                request_id=e.get("request_id"),
                headers=response.headers,
                message=e.get("message"),
                code=e.get("code"),
                location=e.get("location"),
                intermediate_results=e.get("intermediate_results", {}),
            )
            for e in error_content
            if isinstance(e, dict)
        ]
        raise OrchestrationErrorList(errors=errors) from error
