"""Pydantic models for Retrieval API.

This module defines data models for the Retrieval API, which enables querying
and retrieving relevant content from configured data repositories (vector stores
and external document sources).

Model categories:
    - Data repository models (repository information and metadata)
    - Chunk and document models (content structure)
    - Search filter and configuration models (query parameters)
    - Search input and result models (request/response structures)

The Retrieval API supports semantic search combined with metadata filtering
for precise content retrieval across multiple repository types.
"""
from typing import List, Optional, Union, Literal
from pydantic import BaseModel, Field


# --- Common Key/Value models ---

class RetrievalKeyValueListPair(BaseModel):
    key: str
    value: List[str]


class RetrievalDocumentKeyValueListPair(RetrievalKeyValueListPair):
    matchMode: Optional[str]



class RetrievalSearchDocumentKeyValueListPair(BaseModel):
    key: str
    value: List[str]
    selectMode: Optional[List[str]] = None


# --- Retrieval Chunk and Document models ---

class RetrievalChunk(BaseModel):
    id: str
    content: str
    metadata: Optional[List[RetrievalKeyValueListPair]] = Field(default_factory=list)


class RetrievalDocument(BaseModel):
    id: str
    metadata: Optional[List[RetrievalDocumentKeyValueListPair]] = Field(default_factory=list)
    chunks: List[RetrievalChunk]


# --- Data Repository models ---

DataRepositoryType = Union[
    Literal["vector", "help.sap.com"],
    str
]


class DataRepository(BaseModel):
    id: str
    title: str
    type: DataRepositoryType
    metadata: Optional[List[RetrievalKeyValueListPair]] = Field(default_factory=list)


class DataRepositoryWithDocuments(BaseModel):
    id: str
    title: str
    metadata: Optional[List[RetrievalKeyValueListPair]] = Field(default_factory=list)
    documents: List[RetrievalDocument]


# --- Retrieval Filter and Configuration models ---

class RetrievalSearchConfiguration(BaseModel):
    maxChunkCount: Optional[int] = None
    maxDocumentCount: Optional[int] = None


class RetrievalSearchFilter(BaseModel):
    id: str
    dataRepositoryType:  DataRepositoryType
    searchConfiguration: Optional[RetrievalSearchConfiguration] = Field(default_factory=RetrievalSearchConfiguration)
    dataRepositories: Optional[List[str]] = Field(default_factory=list)
    dataRepositoryMetadata: Optional[List[RetrievalKeyValueListPair]] = Field(default_factory=list)
    documentMetadata: Optional[List[RetrievalSearchDocumentKeyValueListPair]] = Field(default_factory=list)
    chunkMetadata: Optional[List[RetrievalKeyValueListPair]] = Field(default_factory=list)


# --- Retrieval Search Input and Results ---

class RetrievalSearchInput(BaseModel):
    query: str
    filters: List[RetrievalSearchFilter]


class RetrievalDataRepositorySearchResult(BaseModel):
    dataRepository: DataRepositoryWithDocuments


class RetrievalPerFilterSearchResult(BaseModel):
    filterId: str
    results: List[RetrievalDataRepositorySearchResult] = Field(default_factory=list)


class RetrievalPerFilterSearchResultError(BaseModel):
    message: str


class RetrievalPerFilterSearchResultWithError(BaseModel):
    filterId: str
    error: RetrievalPerFilterSearchResultError


class RetrievalSearchResults(BaseModel):
    results: List[Union[RetrievalPerFilterSearchResult, RetrievalPerFilterSearchResultWithError]]


# --- List & Single Repository responses ---

class DataRepositories(BaseModel):
    count: Optional[int] = None
    resources: List[DataRepository]

