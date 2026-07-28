"""
Azure Content Filter Model
"""

from enum import Enum
from typing import Union, Literal, Optional

from gen_ai_hub.orchestration_v2.models.base import ABCBaseModel as BaseModel


class AzureThreshold(int, Enum):
    """
    Enumerates the threshold levels for the Azure Content Safety service.

    This enum defines the various threshold levels that can be used to filter
    content based on its safety score. Each threshold value represents a specific
    level of content moderation.

    Values:
        ALLOW_SAFE: Allows only Safe content.
        ALLOW_SAFE_LOW: Allows Safe and Low content.
        ALLOW_SAFE_LOW_MEDIUM: Allows Safe, Low, and Medium content.
        ALLOW_ALL: Allows all content (Safe, Low, Medium, and High).
    """

    ALLOW_SAFE = 0
    ALLOW_SAFE_LOW = 2
    ALLOW_SAFE_LOW_MEDIUM = 4
    ALLOW_ALL = 6


class AzureContentFilter(BaseModel):
    """
    Specific filter configuration for Azure Content Safety.

    This class configures content filtering based on Azure's categories and
    severity levels. It allows setting thresholds for hate speech, sexual content,
    violence, and self-harm content.

    Args:
        hate: Threshold for hate speech content.
        sexual: Threshold for sexual content.
        violence: Threshold for violent content.
        self_harm: Threshold for self-harm content.
        prompt_shield: A flag to use prompt shield
    """

    hate: Optional[Union[AzureThreshold, Literal[0, 2, 4, 6]]] = None
    sexual: Optional[Union[AzureThreshold, Literal[0, 2, 4, 6]]] = None
    violence: Optional[Union[AzureThreshold, Literal[0, 2, 4, 6]]] = None
    self_harm: Optional[Union[AzureThreshold, Literal[0, 2, 4, 6]]] = None

class AzureContentSafetyInput(AzureContentFilter):
    """
    Filter configuration for Azure Content Safety Input

    Args:
            hate: Threshold for hate speech content.
            sexual: Threshold for sexual content.
            violence: Threshold for violent content.
            self_harm: Threshold for self-harm content.
            prompt_shield: A flag to use prompt shield
        """
    prompt_shield: Optional[bool] = False


class AzureContentSafetyOutput(AzureContentFilter):
    """
    Filter configuration for Azure Content Safety Output

    Args:
        hate: Threshold for hate speech content.
        sexual: Threshold for sexual content.
        violence: Threshold for violent content.
        self_harm: Threshold for self-harm content.
        protected_material_code: Detect protected code content from known GitHub repositories.
                    The scan includes software libraries, source code, algorithms,
                    and other proprietary programming content.
    """

    protected_material_code: Optional[bool] = False

__all__ = ["AzureContentFilter", "AzureContentSafetyInput", "AzureContentSafetyOutput", "AzureThreshold"]