"""Clients subpackage for Document Grounding API.

This subpackage contains the API client implementations for interacting with
the SAP Generative AI Hub Document Grounding services.

Available clients:
    - PipelineAPIClient: Manages document vectorization pipelines from various data sources
    - RetrievalAPIClient: Performs retrieval operations across configured data repositories
    - VectorAPIClient: Manages vector collections and performs semantic searches
"""

from .pipeline_api_client import ( # pylint: disable=unused-import
    PATH_DOCUMENT_GROUNDING_PIPELINES,
    PATH_DOCUMENT_GROUNDING,
    PipelineAPIClient
)
from .retrieval_api_client import ( # pylint: disable=unused-import
    PATH_DOCUMENT_GROUNDING_RETRIEVAL,
    RetrievalAPIClient
)
from .vector_api_client import ( # pylint: disable=unused-import
    PATH_DOCUMENT_GROUNDING_VECTOR,
    VectorAPIClient
)

__all__ = [
    "PipelineAPIClient", "RetrievalAPIClient", "VectorAPIClient", "PATH_DOCUMENT_GROUNDING",
    "PATH_DOCUMENT_GROUNDING_VECTOR", "PATH_DOCUMENT_GROUNDING_PIPELINES", "PATH_DOCUMENT_GROUNDING_RETRIEVAL"
]