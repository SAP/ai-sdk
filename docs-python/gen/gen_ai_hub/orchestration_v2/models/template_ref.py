"""
Module for template reference models.
"""
from typing import Literal, Optional
from gen_ai_hub.orchestration_v2.models.base import ABCBaseModel as BaseModel


class TemplateRefByID(BaseModel):
    """
    Represents a prompt template reference for generating prompts or conversations.
    Args:
        id(str): ID of the template in prompt registry
        scope(Optional[Literal["resource_group", "tenant"]]): Defines the scope that is searched
            for the referenced template. 'tenant' indicates the template is shared across all
            resource groups within the tenant, while 'resource_group' indicates the template is
            only accessible within the specific resource group. Defaults to 'tenant'.
    """
    id: str
    scope: Optional[Literal["resource_group", "tenant"]] = "tenant"


class TemplateRefByScenarioNameVersion(BaseModel):
    """
        Represents a prompt template reference for generating prompts or conversations.
        Args:
            scenario(str): Scenario name

            name(str): Name of template

            version(str): Version of template

            scope(Optional[Literal["resource_group", "tenant"]]): Defines the scope that is searched
                for the referenced template. 'tenant' indicates the template is shared across all
                resource groups within the tenant, while 'resource_group' indicates the template is
                only accessible within the specific resource group. Defaults to 'tenant'.
        """
    scenario: str
    name: str
    version: str
    scope: Optional[Literal["resource_group", "tenant"]] = "tenant"


class TemplateRef(BaseModel):
    template_ref: TemplateRefByID | TemplateRefByScenarioNameVersion

__all__ = ["TemplateRef", "TemplateRefByID", "TemplateRefByScenarioNameVersion"]