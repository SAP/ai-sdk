"""LangChain wrappers for OpenAI models via Generative AI Hub."""
import re
from typing import Any, Dict, Optional

from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_openai import ChatOpenAI as ChatOpenAI_  # pylint: disable=import-error, no-name-in-module
from langchain_openai import OpenAI as OpenAI_  # pylint: disable=import-error, no-name-in-module
from langchain_openai import OpenAIEmbeddings as OpenAIEmbeddings_  # pylint: disable=import-error, no-name-in-module
from pydantic import Field, model_validator, ConfigDict

from gen_ai_hub.proxy.core.base import BaseDeployment, BaseProxyClient
from gen_ai_hub.proxy.native.openai import AsyncOpenAI as AsyncOpenAIClient
from gen_ai_hub.proxy.native.openai import OpenAI as OpenAIClient
from gen_ai_hub.proxy.native.openai.clients import DEFAULT_API_VERSION
from .base import BaseAuth


def get_client_params(values):
    """
    Get the client parameters.
    :param values: The client values
    :return: client values + proxy_client
    """
    return {
        'api_key': values.get('openai_api_key', 'EMPTY') or 'EMPTY',
        'organization': values.get('openai_organization', 'EMPTY') or 'EMPTY',
        'proxy_client': values.get('proxy_client', None),
        'timeout': values.get('request_timeout', None),
        'max_retries': values.get('max_retries', 2),
        'default_headers': values.get('default_headers', {}) or {},
        'default_query': values.get('default_query', {}) or {},
        'http_client': values.get('http_client', None),
        'api_version': values.get('openai_api_version', DEFAULT_API_VERSION) or DEFAULT_API_VERSION
    }


class ProxyOpenAI(BaseAuth):
    """Base class for OpenAI models using a proxy.

    :param BaseAuth: Base authentication class
    :type BaseAuth: class
    :return: The ProxyOpenAI class
    :rtype: class
    """
    model_config = ConfigDict(extra='allow')

    @classmethod
    def validate_clients(cls, values: Dict) -> Dict:
        """Validate and initialize OpenAI clients.

        :param values: The input values
        :type values: Dict
        :return: The validated values
        :rtype: Dict
        """
        values['proxy_client'] = cls._get_proxy_client(values)
        client_params = get_client_params(values)
        if not values.get('client'):
            values['client'] = OpenAIClient(**client_params)
        if not values.get('async_client'):
            values['async_client'] = AsyncOpenAIClient(**client_params)
        deployment = values['proxy_client'].select_deployment(
            deployment_id=values.get('deployment_id', None),
            config_id=values.get('config_id', None),
            config_name=values.get('config_name', None),
            model_name=values.get('proxy_model_name', None),
        )
        BaseAuth._set_deployment_parameters(values, deployment)
        return values


