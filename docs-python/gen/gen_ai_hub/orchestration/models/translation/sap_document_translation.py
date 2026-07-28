from gen_ai_hub.orchestration.models.translation.translation import Translation
from gen_ai_hub.orchestration.models.translation.translation import InputTranslationModule, \
    InputTranslationConfig, OutputTranslationModule, OutputTranslationConfig, TranslationType


class SAPDocumentTranslation(Translation):
    """SAPTranslationHub represents the translation service provided by SAP."""

    def __init__(self, input_translation_config: InputTranslationConfig = None,
                 output_translation_config: OutputTranslationConfig = None):
        """Initializes the SAPDocumentTranslation with optional input and output translation configurations.

        :param input_translation_config: the configuration for input translation, defaults to None
        :type input_translation_config: InputTranslationConfig, optional
        :param output_translation_config: the configuration for output translation, defaults to None
        :type output_translation_config: OutputTranslationConfig, optional
        """

        input_translation_module = None
        output_translation_module = None

        if input_translation_config is not None:
            input_translation_module = InputTranslationModule(
                type=TranslationType.SAP_DOCUMENT_TRANSLATION,
                config=input_translation_config
            )

        if output_translation_config is not None:
            output_translation_module = OutputTranslationModule(
                type=TranslationType.SAP_DOCUMENT_TRANSLATION,
                config=output_translation_config
            )
        super().__init__(input_translation=input_translation_module,
                         output_translation=output_translation_module)
