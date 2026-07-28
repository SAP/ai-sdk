import logging
from typing import Dict, Optional, List, Any

from botocore.config import Config
from langchain_aws import ChatBedrock as ChatBedrock_, ChatBedrockConverse as ChatBedrockConverse_
from langchain_community.embeddings import BedrockEmbeddings as BedrockEmbeddings_
from pydantic import BaseModel, ConfigDict, model_validator

from gen_ai_hub.proxy.core.base import BaseProxyClient
from gen_ai_hub.proxy.gen_ai_hub_proxy.client import Deployment
from gen_ai_hub.proxy.native.amazon.clients import Session


def _parse_minor_version(raw: str) -> tuple:
    """Parses a Claude minor version like ``4`` or ``4.6`` into a comparable tuple."""
    if "." in raw:
        major, minor = raw.split(".", 1)
        return int(major), int(minor)
    return int(raw), 0


class AICoreBedrockBaseModel(BaseModel):
    """AICoreBedrockBaseModel provides all adjustments
    to boto3 based LangChain classes to enable communication
    with SAP AI Core."""

    model_config = ConfigDict(extra='allow')

    def __init__(
            self,
            *args,
            model_id: str = "",
            deployment_id: str = "",
            model_name: str = "",
            config_id: str = "",
            config_name: str = "",
            proxy_client: Optional[BaseProxyClient] = None,
            **kwargs,
    ):
        """Initializes the AICoreBedrockBaseModel with AICore specific parameters. 
            Extends the constructor of the base class with aicore specific parameters

        :param model_id: the model identifier, defaults to ""
        :type model_id: str, optional
        :param deployment_id: the deployment identifier, defaults to ""
        :type deployment_id: str, optional
        :param model_name: the model name, defaults to ""
        :type model_name: str, optional
        :param config_id: the configuration identifier, defaults to ""
        :type config_id: str, optional
        :param config_name: the configuration name, defaults to ""
        :type config_name: str, optional
        :param proxy_client: the proxy client to use, defaults to None
        :type proxy_client: Optional[BaseProxyClient], optional
        """
        client_params = {
            "deployment_id": deployment_id,
            "model_name": model_name,
            "config_id": config_id,
            "config_name": config_name,
            "proxy_client": proxy_client,
        }
        kwargs["client_params"] = client_params
        super().__init__(*args, model_id=model_id, **kwargs)

    @staticmethod
    def get_corresponding_model_id(full_model_name, model_version='latest'):
        """Gets the corresponding model ID for a given model name.
        :param full_model_name: the model name
        :type full_model_name: str
        :param model_version: the model version
        :type model_version: str
        :return: the corresponding model ID
        :rtype: str
        """
        provider, model_name = full_model_name.split("--", maxsplit=1)
        if model_name.startswith('claude'):
            claude, base_model_version, base_model_name = model_name.split('-')
            base_model_version_major, base_model_version_minor = _parse_minor_version(base_model_version)
            if base_model_version_major >= 4:
                # Reorder: claude-{name}-{major}-{minor}
                model_name = '-'.join([claude, base_model_name, str(base_model_version_major), str(base_model_version_minor)])
                return '.'.join([provider, model_name])
        return f"{provider}.{model_name}-{model_version}"

    # pylint: disable=no-self-argument
    @model_validator(mode='before')
    def validate_environment(cls, values: Dict) -> Dict:
        """Validates and sets up the environment for the model.

        :param values: the input values
        :type values: Dict
        :return: the validated values
        :rtype: Dict
        """
        client_params = values.get("client_params")
        if not client_params and "model_kwargs" in values and isinstance(values["model_kwargs"], dict):
            client_params = values["model_kwargs"].get("client_params")
        
        if client_params and not values.get("client"):
            if "config" in values and values["config"] is not None:
                client_params["config"] = values["config"]
            values["client"] = Session().client(**client_params)
        
        if values.get('model_id') in (None, ''):
            deployment = values["client"].aicore_deployment
            values["model_id"] = cls.get_corresponding_model_id(
                deployment.model_name,
                deployment.model_version
            )
        
        # Remove client_params from model_kwargs to prevent it from being passed to AWS API
        if "model_kwargs" in values and isinstance(values["model_kwargs"], dict):
            values["model_kwargs"].pop("client_params", None)
        
        # Remove client_params from top level to prevent it from being passed to AWS API
        values.pop("client_params", None)

        return values


class ChatBedrock(AICoreBedrockBaseModel, ChatBedrock_):
    """Drop-in replacement for LangChain ChatBedrock."""

    model_config = ConfigDict(extra='allow')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ChatBedrockConverse(AICoreBedrockBaseModel, ChatBedrockConverse_):
    """Drop-in replacement for LangChain ChatBedrockConverse."""

    model_config = ConfigDict(extra='allow')

    def __init__(self, *args, **kwargs):
        self.extract_model_kwargs_parameters(kwargs)

        super().__init__(*args, **kwargs)

    def extract_model_kwargs_parameters(self, kwargs):
        """Extracts specific parameters from model_kwargs and moves them to the top level of kwargs.

        :param kwargs: the input keyword arguments
        :type kwargs: Dict
        """
        # Extract parameters from model_kwargs to avoid circular reference issues
        model_kwargs = kwargs.get('model_kwargs', {})
        if isinstance(model_kwargs, dict):
            # Extract common parameters that should be passed directly
            for param_name in ['temperature', 'max_tokens', 'top_p', 'stop_sequences']:
                if param_name in model_kwargs and param_name not in kwargs:
                    kwargs[param_name] = model_kwargs.pop(param_name)

            # Clean up model_kwargs if it's now empty
            if not model_kwargs:
                kwargs.pop('model_kwargs', None)
            else:
                kwargs['model_kwargs'] = model_kwargs


