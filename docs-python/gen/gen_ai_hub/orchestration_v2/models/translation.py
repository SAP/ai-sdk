"""
Translation module configuration models.
"""

from enum import Enum
from typing import Optional, Literal, Union

from pydantic import Field

from gen_ai_hub.orchestration_v2.models.base import ABCBaseModel as BaseModel


class TranslationType(str, Enum):
    """Enumerates supported translation types."""
    SAP_DOCUMENT_TRANSLATION = "sap_document_translation"


class TranslationConfig(BaseModel):
    """
    Configuration for sap_document_translation translation provider.

    Args:
        source_language: Language of the text to be translated. Example: de-DE

        target_language: Language to which the text should be translated. Example: en-US
    """

    source_language: Optional[str] = None
    target_language: str


class SAPDocumentTranslation(BaseModel):
    """
    Configuration for translation module.

    Args:
        type: The type of translation module (e.g., 'sap_document_translation').

        config: Configuration object for the translation module.
    """
    type_: TranslationType = Field(default=TranslationType.SAP_DOCUMENT_TRANSLATION, alias="type")
    config: TranslationConfig


class SAPDocumentTranslationApplyToSelector(BaseModel):
    """
    This selector allows you to define the scope of translation, such as specific placeholders or
    messages with specific roles.
    For example, {"category": "placeholders",
              "items": ["user_input"],
              "source_language": "de-DE"}
              targets the value of "user_input" in placeholder_values specified in the request payload;
              and considers the value to be in German.
    """
    category: Literal["placeholders", "template_roles"]
    items: list[str]
    source_language: str

class InputTranslationConfig(TranslationConfig):
    """
    Configuration for input translation.

    Args:
        source_language: Language of the text to be translated. Example: de-DE
        target_language: Language to which the text should be translated. Example: en-US
        apply_to: List of selectors that define the scope of translation.
    """
    apply_to: Optional[list[SAPDocumentTranslationApplyToSelector]] = None


class OutputTranslationConfig(TranslationConfig):
    target_language: Union[str, SAPDocumentTranslationApplyToSelector]


class SAPDocumentTranslationInput(SAPDocumentTranslation):
    """
    Configuration for input translation

    Args:
        type: The type of translation module (e.g., 'sap_document_translation').

        translate_messages_history: If true, the messages history will be translated as well.

        config: Configuration object for the translation module.
    """
    translate_messages_history: Optional[bool] = None
    config: Union[InputTranslationConfig, TranslationConfig]

class SAPDocumentTranslationOutput(SAPDocumentTranslation):
    """
    Configuration for output translation

    Args:
        type: The type of translation module (e.g., 'sap_document_translation').

        config: Configuration object for the translation module.
    """
    config: Union[OutputTranslationConfig, TranslationConfig]

class TranslationModuleConfig(BaseModel):
    """
    Configuration for translation module

    Args:
        input: Configuration for input translation

        output: Configuration for output translation
    """
    input: Optional[Union[SAPDocumentTranslationInput, SAPDocumentTranslation]] = None
    output: Optional[Union[SAPDocumentTranslationOutput, SAPDocumentTranslation]] = None

__al__ = ["TranslationType", "TranslationConfig", "SAPDocumentTranslation", "SAPDocumentTranslationApplyToSelector",
          "InputTranslationConfig", "OutputTranslationConfig", "SAPDocumentTranslationInput",
          "SAPDocumentTranslationOutput", "TranslationModuleConfig"]