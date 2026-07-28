import re
from enum import Enum
from typing import Optional

from gen_ai_hub.orchestration.models.base import JSONSerializable


class ResponseFormatType(str, Enum):
    """
    Enumerates the supported response format.

    Response format that the model output should adhere to. This is the same as the OpenAI definition.

    Values:
        TEXT: Response format as text
        JSON_OBJECT: Response format as json object
        JSON_SCHEMA: Response format as defined json schema
    """
    TEXT = "text"
    JSON_OBJECT = "json_object"
    JSON_SCHEMA = "json_schema"


class ResponseFormatText(JSONSerializable):
    """
    Response format that the model output should adhere to. 
    """

    def to_dict(self):
        """Converts the ResponseFormatText instance to a dictionary.

        :return: A dictionary representation of the ResponseFormatText.
        :rtype: dict
        """
        return {"type": ResponseFormatType.TEXT}


class ResponseFormatJsonObject(JSONSerializable):
    """
    Response format JSON Object that the model output should adhere to.
    """

    def to_dict(self):
        """Converts the ResponseFormatJsonObject instance to a dictionary.

        :return: A dictionary representation of the ResponseFormatJsonObject.
        :rtype: dict
        """
        return {"type": ResponseFormatType.JSON_OBJECT}


class ResponseFormatJsonSchema(JSONSerializable):
    """
    Response format JSON Schema that the model output should adhere to.
    """

    def __init__(
            self,
            name,
            schema: object = None,
            description: Optional[str] = None,
            strict: bool = False
    ):
        """Initializes a ResponseFormatJsonSchema instance.

        :param name: the name of the response format.
        :type name: str
        :param schema: the schema for the response format described as a JSON Schema object, defaults to None
        :type schema: object, optional
        :param description: A description of what the response format is for, defaults to None
        :type description: Optional[str], optional
        :param strict: Whether to enable strict schema adherence when generating the output, defaults to False
        :type strict: bool, optional
        """
        self.name = Validator.validate_name(name)
        self.desciption = description
        self.schema = schema
        self.strict = strict

    def to_dict(self):
        """Converts the ResponseFormatJsonSchema instance to a dictionary.

        :return: A dictionary representation of the ResponseFormatJsonSchema.
        :rtype: dict
        """
        json_schema = {
                "name": self.name,
                "strict": self.strict,
                "schema": self.schema
        }
        if self.desciption:
            json_schema['description'] = self.desciption
        return {
            "type": ResponseFormatType.JSON_SCHEMA,
            "json_schema": json_schema
        }


class ResponseFormatFactory():
    """
    Factory class that maps response format input to classes that can handle to_dict conversion.
    """
    @staticmethod
    def create_response_format_object(response_format):
        """Creates a response format object based on the provided response format.

        :param response_format: The response format input.
        :type response_format: Union[ResponseFormatType, ResponseFormatJsonSchema]
        :return: An instance of the corresponding response format class.
        :rtype: Optional[JSONSerializable]
        """
        if response_format == ResponseFormatType.TEXT:
            return ResponseFormatText()

        if response_format == ResponseFormatType.JSON_OBJECT:
            return ResponseFormatJsonObject()

        if isinstance(response_format, ResponseFormatJsonSchema):
            return response_format
        
        return None

 
class Validator():
    """
    A utility class for validating response format names.

    This class provides methods to validate the names of response formats to ensure 
    they adhere to specified patterns and length constraints.
    """
    @staticmethod
    def validate_name(name):
        """Validates the name of the response format.

        :param name: The name to validate.
        :type name: str
        :raises ValueError: If the name does not match the required pattern or exceeds the maximum length.
        :return: The validated name.
        :rtype: str
        """
        pattern = r'^[a-zA-Z0-9_-]+$'
        if re.match(pattern, name):
            if len(name) > 64:
                raise ValueError("The name of the response format must be a-z, A-Z, 0-9, "
                                 "or contain underscores and dashes, with a maximum length of 64.")
        else:
            raise ValueError("The name of the response format must be a-z, A-Z, 0-9, "
                             "or contain underscores and dashes, with a maximum length of 64.")

        return name
    