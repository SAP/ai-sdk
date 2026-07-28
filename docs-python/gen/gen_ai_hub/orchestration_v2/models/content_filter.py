"""
Content filter models for various providers.
"""

from enum import Enum
from typing import Optional, Union

from pydantic import Field

from gen_ai_hub.orchestration_v2.models.azure_content_filter import (AzureContentSafetyInput, AzureContentSafetyOutput,
                                                                     AzureContentFilter)
from gen_ai_hub.orchestration_v2.models.base import ABCBaseModel as BaseModel
from gen_ai_hub.orchestration_v2.models.llama_guard_3_filter import LlamaGuard38bFilter


class ContentFilterProvider(str, Enum):
    """
    Enumerates supported content filter providers.

    This enum defines the available content filtering services that can be used
    for content moderation tasks. Each enum value represents a specific provider.

    Values:
        AZURE: Represents the Azure Content Safety service.

        LLAMA_GUARD_3_8B: Represents the Llama Guard 3 based on Llama-3.1-8B pretrained model.
    """

    AZURE = "azure_content_safety"
    LLAMA_GUARD_3_8B = "llama_guard_3_8b"

class ContentFilter(BaseModel):
    """
    Base class for content filtering configurations.

    This class provides a generic structure for defining content filters
    from various providers. It allows for specifying the provider and
    associated configuration parameters.

    Args:
        type: The name of the content filter provider.

        config: A dictionary containing the configuration parameters for the content filter.
    """
    type_: ContentFilterProvider = Field(..., alias="type")
    config: Optional[Union[AzureContentFilter, LlamaGuard38bFilter]] = None

class LlamaGuard38bFilterConfig(ContentFilter):
    type_: ContentFilterProvider = Field(default=ContentFilterProvider.LLAMA_GUARD_3_8B, alias="type")
    config: LlamaGuard38bFilter

class AzureContentSafetyInputFilterConfig(ContentFilter):
    type_: ContentFilterProvider = Field(default=ContentFilterProvider.AZURE, alias="type")
    config: Optional[AzureContentSafetyInput] = None

class AzureContentSafetyOutputFilterConfig(ContentFilter):
    type_: ContentFilterProvider = Field(default=ContentFilterProvider.AZURE, alias="type")
    config: Optional[AzureContentSafetyOutput] = None

class FilteringStreamOptions(BaseModel):
    """
    overlap: Number of characters that should be additionally sent to content filtering services
    from previous chunks as additional context.
    """
    overlap: Optional[int] = Field(default=0, ge=0, le=10000)

__all__ = ["ContentFilterProvider", "ContentFilter", "LlamaGuard38bFilterConfig", "AzureContentSafetyInputFilterConfig",
           "AzureContentSafetyOutputFilterConfig", "FilteringStreamOptions"]