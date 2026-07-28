"""Document Grounding package for SAP Generative AI Hub.

This package provides APIs for document grounding capabilities including:
- Pipeline management for document vectorization from various data sources
- Vector store operations for semantic search
- Retrieval operations for querying document repositories

The package includes three main API clients:
- PipelineAPIClient: Manages document vectorization pipelines
- VectorAPIClient: Manages vector collections and semantic search
- RetrievalAPIClient: Performs retrieval operations across data repositories
"""
from .client import PipelineAPIClient, VectorAPIClient, RetrievalAPIClient
from .models import *

__all__ = [
    # Pipeline models
    "CreatePipelineRequest",
    "MSSharePointPipelineCreateRequest",
    "S3PipelineCreateRequest",
    "SFTPPipelineCreateRequest",
    "SearchPipelineRequest",
    "DataRepositoryMetadataItem",
    "CommonConfiguration",
    "MetaData",
    "MSSharePointConfiguration",
    "SharePointConfig",
    "SharePointSite",
    "ManualPipelineTrigger",
    "PipelineIdResponse",
    "GetPipelineResponse",
    "GetPipelinesResponse",
    "GetPipelineStatusResponse",
    "PipelineExecution",
    "GetPipelineExecutionsResponse",
    "Document",
    "DocumentsStatusResponse",
    "MSSharePointPipelineGetResponse",
    "S3PipelineGetResponse",
    "SFTPPipelineGetResponse",
    "SearchPipelineData",
    "SearchPipelinesResponse",
    "PipelineExecutionStatus",
    "DocumentStatus",
    "BasePipelineResponse",
    "MSSharePointConfigurationGetResponse",
    # Retrieval models
    "RetrievalKeyValueListPair",
    "RetrievalDocumentKeyValueListPair",
    "RetrievalSearchDocumentKeyValueListPair",
    "RetrievalChunk",
    "RetrievalDocument",
    "DataRepositoryType",
    "DataRepository",
    "DataRepositoryWithDocuments",
    "RetrievalSearchConfiguration",
    "RetrievalSearchFilter",
    "RetrievalSearchInput",
    "RetrievalDataRepositorySearchResult",
    "RetrievalPerFilterSearchResult",
    "RetrievalPerFilterSearchResultError",
    "RetrievalPerFilterSearchResultWithError",
    "RetrievalSearchResults",
    "DataRepositories",
    # Vector models
    "VectorKeyValueListPair",
    "EmbeddingConfig",
    "CollectionCreateRequest",
    "Collection",
    "CollectionsListResponse",
    "TextOnlyBaseChunk",
    "BaseDocument",
    "DocumentWithoutChunks",
    "VectorDocument",
    "DocumentsCreateRequest",
    "DocumentsUpdateRequest",
    "DocumentsListResponse",
    "DocumentsResponse",
    "CollectionCreatedResponse",
    "CollectionDeletedResponse",
    "CollectionPendingResponse",
    "CollectionCreationStatusResponse",
    "CollectionDeletionStatusResponse",
    "VectorSearchConfiguration",
    "VectorSearchDocumentKeyValueListPair",
    "VectorSearchFilter",
    "TextSearchRequest",
    "VectorChunk",
    "DocumentOutput",
    "DocumentsChunk",
    "VectorPerFilterSearchResult",
    "VectorSearchResults",
    # Clients
    "PipelineAPIClient",
    "RetrievalAPIClient",
    "VectorAPIClient"

]