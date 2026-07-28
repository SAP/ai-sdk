"""Pydantic models for Pipeline API.

This module defines data models for the Pipeline API, which manages document
vectorization pipelines from various data sources (Microsoft SharePoint, AWS S3, SFTP).

Model categories:
    - Pipeline configuration models (create/get requests and responses)
    - Pipeline execution models (tracking pipeline runs)
    - Document models (tracking document processing status)
    - Search and metadata models (filtering pipelines by metadata)
    - Trigger models (manual pipeline execution)

All models use Pydantic for validation and serialization.
"""
from typing import List, Optional, Union, Annotated, Literal
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

# --- Models for Pipeline API ---

class MetaData(BaseModel):
    destination: str

class SharePointSite(BaseModel):
    name: str
    includePaths: Optional[List[str]] = None

class SharePointConfig(BaseModel):
    site: SharePointSite

class MSSharePointConfiguration(BaseModel):
    destination: str
    sharePoint: SharePointConfig

class CommonConfiguration(BaseModel):
    destination: str

class MSSharePointPipelineCreateRequest(BaseModel):
    type: Literal["MSSharePoint"] = "MSSharePoint"
    configuration: MSSharePointConfiguration
    metadata: Optional[MetaData] = None

class S3PipelineCreateRequest(BaseModel):
    type: Literal["S3"] = "S3"
    configuration: CommonConfiguration
    metadata: Optional[MetaData] = None

class SFTPPipelineCreateRequest(BaseModel):
    type: Literal["SFTP"] = "SFTP"
    configuration: CommonConfiguration
    metadata: Optional[MetaData] = None

CreatePipelineRequest = Union[
    MSSharePointPipelineCreateRequest,
    S3PipelineCreateRequest,
    SFTPPipelineCreateRequest
]

class PipelineIdResponse(BaseModel):
    pipelineId: str

class BasePipelineResponse(BaseModel):
    id: str
    type: str
    metadata: Optional[MetaData] = None

class MSSharePointConfigurationGetResponse(BaseModel):
    destination: str
    sharePoint: SharePointConfig

class MSSharePointPipelineGetResponse(BasePipelineResponse):
    type: Literal["MSSharePoint"] = "MSSharePoint"
    configuration: MSSharePointConfigurationGetResponse

class S3PipelineGetResponse(BasePipelineResponse):
    type: Literal["S3"] = "S3"
    configuration: CommonConfiguration

class SFTPPipelineGetResponse(BasePipelineResponse):
    type: Literal["SFTP"] = "SFTP"
    configuration: CommonConfiguration

GetPipelineResponse = Annotated[
    MSSharePointPipelineGetResponse | S3PipelineGetResponse | SFTPPipelineGetResponse,
    Field(discriminator="type")
]

class GetPipelinesResponse(BaseModel):
    count: Optional[int]
    resources: List[GetPipelineResponse]

class GetPipelineStatusResponse(BaseModel):
    lastStarted: Optional[str]
    status: Optional[str]

# --- Search ---

class DataRepositoryMetadataItem(BaseModel):
    key: str
    value: List[str]


class SearchPipelineRequest(BaseModel):
    dataRepositoryMetadata: List[DataRepositoryMetadataItem]


class SearchPipelineData(BaseModel):
    pipelineId: str


class SearchPipelinesResponse(BaseModel):
    count: Optional[int]
    resources: List[SearchPipelineData]


# --- Executions (Pipeline Runs) ---

class PipelineExecutionStatus(str, Enum):
    NEW = "NEW"
    UNKNOWN = "UNKNOWN"
    INPROGRESS = "INPROGRESS"
    FINISHED = "FINISHED"
    FINISHED_WITH_ERRORS = "FINISHEDWITHERRORS"
    TIMEOUT = "TIMEOUT"

class PipelineExecution(BaseModel):
    id: str
    status: Optional[PipelineExecutionStatus] = None
    createdAt: Optional[datetime] = None
    modifiedAt: Optional[datetime] = None


class GetPipelineExecutionsResponse(BaseModel):
    count: Optional[int]
    resources: List[PipelineExecution]


# --- Documents ---

class DocumentStatus(str, Enum):
    TO_BE_PROCESSED = "TO_BE_PROCESSED"
    INDEXED = "INDEXED"
    REINDEXED = "REINDEXED"
    DEINDEXED = "DEINDEXED"
    FAILED = "FAILED"
    FAILED_TO_BE_RETRIED = "FAILED_TO_BE_RETRIED"
    TO_BE_SCHEDULED = "TO_BE_SCHEDULED"

class Document(BaseModel):
    id: str
    status: Optional[DocumentStatus] = None
    viewLocation: Optional[str] = None
    downloadLocation: Optional[str] = None
    absoluteUrl: Optional[str] = None
    title: Optional[str] = None
    metadataId: Optional[str] = None
    createdTimestamp: Optional[datetime] = None
    lastUpdatedTimestamp: Optional[datetime] = None


class DocumentsStatusResponse(BaseModel):
    count: Optional[int]
    resources: List[Document]


# --- Trigger ---

class ManualPipelineTrigger(BaseModel):
    pipelineId: str
    metadataOnly: Optional[bool] = None
