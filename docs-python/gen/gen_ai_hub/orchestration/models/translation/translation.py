from gen_ai_hub.orchestration.models.base import JSONSerializable
from enum import Enum


class TranslationType(str, Enum):
    """Enumerates supported translation types."""
    SAP_DOCUMENT_TRANSLATION = "sap_document_translation"


class InputTranslationConfig(JSONSerializable):
    """Configuration for input translation. These parameters are specific to SAP Translation Hub."""

    def __init__(self, source_language: str, target_language: str):
        """Initializes the InputTranslationConfig with source and target languages.

        :param source_language: the source language code (e.g., 'de-DE' for German).
        :type source_language: str
        :param target_language: the target language code (e.g., 'en-US' for US English).
        :type target_language: str
        """
  
        self.source_language = source_language
        self.target_language = target_language

    def to_dict(self):
        """to_dict method to convert the configuration to a dictionary.

        :return: dictionary representation of the configuration.
        :rtype: dict
        """

        return {
            "source_language": self.source_language,
            "target_language": self.target_language
        }


class InputTranslationModule(JSONSerializable):
    """Configuration for input translation module.

    :param JSONSerializable: _description_
    :type JSONSerializable: _type_
    :return: _description_
    :rtype: _type_
    """

    def __init__(self, type: str, config: InputTranslationConfig):
        """Initializes the InputTranslationModule with type and configuration.

        :param type: The type of translation module (e.g., 'sap_document_translation').
        :type type: str
        :param config: Configuration object for the translation module.
        :type config: InputTranslationConfig
        """

        self.type = type
        self.config = config

    def to_dict(self):
        """to_dict method to convert the module to a dictionary.

        :return: dictionary representation of the module.
        :rtype: dict
        """
        return {
            "type": self.type,
            "config": self.config.to_dict()
        }


class OutputTranslationConfig(JSONSerializable):
    """Configuration for output translation.

    :param JSONSerializable: _description_
    :type JSONSerializable: _type_
    :return: _description_
    :rtype: _type_
    """

    def __init__(self, target_language: str, source_language: str = None):
        """Initializes the OutputTranslationConfig with target and optional source languages. These parameters are specific to SAP Translation Hub.

        :param target_language: the target language code (e.g., 'en-US' for US English).
        :type target_language: str
        :param source_language: the source language code (e.g., 'de-DE' for German), defaults to None
        :type source_language: str, optional
        """
        self.target_language = target_language
        self.source_language = source_language

    def to_dict(self):
        """to_dict method to convert the configuration to a dictionary.
        :return: dictionary representation of the configuration.
        :rtype: dict
        """

        return {
            "target_language": self.target_language,
            "source_language": self.source_language
        }


class OutputTranslationModule(JSONSerializable):
    """Configuration for output translation module."""

    def __init__(self, type: str, config: OutputTranslationConfig):
        """Initializes the OutputTranslationModule with type and configuration.

        :param type: The type of translation module (e.g., 'sap_document_translation').
        :type type: str
        :param config: Configuration object for the translation module.
        :type config: OutputTranslationConfig
        """

        self.type = type
        self.config = config

    def to_dict(self):
        """to_dict method to convert the module to a dictionary.
        :return: dictionary representation of the module.
        :rtype: dict
        """

        return {
            "type": self.type,
            "config": self.config.to_dict()
        }


class Translation:
    """Translation module for managing input and output translations."""

    def __init__(self, input_translation: InputTranslationModule = None,
                 output_translation: OutputTranslationModule = None):
        """Initializes the Translation module with optional input and output translation configurations.

        :param input_translation: the configuration for input translation, defaults to None
        :type input_translation: InputTranslationModule, optional
        :param output_translation: the configuration for output translation, defaults to None
        :type output_translation: OutputTranslationModule, optional
        """
        self.input_translation = input_translation
        self.output_translation = output_translation
