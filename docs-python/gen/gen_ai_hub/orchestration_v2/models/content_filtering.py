"""
Module for managing and applying content filters in the orchestration system.
"""

from typing import List, Optional, Union

from pydantic import model_validator, Field

from gen_ai_hub.orchestration_v2.models.base import ABCBaseModel as BaseModel
from gen_ai_hub.orchestration_v2.models.content_filter import (AzureContentSafetyOutputFilterConfig,
AzureContentSafetyInputFilterConfig, LlamaGuard38bFilterConfig, FilteringStreamOptions, ContentFilter)


class InputFiltering(BaseModel):
    """Module for managing and applying input content filters.

        Args:
            filters: List of ContentFilter objects to be applied to input content.
    """
    filters: List[
        Union[AzureContentSafetyInputFilterConfig, LlamaGuard38bFilterConfig, ContentFilter]
    ] = Field(min_length=1)


class OutputFiltering(BaseModel):
    """Module for managing and applying output content filters.

        Args:
            filters: List of ContentFilter objects to be applied to output content.

            stream_options: Module-specific streaming options.
    """

    filters: List[
        Union[AzureContentSafetyOutputFilterConfig, LlamaGuard38bFilterConfig, ContentFilter]
    ] = Field(min_length=1)
    stream_options: Optional[FilteringStreamOptions] = None


class FilteringModuleConfig(BaseModel):
    """Module for managing and applying content filters.

    Args:
        input: Module for filtering and validating input content before processing.

        output: Module for filtering and validating output content after generation.
    """

    input: Optional[InputFiltering] = None
    output: Optional[OutputFiltering] = None

    @model_validator(mode="after")
    def enforce_min_properties(cls, values):  # pylint: disable=no-self-argument
        """
        Ensure at least one of input or output filtering is provided.
        """
        assert values.input is not None or values.output is not None, \
            "FilteringModuleConfig must have at least one property: input or output."
        return values

__all__ = ["InputFiltering", "OutputFiltering", "FilteringModuleConfig"]