"""
Response format models for model output specification.
"""

import re
from enum import Enum
from typing import Optional

from pydantic import Field, field_validator

from gen_ai_hub.orchestration_v2.models.base import ABCBaseModel as BaseModel


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


class ResponseFormatText(BaseModel):
    """
    Response format that the model output should adhere to. 
    """
    type_: ResponseFormatType = Field(default=ResponseFormatType.TEXT, alias="type")


class ResponseFormatJsonObject(BaseModel):
    """
    Response format JSON Object that the model output should adhere to.
    """
    type_: ResponseFormatType = Field(default=ResponseFormatType.JSON_OBJECT, alias="type")


class JSONResponseSchema(BaseModel):
    """
        Response format JSON Schema that the model output should adhere to.

        Args:
            name: The name of the response format.

            description: A description of what the response format is for.

            schema: A schema for the response format described as a JSON Schema object.

            strict: Whether to enable strict schema adherence when generating the output.
    """
    name: str
    description: Optional[str] = None
    schema_: dict = Field(default_factory=dict,
                          alias="schema",
                          description="The schema for the response format, described as a JSON Schema object.")
    strict: bool = False

    @field_validator("name", mode="before")
    def validate_name(cls, name):  # pylint: disable=no-self-argument
        """validates the name of the response format.

        :param name: the name to validate
        :type name: str
        :raises ValueError: if the name does not match the required pattern or exceeds the maximum length
        :return: the validated name
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


class ResponseFormatJsonSchema(BaseModel):
    type_: ResponseFormatType = Field(default=ResponseFormatType.JSON_SCHEMA, alias="type")
    json_schema: JSONResponseSchema

__all__ = ["ResponseFormatType", "ResponseFormatText", "ResponseFormatJsonObject", "ResponseFormatJsonSchema",
           "JSONResponseSchema"]