from typing import List, Optional, Dict, Any
from pydantic.config import ConfigDict

from pydantic import BaseModel, Field, field_validator
from gen_ai_hub.orchestration_v2 import (ResponseFormatText, ResponseFormatJsonObject, ResponseFormatJsonSchema,
                                         FunctionTool, ImagePart, TextPart, ImageItem, ImageUrl, ContentPart)


class PromptTemplate(BaseModel):
    """
    Represents a prompt template.

    Args:
        role: The role of the prompt template.

        content: The content of the prompt template.
    """

    role: str
    """The role of the prompt template."""
    content: str  | List[str| ContentPart| ImageItem]
    """The content of the prompt template."""

    @field_validator("content", mode="before")
    def content_validation(cls, content):  # pylint: disable=no-self-argument
        """
        Validates and maps the content field to the appropriate types.
        """

        mapped_content = []

        if isinstance(content, str):
            mapped_content = content
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, (ContentPart, dict)):
                    mapped_content.append(item)
                elif isinstance(item, str):
                    mapped_content.append(TextPart(text=item))
                elif isinstance(item, ImageItem):
                    mapped_content.append(ImagePart(image_url=ImageUrl(url=item.url, detail=item.detail)))
                else:
                    raise ValueError("Prompt template content list must contain only "
                                     "str, ImageItem, TextPart, or ImagePart objects")
        else:
            raise ValueError("Prompt template content must be a str or list of "
                             "str, ImageItem, TextPart, or ImagePart objects")
        return mapped_content



class PromptTemplateSpec(BaseModel):
    """
    Represents a prompt template specification.

    Args:
        Args:
        template: A list of prompt messages that form the template.

        defaults: A dict of default values for template variables.

        tools: A list of tool definitions.

        response_format: A response format that the model output should adhere to.

        additional_fields: Additional fields for the prompt template.
    """
    template: List[PromptTemplate]
    defaults: Optional[dict] = None
    response_format: Optional[ResponseFormatText | ResponseFormatJsonObject | ResponseFormatJsonSchema] = None
    tools: Optional[List[dict | FunctionTool]] = None
    additional_fields: Optional[Dict[Any, Any]] = Field(default_factory=dict)


class PromptTemplatePostRequest(BaseModel):
    """
    Represents a request to create a prompt template.

    Args:
        name: The name of the prompt template.

        version: The version of the prompt template.

        scenario: The scenario of the prompt template.

        spec: The specification of the prompt template.
    """
    name: str
    """The name of the prompt template."""
    version: str
    """The version of the prompt template."""
    scenario: str
    """The scenario of the prompt template."""
    spec: PromptTemplateSpec
    """The specification of the prompt template."""


class PromptTemplatePostResponse(BaseModel):
    """
    Represents a response to a request to create a prompt template.

    Args:
        message: The message of the response.

        id: The ID of the prompt template.

        scenario: The scenario of the prompt template.

        name: The name of the prompt template.

        version: The version of the prompt template.
    """
    message: str
    """The message of the response."""
    id: str
    """The ID of the prompt template."""
    scenario: str
    """The scenario of the prompt template."""
    name: str
    """The name of the prompt template."""
    version: str
    """The version of the prompt template."""


class PromptTemplateGetResponse(BaseModel):
    """
    Represents a response to a request to get a prompt template.

    Args:
        id: The ID of the prompt template.

        name: The name of the prompt template.

        version: The version of the prompt template.

        scenario: The scenario of the prompt template.

        creation_timestamp: The creation timestamp of the prompt template.

        managed_by: The manager of the prompt template.

        is_version_head: Whether the version is the head version.

        spec: The specification of the prompt template.
    """
    id: str
    """The ID of the prompt template."""
    name: str
    """The name of the prompt template."""
    version: str
    """The version of the prompt template."""
    scenario: str
    """The scenario of the prompt template."""
    creation_timestamp: Optional[str] = None
    """The creation timestamp of the prompt template."""
    managed_by: Optional[str] = None
    """The manager of the prompt template."""
    is_version_head: Optional[bool] = None
    """Whether the version is the head version."""
    spec: Optional[PromptTemplateSpec] = None
    """The specification of the prompt template."""


class PromptTemplateListResponse(BaseModel):
    """
    Represents a response to a request to list prompt templates.

    Args:
        count: The number of prompt templates.

        resources: The list of PromptGetResponse objects.
    """
    count: int
    """The number of prompt templates."""
    resources: List[PromptTemplateGetResponse]
    """The list of PromptGetResponse objects."""


class PromptTemplateDeleteResponse(BaseModel):
    """
    Represents a response to a request to delete a prompt template.

    Args:
        message: The message of the response.
    """
    message: str
    """The message of the response."""


class PromptTemplateSubstitutionRequest(BaseModel):
    """
    Represents a request to substitute a prompt template.

    Args:
        input_params: User provided values to replace the placeholders of the prompt template.
    """
    model_config = ConfigDict(populate_by_name=True)
    """Pydantic configuration to allow population by field name."""
    input_params: Optional[Dict[Any, Any]] = Field(default_factory=dict, alias='inputParams')
    """User provided values to replace the placeholders of the prompt template."""


class PromptTemplateSubstitutionResponse(BaseModel):
    """
    Represents a response to a request to substitute a prompt template.

    Args:
        parsed_prompt: The parsed prompt.

        resource: List of TemplateGetResponse objects.
    """
    parsed_prompt: List[PromptTemplate]
    """The parsed prompt."""
    resource: Optional[PromptTemplateGetResponse] = None
    """List of TemplateGetResponse objects."""
