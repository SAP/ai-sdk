from gen_ai_hub.orchestration.models.content_filter import ContentFilter, ContentFilterProvider


class LlamaGuard38bFilter(ContentFilter):
    """
    Specific implementation of ContentFilter for Llama Guard 3. Llama Guard 3 is a 
    Llama-3.1-8B pretrained model, fine-tuned for content safety classification.
    """

    def __init__(
            self,
            violent_crimes: bool = False,
            non_violent_crimes: bool = False,
            sex_crimes: bool = False,
            child_exploitation: bool = False,
            defamation: bool = False,
            specialized_advice: bool = False,
            privacy: bool = False,
            intellectual_property: bool = False,
            indiscriminate_weapons: bool = False,
            hate: bool = False,
            self_harm: bool = False,
            sexual_content: bool = False,
            elections: bool = False,
            code_interpreter_abuse: bool = False,
            **kwargs): # pylint: disable=too-many-arguments
        """Initializes the LlamaGuard38bFilter with specified content filtering options.

        :param violent_crimes: Responses that enable, encourage, or endorse the commission of violent crimes. 
            Defaults to False.
        :type violent_crimes: bool, optional
        :param non_violent_crimes: Responses that enable, encourage, or endorse the commission of non-violent crimes. 
            Defaults to False.
        :type non_violent_crimes: bool, optional
        :param sex_crimes: Responses that enable, encourage, or endorse the commission of sex-related crimes. 
            Defaults to False.
        :type sex_crimes: bool, optional
        :param child_exploitation: Responses that contain, describe, enable or endorse the sexual abuse of children. 
            Defaults to False.
        :type child_exploitation: bool, optional
        :param defamation: Responses that are both verifiably false and likely to injure a living person's reputation. 
            Defaults to False.
        :type defamation: bool, optional
        :param specialized_advice: Responses that contain specialized financial, medical or legal advice.
            Defaults to False.
        :type specialized_advice: bool, optional
        :param privacy: Responses that contain sensitive or nonpublic personal information. Defaults to False.
        :type privacy: bool, optional
        :param intellectual_property: Responses that may violate the intellectual property rights of any third party. 
            Defaults to False.
        :type intellectual_property: bool, optional
        :param indiscriminate_weapons: Responses that enable, encourage, or endorse the creation of indiscriminate 
            weapons. Defaults to False.
        :type indiscriminate_weapons: bool, optional
        :param hate: Responses that demean or dehumanize people on the basis of their sensitive, 
            personal characteristics. Defaults to False.
        :type hate: bool, optional
        :param self_harm: Responses that enable, encourage, or endorse acts of intentional self-harm. Defaults to False.
        :type self_harm: bool, optional
        :param sexual_content: Responses that contain erotica. Defaults to False.
        :type sexual_content: bool, optional
        :param elections: Responses that contain factually incorrect information about electoral systems and processes.
            Defaults to False.
        :type elections: bool, optional
        :param code_interpreter_abuse: Responses that seek to abuse code interpreters. Defaults to False.
        :type code_interpreter_abuse: bool, optional
        """

        super().__init__(
            provider=ContentFilterProvider.LLAMA_GUARD_3_8B,
            config={
                "violent_crimes": violent_crimes,
                "non_violent_crimes": non_violent_crimes,
                "sex_crimes": sex_crimes,
                "child_exploitation": child_exploitation,
                "defamation": defamation,
                "specialized_advice": specialized_advice,
                "privacy": privacy,
                "intellectual_property": intellectual_property,
                "indiscriminate_weapons": indiscriminate_weapons,
                "hate": hate,
                "self_harm": self_harm,
                "sexual_content": sexual_content,
                "elections": elections,
                "code_interpreter_abuse": code_interpreter_abuse,
                **kwargs
            }
        )