class ChatOpenAI(ProxyOpenAI, ChatOpenAI_):
    """ChatOpenAI model using a proxy.

    :param ProxyOpenAI: Base class for OpenAI models using a proxy
    :type ProxyOpenAI: class
    :param ChatOpenAI_: ChatOpenAI class from langchain_openai
    :type ChatOpenAI_: class
    """
    model_name: Optional[str] = None
    openai_api_version: Optional[str] = Field(default=None, alias='api_version')

    model_config = ConfigDict(extra='allow')

    def __new__(cls, **data: Any):  # type: ignore
        """
        Initialize the OpenAI object.
        :param data: Additional data to initialize the object
        :type data: Any
        :return: The initialized OpenAI object
        :rtype: OpenAIBase
        """
        data['model_name'] = data.get('model_name', '') or ''
        return ChatOpenAI_.__new__(cls)

    # pylint: disable=no-self-argument
    def __init__(self, *args, **kwargs):
        """Initialize the ChatOpenAI object."""
        n = kwargs.pop('n', 1)
        super().__init__(*args, openai_api_key='???', n=n, **kwargs)

    @model_validator(mode='before')
    def validate_environment(cls, values: Dict) -> Dict:
        """Validates the environment.

        :param values: The input values
        :type values: Dict
        :raises ValueError: n must be at least 1.
        :return: The validated values
        :rtype: Dict
        """
        values = cls.validate_clients(values)
        if values['n'] < 1:
            raise ValueError('n must be at least 1.')
        if values['n'] > 1 and values['streaming']:
            raise ValueError('n must be 1 when streaming.')
        if isinstance(values['client'], OpenAIClient):
            values['root_client'] = values['client']  # Store full client for beta API access
            values['client'] = values['client'].chat.completions
        if isinstance(values['async_client'], AsyncOpenAIClient):
            values['root_async_client'] = values['async_client']  # Store full client for beta API access
            values['async_client'] = values['async_client'].chat.completions
        values['model_name'] = values.get('model_name', None) or values.get('model', None) or values.get(
            'proxy_model_name', None)
        return values

    @property
    def _default_params(self) -> Dict[str, Any]:
        """Returns the default parameters for the OpenAI object.

        :return: The default parameters
        :rtype: Dict[str, Any]
        """
        return {
            **super()._default_params, 'deployment_id': self.deployment_id,
            'config_id': self.config_id,
            'config_name': self.config_name,
            'model_name': self.proxy_model_name,
            'model': ''
        }

    def _create_chat_result(self, response: Any, generation_info: Optional[Dict[str, Any]] = None) -> Any:
        """Override to handle Cohere's response format which uses model_extra instead of choices.

        :param response: The response from the API.
        :type response: Any
        :param generation_info: Additional generation information.
        :type generation_info: Optional[Dict[str, Any]]
        :return: The chat result.
        :rtype: Any
        """

        # Check if this is a Cohere model response
        if (hasattr(response, 'model_extra') and
                response.model_extra and
                'message' in response.model_extra and
                self.proxy_model_name and
                re.search(r"^cohere--", self.proxy_model_name)):

            # Extract content from Cohere's response format
            cohere_message = response.model_extra.get('message', {})
            content_parts = cohere_message.get('content', [])

            content_text = ""
            for part in content_parts:
                if isinstance(part, dict) and part.get('type') == 'text':
                    content_text += part.get('text', '')

            message = AIMessage(content=content_text)
            generation = ChatGeneration(message=message)
            token_usage = response.usage.model_extra if response.usage and response.usage.model_extra else {}

            return ChatResult(generations=[generation], llm_output=token_usage)

        # For non-Cohere models, use the default implementation
        return super()._create_chat_result(response)


class OpenAI(ProxyOpenAI, OpenAI_):
    """OpenAI model using a proxy."""
    model_name: Optional[str] = None
    openai_api_version: Optional[str] = Field(default=None, alias='api_version')

    model_config = ConfigDict(extra='allow')

    def __init__(self, *args, **kwargs):
        """Initialize the OpenAI object."""
        n = kwargs.pop('n', 1)
        super().__init__(*args, openai_api_key='???', n=n, **kwargs)

    def __new__(cls, **data: Any):  # type: ignore
        """Initialize the OpenAI object."""
        data['model_name'] = data.get('model_name', '') or ''
        return OpenAI_.__new__(cls)

    # pylint: disable=no-self-argument
    @model_validator(mode='before')
    def validate_environment(cls, values: Dict) -> Dict:
        """Validates the environment.

        :param values: The input values
        :type values: Dict
        :return: The validated values
        :rtype: Dict
        """
        values = cls.validate_clients(values)
        if values['n'] < 1:
            raise ValueError('n must be at least 1.')
        if values['n'] > 1 and values['streaming']:
            raise ValueError('n must be 1 when streaming.')
        if isinstance(values['client'], OpenAIClient):
            values['root_client'] = values['client']
            values['client'] = values['client'].completions
        if isinstance(values['async_client'], AsyncOpenAIClient):
            values['root_async_client'] = values['async_client']
            values['async_client'] = values['async_client'].completions
        values['model_name'] = values.get('model_name', None) or values.get('model', None) or values.get(
            'proxy_model_name', None)
        return values

    @property
    def _default_params(self) -> Dict[str, Any]:
        params = super()._default_params
        return {
            **params, 'deployment_id': self.deployment_id,
            'config_id': self.config_id,
            'config_name': self.config_name,
            'model_name': self.proxy_model_name,
            'model': ''
        }


