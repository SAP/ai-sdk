"""
Exceptions for the orchestration service module.
"""

from gen_ai_hub.orchestration_v2.models.response import ModuleResults

import httpx
from typing import Optional


class OrchestrationError(Exception):
    """
    This exception is raised when an error occurs during the execution of the
    orchestration service, typically due to incorrect usage, invalid configurations,
    or issues with run parameters defined by the user.
    """

    def __init__(
            self,
            request_id: str,
            headers: httpx.Headers,
            message: str,
            code: int,
            location: str,
            intermediate_results: ModuleResults | dict,
            retries: int = 0,
    ):
        """Initializes the OrchestrationError with detailed context.

        :param request_id: unique identifier for the request that encountered the error.
        :type request_id: str
        :param headers: HTTP headers associated with the request, useful in case of e.g. rate limiting..
        :type headers: httpx.Headers
        :param message: Detailed error message describing the issue.
        :type message: str
        :param code: Error code associated with the specific type of failure.
        :type code: int
        :param location: Specific component or step in the orchestration process where the error occurred.
        :type location: str
        :param intermediate_results: State information and partial results from various modules
            at the time of the error, useful for debugging.
        :type intermediate_results: ModuleResults
        :param retries: Number of retries attempted before the error was raised.
        :type retries: int, optional
        :param errors: Raw error payload(s) from the API. Can contain multiple errors.
        :type errors: Optional[list[dict[str, Any]]]
        """
        self.request_id = request_id
        self.headers = headers
        self.message = message
        self.code = code
        self.location = location
        self.intermediate_results = intermediate_results
        self.retries = retries
        super().__init__(message)

class OrchestrationErrorList(Exception):
    def __init__(self, errors: list[OrchestrationError]):
        self.errors = errors
        super().__init__(errors[0].message)


__all__ = ["OrchestrationError", "OrchestrationErrorList"]