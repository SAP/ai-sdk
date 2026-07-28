from enum import Enum
from typing import List, Dict, Any

from gen_ai_hub.orchestration.models.base import JSONSerializable


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


class DocumentMetadata(JSONSerializable):
    """Restrict documents considered during search to those annotated with the given metadata."""

    def __init__(self, key: str, value: List[str], select_mode: List[str] = None):
        """Initializes the DocumentMetadata instance.

        :param key: The key for the metadata.
        :type key: str
        :param value: The list of values for the metadata.
        :type value: List[str]
        :param select_mode: Select mode for search filters.
        :type select_mode: List[str], optional
        """
        self.key = key
        self.value = value
        self.select_mode = select_mode

    def to_dict(self):
        """Converts the DocumentMetadata instance to a dictionary representation.

        :return: Dictionary representation of the DocumentMetadata.
        :rtype: dict
        """
        config = {"key": self.key, "value": self.value}
        if self.select_mode:
            config["select_mode"] = self.select_mode

        return config


class GroundingFilterSearch(JSONSerializable):
    """Search configuration for the data repository."""

    def __init__(self, max_chunk_count: int = None, max_document_count: int = None):
        """Initializes the GroundingFilterSearch instance.

        :param max_chunk_count: maximum number of chunks > 0 to return, defaults to None
        :type max_chunk_count: int, optional
        :param max_document_count: Maximum number of documents > 0 to return.
            Only supports 'vector' dataRepositoryType. Cannot be used with 'maxChunkCount'.
            If maxDocumentCount is given, then only one chunk per document is returned, defaults to None
        :type max_document_count: int, optional
        :raises ValueError: If both max_chunk_count and max_document_count are set.
        """
        self.max_chunk_count = max_chunk_count
        self.max_document_count = max_document_count
        if self.max_chunk_count and self.max_document_count:
            raise ValueError("Cannot set both max_chunk_count and max_document_count")

    def to_dict(self):
        """Converts the GroundingFilterSearch instance to a dictionary representation.

        :return: Dictionary representation of the GroundingFilterSearch.
        :rtype: dict
        """
        config = {}
        if self.max_chunk_count:
            config["max_chunk_count"] = self.max_chunk_count
        if self.max_document_count:
            config["max_document_count"] = self.max_document_count
        return config


class DocumentGroundingFilter(JSONSerializable):
    """Module for configuring document grounding filters."""

    def __init__(self,
                 id: str,
                 data_repository_type: str,
                 search_config: GroundingFilterSearch = None,
                 data_repositories: List[str] = None,
                 data_repository_metadata: List[Dict[str, Any]] = None,
                 document_metadata: List[DocumentMetadata] = None,
                 chunk_metadata: List[Dict[str, Any]] = None
                 ):
        """Initializes the DocumentGroundingFilter instance.

        :param id: The unique identifier for the grounding filter.
        :type id: str
        :param data_repository_type: Only include DataRepositories with the given type:
            'vector' or 'url' of website supporting elastic search.
        :type data_repository_type: str
        :param search_config: GroundingFilterSearchConfiguration object, defaults to None
        :type search_config: GroundingFilterSearch, optional
        :param data_repositories: list of data repositories to search.
            Specify ['*'] to search across all DataRepositories or
            give a specific list of DataRepository ids, defaults to None
        :type data_repositories: List[str], optional
        :param data_repository_metadata: The metadata for the data repository,
            Restrict DataRepositories considered during search to those annotated with the given
            metadata. Useful when combined with dataRepositories=['*'], defaults to None
        :type data_repository_metadata: List[Dict[str, Any]], optional
        :param document_metadata: DocumentMetadata object, defaults to None
        :type document_metadata: List[DocumentMetadata], optional
        :param chunk_metadata: Restrict chunks considered during search to those with the given metadata, 
            defaults to None
        :type chunk_metadata: List[Dict[str, Any]], optional
        """

        self.id = id
        self.data_repository_type = data_repository_type
        self.search_config = search_config
        self.data_repositories = data_repositories
        self.data_repository_metadata = data_repository_metadata
        self.document_metadata = document_metadata
        self.chunk_metadata = chunk_metadata

    def to_dict(self):
        """Converts the DocumentGroundingFilter instance to a dictionary representation.

        :return: Dictionary representation of the DocumentGroundingFilter.
        :rtype: dict
        """
        config = {
            "id": self.id,
            "data_repository_type": self.data_repository_type,
        }
        if self.search_config:
            config["search_config"] = self.search_config.to_dict()
        if self.data_repositories:
            config["data_repositories"] = self.data_repositories
        if self.data_repository_metadata:
            config["data_repository_metadata"] = self.data_repository_metadata
        if self.document_metadata:
            config["document_metadata"] = [metadata.to_dict() for metadata in self.document_metadata]
        if self.chunk_metadata:
            config["chunk_metadata"] = self.chunk_metadata
        return config


class DocumentGrounding(JSONSerializable):
    """defines the detailed configuration for the Grounding module."""

    def __init__(self, input_params: List[str], output_param: str, filters: List[DocumentGroundingFilter] = None,
                 metadata_params: List[str] = None):
        """Initializes the DocumentGrounding instance.

        :param input_params: The list of input parameters used for grounding input questions.
        :type input_params: List[str]
        :param output_param: Parameter name used for grounding output.
        :type output_param: str
        :param filters: List of DocumentGroundingFilter objects, defaults to None
        :type filters: List[DocumentGroundingFilter], optional
        :param metadata_params: Parameter name used for specifying metadata parameters, defaults to None
        :type metadata_params: List[str], optional
        """
        self.input_params = input_params
        self.output_param = output_param
        self.filters = filters
        self.metadata_params = metadata_params

    def to_dict(self):
        """Converts the DocumentGrounding instance to a dictionary representation.

        :return: Dictionary representation of the DocumentGrounding.
        :rtype: dict
        """
        config = {
            "input_params": self.input_params,
            "output_param": self.output_param,
        }
        if self.filters:
            config["filters"] = [filter.to_dict() for filter in self.filters]
        if self.metadata_params:
            config["metadata_params"] = self.metadata_params

        return config


class GroundingModule(JSONSerializable):
    """Module for managing and applying grounding aka RAG configurations."""

    def __init__(self, type: str, config: DocumentGrounding):
        """Initializes the GroundingModule instance.

        :param type: The type of the grounding module.
        :type type: str
        :param config: Configuration for the grounding module.
        :type config: DocumentGrounding
        """
        self.type = type
        self.config = config

    def to_dict(self):
        """Converts the GroundingModule instance to a dictionary representation.

        :return: Dictionary representation of the GroundingModule.
        :rtype: dict
        """
        return {
            "type": self.type,
            "config": self.config.to_dict(),
        }
