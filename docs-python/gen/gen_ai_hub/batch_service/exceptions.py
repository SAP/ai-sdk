"""
Exceptions for the batch service module.
"""

import httpx


class BatchServiceError(Exception):
    """
    Raised when the batch service returns an error response.

    Captures the request_id from the error payload for tracing.
    """

    def __init__(
        self,
        request_id: str,
        message: str,
        status_code: int,
        headers: httpx.Headers,
    ):
        self.request_id = request_id
        self.message = message
        self.status_code = status_code
        self.headers = headers
        super().__init__(message)


__all__ = ["BatchServiceError"]
