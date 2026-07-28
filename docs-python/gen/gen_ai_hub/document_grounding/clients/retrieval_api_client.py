"""Retrieval API client for Document Grounding.

This module provides the RetrievalAPIClient class for querying and retrieving
relevant content from configured data repositories. The Retrieval API combines
semantic search with repository metadata filtering and supports custom retrieval
configurations for chunk/document granularity.

Supported repository types:
    - Vector stores
    - External document sources (e.g., help.sap.com)

API Reference: https://api.sap.com/api/DOCUMENT_GROUNDING_API/resource/Retrieval
"""
import humps
from typing import Optional

from gen_ai_hub import GenAIHubProxyClient
from gen_ai_hub.proxy import get_proxy_client
from gen_ai_hub.proxy.gen_ai_hub_proxy.client import GenAIHubRestClient

from ..models.retrieval import (
    DataRepositories,
    DataRepository,
    RetrievalSearchInput,
    RetrievalSearchResults,
)

# Constants
PATH_DOCUMENT_GROUNDING_RETRIEVAL = "/lm/document-grounding/retrieval"


class RetrievalAPIClient:
    """
    The Retrieval API enables querying and retrieving relevant content from configured data repositories,
    such as vector or external document sources (e.g., help.sap.com).

    Retrieval combines semantic search with repository metadata filtering and supports custom
    retrieval configurations for chunk/document granularity.

    Reference: https://api.sap.com/api/DOCUMENT_GROUNDING_API/resource/Retrieval
    """

    def __init__(self, proxy_client: Optional[GenAIHubProxyClient] = None):
        """Initialize the RetrievalAPIClient.

        :param proxy_client: Optional proxy client for making API requests.
        :type proxy_client: Optional[GenAIHubProxyClient], optional
        """

        self.proxy_client = proxy_client or get_proxy_client(proxy_version="gen-ai-hub")
        self.rest_client = GenAIHubRestClient(self.proxy_client)
        self.path = PATH_DOCUMENT_GROUNDING_RETRIEVAL

    # --- Data Repositories ---

    def get_data_repositories(
        self,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        count: Optional[bool] = None,
    ) -> DataRepositories:
        """List all data repositories available to the tenant.

        :param top: the number of items to return, defaults to None
        :type top: Optional[int], optional
        :param skip: the number of items to skip, defaults to None
        :type skip: Optional[int], optional
        :param count: whether to include a count of total items, defaults to None
        :type count: Optional[bool], optional
        :return: DataRepositories model containing the list of data repositories
        :rtype: DataRepositories
        """

        params = {}
        if top is not None:
            params["$top"] = top
        if skip is not None:
            params["$skip"] = skip
        if count is not None:
            params["$count"] = count

        response = self.rest_client.get(path=f"{self.path}/dataRepositories", params=params)
        response = humps.camelize(response)  # rest_client (ai api sdk) returns snake_case responses
        return DataRepositories(**response)

    def get_data_repository_by_id(self, repository_id: str) -> DataRepository:
        """Get a single data repository by its unique ID.

        :param repository_id: the unique identifier of the data repository
        :type repository_id: str
        :return: DataRepository model representing the data repository
        :rtype: DataRepository
        """

        response = self.rest_client.get(path=f"{self.path}/dataRepositories/{repository_id}")
        response = humps.camelize(response)  # rest_client (ai api sdk) returns snake_case responses
        return DataRepository(**response)

    # --- Search ---

    def search(self, search_input: RetrievalSearchInput) -> RetrievalSearchResults:
        """Perform a retrieval search for relevant content.

        :param search_input: RetrievalSearchInput model defining the query and filters.
        :type search_input: RetrievalSearchInput
        :return: RetrievalSearchResults model containing repositories, documents, and chunks.
        :rtype: RetrievalSearchResults
        """

        response = self.rest_client.post(
            path=f"{self.path}/search",
            body=search_input.model_dump(exclude_none=True),
        )

        response = humps.camelize(response) # rest_client (ai api sdk) returns snake_case responses
        return RetrievalSearchResults(**response)
