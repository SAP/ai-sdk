from typing import List, Optional
from pydantic import model_validator

from gen_ai_hub.orchestration_v2.models.base import ABCBaseModel as BaseModel
from gen_ai_hub.orchestration_v2.models.config import OrchestrationConfig, OrchestrationConfigReference
from gen_ai_hub.orchestration_v2.models.message import ChatMessage

class CompletionPostRequest(BaseModel):
    """
    Represents a request for the orchestration process, including configuration,
    template values, and message history.
    """
    config: Optional[OrchestrationConfig] = None
    config_ref: Optional[OrchestrationConfigReference] = None
    placeholder_values: Optional[dict[str, str]] = None
    messages_history: Optional[List[ChatMessage]] = None

    @model_validator(mode="after")
    def validate_config_or_ref(self):
        """validates that exactly one of 'config' or 'config_ref' is provided.

        :raises ValueError: If neither or both 'config' and 'config_ref' are provided.
        :return: The validated OrchestrationRequest instance.
        :rtype: CompletionPostRequest
        """
        if (self.config is None) == (self.config_ref is None):
            raise ValueError(
                "Exactly one of 'config' or 'config_ref' must be provided."
            )
        return self

__all__ = ["CompletionPostRequest"]