class OpenAIEmbeddings(ProxyOpenAI, OpenAIEmbeddings_):
    """OpenAI Embeddings model using a proxy."""
    model: Optional[str] = None
    tiktoken_model_name: Optional[str] = 'text-embedding-ada-002'
    chunk_size: int = 16
    openai_api_version: Optional[str] = Field(default=None, alias='api_version')
    input_type: Optional[str] = Field(
        default=None,
        description="Required for NVIDIA models: 'query' for search queries, 'passage' for documents. "
    )

    model_config = ConfigDict(extra='allow')

    def __init__(self, *args, **kwargs):
        """Initialize the OpenAIEmbeddings object."""
        super().__init__(*args, openai_api_key='???', **kwargs)

    # pylint: disable=no-self-argument
    @model_validator(mode='before')
    def validate_environment(cls, values: Dict) -> Dict:
        """Validates the environment.

        :param values: The input values
        :type values: Dict
        :return: The validated values
        :rtype: Dict
        """
        values = cls.validate_clients(values)
        if isinstance(values['client'], OpenAIClient):
            values['client']: OpenAIClient = values['client'].embeddings
        if isinstance(values['async_client'], AsyncOpenAIClient):
            values['async_client']: AsyncOpenAIClient = values['async_client'].embeddings
        values['model'] = values.get('model', None) or values.get('model_name', None) or values.get(
            'proxy_model_name', None)
        return values

    def _get_len_safe_embeddings(self, texts, *, engine, **kwargs):
        """Override embedding creation to handle NVIDIA-specific requirements.
        
        For NVIDIA models:
        - Requires explicit input_type parameter: 'query' for search queries, 'passage' for documents
        - Bypasses Langchain's tokenization to send raw text strings directly to the API
          (NVIDIA models require string input, not tokenized arrays)
        - Filters out Langchain-specific parameters not supported by OpenAI API
        - Returns standard embedding format: List[List[float]]
        
        For non-NVIDIA models, delegates to parent class implementation.
        """
        if self.model and 'nvidia' in self.model.lower():
            if not self.input_type:
                raise ValueError(f"input_type parameter is required for NVIDIA models (model: {self.model}).")

            if self.input_type not in ('query', 'passage'):
                raise ValueError(
                    f"input_type must be either 'query' or 'passage', got '{self.input_type}'"
                )

            kwargs['extra_body'] = {'input_type': self.input_type}

            api_kwargs = {key: val for key, val in kwargs.items()
                          if key not in ('chunk_size', 'engine')}

            # Send raw text strings directly (no tokenization)
            response = self.client.create(
                input=texts,
                model_name=self.model,
                deployment_id=self.deployment_id,
                **api_kwargs
            )
            return [list(map(float, e.embedding)) for e in response.data]

        return super()._get_len_safe_embeddings(texts, engine=engine, **kwargs)

    @property
    def _invocation_params(self) -> Dict:
        params = super()._invocation_params
        return {
            **params,
            'deployment_id': self.deployment_id,
            'config_id': self.config_id,
            'config_name': self.config_name,
            'model': self.model,
        }


def init_chat_model(
        proxy_client: BaseProxyClient,
        deployment: BaseDeployment,
        temperature: float = 0.0,
        max_tokens: int = 256,
        top_k: Optional[int] = None,
        top_p: float = 1.0,
):
    """Initialize the ChatOpenAI model.

    :param proxy_client: the proxy client
    :type proxy_client: BaseProxyClient
    :param deployment: the deployment
    :type deployment: BaseDeployment
    :param temperature: the temperature, defaults to 0.0
    :type temperature: float, optional
    :param max_tokens: the maximum tokens, defaults to 256
    :type max_tokens: int, optional
    :param top_k: the top k, defaults to None
    :type top_k: Optional[int], optional
    :param top_p: the top p, defaults to 1.0
    :type top_p: float, optional
    :return: the ChatOpenAI model
    :rtype: ChatOpenAI
    """
    return ChatOpenAI(
        deployment_id=deployment.deployment_id,
        proxy_client=proxy_client,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
    )


def init_embedding_model(proxy_client: BaseProxyClient, deployment: BaseDeployment):
    """Initialize the OpenAIEmbeddings model.

    :param proxy_client: the proxy client
    :type proxy_client: BaseProxyClient
    :param deployment: the deployment
    :type deployment: BaseDeployment
    :return: the OpenAIEmbeddings model
    :rtype: OpenAIEmbeddings
    """
    kwarg = {
        'deployment_id': deployment.deployment_id,
        'proxy_client': proxy_client,
        'chunk_size': 16,
    }
    if 'nvidia' in deployment.model_name.lower():
        return OpenAIEmbeddings(input_type='query', **kwarg)
    return OpenAIEmbeddings(**kwarg)
