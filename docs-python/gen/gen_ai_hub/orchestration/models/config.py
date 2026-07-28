from typing import Optional, Union

from gen_ai_hub.orchestration.models.base import JSONSerializable
from gen_ai_hub.orchestration.models.content_filtering import ContentFiltering
from gen_ai_hub.orchestration.models.data_masking import DataMasking
from gen_ai_hub.orchestration.models.document_grounding import GroundingModule
from gen_ai_hub.orchestration.models.llm import LLM
from gen_ai_hub.orchestration.models.template import Template
from gen_ai_hub.orchestration.models.template_ref import TemplateRef
from gen_ai_hub.orchestration.models.translation.translation import Translation


class OrchestrationConfig(JSONSerializable):
    """
    Configuration for the Orchestration Service's content generation process.

    Defines modules for a harmonized API that combines LLM-based content generation
    with additional processing functionalities.

    The orchestration service allows for advanced content generation by processing inputs through a series of steps:
    template rendering, text generation via LLMs, and optional input/output transformations such as data masking
    or filtering.
    """

    def __init__(
            self,
            template: Union[Template, TemplateRef],
            llm: LLM,
            filtering: Optional[ContentFiltering] = None,
            data_masking: Optional[DataMasking] = None,
            grounding: Optional[GroundingModule] = None,
            stream_options: Optional[dict] = None,
            translation: Optional[Translation] = None,
    ):
        """Initializes the OrchestrationConfig with specified modules.

        :param template: template for rendering input prompts
        :type template: Union[Template, TemplateRef]
        :param llm: language model for text generation
        :type llm: LLM
        :param filtering: content filtering module, defaults to None
        :type filtering: Optional[ContentFiltering], optional
        :param data_masking: data masking module, defaults to None
        :type data_masking: Optional[DataMasking], optional
        :param grounding: document grounding module, defaults to None
        :type grounding: Optional[GroundingModule], optional
        :param stream_options: global streaming options, defaults to None
        :type stream_options: Optional[dict], optional
        :param translation: translation module, defaults to None
        :type translation: Optional[Translation], optional
        """

        self.template = template
        self.llm = llm
        self.filtering = filtering
        self.data_masking = data_masking
        self.grounding = grounding
        self.stream_options = stream_options
        self._stream = False
        self.translation = translation

    def _get_module_configurations(self):
        configs = {
            "templating_module_config": self.template.to_dict(),
            "llm_module_config": self.llm.to_dict(),
        }

        if self.data_masking:
            configs["masking_module_config"] = self.data_masking.to_dict()

        if self.filtering:
            configs["filtering_module_config"] = self.filtering.to_dict()

        if self.grounding:
            configs["grounding_module_config"] = self.grounding.to_dict()

        if self.translation:
            if self.translation.input_translation:
                configs["input_translation_module_config"] = self.translation.input_translation.to_dict()
            if self.translation.output_translation:
                configs["output_translation_module_config"] = self.translation.output_translation.to_dict()

        return configs

    def to_dict(self):
        """Converts the orchestration configuration to a dictionary format.

        :return: dictionary representation of the orchestration configuration.
        :rtype: dict
        """

        config = {
            "module_configurations": self._get_module_configurations(),
            **({"stream": True} if self._stream else {}),
            **({"stream_options": self.stream_options} if self._stream and self.stream_options else {})
        }

        return config
