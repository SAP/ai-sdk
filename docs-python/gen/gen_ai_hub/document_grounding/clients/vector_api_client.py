"""Vector API client for Document Grounding.

This module provides the VectorAPIClient class for managing vector-based document
collections and performing semantic searches. The Vector API enables creating,
retrieving, updating, and deleting collections, as well as managing documents
within those collections.

Key capabilities:
    - Collection management (create, read, update, delete)
    - Document management within collections
    - Semantic vector search across collections
    - Collection status tracking (creation/deletion)

API Reference: https://api.sap.com/api/DOCUMENT_GROUNDING_API/resource/Vector
"""
import humps
import requests
from typing import Optional

from gen_ai_hub import GenAIHubProxyClient
from gen_ai_hub.proxy import get_proxy_client
from gen_ai_hub.proxy.gen_ai_hub_proxy.client import GenAIHubRestClient
from pydantic import TypeAdapter

from ..models.vector import (
    CollectionCreateRequest,
    Collection,
    CollectionsListResponse,
    DocumentsCreateRequest,
    DocumentsUpdateRequest,
    Document,
    DocumentsResponse,
    DocumentsListResponse, CollectionCreationStatusResponse, CollectionDeletionStatusResponse, TextSearchRequest,
    VectorSearchResults,
)

# Constants
PATH_DOCUMENT_GROUNDING_VECTOR = "/lm/document-grounding/vector"


