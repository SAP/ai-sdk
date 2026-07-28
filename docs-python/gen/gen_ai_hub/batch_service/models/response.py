"""
Response models for the LLM Batch Service API.
"""

from enum import Enum
from typing import Optional

from pydantic import Field

from gen_ai_hub.batch_service.models.base import ResponseBaseModel


class BatchStatus(str, Enum):
    """Enumeration of possible lifecycle states for a batch job.

    :cvar PENDING: Job has been accepted and is waiting to be scheduled.
    :cvar RUNNING: Job is actively being processed.
    :cvar COMPLETED: Job finished successfully.
    :cvar FAILED: Job terminated with an error.
    :cvar CANCELLED: Job was cancelled by the user.
    :cvar CANCELLING: Cancellation has been requested and is in progress.
    """

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    CANCELLING = "CANCELLING"


class BatchCreateResponse(ResponseBaseModel):
    """Response returned by ``POST /llm-batch-service/v1/batches``.

    Confirms that the batch job has been accepted and provides the assigned
    identifier and initial status.

    :param id: Unique identifier (UUID) of the created batch job.
    :type id: str
    :param created_at: ISO 8601 timestamp of when the job was created.
    :type created_at: str, optional
    :param status: Initial status of the job, typically ``"PENDING"``.
    :type status: str, optional
    :param message: Human-readable confirmation message from the service.
    :type message: str, optional
    """

    id: str = Field(..., description="Unique identifier of the batch job")
    created_at: Optional[str] = Field(None, description="ISO 8601 creation timestamp")
    status: Optional[str] = Field(None, description="Initial job status")
    message: Optional[str] = Field(None, description="Human-readable status message")


class BatchSummary(ResponseBaseModel):
    """Summary entry for a single batch job as returned in a list response.

    :param id: Unique identifier (UUID) of the batch job.
    :type id: str
    :param type: Batch processing type (e.g. ``"llm-native"``).
    :type type: str, optional
    :param provider: LLM provider name (e.g. ``"azure-openai"``).
    :type provider: str, optional
    :param created_at: ISO 8601 timestamp of when the job was created.
    :type created_at: str, optional
    :param status: Current status of the job.
    :type status: str, optional
    """

    id: str = Field(..., description="Unique identifier of the batch job")
    type: Optional[str] = Field(None, description="Batch processing type")
    provider: Optional[str] = Field(None, description="LLM provider name")
    created_at: Optional[str] = Field(None, description="ISO 8601 creation timestamp")
    status: Optional[str] = Field(None, description="Current job status")


class BatchListResponse(ResponseBaseModel):
    """Response returned by ``GET /llm-batch-service/v1/batches``.

    Contains a count and a list of batch job summaries for the current
    resource group.

    :param count: Total number of batch jobs.
    :type count: int, optional
    :param resources: List of batch job summaries.
    :type resources: list[:class:`BatchSummary`], optional
    """

    count: Optional[int] = Field(None, description="Total number of batch jobs")
    resources: Optional[list[BatchSummary]] = Field(None, description="List of batch job summaries")


class BatchStatusDetail(ResponseBaseModel):
    """Status block embedded inside :class:`BatchDetailResponse`.

    :param current_status: The job's current lifecycle status.
    :type current_status: str, optional
    :param target_status: The terminal status the job is expected to reach.
    :type target_status: str, optional
    :param updated_at: ISO 8601 timestamp of the last status change.
    :type updated_at: str, optional
    :param message: Optional human-readable description of the current status.
    :type message: str, optional
    """

    current_status: Optional[str] = Field(None, description="Current job status")
    target_status: Optional[str] = Field(None, description="Target terminal status")
    updated_at: Optional[str] = Field(None, description="ISO 8601 timestamp of last status update")
    message: Optional[str] = Field(None, description="Optional human-readable status message")


class BatchInputDetail(ResponseBaseModel):
    """Input configuration as returned in a batch detail response.

    :param uri: Object-store URI of the input ``.jsonl`` file.
    :type uri: str, optional
    """

    uri: Optional[str] = Field(None, description="Input file URI")


class BatchOutputDetail(ResponseBaseModel):
    """Output configuration as returned in a batch detail response.

    :param uri: Object-store URI of the output directory.
    :type uri: str, optional
    """

    uri: Optional[str] = Field(None, description="Output directory URI")


