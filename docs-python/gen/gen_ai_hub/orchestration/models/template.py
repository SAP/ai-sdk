from typing import List, Optional, Union, NamedTuple, Dict, Any

from gen_ai_hub.orchestration.models.base import JSONSerializable
from gen_ai_hub.orchestration.models.message import Message
from gen_ai_hub.orchestration.models.response_format import (
    ResponseFormatType,
    ResponseFormatJsonSchema,
    ResponseFormatFactory
)
from gen_ai_hub.orchestration.models.tools import ChatCompletionTool


class TemplateValue(NamedTuple):
    """
    Represents a named value for use in template substitution.

    This class pairs a name with a corresponding value, which can be a string,
    integer, or float. It's designed to be used in template rendering processes
    where named placeholders are replaced with specific values.
    """

    name: str
    """The identifier for this template value."""
    value: Union[str, int, float]
    """The actual value to be used in substitution."""

class Template(JSONSerializable):
    """
    Represents a configurable template for generating prompts or conversations.
    """

    def __init__(
        self,
        messages: List[Message],
        defaults: Optional[List[TemplateValue]] = None,
        tools: Optional[List[Union[dict, ChatCompletionTool]]] = None,
        response_format: Optional[Union[
            ResponseFormatType.TEXT,
            ResponseFormatType.JSON_OBJECT,
            ResponseFormatJsonSchema
        ]] = None,
    ):
        """Initializes a Template instance.

        :param messages: list of prompt messages that form the template._
        :type messages: List[Message]
        :param defaults: list of default values for template variables, defaults to None
        :type defaults: Optional[List[TemplateValue]], optional
        :param tools: list of tool definitions, defaults to None
        :type tools: Optional[List[Union[dict, ChatCompletionTool]]], optional
        :param response_format: response format that the model output should adhere to, defaults to None
        :type response_format: Optional[Union[ ResponseFormatType.TEXT, 
            ResponseFormatType.JSON_OBJECT, ResponseFormatJsonSchema ]], optional
        """
        self.messages = messages
        self.defaults = defaults or []
        self.tools = tools or []
        self.response_format = response_format

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Template instance to a dictionary representation.
            Serializes the template to a dictionary, converting tools as needed.

        :raises ValueError: If an invalid tool is encountered in the tools list.
        :return: A dictionary representation of the Template instance.
        :rtype: Dict[str, Any]
        """

        template_dict: Dict[str, Any] = {
            "template": [message.to_dict() for message in self.messages],
            "defaults": {default.name: default.value for default in self.defaults},
        }

        if self.tools:
            tool_dicts = []
            for idx, tool in enumerate(self.tools):
                if isinstance(tool, ChatCompletionTool):
                    tool_dicts.append(tool.to_dict())
                elif isinstance(tool, dict):
                    tool_dicts.append(tool)
                else:
                    raise ValueError(
                        f"Invalid tool at index {idx}: {tool!r} (type: {type(tool).__name__}). "
                        "If you are passing a function, decorate it with @function_tool."
                    )
            template_dict["tools"] = tool_dicts

        if self.response_format:
            template_dict["response_format"] = (
                ResponseFormatFactory.create_response_format_object(
                    self.response_format
                ).to_dict()
            )

        return template_dict