class VectorAPIClient:
    """The Vector API provides management and search capabilities for vector-based document collections.

    It enables creating, retrieving, updating, and deleting collections, as well as
    managing documents and performing semantic vector searches within those collections.

    Reference: https://api.sap.com/api/DOCUMENT_GROUNDING_API/resource/Vector
    """

    def __init__(self, proxy_client: Optional[GenAIHubProxyClient] = None):
        """Initializes the VectorAPIClient

        :param proxy_client: Optional proxy client to use for requests
        :type proxy_client: Optional[GenAIHubProxyClient], optional
        """

        self.proxy_client = proxy_client or get_proxy_client(proxy_version="gen-ai-hub")
        self.rest_client = GenAIHubRestClient(self.proxy_client)
        self.path = PATH_DOCUMENT_GROUNDING_VECTOR

    # --- Collections ---

    def get_collections(
            self, top: Optional[int] = None, skip: Optional[int] = None, count: Optional[bool] = None
    ) -> CollectionsListResponse:
        """Get all collections.

        :param top: the number of collections to retrieve, defaults to None
        :type top: Optional[int], optional
        :param skip: the number of collections to skip, defaults to None
        :type skip: Optional[int], optional
        :param count: whether to include the total count of collections, defaults to None
        :type count: Optional[bool], optional
        :return: A CollectionsListResponse object containing the list of collections
        :rtype: CollectionsListResponse
        """

        params = {}
        if top is not None:
            params["$top"] = top
        if skip is not None:
            params["$skip"] = skip
        if count is not None:
            params["$count"] = count
        response = self.rest_client.get(path=f"{self.path}/collections", params=params)
        response = humps.camelize(response)  # rest_client (ai api sdk) returns snake_case responses
        return CollectionsListResponse(**response)

    def create_collection(self, collection_request: CollectionCreateRequest) -> requests.Response:
        """Create a new collection.

        :param collection_request: The object containing the collection configuration.
        :type collection_request: CollectionCreateRequest
        :return: requests.Response empty object with 202 status code
        :rtype: requests.Response
        """

        response = self.rest_client.post(
            path=f"{self.path}/collections",
            body=collection_request.model_dump(exclude_none=True)
        )
        if response == "":  # rest_client (ai api sdk) returns empty string for 202 No Content
            response = requests.Response()
            response.status_code = 202
        return response

    def get_collection_by_id(self, collection_id: str) -> Collection:
        """Get collection details by ID.

        :param collection_id: The ID of the collection to retrieve.
        :type collection_id: str
        :return: A Collection object containing the collection details
        :rtype: Collection
        """

        response = self.rest_client.get(path=f"{self.path}/collections/{collection_id}")
        response = humps.camelize(response)  # rest_client (ai api sdk) returns snake_case responses
        return Collection(**response)

    def delete_collection(self, collection_id: str) -> requests.Response:
        """Delete collection by ID.

        :param collection_id: The ID of the collection to delete.
        :type collection_id: str
        :return: requests.Response empty object with 204 status code
        :rtype: requests.Response
        """

        response = self.rest_client.delete(path=f"{self.path}/collections/{collection_id}")
        if response == "":  # rest_client (ai api sdk) returns empty string for 204 No Content
            response = requests.Response()
            response.status_code = 204
        return response

    # --- Documents ---

    def get_documents(self, collection_id: str, top: Optional[int] = None,
                      skip: Optional[int] = None, count: Optional[bool] = None) -> DocumentsResponse:
        """Get documents from a collection.

        :param collection_id: The ID of the collection to retrieve documents from.
        :type collection_id: str
        :param top: the number of documents to retrieve, defaults to None
        :type top: Optional[int], optional
        :param skip: the number of documents to skip, defaults to None
        :type skip: Optional[int], optional
        :param count: whether to include the total count of documents, defaults to None
        :type count: Optional[bool], optional
        :return: A DocumentsResponse object containing the list of documents
        :rtype: DocumentsResponse
        """

        params = {}
        if top is not None:
            params['$top'] = top
        if skip is not None:
            params['$skip'] = skip
        if count is not None:
            params['$count'] = count
        response = self.rest_client.get(
            path=f"{self.path}/collections/{collection_id}/documents",
            params=params
        )
        response = humps.camelize(response)  # rest_client (ai api sdk) returns snake_case responses
        return DocumentsResponse(**response)

    def create_documents(self, collection_id: str, request: DocumentsCreateRequest) -> DocumentsListResponse:
        """Create documents in a collection.

        :param collection_id: The ID of the collection to add documents to.
        :type collection_id: str
        :param request: The object containing the documents to create.
        :type request: DocumentsCreateRequest
        :return: A DocumentsListResponse object containing the created documents
        :rtype: DocumentsListResponse
        """

        response = self.rest_client.post(
            path=f"{self.path}/collections/{collection_id}/documents",
            body=request.model_dump(exclude_none=True)
        )
        response = humps.camelize(response)  # rest_client (ai api sdk) returns snake_case responses
        return DocumentsListResponse(**response)

    def update_documents(self, collection_id: str, request: DocumentsUpdateRequest) -> DocumentsListResponse:
        """Update documents in a collection.

        :param collection_id: The ID of the collection to update documents in.
        :type collection_id: str
        :param request: The object containing the documents to update.
        :type request: DocumentsUpdateRequest
        :return: A DocumentsListResponse object containing the updated documents
        :rtype: DocumentsListResponse
        """

        response = self.rest_client.patch(
            path=f"{self.path}/collections/{collection_id}/documents",
            body=request.model_dump(exclude_none=True)
        )
        response = humps.camelize(response)  # rest_client (ai api sdk) returns snake_case responses
        return DocumentsListResponse(**response)

    def get_document_by_id(self, collection_id: str, document_id: str) -> Document:
        """Get a document by ID from a collection.

        :param collection_id: The ID of the collection to retrieve the document from.
        :type collection_id: str
        :param document_id: The ID of the document to retrieve.
        :type document_id: str
        :return: A Document object containing the document details
        :rtype: Document
        """

        response = self.rest_client.get(
            path=f"{self.path}/collections/{collection_id}/documents/{document_id}"
        )
        response = humps.camelize(response)  # rest_client (ai api sdk) returns snake_case responses
        return Document(**response)

    def delete_document(self, collection_id: str, document_id: str) -> requests.Response:
        """Delete a document from a collection.

        :param collection_id: The ID of the collection to delete the document from.
        :type collection_id: str
        :param document_id: The ID of the document to delete.
        :type document_id: str
        :return: requests.Response empty object with 204 status code
        :rtype: requests.Response
        """

        response = self.rest_client.delete(
            path=f"{self.path}/collections/{collection_id}/documents/{document_id}"
        )
        if response == "":  # 204 No Content
            response = requests.Response()
            response.status_code = 204
        return response

    # --- Collection statuses ---

    def get_collection_creation_status(self, collection_id: str) -> CollectionCreationStatusResponse:
        """Get creation status for a collection.

        :param collection_id: The ID of the collection to retrieve the creation status for.
        :type collection_id: str
        :return: A CollectionCreationStatusResponse object containing the creation status
        :rtype: CollectionCreationStatusResponse
        """

        response = self.rest_client.get(path=f"{self.path}/collections/{collection_id}/creationStatus")
        response = humps.camelize(response)  # rest_client (ai api sdk) returns snake_case responses
        adapter = TypeAdapter(CollectionCreationStatusResponse)
        return adapter.validate_python(response)

    def get_collection_deletion_status(self, collection_id: str) -> CollectionDeletionStatusResponse:
        """Get deletion status for a collection.

        :param collection_id: The ID of the collection to retrieve the deletion status for.
        :type collection_id: str
        :return: A CollectionDeletionStatusResponse object containing the deletion status
        :rtype: CollectionDeletionStatusResponse
        """

        response = self.rest_client.get(path=f"{self.path}/collections/{collection_id}/deletionStatus")
        response = humps.camelize(response)  # rest_client (ai api sdk) returns snake_case responses
        adapter = TypeAdapter(CollectionDeletionStatusResponse)
        return adapter.validate_python(response)

    # --- Search ---

    def search(self, request: TextSearchRequest) -> VectorSearchResults:
        """Perform semantic search in vector collections.

        :param request: The object containing the search parameters.
        :type request: TextSearchRequest
        :return: A VectorSearchResults object containing the search results
        :rtype: VectorSearchResults
        """

        response = self.rest_client.post(
            path=f"{self.path}/search",
            body=request.model_dump(exclude_none=True)
        )
        response = humps.camelize(response)  # rest_client (ai api sdk) returns snake_case responses
        return VectorSearchResults(**response)
