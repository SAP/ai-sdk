"""Client module for Document Grounding API.

This module provides convenient imports for all Document Grounding API clients
and their associated constants. It serves as the main entry point for accessing
Pipeline, Retrieval, and Vector API functionality.

Exported clients:
    - PipelineAPIClient: Client for managing document vectorization pipelines
    - RetrievalAPIClient: Client for retrieval operations across data repositories
    - VectorAPIClient: Client for vector collection management and semantic search

Exported constants:
    - PATH_DOCUMENT_GROUNDING: Base path for document grounding endpoints
    - PATH_DOCUMENT_GROUNDING_PIPELINES: Path for pipeline endpoints
    - PATH_DOCUMENT_GROUNDING_RETRIEVAL: Path for retrieval endpoints
    - PATH_DOCUMENT_GROUNDING_VECTOR: Path for vector endpoints
"""
from .clients.pipeline_api_client import ( # pylint: disable=unused-import
    PATH_DOCUMENT_GROUNDING_PIPELINES,
    PATH_DOCUMENT_GROUNDING,
    PipelineAPIClient
)
from .clients.retrieval_api_client import ( # pylint: disable=unused-import
    PATH_DOCUMENT_GROUNDING_RETRIEVAL,
    RetrievalAPIClient
)
from .clients.vector_api_client import ( # pylint: disable=unused-import
    PATH_DOCUMENT_GROUNDING_VECTOR,
    VectorAPIClient
)

__all__ = [
    "PipelineAPIClient",
    "RetrievalAPIClient",
    "VectorAPIClient",
]