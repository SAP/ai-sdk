from gen_ai_hub.orchestration.models.base import JSONSerializable


class TemplateRef(JSONSerializable):
    """
    Represents a prompt template reference for generating prompts or conversations.

    This is a factory class for creating a reference to a prompt template.
    It is used to reference a template by id, or the tuple: scenario, name, version

    """

    def __init__(self, **kwargs):
        """Initializes a TemplateRef instance with dynamic attributes."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_id(
            cls,
            prompt_template_id: str
    ):
        """Creates a TemplateRef instance from a prompt template ID.

        :param prompt_template_id: The ID of the prompt template.
        :type prompt_template_id: str
        :return: A TemplateRef instance with the specified ID.
        :rtype: TemplateRef
        """
        return cls(id=prompt_template_id)

    @classmethod
    def from_tuple(
            cls,
            scenario: str,
            name: str,
            version: str
    ):
        """Creates a TemplateRef instance from a scenario, name, and version.

        :param scenario: The scenario of the prompt template.
        :type scenario: str
        :param name: The name of the prompt template.
        :type name: str
        :param version: The version of the prompt template.
        :type version: str
        :return: A TemplateRef instance with the specified scenario, name, and version.
        :rtype: TemplateRef
        """
        return cls(scenario=scenario, name=name, version=version)

    def to_dict(self):
        """Converts the TemplateRef instance to a dictionary representation.

        :return: A dictionary representation of the TemplateRef instance.
        :rtype: dict
        """
        template_ref = {}
        for key, value in self.__dict__.items():
            template_ref[key] = value
        return { "template_ref": template_ref }
