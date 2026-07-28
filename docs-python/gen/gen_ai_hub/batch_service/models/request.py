"""
Request models for the LLM Batch Service API.
"""

from typing import Literal

from pydantic import Field

from gen_ai_hub.batch_service.models.base import ABCBaseModel


class BatchInput(ABCBaseModel):
    """Input configuration for a batch job.

    Points to the ``.jsonl`` file in an object store that contains the
    individual LLM requests to be processed.

    :param uri: Fully qualified object-store URI of the input file.
        Must point to a ``.jsonl`` file (e.g. ``ai://my-store/input/requests.jsonl``).
    :type uri: str
    """

    uri: str = Field(..., description="Input file URI (must be a .jsonl file)")


class BatchOutput(ABCBaseModel):
    """Output configuration for a batch job.

    Points to the directory in an object store where results will be written
    once the job completes.

    :param uri: Fully qualified object-store URI of the output directory
        (e.g. ``ai://my-store/output/``).
    :type uri: str
    """

    uri: str = Field(..., description="Output directory URI")


class BatchSpec(ABCBaseModel):
    """Specification of the LLM to use for a batch job.

    :param provider: LLM provider name as registered in SAP AI Core
        (e.g. ``"azure-openai"``).
    :type provider: str
    :param model: Model name to use for inference
        (e.g. ``"gpt-4.1-mini"``).
    :type model: str
    """

    provider: str = Field(..., description="LLM provider name")
    model: str = Field(..., description="Model name")


class BatchCreateRequest(ABCBaseModel):
    """Request body sent to ``POST /llm-batch-service/v1/batches``.

    Describes a new batch processing job: where to read input from, where to
    write output, and which model to use.

    :param type: Batch processing type. Currently only ``"llm-native"`` is
        supported.
    :type type: Literal["llm-native"]
    :param input: Input file configuration.
    :type input: :class:`BatchInput`
    :param output: Output directory configuration.
    :type output: :class:`BatchOutput`
    :param spec: LLM provider and model specification.
    :type spec: :class:`BatchSpec`
    """

    type: Literal["llm-native"] = Field(..., description="Type of batch processing")
    input: BatchInput = Field(..., description="Input file configuration")
    output: BatchOutput = Field(..., description="Output directory configuration")
    spec: BatchSpec = Field(..., description="Batch job specification")
