from typing import List, Optional

from gen_ai_hub.orchestration.models.base import JSONSerializable
from gen_ai_hub.orchestration.models.content_filter import ContentFilter


class InputFiltering(JSONSerializable):
    """Module for managing and applying input content filters."""

    def __init__(
            self,
            filters: List[ContentFilter]
    ):
        """Initializes the InputFiltering with specified filters.

        :param filters: List of ContentFilter objects to be applied to input content.
        :type filters: List[ContentFilter]
        """
        self.filters = filters

    def to_dict(self):
        """to_dict method to convert the input filtering configuration to a dictionary.

        :return: dictionary representation of the input filtering configuration.
        :rtype: dict
        """
        return {
            "filters": [f.to_dict() for f in self.filters],
        }


class OutputFiltering(JSONSerializable):
    """Module for managing and applying output content filters."""

    def __init__(self,
                 filters: List[ContentFilter],
                 stream_options: Optional[dict] = None
                 ):
        """Initializes the OutputFiltering with specified filters and optional streaming options.

        :param filters: List of ContentFilter objects to be applied to output content.
        :type filters: List[ContentFilter]
        :param stream_options: Module-specific streaming options, defaults to None
        :type stream_options: Optional[dict], optional
        """
        self.filters = filters
        self.stream_options = stream_options

    def to_dict(self):
        """to_dict method to convert the output filtering configuration to a dictionary.

        :return: dictionary representation of the output filtering configuration.
        :rtype: dict
        """

        config = {
            "filters": [f.to_dict() for f in self.filters],
        }

        if self.stream_options:
            config["stream_options"] = self.stream_options

        return config

class ContentFiltering(JSONSerializable):
    """Module for managing and applying content filters."""

    def __init__(
            self,
            input_filtering: Optional[InputFiltering] = None,
            output_filtering: Optional[OutputFiltering] = None
    ):
        """Initializes the ContentFiltering with optional input and output filtering configurations.

        :param input_filtering: the configuration for input filtering, defaults to None
        :type input_filtering: Optional[InputFiltering], optional
        :param output_filtering: the configuration for output filtering, defaults to None
        :type output_filtering: Optional[OutputFiltering], optional
        """
        self.input_filtering = input_filtering
        self.output_filtering = output_filtering

    def to_dict(self):
        """to_dict method to convert the content filtering configuration to a dictionary.

        :return: dictionary representation of the content filtering configuration.
        :rtype: dict
        """
        config = {}
        if self.input_filtering:
            config["input"] = self.input_filtering.to_dict()
        if self.output_filtering:
            config["output"] = self.output_filtering.to_dict()

        return config