class BatchDetailResponse(ResponseBaseModel):
    """Response returned by ``GET /llm-batch-service/v1/batches/{batch_id}``.

    Provides the full configuration and current status of a specific batch job.

    :param id: Unique identifier (UUID) of the batch job.
    :type id: str, optional
    :param type: Batch processing type (e.g. ``"llm-native"``).
    :type type: str, optional
    :param provider: LLM provider name (e.g. ``"azure-openai"``).
    :type provider: str, optional
    :param created_at: ISO 8601 timestamp of when the job was created.
    :type created_at: str, optional
    :param input: Input file configuration.
    :type input: :class:`BatchInputDetail`, optional
    :param output: Output directory configuration.
    :type output: :class:`BatchOutputDetail`, optional
    :param spec: Raw job specification dict as stored by the service.
    :type spec: dict, optional
    :param status: Current status details.
    :type status: :class:`BatchStatusDetail`, optional
    """

    id: Optional[str] = Field(None, description="Unique identifier of the batch job")
    type: Optional[str] = Field(None, description="Batch processing type")
    provider: Optional[str] = Field(None, description="LLM provider name")
    created_at: Optional[str] = Field(None, description="ISO 8601 creation timestamp")
    input: Optional[BatchInputDetail] = Field(None, description="Input configuration")
    output: Optional[BatchOutputDetail] = Field(None, description="Output configuration")
    spec: Optional[dict] = Field(None, description="Batch job specification")
    status: Optional[BatchStatusDetail] = Field(None, description="Current status details")


class BatchStatusResponse(ResponseBaseModel):
    """Response returned by ``GET /llm-batch-service/v1/batches/{batch_id}/status``.

    :param current_status: The job's current lifecycle status.
    :type current_status: str, optional
    :param target_status: The terminal status the job is expected to reach.
    :type target_status: str, optional
    :param updated_at: ISO 8601 timestamp of the last status change.
    :type updated_at: str, optional
    :param message: Optional human-readable description of the current status.
    :type message: str, optional
    """

    current_status: Optional[str] = Field(None, description="Current job status")
    target_status: Optional[str] = Field(None, description="Target terminal status")
    updated_at: Optional[str] = Field(None, description="ISO 8601 timestamp of last status update")
    message: Optional[str] = Field(None, description="Optional human-readable status message")


class BatchCancelResponse(ResponseBaseModel):
    """Response returned by ``PATCH /llm-batch-service/v1/batches/{batch_id}/cancel``.

    Confirms that the cancellation request has been accepted. The job will
    transition to ``CANCELLING`` and eventually ``CANCELLED``.

    :param id: Unique identifier (UUID) of the batch job.
    :type id: str, optional
    :param created_at: ISO 8601 timestamp of when the job was originally created.
    :type created_at: str, optional
    :param message: Human-readable confirmation that cancellation was scheduled.
    :type message: str, optional
    """

    id: Optional[str] = Field(None, description="Unique identifier of the batch job")
    created_at: Optional[str] = Field(None, description="ISO 8601 creation timestamp")
    message: Optional[str] = Field(None, description="Human-readable confirmation message")


class BatchDeleteResponse(ResponseBaseModel):
    """Response returned by ``DELETE /llm-batch-service/v1/batches/{batch_id}``.

    Confirms that the batch job record has been deleted. Only jobs in a
    terminal state (``COMPLETED``, ``FAILED``, or ``CANCELLED``) can be deleted.

    :param id: Unique identifier (UUID) of the deleted batch job.
    :type id: str, optional
    :param created_at: ISO 8601 timestamp of when the job was originally created.
    :type created_at: str, optional
    :param message: Human-readable confirmation of the deletion.
    :type message: str, optional
    """

    id: Optional[str] = Field(None, description="Unique identifier of the batch job")
    created_at: Optional[str] = Field(None, description="ISO 8601 creation timestamp")
    message: Optional[str] = Field(None, description="Human-readable confirmation message")


class ErrorResponse(ResponseBaseModel):
    """Error response body returned by the batch service on 4xx/5xx responses.

    :param request_id: Unique request identifier, useful for tracing the
        error in service logs.
    :type request_id: str
    :param message: Human-readable description of the error.
    :type message: str
    """

    request_id: str = Field(..., description="Unique request identifier for tracing")
    message: str = Field(..., description="Human-readable error message")
