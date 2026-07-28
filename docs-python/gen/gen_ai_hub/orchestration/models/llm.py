from typing import Optional, Dict

from gen_ai_hub.orchestration.models.base import JSONSerializable


class LLM(JSONSerializable):
    """
    Represents a Large Language Model (LLM) configuration.

    This class encapsulates the details required to specify and configure a particular
    LLM for use in natural language processing tasks. It includes the model's name,
    version, and any additional parameters needed for its operation.
    """

    def __init__(
        self,
        name: str,
        version: str = "latest",
        parameters: Optional[Dict] = None,
    ):
        """Initializes the LLM with specified name, version, and parameters.

        :param name: Name of the LLM.
        :type name: str
        :param version: Version of the LLM, defaults to "latest"
        :type version: str, optional
        :param parameters: Additional parameters for the LLM, defaults to None
        
            Common parameters include:
            
            - 'temperature': Controls randomness in output. Lower values (e.g., 0.2)
              make output more focused and deterministic, while higher values (e.g., 0.8)
              make output more diverse and creative.
                
            - 'max_tokens': Sets the maximum number of tokens to generate in the response.
              This can help control the length of the model's output.

        :type parameters: Optional[Dict], optional
        """
        self.name = name
        self.version = version
        self.parameters = parameters or {}

    def to_dict(self):
        """Converts the LLM instance to a dictionary representation.

        :return: Dictionary representation of the LLM.
        :rtype: dict
        """
        return {
            "model_name": self.name,
            "model_version": self.version,
            "model_params": self.parameters,
        }
