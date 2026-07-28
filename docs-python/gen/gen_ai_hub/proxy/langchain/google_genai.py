"""Drop-in replacements for langchain_google_genai models with SAP AI Core integration."""

from typing import Optional

from langchain_google_genai import ChatGoogleGenerativeAI as ChatGoogleGenerativeAI_
from langchain_google_genai import GoogleGenerativeAIEmbeddings as GoogleGenerativeAIEmbeddings_
from pydantic import model_validator, ConfigDict

from gen_ai_hub.proxy.core.base import BaseProxyClient
from gen_ai_hub.proxy.core.utils import if_str_set
from gen_ai_hub.proxy.gen_ai_hub_proxy.client import Deployment
from gen_ai_hub.proxy.native.google_genai.clients import Client as GenAIHubNativeClient


class _BaseGoogleGenerativeAI:
    """Base class for Google Generative AI models with common functionality."""

    model_config = ConfigDict(extra='allow')

    def __init__(
            self,
            model: str = "",
            proxy_model_name: str = "",
            model_id: str = "",
            deployment_id: str = "",
            config_id: str = "",
            config_name: str = "",
            proxy_client: Optional[BaseProxyClient] = None,
            **kwargs,
    ):
        """
        Parameters:
            model (str): The model name to use.
            proxy_model_name (str): The proxy model name to use.
            model_id (str): The model ID to use.
            deployment_id (str): The deployment ID to use.
            config_id (str): The configuration ID to use.
            config_name (str): The configuration name to use.
            proxy_client (Optional[BaseProxyClient]): The proxy client to use.
            **kwargs: Additional keyword arguments.
        """
        resolved_model_name, updated_kwargs = self._setup_client_and_kwargs(
            model=model,
            proxy_model_name=proxy_model_name,
            model_id=model_id,
            deployment_id=deployment_id,
            config_id=config_id,
            config_name=config_name,
            proxy_client=proxy_client,
            kwargs=kwargs,
        )

        # Call the appropriate parent class constructor
        self._init_parent(model=resolved_model_name, **updated_kwargs)

    def _init_parent(self, **kwargs):
        raise NotImplementedError("Subclasses must implement _init_parent")

    def _setup_client_and_kwargs(
            self,
            model: str,
            proxy_model_name: str,
            model_id: str,
            deployment_id: str,
            config_id: str,
            config_name: str,
            proxy_client: Optional[BaseProxyClient],
            kwargs: dict,
    ) -> tuple[str, dict]:
        if model_id != "":
            raise ValueError(
                "Parameter not supported. Please use a variation of deployment_id, "
                "model_name, config_id and config_name to identify a deployment."
            )

        resolved_model_name = if_str_set(
            model, if_str_set(proxy_model_name, kwargs.get("model_name", ""))
        )

        native_client = GenAIHubNativeClient(
            proxy_client=proxy_client,
            deployment_id=deployment_id,
            config_id=config_id,
            config_name=config_name
        )

        kwargs["client"] = native_client
        kwargs["google_api_key"] = "dummy_key"

        return resolved_model_name, kwargs

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: dict) -> dict:
        """Override to prevent LangChain from looking for local GOOGLE_API_KEY env vars."""
        if not values.get("google_api_key"):
            values["google_api_key"] = "dummy_key"
        return values

    @model_validator(mode="after")
    def _determine_backend(self):
        """Override to skip backend determination since we use our own client."""
        object.__setattr__(self, "_use_vertexai", True)
        return self

    @model_validator(mode="after")
    def _initialize_client(self):
        """Override to prevent the parent class from creating its own client."""
        return self


class ChatGoogleGenerativeAI(_BaseGoogleGenerativeAI, ChatGoogleGenerativeAI_):
    """Drop-in replacement for langchain_google_genai.ChatGoogleGenerativeAI."""

    def _init_parent(self, **kwargs):
        ChatGoogleGenerativeAI_.__init__(self, **kwargs)


class GoogleGenerativeAIEmbeddings(_BaseGoogleGenerativeAI, GoogleGenerativeAIEmbeddings_):
    """Drop-in replacement for langchain_google_genai.GoogleGenerativeAIEmbeddings."""

    def _init_parent(self, **kwargs):
        GoogleGenerativeAIEmbeddings_.__init__(self, **kwargs)

def init_chat_model(
        proxy_client: BaseProxyClient,
        deployment: Deployment,
        temperature: float = 0.0,
        max_tokens: int = 256,
        top_k: Optional[int] = None,
        top_p: float = 1.0,
):
    """Initialize a ChatGoogleGenerativeAI model with the given parameters.

    :param proxy_client: proxy client to use for the model
    :type proxy_client: BaseProxyClient
    :param deployment: deployment information for the model
    :type deployment: Deployment
    :param temperature: sampling temperature, defaults to 0.0
    :type temperature: float, optional
    :param max_tokens: maximum number of tokens to generate, defaults to 256
    :type max_tokens: int, optional
    :param top_k: k for top-k sampling, defaults to None
    :type top_k: Optional[int], optional
    :param top_p: p for nucleus sampling, defaults to 1.0
    :type top_p: float, optional
    :return: initialized ChatGoogleGenerativeAI model
    :rtype: ChatGoogleGenerativeAI
    """
    return ChatGoogleGenerativeAI(
        model=deployment.model_name,
        deployment_id=deployment.deployment_id,
        proxy_client=proxy_client,
        temperature=temperature,
        max_output_tokens=max_tokens,
        top_k=top_k,
        top_p=top_p,
    )

def init_embedding_model(proxy_client: BaseProxyClient, deployment: Deployment):
    return GoogleGenerativeAIEmbeddings(
        model=deployment.model_name,
        deployment_id=deployment.deployment_id,
        proxy_client=proxy_client,
        config_id=getattr(deployment, 'config_id', ''),
        config_name=getattr(deployment, 'config_name', ''),
    )
