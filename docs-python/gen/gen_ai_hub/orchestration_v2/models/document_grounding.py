"""
Module for defining document grounding configurations.
"""

from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import Field, model_validator, ValidationError

from gen_ai_hub.orchestration_v2.models.base import ABCBaseModel as BaseModel


class GroundingType(str, Enum):
    """
    Enumerates supported grounding types.
    """
    DOCUMENT_GROUNDING_SERVICE = "document_grounding_service"


class DataRepositoryType(str, Enum):
    """
    Enumerates data repository types.
    """
    VECTOR = "vector"  # DataRepository with vector embeddings
    URL = "help.sap.com"  # website supporting elastic search


class KeyValueListPair(BaseModel):
    key: str
    value: List[str]


class DocumentMetadataKeyValueListPairs(KeyValueListPair):
    """Restrict documents considered during search to those annotated with the given metadata.

    Args:
        key: The key for the metadata.

        value: The list of values for the metadata.

        select_mode: Select mode for search filters.
    """
    select_mode: Optional[List[Literal['ignoreIfKeyAbsent']]] = None


class GroundingSearchConfig(BaseModel):
    """Search configuration for the data repository.

    Args:
        max_chunk_count(int, minimum: 0, exclusiveMinimum: true): Maximum number of chunks to be returned.
        Cannot be used with 'maxDocumentCount'.

        max_document_count(int, minimum: 0, exclusiveMinimum: true): [Only supports 'vector' dataRepositoryType]
        - Maximum number of documents to be returned. Cannot be used with 'maxChunkCount'.
        If maxDocumentCount is given, then only one chunk per document is returned.
    """
    max_chunk_count: Optional[int] = Field(default=None, gt=0)
    max_document_count: Optional[int] = Field(default=None, gt=0)

    @model_validator(mode='after')
    def validate_max_chunk_count_and_max_document_count(self):
        if self.max_chunk_count and self.max_document_count:
            raise ValueError("Cannot specify both maxChunkCount and maxDocumentCount.")
        return self


class DocumentGroundingFilter(BaseModel):
    """Module for configuring document grounding filters.
    
    Args:
        id: The unique identifier for the grounding filter.

        search_config: GroundingSearchConfig object.

        data_repository_type: Only include DataRepositories with the given type:
                                vector, help.sap.com.

        data_repositories: list of data repositories to search.
                           Specify ['*'] to search across all DataRepositories or
                           give a specific list of DataRepository ids.

        data_repository_metadata: The metadata for the data repository.
                                  Restrict DataRepositories considered during search to those annotated with the given
                                  metadata. Useful when combined with dataRepositories=['*']

        document_metadata: DocumentMetadata object.

        chunk_metadata: Restrict chunks considered during search to those with the given metadata.
    """

    id: Optional[str] = None
    data_repository_type: Union[DataRepositoryType, Literal["vector", "help.sap.com"]]
    search_config: Optional[GroundingSearchConfig] = None
    data_repositories: Optional[List[str]] = None
    data_repository_metadata: Optional[List[KeyValueListPair]] = None
    document_metadata: Optional[List[DocumentMetadataKeyValueListPairs]] = None
    chunk_metadata: Optional[List[KeyValueListPair]] = None


class DocumentGroundingPlaceholders(BaseModel):
    """
        input: The list of input parameters used for grounding input questions (minItems: 1).
        output: Parameter name used for grounding output.
    """
    input: List[str] = Field(min_length=1)
    output: str


class DocumentGroundingConfig(BaseModel):
    """defines the detailed configuration for the Grounding module.

    Args:
        filters: List of DocumentGroundingFilter objects.

        placeholders: Placeholders to be used for grounding input questions and output.

        metadata_params: Parameter name used for specifying metadata parameters.
    """
    filters: Optional[List[DocumentGroundingFilter]] = None
    placeholders: DocumentGroundingPlaceholders
    metadata_params: Optional[list[str]] = None


class GroundingModuleConfig(BaseModel):
    """Module for managing and applying grounding aka RAG configurations.

    Args:
        type: The type of the grounding module.

        config: Configuration dictionary for the grounding module.
    """

    type: GroundingType = GroundingType.DOCUMENT_GROUNDING_SERVICE
    config: DocumentGroundingConfig

__all__ = ["GroundingType", "DataRepositoryType", "DocumentGroundingFilter", "DocumentGroundingPlaceholders",
           "DocumentGroundingConfig", "GroundingModuleConfig", "KeyValueListPair", "DocumentMetadataKeyValueListPairs"]