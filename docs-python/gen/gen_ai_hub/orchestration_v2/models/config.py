"""
Orchestration Service configuration models.
"""

from typing import Annotated, List, Optional

from pydantic import Field

from gen_ai_hub.orchestration_v2.models.base import ABCBaseModel as BaseModel
from gen_ai_hub.orchestration_v2.models.content_filtering import FilteringModuleConfig
from gen_ai_hub.orchestration_v2.models.data_masking import MaskingModuleConfig
from gen_ai_hub.orchestration_v2.models.document_grounding import GroundingModuleConfig
from gen_ai_hub.orchestration_v2.models.streaming import GlobalStreamOptions
from gen_ai_hub.orchestration_v2.models.template import PromptTemplatingModuleConfig
from gen_ai_hub.orchestration_v2.models.translation import TranslationModuleConfig


class ModuleConfig(BaseModel):
    """
    Configuration for the Orchestration Service's content generation process.

    Defines modules for a harmonized API that combines LLM-based content generation
    with additional processing functionalities.

    The orchestration service allows for advanced content generation by processing inputs through a series of steps:
    template rendering, text generation via LLMs, and optional input/output transformations such as data masking
    or filtering.

    Args:
        prompt_templating: Template object for rendering input prompts and language model for text generation.

        filtering: Module for filtering and validating input/output content.

        masking: Module for anonymizing or pseudonymizing sensitive information.

        grounding: Module for document grounding.

        translation: Module for translating input and output content.
    """

    prompt_templating: PromptTemplatingModuleConfig
    filtering: Optional[FilteringModuleConfig] = None
    masking: Optional[MaskingModuleConfig] = None
    grounding: Optional[GroundingModuleConfig] = None
    translation: Optional[TranslationModuleConfig] = None


class OrchestrationConfig(BaseModel):
    """
    Configuration for the Orchestration Service's content generation process.
    
    Args:
        modules: Either a single ModuleConfig or a list of ModuleConfigs. When a list is provided,
        the orchestration service will try each configuration in order until one succeeds.

        stream: Optional streaming configuration.
    """
    modules: ModuleConfig | Annotated[List[ModuleConfig], Field(min_length=1)]
    stream: Optional[GlobalStreamOptions] = None


class CompletionRequestConfigurationReferenceByIdConfigRef(BaseModel):
    """Represents a reference to an orchestration config identified by a unique ID.

    Args:
        id (str): The unique identifier for the configuration.
    """
    id: str

class CompletionRequestConfigurationReferenceByNameScenarioVersionConfigRef(BaseModel):
    """
    Represents a reference to aan orchestration config identified by name, scenario, and version.

    Args:
        scenario(str): Scenario name

        name(str): Name of config

        version(str): Version of config
    """
    scenario: str
    name: str
    version: str

OrchestrationConfigReference = (CompletionRequestConfigurationReferenceByIdConfigRef |
                                CompletionRequestConfigurationReferenceByNameScenarioVersionConfigRef)

__all__ = ["ModuleConfig", "OrchestrationConfig", "OrchestrationConfigReference",
           "CompletionRequestConfigurationReferenceByIdConfigRef",
           "CompletionRequestConfigurationReferenceByNameScenarioVersionConfigRef"]