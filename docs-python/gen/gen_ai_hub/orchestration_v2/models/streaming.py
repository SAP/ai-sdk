"""
Streaming options for content generation.
"""

from typing import List, Optional

from pydantic import model_validator

from gen_ai_hub.orchestration_v2.models.base import ABCBaseModel as BaseModel


class GlobalStreamOptions(BaseModel):
    """
    Represents options for streaming content generation.
    Args:
        enabled(bool, optional): If true, the response will be streamed back to the client.

        chunk_size(int, optional): Minimum number of characters per chunk that post-LLM modules operate on.

        delimiters(list(str), optional): List of delimiters to split the input text into chunks.Please note,
        this is a required parameter when input_translation_module_config or
        output_translation_module_config are configured.
    """
    enabled: Optional[bool] = False
    chunk_size: Optional[int] = 100
    delimiters: Optional[List[str]] = None

    def model_dump(self, **kwargs):
        """Override model_dump to exclude chunk_size and delimiters when enabled is False."""
        data = super().model_dump(**kwargs)
        if not self.enabled:
            # Remove chunk_size and delimiters from output when streaming is disabled
            data.pop('chunk_size', None)
            data.pop('delimiters', None)
        return data

__all__ = ["GlobalStreamOptions"]