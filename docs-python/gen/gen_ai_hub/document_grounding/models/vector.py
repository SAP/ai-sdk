"""Pydantic models for Vector API.

This module defines data models for the Vector API, which provides management
and search capabilities for vector-based document collections.

Model categories:
    - Collection models (collection configuration and management)
    - Document and chunk models (content structure with embeddings)
    - Embedding configuration models (embedding model settings)
    - Search models (semantic search requests and results)
    - Status models (collection creation/deletion tracking)

The Vector API enables semantic search across document collections using
vector embeddings for similarity-based retrieval.
"""
from typing import List, Optional, Annotated, Literal
from pydantic import BaseModel, Field


# --- Models for Vector API ---

# --- Common key-value metadata pair ---
class VectorKeyValueListPair(BaseModel):
    key: str
    value: List[str]


# --- Embedding Config ---
class EmbeddingConfig(BaseModel):
    modelName: Optional[str] = Field(default="text-embedding-3-large")


# --- Collection Models ---
class CollectionCreateRequest(BaseModel):
    title: Optional[str] = None
    embeddingConfig: EmbeddingConfig
    metadata: Optional[List[VectorKeyValueListPair]] = []


class Collection(BaseModel):
    id: str
    title: Optional[str] = None
    embeddingConfig: EmbeddingConfig
    metadata: Optional[List[VectorKeyValueListPair]] = []


class CollectionsListResponse(BaseModel):
    count: Optional[int] = None
    resources: List[Collection]


# --- Chunk and Document Models ---
class TextOnlyBaseChunk(BaseModel):
    content: str
    metadata: Optional[List[VectorKeyValueListPair]] = []


class BaseDocument(BaseModel):
    chunks: List[TextOnlyBaseChunk]
    metadata: List[VectorKeyValueListPair]


class DocumentWithoutChunks(BaseModel):
    id: str
    metadata: List[VectorKeyValueListPair]


class Document(BaseDocument):
    id: str


class DocumentsCreateRequest(BaseModel):
    documents: List[BaseDocument]


class DocumentsUpdateRequest(BaseModel):
    documents: List[Document]


class DocumentsListResponse(BaseModel):
    documents: List[DocumentWithoutChunks]


class DocumentsResponse(BaseModel):
    count: Optional[int] = None
    resources: List[DocumentWithoutChunks]


# --- Collection Status Models ---

class CollectionCreatedResponse(BaseModel):
    collectionURL: str = Field(alias="collectionUrl")
    status: Literal["CREATED"] = "CREATED"


class CollectionDeletedResponse(BaseModel):
    collectionURL: str = Field(alias="collectionUrl")
    status: Literal["DELETED"] = "DELETED"


class CollectionPendingResponse(BaseModel):
    Location: str = Field(alias="location")
    status: Literal["PENDING"] = "PENDING"


CollectionCreationStatusResponse = Annotated[
    CollectionCreatedResponse | CollectionPendingResponse,
    Field(discriminator="status")
]

CollectionDeletionStatusResponse = Annotated[
    CollectionDeletedResponse | CollectionPendingResponse,
    Field(discriminator="status")
]

# --- Vector Search Models ---
class VectorSearchConfiguration(BaseModel):
    maxChunkCount: Optional[int] = None
    maxDocumentCount: Optional[int] = None


class VectorSearchDocumentKeyValueListPair(BaseModel):
    key: str
    value: List[str]
    selectMode: Optional[List[str]] = None


class VectorSearchFilter(BaseModel):
    id: str
    collectionIds: List[str]
    configuration: VectorSearchConfiguration
    collectionMetadata: Optional[List[VectorKeyValueListPair]] = []
    documentMetadata: Optional[List[VectorSearchDocumentKeyValueListPair]] = []
    chunkMetadata: Optional[List[VectorKeyValueListPair]] = []


class TextSearchRequest(BaseModel):
    query: str
    filters: List[VectorSearchFilter]


# --- Vector Search Results ---
class VectorChunk(BaseModel):
    id: str
    content: str
    metadata: Optional[List[VectorKeyValueListPair]] = []


class DocumentOutput(BaseModel):
    id: str
    metadata: Optional[List[VectorKeyValueListPair]] = []
    chunks: List[VectorChunk]


class DocumentsChunk(BaseModel):
    id: str
    title: str
    metadata: Optional[List[VectorKeyValueListPair]] = []
    documents: List[DocumentOutput]


class VectorPerFilterSearchResult(BaseModel):
    filterId: str
    results: List[DocumentsChunk]


class VectorSearchResults(BaseModel):
    results: List[VectorPerFilterSearchResult]
