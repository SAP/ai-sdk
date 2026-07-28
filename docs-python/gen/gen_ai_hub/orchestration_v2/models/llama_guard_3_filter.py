"""
Llama Guard 3 Content Filter Model
"""

from gen_ai_hub.orchestration_v2.models.base import ABCBaseModel as BaseModel


class LlamaGuard38bFilter(BaseModel):
    """
    Specific implementation of ContentFilter for Llama Guard 3. Llama Guard 3 is a 
    Llama-3.1-8B pretrained model, fine-tuned for content safety classification.

    Args:
        violent_crimes: Responses that enable, encourage, or endorse the commission of violent crimes.

        non_violent_crimes: Responses that enable, encourage, or endorse the commission of non-violent crimes.

        sex_crimes: Responses that enable, encourage, or endorse the commission of sex-related crimes.

        child_exploitation: Responses that contain, describe, enable or endorse the sexual abuse of children.

        defamation: Responses that are both verifiably false and likely to injure a living person's reputation.

        specialized_advice: Responses that contain specialized financial, medical or legal advice.

        privacy: Responses that contain sensitive or nonpublic personal information.

        intellectual_property: Responses that may violate the intellectual property rights of any third party.

        indiscriminate_weapons: Responses that enable, encourage, or endorse the creation of indiscriminate weapons.

        hate: Responses that demean or dehumanize people on the basis of their sensitive, personal characteristics.

        self_harm: Responses that enable, encourage, or endorse acts of intentional self-harm.

        sexual_content: Responses that contain erotica.

        elections: Responses that contain factually incorrect information about electoral systems and processes.

        code_interpreter_abuse: Responses that seek to abuse code interpreters.
    """

    violent_crimes: bool = False
    non_violent_crimes: bool = False
    sex_crimes: bool = False
    child_exploitation: bool = False
    defamation: bool = False
    specialized_advice: bool = False
    privacy: bool = False
    intellectual_property: bool = False
    indiscriminate_weapons: bool = False
    hate: bool = False
    self_harm: bool = False
    sexual_content: bool = False
    elections: bool = False
    code_interpreter_abuse: bool = False

__all__ = ["LlamaGuard38bFilter"]