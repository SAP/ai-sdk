"""
Module defining the LLM (Large Language Model) configuration model.
"""

from typing import Optional, Dict

from pydantic import Field

from gen_ai_hub.orchestration_v2.models.base import ABCBaseModel as BaseModel


class LLMModelDetails(BaseModel):
    """
    The model and parameters to be used for the prompt templating.
    This is the model that will be used to generate the response.

    Args:
        name: Name of the model as in LLM Access configuration.

        version: Version of the model to be used. Defaults to "latest".

        params: Additional parameters for the model. Default values are used for mandatory parameters.

        timeout: Timeout for the LLM request in seconds. This parameter is currently ignored for Vertex AI models.

        max_retries: Maximum number of retries for the LLM request. This parameter is currently ignored for Vertex AI models.
    """
    name: str
    version: Optional[str] = "latest"
    params: Optional[Dict] = None
    timeout: Optional[int] = Field(default=600, ge=1, le=600)
    max_retries: Optional[int] = Field(default=2, ge=0, le=5)

__all__ = ["LLMModelDetails"]