class BedrockEmbeddings(AICoreBedrockBaseModel, BedrockEmbeddings_):
    """Drop-in replacement for LangChain BedrockEmbeddings."""

    model_config = ConfigDict(extra='allow')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def _build_bedrock_model_kwargs(
        deployment: Deployment,
        temperature: float,
        max_tokens: int,
        top_k: Optional[int],
        top_p: float,
        stop_sequences: Optional[List[str]],
        config: Optional[Config]
) -> Dict[str, Any]:
    """Builds the model_kwargs dictionary for Bedrock models."""
    if top_k:
        logging.warning(
            "Top-k is disabled for Amazon Bedrock models. Ignoring top-k value."
        )

    model_kwargs = {
        "temperature": temperature,
    }

    if config:
        model_kwargs["config"] = config

    if deployment.model_name.startswith("anthropic"):
        model_kwargs["max_tokens"] = max_tokens
        model_kwargs["top_p"] = top_p
    else:  # Assuming Amazon bedrock models otherwise
        model_kwargs["maxTokenCount"] = max_tokens
        model_kwargs["topP"] = top_p
        if stop_sequences:
            model_kwargs["stopSequences"] = stop_sequences

    return model_kwargs

def init_chat_model(
        proxy_client: BaseProxyClient,
        deployment: Deployment,
        temperature: float = 0.0,
        max_tokens: int = 256,
        top_k: Optional[int] = None,
        top_p: float = 1.0,
        stop_sequences: List[str] = None,
        model_id: Optional[str] = '',
        config: Optional[Config] = None
):
    """Initializes a chat model using the legacy Bedrock Invoke API (`ChatBedrock`).

    :param proxy_client: the proxy client to use
    :type proxy_client: BaseProxyClient
    :param deployment: the deployment information
    :type deployment: Deployment
    :param temperature: the temperature for the model, defaults to 0.0
    :type temperature: float, optional
    :param max_tokens: the maximum number of tokens to generate, defaults to 256
    :type max_tokens: int, optional
    :param top_k: the top-k sampling parameter, defaults to None
    :type top_k: Optional[int], optional
    :param top_p: the top-p sampling parameter, defaults to 1.0
    :type top_p: float, optional
    :param stop_sequences: the stop sequences for the model, defaults to None
    :type stop_sequences: List[str], optional
    :param model_id: the model identifier, defaults to ''
    :type model_id: Optional[str], optional
    :param config: the botocore configuration, defaults to None
    :type config: Optional[Config], optional
    :return: the initialized chat model
    :rtype: ChatBedrock
    """

    model_kwargs = _build_bedrock_model_kwargs(
        deployment=deployment,
        temperature=temperature,
        max_tokens=max_tokens,
        top_k=top_k,
        top_p=top_p,
        stop_sequences=stop_sequences,
        config=config
    )

    return ChatBedrock(
        model_name=deployment.model_name,
        model_id=model_id,
        deployment_id=deployment.deployment_id,
        proxy_client=proxy_client,
        model_kwargs=model_kwargs
    )

def init_chat_converse_model(
        proxy_client: BaseProxyClient,
        deployment: Deployment,
        temperature: float = 0.0,
        max_tokens: int = 256,
        top_k: Optional[int] = None,
        top_p: float = 1.0,
        stop_sequences: List[str] = None,
        model_id: Optional[str] = '',
        config: Optional[Config] = None
):
    """Initializes a chat model using the newer Bedrock Converse API (`ChatBedrockConverse`).
    The Converse API offers several advantages over the older Invoke API:

    - Unified interface for different models and modalities.

    - Native support for tool use (function calling).

    - Standardized request/response structure.

    :param proxy_client: the proxy client to use
    :type proxy_client: BaseProxyClient
    :param deployment: the deployment information
    :type deployment: Deployment
    :param temperature: the temperature for the model, defaults to 0.0
    :type temperature: float, optional
    :param max_tokens: the maximum number of tokens to generate, defaults to 256
    :type max_tokens: int, optional
    :param top_k: the top-k sampling parameter, defaults to None
    :type top_k: Optional[int], optional
    :param top_p: the top-p sampling parameter, defaults to 1.0
    :type top_p: float, optional
    :param stop_sequences: the stop sequences for the model, defaults to None
    :type stop_sequences: List[str], optional
    :param model_id: the model identifier, defaults to ''
    :type model_id: Optional[str], optional
    :param config: the botocore configuration, defaults to None
    :type config: Optional[Config], optional
    :return: the initialized chat model
    :rtype: ChatBedrockConverse
    """
    return ChatBedrockConverse(
        model_name=deployment.model_name,
        model_id=model_id,
        deployment_id=deployment.deployment_id,
        proxy_client=proxy_client,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stop_sequences=stop_sequences,
        config = config
    )

def init_embedding_model(proxy_client: BaseProxyClient, deployment: Deployment, model_id: Optional[str] = ''):
    """Initializes an embedding model using BedrockEmbeddings.

    :param proxy_client: the proxy client to use
    :type proxy_client: BaseProxyClient
    :param deployment: the deployment information
    :type deployment: Deployment
    :param model_id: the model identifier, defaults to ''
    :type model_id: Optional[str], optional
    :return: the initialized embedding model
    :rtype: BedrockEmbeddings
    """
    return BedrockEmbeddings(deployment_id=deployment.deployment_id, proxy_client=proxy_client, model_id=model_id)
