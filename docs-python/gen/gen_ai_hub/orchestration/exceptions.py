import httpx
from typing import Dict, Any


class OrchestrationError(Exception):
    """
    This exception is raised when an error occurs during the execution of the
    orchestration service, typically due to incorrect usage, invalid configurations,
    or issues with run parameters defined by the user.
    """

    def __init__(
        self,
        request_id: str,
        http_headers: httpx.Headers,
        message: str,
        code: int,
        location: str,
        module_results: Dict[str, Any],
        retries: int = 0,
    ):
        """The constructor for OrchestrationError class.

        :param request_id: unique identifier for the request
        :type request_id: str
        :param http_headers: the HTTP headers associated with the error, useful in case of e.g. rate limiting.
        :type http_headers: httpx.Headers
        :param message: Detailed error message describing the issue.
        :type message: str
        :param code: Error code associated with the specific type of failure
        :type code: int
        :param location: Specific component or step in the orchestration process where the error occurred
        :type location: str
        :param module_results: State information and partial results from various modules at the time of the error, 
                               useful for debugging
        :type module_results: Dict[str, Any]
        :param retries: the number of retries attempted
        :type retries: int, optional
        """
        self.request_id = request_id
        self.http_headers = http_headers
        self.message = message
        self.code = code
        self.location = location
        self.module_results = module_results
        self.retries = retries
        super().__init__(message)
