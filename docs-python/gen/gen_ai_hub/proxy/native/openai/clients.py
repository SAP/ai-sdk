from __future__ import annotations

import contextvars
import re
from contextlib import contextmanager
from typing import Optional, Union, List, TypeVar, Iterable

import httpx
from openai import AsyncOpenAI as AsyncOpenAI_
from openai import OpenAI as OpenAI_
from openai import resources
from openai._streaming import Stream, AsyncStream
from openai._types import Omit
from openai.lib._parsing._responses import TextFormatT
from openai.resources.chat import AsyncChat as AsyncChat_
from openai.resources.chat import Chat as Chat_
from openai.resources.chat.completions import AsyncCompletions as AsyncChatCompletions_
from openai.resources.chat.completions import Completions as ChatCompletions_
from openai.resources.completions import AsyncCompletions as AsyncCompletions_
from openai.resources.completions import Completions as Completions_
from openai.resources.embeddings import AsyncEmbeddings as AsyncEmbeddings_
from openai.resources.embeddings import Embeddings as Embeddings_
from openai.resources.responses import Responses as Responses_
from openai.resources.responses  import AsyncResponses as AsyncResponses_
from openai.types import Completion, Embedding
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam
from openai.types.chat.parsed_chat_completion import ParsedChatCompletion
from openai.types.responses import Response, ResponseStreamEvent, ResponseInputParam, ParsedResponse


from gen_ai_hub.proxy.core import get_proxy_client
from gen_ai_hub.proxy.core.base import BaseProxyClient
from gen_ai_hub.proxy.core.utils import NOT_GIVEN, NotGiven, if_set, kwargs_if_set

DEFAULT_API_VERSION = '2025-03-01-preview'  # https://learn.microsoft.com/en-us/azure/ai-foundry/openai/api-version-lifecycle?tabs=key#api-evolution

# Model name patterns
COHERE_MODEL_PATTERN = r"^cohere--"
O_SERIES_MODEL_PATTERN = r"^o\d+"
GPT_5_MODEL_PATTERN = r"^gpt-5(-mini|-nano)?$"
COHERE_REASONING_MODEL_PATTERN = r"^cohere--command-.*-reasoning$"

ResponseFormatT = TypeVar('ResponseFormatT')
_current_deployment = contextvars.ContextVar('current_deployment')


@contextmanager
def set_deployment(value):
    """Context manager to set the current deployment.

    :param value: The deployment to set as current.
    :type value: Deployment
    """
    token = _current_deployment.set(value)
    try:
        yield
    finally:
        _current_deployment.reset(token)


def get_current_deployment():
    """Get the current deployment from the context variable.

    :return: The current deployment.
    :rtype: Deployment
    """
    return _current_deployment.get(None)


class Embeddings(Embeddings_):
    """
    A class that represents the Embeddings. It extends the Embeddings_ class
    and provides functionality to create embeddings based on the provided input.
    """

    def create(self,
               *,
               input: Union[str, List[str], List[int], List[List[int]], None],
               model: str | None | NotGiven = NOT_GIVEN,
               deployment_id: str | None | NotGiven = NOT_GIVEN,
               model_name: str | None | NotGiven = NOT_GIVEN,
               model_version: str | None | NotGiven = NOT_GIVEN,
               config_id: str | None | NotGiven = NOT_GIVEN,
               config_name: str | None | NotGiven = NOT_GIVEN,
               **kwargs) -> Embedding:
        """Creates embeddings based on the provided input and model information.

        For NVIDIA models, use extra_body to specify additional parameters:
            extra_body={'input_type': 'query'|'passage'}

        :param input: the input data for which embeddings are to be created.
        :type input: Union[str, List[str], List[int], List[List[int]], None]
        :param model:the model to use for creating embeddings, defaults to NOT_GIVEN
        :type model: str | None | NotGiven, optional
        :param deployment_id: the ID of the deployment to use, defaults to NOT_GIVEN
        :type deployment_id: str | None | NotGiven, optional
        :param model_name: the name of the model to use, defaults to NOT_GIVEN
        :type model_name: str | None | NotGiven, optional
        :param model_version: the model version, defaults to NOT_GIVEN
        :type model_version: str | None | NotGiven, optional
        :param config_id: the ID of the config to use, defaults to NOT_GIVEN
        :type config_id: str | None | NotGiven, optional
        :param config_name: the name of the config to use, defaults to NOT_GIVEN
        :type config_name: str | None | NotGiven, optional
        :param kwargs: additional keyword arguments.
        :type kwargs: dict
        :raises ValueError: if the deployment cannot be selected or the model name is not provided.
        :return: the created embeddings.
        :rtype: Embedding
        """
        proxy_client: BaseProxyClient = self._client.proxy_client
        model_name = if_set(model_name, if_set(model))
        model_identification = kwargs_if_set(
            deployment_id=deployment_id,
            model_name=model_name,
            model_version=model_version,
            config_id=config_id,
            config_name=config_name,
        )
        deployment = proxy_client.select_deployment(**model_identification)
        model_name = deployment.model_name or '???'

        with set_deployment(deployment):
            return super().create(input=input, model=model_name, **kwargs)


class AsyncEmbeddings(AsyncEmbeddings_):
    """
    The AsyncEmbeddings class is a subclass of AsyncEmbeddings_. This class is used for creating
    embeddings asynchronously. It provides an interface for fetching embeddings of a given input
    from a selected deployment on a proxy client.
    """

    async def create(self,
                     *,
                     input: Union[str, List[str], List[int], List[List[int]], None],
                     model: str | None | NotGiven = NOT_GIVEN,
                     deployment_id: str | None | NotGiven = NOT_GIVEN,
                     model_name: str | None | NotGiven = NOT_GIVEN,
                     model_version: str | None | NotGiven = NOT_GIVEN,
                     config_id: str | None | NotGiven = NOT_GIVEN,
                     config_name: str | None | NotGiven = NOT_GIVEN,
                     **kwargs) -> Embedding:
        """Asynchronously creates embeddings for the given input using a specific model.

        :param input: the input data for which embeddings are to be created.
        :type input: Union[str, List[str], List[int], List[List[int]], None]
        :param model: the model to use for creating embeddings, defaults to NOT_GIVEN
        :type model: str | None | NotGiven, optional
        :param deployment_id: the ID of the deployment to use, defaults to NOT_GIVEN
        :type deployment_id: str | None | NotGiven, optional
        :param model_name: the name of the model to use, defaults to NOT_GIVEN
        :type model_name: str | None | NotGiven, optional
        :param model_version: the model version, defaults to NOT_GIVEN
        :type model_version: str | None | NotGiven, optional
        :param config_id: the ID of the config to use, defaults to NOT_GIVEN
        :type config_id: str | None | NotGiven, optional
        :param config_name: the name of the config to use, defaults to NOT_GIVEN
        :type config_name: str | None | NotGiven, optional
        :return: the created embeddings.
        :rtype: Embedding
        """
        proxy_client: BaseProxyClient = self._client.proxy_client
        model_name = if_set(model_name, if_set(model))
        model_identification = kwargs_if_set(
            deployment_id=deployment_id,
            model_name=model_name,
            model_version=model_version,
            config_id=config_id,
            config_name=config_name,
        )
        deployment = proxy_client.select_deployment(**model_identification)
        model_name = deployment.model_name or '???'

        with set_deployment(deployment):
            return await super().create(input=input, model=model_name, **kwargs)


class Completions(Completions_):
    """
    The Completions class is a subclass of Completions_. It provides a way to create a completion given a prompt and
     certain other configurations. It extends from the base class Completions_ and overrides the create method to cater
     to the specific requirements.
    """

    def create(self,
               *,
               prompt: Union[str, List[str], List[int], List[List[int]], None],
               model: str | None | NotGiven = NOT_GIVEN,
               deployment_id: str | None | NotGiven = NOT_GIVEN,
               model_name: str | None | NotGiven = NOT_GIVEN,
               model_version: str | None | NotGiven = NOT_GIVEN,
               config_id: str | None | NotGiven = NOT_GIVEN,
               config_name: str | None | NotGiven = NOT_GIVEN,
               **kwargs) -> Completion | Stream[Completion]:
        """This method creates a completion based on the provided parameters. It uses a proxy client to select a
        deployment and then calls the create method of the parent class to generate a completion.

        :param prompt: the input prompt(s) for the completion.
        :type prompt: Union[str, List[str], List[int], List[List[int]], None]
        :param model: the model to be used for the completion, defaults to NOT_GIVEN
        :type model: str | None | NotGiven, optional
        :param deployment_id: the deployment id, defaults to NOT_GIVEN
        :type deployment_id: str | None | NotGiven, optional
        :param model_name: the model name, defaults to NOT_GIVEN
        :type model_name: str | None | NotGiven, optional
        :param model_version: the model version, defaults to NOT_GIVEN
        :type model_version: str | None | NotGiven, optional
        :param config_id: the configuration id, defaults to NOT_GIVEN
        :type config_id: str | None | NotGiven, optional
        :param config_name: the configuration name, defaults to NOT_GIVEN
        :type config_name: str | None | NotGiven, optional
        :return: the completion or stream of completions created based on the provided prompt.
        :rtype: Completion | Stream[Completion]
        """
        proxy_client: BaseProxyClient = self._client.proxy_client
        model_name = if_set(model_name, if_set(model))
        model_identification = kwargs_if_set(
            deployment_id=deployment_id,
            model_name=model_name,
            model_version=model_version,
            config_id=config_id,
            config_name=config_name,
        )
        deployment = proxy_client.select_deployment(**model_identification)
        model_name = deployment.model_name or '???'
        with set_deployment(deployment):
            kwargs.pop("root_client", None)
            kwargs.pop("root_async_client", None)
            return super().create(prompt=prompt, model=model_name, **kwargs)


class AsyncCompletions(AsyncCompletions_):
    """
    AsyncCompletions is a subclass of AsyncCompletions_. It provides a way to create a completion given a prompt and
     certain other configurations in asynchronous way. It extends from the base class Completions_ and overrides the
     create method to cater to the specific requirements.
    """

    async def create(self,
                     *,
                     prompt: Union[str, List[str], List[int], List[List[int]], None],
                     model: str | None | NotGiven = NOT_GIVEN,
                     deployment_id: str | None | NotGiven = NOT_GIVEN,
                     model_name: str | None | NotGiven = NOT_GIVEN,
                     model_version: str | None | NotGiven = NOT_GIVEN,
                     config_id: str | None | NotGiven = NOT_GIVEN,
                     config_name: str | None | NotGiven = NOT_GIVEN,
                     **kwargs) -> Completion | Stream[Completion]:
        """Asynchronously creates a completion or a stream of completions based on the given prompt and 
        other parameters.

        :param prompt: the input prompt(s) for the completion.
        :type prompt: Union[str, List[str], List[int], List[List[int]], None]
        :param model: the model to be used for the completion, defaults to NOT_GIVEN
        :type model: str | None | NotGiven, optional
        :param deployment_id: the deployment id, defaults to NOT_GIVEN
        :type deployment_id: str | None | NotGiven, optional
        :param model_name: the model name, defaults to NOT_GIVEN
        :type model_name: str | None | NotGiven, optional
        :param model_version: the model version, defaults to NOT_GIVEN
        :type model_version: str | None | NotGiven, optional
        :param config_id: the configuration id, defaults to NOT_GIVEN
        :type config_id: str | None | NotGiven, optional
        :param config_name: the configuration name, defaults to NOT_GIVEN
        :type config_name: str | None | NotGiven, optional
        :return: the completion or stream of completions created based on the provided prompt.
        :rtype: Completion | Stream[Completion]
        """
        proxy_client: BaseProxyClient = self._client.proxy_client
        model_name = if_set(model_name, if_set(model))
        model_identification = kwargs_if_set(
            deployment_id=deployment_id,
            model_name=model_name,
            model_version=model_version,
            config_id=config_id,
            config_name=config_name,
        )
        deployment = proxy_client.select_deployment(**model_identification)
        model_name = deployment.model_name or '???'
        with set_deployment(deployment):
            kwargs.pop("root_client", None)
            kwargs.pop("root_async_client", None)
            return await super().create(prompt=prompt, model=model_name, **kwargs)


class Chat(Chat_):
    """A class that handles chat completions, extending from the class 'Chat_'."""

    def __init__(self, client: OpenAI) -> None:
        """Initializes the Chat class with the provided OpenAI client.

        :param client: The OpenAI client to be used for chat completions.
        :type client: OpenAI
        """
        super().__init__(client)
        self.completions = ChatCompletions(client)


class ChatCompletions(ChatCompletions_):
    """
        A class that handles chat completions, extending from the class 'ChatCompletions_'.
    """

    def _prepare_chat(self, config_id, config_name, deployment_id, kwargs, model, model_name, model_version):
        """
        Prepares the deployment and model name for the create and parse completion request.
        
        Args:
            config_id: The configuration ID to use for chat completion
            config_name: The configuration name to use for chat completion  
            deployment_id: The deployment ID to use for chat completion
            kwargs: Keyword arguments dictionary that may be modified
            model: The model to use for chat completion
            model_name: The model name to use for chat completion,
            model_version: The model version to use for chat completion
            
        Returns:
            tuple: (deployment, model_name) prepared for the request
        """
        proxy_client: BaseProxyClient = self._client.proxy_client
        model_name = if_set(model_name, if_set(model))
        model_identification = kwargs_if_set(
            deployment_id=deployment_id,
            model_name=model_name,
            model_version=model_version,
            config_id=config_id,
            config_name=config_name,
        )
        deployment = proxy_client.select_deployment(**model_identification)
        model_name = deployment.model_name or '???'
        # Reasoning models do not support temperature
        if not self.supports_temperature(model_name) and 'temperature' in kwargs:
            kwargs.pop('temperature')
        # Cohere models do not support the 'n' and 'max_completion_tokens' parameters
        if model_name and re.search(COHERE_MODEL_PATTERN, model_name):
            kwargs.pop('n', None)
            kwargs.pop('max_completion_tokens', None)
        return deployment, model_name

    def create(self,
               *,
               messages: List[ChatCompletionMessageParam],
               model: str | None | NotGiven = NOT_GIVEN,
               deployment_id: str | None | NotGiven = NOT_GIVEN,
               model_name: str | None | NotGiven = NOT_GIVEN,
               model_version: str | None | NotGiven = NOT_GIVEN,
               config_id: str | None | NotGiven = NOT_GIVEN,
               config_name: str | None | NotGiven = NOT_GIVEN,
               **kwargs) -> ChatCompletion:
        """Creates a chat completion using the provided parameters.

        :param messages: the list of chat completion message parameters.
        :type messages: List[ChatCompletionMessageParam]
        :param model: the model to use for chat completion, defaults to NOT_GIVEN
        :type model: str | None | NotGiven, optional
        :param deployment_id: the deployment ID to use for chat completion, defaults to NOT_GIVEN
        :type deployment_id: str | None | NotGiven, optional
        :param model_name: the model name to use for chat completion, defaults to NOT_GIVEN
        :type model_name: str | None | NotGiven, optional
        :param model_version: the model version to use for chat completion, defaults to NOT_GIVEN
        :type model_version: str | None | NotGiven, optional
        :param config_id: the configuration ID to use for chat completion, defaults to NOT_GIVEN
        :type config_id: str | None | NotGiven, optional
        :param config_name: the configuration name to use for chat completion, defaults to NOT_GIVEN
        :type config_name: str | None | NotGiven, optional
        :return: the chat completion created with the provided parameters.
        :rtype: ChatCompletion
        """
        deployment, model_name = self._prepare_chat(config_id, config_name, deployment_id, kwargs, model, model_name,
                                                    model_version)

        with set_deployment(deployment):
            return super().create(messages=messages, model=model_name, **kwargs)

    def parse(self,
              *,
              messages: Iterable[ChatCompletionMessageParam],
              model: str | None | NotGiven = NOT_GIVEN,
              deployment_id: str | None | NotGiven = NOT_GIVEN,
              model_name: str | None | NotGiven = NOT_GIVEN,
              model_version: str | None | NotGiven = NOT_GIVEN,
              config_id: str | None | NotGiven = NOT_GIVEN,
              config_name: str | None | NotGiven = NOT_GIVEN,
              response_format: type[ResponseFormatT] | NotGiven = NOT_GIVEN,
              **kwargs) -> ParsedChatCompletion[ResponseFormatT]:
        """Parses chat completions using the provided parameters and returns a ParsedChatCompletion object.
        This method provides richer integrations with Python specific types by converting pydantic models
        into JSON schemas and parsing the response content back into the given model.

        :param messages: the list of chat completion message parameters.
        :type messages: Iterable[ChatCompletionMessageParam]
        :param model: the model to use for chat completion, defaults to NOT_GIVEN
        :type model: str | None | NotGiven, optional
        :param deployment_id: the deployment ID to use for chat completion, defaults to NOT_GIVEN
        :type deployment_id: str | None | NotGiven, optional
        :param model_name: the model name to use for chat completion, defaults to NOT_GIVEN
        :type model_name: str | None | NotGiven, optional
        :param model_version: the model version to use for chat completion, defaults to NOT_GIVEN
        :type model_version: str | None | NotGiven, optional
        :param config_id: the configuration ID to use for chat completion, defaults to NOT_GIVEN
        :type config_id: str | None | NotGiven, optional
        :param config_name: the configuration name to use for chat completion, defaults to NOT_GIVEN
        :type config_name: str | None | NotGiven, optional
        :param response_format: the response format type for structured output, defaults to NOT_GIVEN
        :type response_format: type[ResponseFormatT] | NotGiven, optional
        :return: the parsed chat completion with the structured response.
        :rtype: ParsedChatCompletion[ResponseFormatT]
        """
        deployment, model_name = self._prepare_chat(config_id, config_name, deployment_id, kwargs, model, model_name,
                                                    model_version)

        with set_deployment(deployment):
            return super().parse(messages=messages, model=model_name, response_format=response_format, **kwargs)

    @staticmethod
    def supports_temperature(model_name: str) -> bool:
        """Checks if the given model supports the `temperature` parameter.
        Reasoning models do not support temperature e.g., o1[-mini], o3[-mini], 5[-mini, -nano],
        cohere--command-a-reasoning

        :param model_name: the name of the model to check.
        :type model_name: str
        :return: True if the model supports `temperature`, False otherwise
        :rtype: bool
        """
        return (not re.search(O_SERIES_MODEL_PATTERN, model_name)
                and not re.search(GPT_5_MODEL_PATTERN, model_name)
                and not re.search(COHERE_REASONING_MODEL_PATTERN, model_name))


class Responses(Responses_):
    """
        The Responses class is a subclass of Responses_. It provides a way to create a response for the given input and
         certain other configurations. It extends from the base class Responses_ and overrides the create method to
         cater to the specific requirements.
    """

    def _prepare_chat(self, config_id, config_name, deployment_id, kwargs, model, model_name, model_version):
        """
        Prepares the deployment and model name for the create and parse responses request.

        Args:
            config_id: The configuration ID to use for chat completion
            config_name: The configuration name to use for chat completion
            deployment_id: The deployment ID to use for chat completion
            kwargs: Keyword arguments dictionary that may be modified
            model: The model to use for chat completion
            model_name: The model name to use for chat completion,
            model_version: The model version to use for chat completion

        Returns:
            tuple: (deployment, model_name) prepared for the request
        """
        proxy_client: BaseProxyClient = self._client.proxy_client
        model_name = if_set(model_name, if_set(model))
        model_identification = kwargs_if_set(
            deployment_id=deployment_id,
            model_name=model_name,
            model_version=model_version,
            config_id=config_id,
            config_name=config_name,
        )
        deployment = proxy_client.select_deployment(**model_identification)
        model_name = deployment.model_name or '???'
        # Reasoning models do not support temperature
        if not self.supports_temperature(model_name) and 'temperature' in kwargs:
            kwargs.pop('temperature')
        # Cohere models do not support the 'n' and 'max_completion_tokens' parameters
        if model_name and re.search(COHERE_MODEL_PATTERN, model_name):
            kwargs.pop('n', None)
            kwargs.pop('max_completion_tokens', None)
        return deployment, model_name

    def create(self,
               *,
               input: str | ResponseInputParam | Omit = None,
               instructions: str | Omit = None,
               model: str | None | NotGiven = NOT_GIVEN,
               deployment_id: str | None | NotGiven = NOT_GIVEN,
               model_name: str | None | NotGiven = NOT_GIVEN,
               model_version: str | None | NotGiven = NOT_GIVEN,
               config_id: str | None | NotGiven = NOT_GIVEN,
               config_name: str | None | NotGiven = NOT_GIVEN,
               **kwargs) -> Response | Stream[ResponseStreamEvent]:
        """This method creates a response based on the provided parameters. It uses a proxy client to select a
        deployment and then calls the create method of the parent class to generate a response.

        :param input: Text, image, or file inputs to the model, used to generate a response, defaults to NOT_GIVEN
        :type input: str | ResponseInputParam | None | NotGiven, optional
        :param instructions: A system (or developer) message inserted into the model's context, defaults to NOT_GIVEN
        :type instructions: str | None | NotGiven, optional
        :param model: the model to be used for the completion, defaults to NOT_GIVEN
        :type model: str | None | NotGiven, optional
        :param deployment_id: the deployment id, defaults to NOT_GIVEN
        :type deployment_id: str | None | NotGiven, optional
        :param model_name: the model name, defaults to NOT_GIVEN
        :type model_name: str | None | NotGiven, optional
        :param model_version: the model version, defaults to NOT_GIVEN
        :type model_version: str | None | NotGiven, optional
        :param config_id: the configuration id, defaults to NOT_GIVEN
        :type config_id: str | None | NotGiven, optional
        :param config_name: the configuration name, defaults to NOT_GIVEN
        :type config_name: str | None | NotGiven, optional
        :return: the response or stream of responsess created based on the provided input.
        :rtype: Response | Stream[ResponseStreamEvent]:
        """
        deployment, model_name = self._prepare_chat(config_id, config_name, deployment_id, kwargs, model, model_name,
                                                    model_version)

        with set_deployment(deployment):
            kwargs.pop("root_client", None)
            kwargs.pop("root_async_client", None)
            return super().create(instructions=instructions, input=input, model=model_name, **kwargs)

    def parse(
        self,
            *,
            input: str | ResponseInputParam | Omit = None,
            instructions: str | Omit = None,
            model: str | None | NotGiven = NOT_GIVEN,
            deployment_id: str | None | NotGiven = NOT_GIVEN,
            model_name: str | None | NotGiven = NOT_GIVEN,
            model_version: str | None | NotGiven = NOT_GIVEN,
            config_id: str | None | NotGiven = NOT_GIVEN,
            config_name: str | None | NotGiven = NOT_GIVEN,
            **kwargs) -> ParsedResponse[TextFormatT]:
        """Parses responses using the provided parameters and returns a ParsedResponse object.
        This method provides richer integrations with Python specific types by converting pydantic models
        into JSON schemas and parsing the response content back into the given model

        :param input: Text, image, or file inputs to the model, used to generate a response, defaults to NOT_GIVEN
        :type input: str | ResponseInputParam | None | NotGiven, optional
        :param instructions: A system (or developer) message inserted into the model's context, defaults to NOT_GIVEN
        :type instructions: str | None | NotGiven, optional
        :param model: the model to be used for the completion, defaults to NOT_GIVEN
        :type model: str | None | NotGiven, optional
        :param deployment_id: the deployment id, defaults to NOT_GIVEN
        :type deployment_id: str | None | NotGiven, optional
        :param model_name: the model name, defaults to NOT_GIVEN
        :type model_name: str | None | NotGiven, optional
        :param model_version: the model version, defaults to NOT_GIVEN
        :type model_version: str | None | NotGiven, optional
        :param config_id: the configuration id, defaults to NOT_GIVEN
        :type config_id: str | None | NotGiven, optional
        :param config_name: the configuration name, defaults to NOT_GIVEN
        :type config_name: str | None | NotGiven, optional
        :return: ParsedResponse object
        :rtype: ParsedResponse
        """

        deployment, model_name = self._prepare_chat(config_id, config_name, deployment_id, kwargs, model, model_name,
                                                    model_version)

        with set_deployment(deployment):
            kwargs.pop("root_client", None)
            kwargs.pop("root_async_client", None)
            return super().parse(instructions=instructions, input=input, model=model_name, **kwargs)

    @staticmethod
    def supports_temperature(model_name: str) -> bool:
        """Checks if the given model supports the `temperature` parameter.
        Reasoning models do not support temperature e.g., o1[-mini], o3[-mini], 5[-mini, -nano],
        cohere--command-a-reasoning

        :param model_name: the name of the model to check.
        :type model_name: str
        :return: True if the model supports `temperature`, False otherwise
        :rtype: bool
        """
        return (not re.search(O_SERIES_MODEL_PATTERN, model_name)
                and not re.search(GPT_5_MODEL_PATTERN, model_name)
                and not re.search(COHERE_REASONING_MODEL_PATTERN, model_name))


class AsyncChat(AsyncChat_):
    """A class that handles asynchronous chat completions, extending from the class 'AsyncChat_'."""

    def __init__(self, client: OpenAI) -> None:
        """Initializes the AsyncChat class with the provided OpenAI client.

        :param client: The OpenAI client to be used for chat completions.
        :type client: OpenAI
        """
        super().__init__(client)
        self.completions = AsyncChatCompletions(client)


class AsyncChatCompletions(AsyncChatCompletions_):
    """
    The AsyncChatCompletions class is a derived class which extends AsyncChatCompletions_.
    This class is used to handle asynchronous chat completion requests. It provides methods
    to create and manage chat completions in an asynchronous manner.
    """

    def _prepare_chat(self, config_id, config_name, deployment_id, kwargs, model, model_name, model_version):
        proxy_client: BaseProxyClient = self._client.proxy_client
        model_name = if_set(model_name, if_set(model))
        model_identification = kwargs_if_set(
            deployment_id=deployment_id,
            model_name=model_name,
            model_version=model_version,
            config_id=config_id,
            config_name=config_name,
        )
        deployment = proxy_client.select_deployment(**model_identification)
        model_name = deployment.model_name or '???'

        # Reasoning models do not support temperature
        if not self.supports_temperature(model_name) and 'temperature' in kwargs:
            kwargs.pop('temperature')
        # Cohere models do not support the 'n' and 'max_completion_tokens' parameters
        if model_name and re.search(COHERE_MODEL_PATTERN, model_name):
            kwargs.pop('n', None)
            kwargs.pop('max_completion_tokens', None)

        return deployment, model_name

    async def create(self,
                     *,
                     messages: List[ChatCompletionMessageParam],
                     model: str | None | NotGiven = NOT_GIVEN,
                     deployment_id: str | None | NotGiven = NOT_GIVEN,
                     model_name: str | None | NotGiven = NOT_GIVEN,
                     model_version: str | None | NotGiven = NOT_GIVEN,
                     config_id: str | None | NotGiven = NOT_GIVEN,
                     config_name: str | None | NotGiven = NOT_GIVEN,
                     **kwargs) -> ChatCompletion:
        """Asynchronously creates a new chat completion.

        :param messages: the list of chat completion message parameters.
        :type messages: List[ChatCompletionMessageParam]
        :param model: the model to be used, defaults to NOT_GIVEN
        :type model: str | None | NotGiven, optional
        :param deployment_id: the deployment id, defaults to NOT_GIVEN
        :type deployment_id: str | None | NotGiven, optional
        :param model_name: the model name, defaults to NOT_GIVEN
        :type model_name: str | None | NotGiven, optional
        :param model_version: the model version, defaults to NOT_GIVEN
        :type model_version: str | None | NotGiven, optional
        :param config_id: the configuration id, defaults to NOT_GIVEN
        :type config_id: str | None | NotGiven, optional
        :param config_name: the configuration name, defaults to NOT_GIVEN
        :type config_name: str | None | NotGiven, optional
        :return: the created chat completion.
        :rtype: ChatCompletion
        """
        deployment, model_name = self._prepare_chat(config_id, config_name, deployment_id, kwargs, model, model_name,
                                                    model_version)

        with set_deployment(deployment):
            return await super().create(messages=messages, model=model_name, **kwargs)

    async def parse(self,
                    *,
                    messages: Iterable[ChatCompletionMessageParam],
                    model: str | None | NotGiven = NOT_GIVEN,
                    deployment_id: str | None | NotGiven = NOT_GIVEN,
                    model_name: str | None | NotGiven = NOT_GIVEN,
                    model_version: str | None | NotGiven = NOT_GIVEN,
                    config_id: str | None | NotGiven = NOT_GIVEN,
                    config_name: str | None | NotGiven = NOT_GIVEN,
                    response_format: type[ResponseFormatT] | NotGiven = NOT_GIVEN,
                    **kwargs) -> ParsedChatCompletion[ResponseFormatT]:
        """Asynchronously parses chat completions using the provided parameters and 
        returns a ParsedChatCompletion object.
        This method provides richer integrations with Python specific types by converting pydantic models
        into JSON schemas and parsing the response content back into the given model.

        :param messages: the list of chat completion message parameters.
        :type messages: Iterable[ChatCompletionMessageParam]
        :param model: the model to use for chat completion, defaults to NOT_GIVEN
        :type model: str | None | NotGiven, optional
        :param deployment_id: the deployment ID to use for chat completion, defaults to NOT_GIVEN
        :type deployment_id: str | None | NotGiven, optional
        :param model_name: the model name to use for chat completion, defaults to NOT_GIVEN
        :type model_name: str | None | NotGiven, optional
        :param model_version: the model version to use for chat completion, defaults to NOT_GIVEN
        :type model_version: str | None | NotGiven, optional
        :param config_id: the configuration ID to use for chat completion, defaults to NOT_GIVEN
        :type config_id: str | None | NotGiven, optional
        :param config_name: the configuration name to use for chat completion, defaults to NOT_GIVEN
        :type config_name: str | None | NotGiven, optional
        :param response_format: the response format type for structured output, defaults to NOT_GIVEN
        :type response_format: type[ResponseFormatT] | NotGiven, optional
        :return: the parsed chat completion with the structured response.
        :rtype: ParsedChatCompletion[ResponseFormatT]
        """
        deployment, model_name = self._prepare_chat(config_id, config_name, deployment_id, kwargs, model, model_name,
                                                    model_version)

        with set_deployment(deployment):
            return await super().parse(messages=messages, model=model_name, response_format=response_format, **kwargs)

    @staticmethod
    def supports_temperature(model_name: str) -> bool:
        """Checks if the given model supports the `temperature` parameter.
        Reasoning models do not support temperature e.g., o1[-mini], o3[-mini], cohere--command-a-reasoning

        :param model_name: the name of the model to check.
        :type model_name: str
        :return: True if the model supports `temperature`, False otherwise
        :rtype: bool
        """
        return (not re.search(O_SERIES_MODEL_PATTERN, model_name)
                and not re.search(GPT_5_MODEL_PATTERN, model_name)
                and not re.search(COHERE_REASONING_MODEL_PATTERN, model_name))


class AsyncResponses(AsyncResponses_):
    """
        The asynch Responses class is a subclass of AsyncResponses_.
        It provides a way to create a response for the given input and certain other configurations.
        It extends from the base class AsyncResponses_ and overrides the create method to cater to the specific
        requirements.
    """

    def _prepare_chat(self, config_id, config_name, deployment_id, kwargs, model, model_name, model_version):
        """
        Prepares the deployment and model name for the create and parse responses request.

        Args:
            config_id: The configuration ID to use for chat completion
            config_name: The configuration name to use for chat completion
            deployment_id: The deployment ID to use for chat completion
            kwargs: Keyword arguments dictionary that may be modified
            model: The model to use for chat completion
            model_name: The model name to use for chat completion,
            model_version: The model version to use for chat completion

        Returns:
            tuple: (deployment, model_name) prepared for the request
        """
        proxy_client: BaseProxyClient = self._client.proxy_client
        model_name = if_set(model_name, if_set(model))
        model_identification = kwargs_if_set(
            deployment_id=deployment_id,
            model_name=model_name,
            model_version=model_version,
            config_id=config_id,
            config_name=config_name,
        )
        deployment = proxy_client.select_deployment(**model_identification)
        model_name = deployment.model_name or '???'
        # Reasoning models do not support temperature
        if not self.supports_temperature(model_name) and 'temperature' in kwargs:
            kwargs.pop('temperature')
        # Cohere models do not support the 'n' and 'max_completion_tokens' parameters
        if model_name and re.search(COHERE_MODEL_PATTERN, model_name):
            kwargs.pop('n', None)
            kwargs.pop('max_completion_tokens', None)
        return deployment, model_name

    async def create(self,
               *,
               input: str | ResponseInputParam | Omit = None,
               instructions: str | Omit = None,
               model: str | None | NotGiven = NOT_GIVEN,
               deployment_id: str | None | NotGiven = NOT_GIVEN,
               model_name: str | None | NotGiven = NOT_GIVEN,
               model_version: str | None | NotGiven = NOT_GIVEN,
               config_id: str | None | NotGiven = NOT_GIVEN,
               config_name: str | None | NotGiven = NOT_GIVEN,
               **kwargs) -> Response | AsyncStream[ResponseStreamEvent]:
        """Async method that creates a response based on the provided parameters. It uses a proxy client to select a
        deployment and then calls the create method of the parent class to generate a response.

        :param input: Text, image, or file inputs to the model, used to generate a response, defaults to NOT_GIVEN
        :type input: str | ResponseInputParam | None | NotGiven, optional
        :param instructions: A system (or developer) message inserted into the model's context, defaults to NOT_GIVEN
        :type instructions: str | None | NotGiven, optional
        :param model: the model to be used for the completion, defaults to NOT_GIVEN
        :type model: str | None | NotGiven, optional
        :param deployment_id: the deployment id, defaults to NOT_GIVEN
        :type deployment_id: str | None | NotGiven, optional
        :param model_name: the model name, defaults to NOT_GIVEN
        :type model_name: str | None | NotGiven, optional
        :param model_version: the model version, defaults to NOT_GIVEN
        :type model_version: str | None | NotGiven, optional
        :param config_id: the configuration id, defaults to NOT_GIVEN
        :type config_id: str | None | NotGiven, optional
        :param config_name: the configuration name, defaults to NOT_GIVEN
        :type config_name: str | None | NotGiven, optional
        :return: the response or stream of responsess created based on the provided input.
        :rtype: Response | AsyncStream[ResponseStreamEvent]:
        """
        deployment, model_name = self._prepare_chat(config_id, config_name, deployment_id, kwargs, model, model_name,
                                                    model_version)

        with set_deployment(deployment):
            kwargs.pop("root_client", None)
            kwargs.pop("root_async_client", None)
            return await super().create(instructions=instructions, input=input, model=model_name, **kwargs)

    async def parse(
        self,
            *,
            input: str | ResponseInputParam | Omit = None,
            instructions: str | Omit = None,
            model: str | None | NotGiven = NOT_GIVEN,
            deployment_id: str | None | NotGiven = NOT_GIVEN,
            model_name: str | None | NotGiven = NOT_GIVEN,
            model_version: str | None | NotGiven = NOT_GIVEN,
            config_id: str | None | NotGiven = NOT_GIVEN,
            config_name: str | None | NotGiven = NOT_GIVEN,
            **kwargs) -> ParsedResponse[TextFormatT]:
        """Async parses responses using the provided parameters and returns a ParsedResponse object.
        This method provides richer integrations with Python specific types by converting pydantic models
        into JSON schemas and parsing the response content back into the given model

        :param input: Text, image, or file inputs to the model, used to generate a response, defaults to NOT_GIVEN
        :type input: str | ResponseInputParam | None | NotGiven, optional
        :param instructions: A system (or developer) message inserted into the model's context, defaults to NOT_GIVEN
        :type instructions: str | None | NotGiven, optional
        :param model: the model to be used for the completion, defaults to NOT_GIVEN
        :type model: str | None | NotGiven, optional
        :param deployment_id: the deployment id, defaults to NOT_GIVEN
        :type deployment_id: str | None | NotGiven, optional
        :param model_name: the model name, defaults to NOT_GIVEN
        :type model_name: str | None | NotGiven, optional
        :param model_version: the model version, defaults to NOT_GIVEN
        :type model_version: str | None | NotGiven, optional
        :param config_id: the configuration id, defaults to NOT_GIVEN
        :type config_id: str | None | NotGiven, optional
        :param config_name: the configuration name, defaults to NOT_GIVEN
        :type config_name: str | None | NotGiven, optional
        :return: ParsedResponse object
        :rtype: ParsedResponse
        """

        deployment, model_name = self._prepare_chat(config_id, config_name, deployment_id, kwargs, model, model_name,
                                                    model_version)

        with set_deployment(deployment):
            kwargs.pop("root_client", None)
            kwargs.pop("root_async_client", None)
            return await super().parse(instructions=instructions, input=input, model=model_name, **kwargs)

    @staticmethod
    def supports_temperature(model_name: str) -> bool:
        """Checks if the given model supports the `temperature` parameter.
        Reasoning models do not support temperature e.g., o1[-mini], o3[-mini], 5[-mini, -nano],
        cohere--command-a-reasoning

        :param model_name: the name of the model to check.
        :type model_name: str
        :return: True if the model supports `temperature`, False otherwise
        :rtype: bool
        """
        return (not re.search(O_SERIES_MODEL_PATTERN, model_name)
                and not re.search(GPT_5_MODEL_PATTERN, model_name)
                and not re.search(COHERE_REASONING_MODEL_PATTERN, model_name))

class OpenAIWithRawResponse:
    """
    This class is a wrapper for the OpenAI API client that provides raw responses.
    Note: The properties 'edits', 'files', 'images', 'audio', 'moderations', 'models',
    'fine_tuning', 'fine_tunes' and 'beta' are placeholders and currently do not provide any
    functionality.

    Attributes:
        completions: An instance of CompletionsWithRawResponse class.

        chat: An instance of ChatWithRawResponse class.

        edits: Not currently used.

        embeddings: An instance of EmbeddingsWithRawResponse class if client.embeddings is not None.

        files: Not currently used.

        images: Not currently used.

        audio: Not currently used.

        moderations: Not currently used.

        models: Not currently used.

        fine_tuning: Not currently used.

        fine_tunes: Not currently used.

        beta: Not currently used.

    The class is designed to provide the raw responses from OpenAI's API endpoints. It currently supports completions,
    chat, and embeddings endpoints.
    """

    def __init__(self, client: OpenAI) -> None:
        """Initializes the OpenAIWithRawResponse class with the provided OpenAI client.

        :param client: An instance of OpenAI client.
        :type client: OpenAI
        """
        self.completions = resources.CompletionsWithRawResponse(client.completions)
        self.chat = resources.ChatWithRawResponse(client.chat)
        self.edits = None
        self.embeddings = resources.EmbeddingsWithRawResponse(client.embeddings) if client.embeddings else None
        self.files = None
        self.images = None
        self.audio = None
        self.moderations = None
        self.models = None
        self.fine_tuning = None
        self.fine_tunes = None
        self.beta = self  # required for structure_outputs when using langchain


class AsyncOpenAIWithRawResponse:
    """
    A class that provides an asynchronous interface to the OpenAI API, returning raw responses.

    This class wraps the core functionality of OpenAI's API, offering access to completions,
    chat capabilities, and embeddings. It is designed to work with OpenAI's asynchronous client,
    allowing for concurrent requests to the API.

    Note: The properties 'edits', 'files', 'images', 'audio', 'moderations', 'models',
    'fine_tuning', 'fine_tunes' and 'beta' are placeholders and currently do not provide any
    functionality.

    Attributes:
        completions: An instance of `resources.AsyncCompletionsWithRawResponse` for managing completions with the API.
        
        chat: An instance of `resources.AsyncChatWithRawResponse` for managing chat with the API.

        embeddings: An instance of `resources.AsyncEmbeddingsWithRawResponse` for managing embeddings with the API.

        edits: Currently a placeholder with no functionality.
    
        files: Currently a placeholder with no functionality.
    
        images: Currently a placeholder with no functionality.
    
        audio: Currently a placeholder with no functionality.
    
        moderations: Currently a placeholder with no functionality.
    
        models: Currently a placeholder with no functionality.
    
        fine_tuning: Currently a placeholder with no functionality.
    
        fine_tunes: Currently a placeholder with no functionality.
    
        beta: Currently a placeholder with no functionality.
    """

    def __init__(self, client: AsyncOpenAI) -> None:
        """Initializes the AsyncOpenAIWithRawResponse class with the provided AsyncOpenAI client.

        :param client: An instance of AsyncOpenAI client.
        :type client: AsyncOpenAI
        """
        self.completions = resources.AsyncCompletionsWithRawResponse(client.completions)
        self.chat = resources.AsyncChatWithRawResponse(client.chat)
        self.edits = None
        self.embeddings = resources.AsyncEmbeddingsWithRawResponse(client.embeddings)
        self.files = None
        self.images = None
        self.audio = None
        self.moderations = None
        self.models = None
        self.fine_tuning = None
        self.fine_tunes = None
        self.beta = None


def _prepare_url(url: str) -> httpx.URL:
    deployment = get_current_deployment()
    prediction_url = deployment.prediction_url
    if prediction_url:
        return httpx.URL(prediction_url)

    url = httpx.URL(url)
    if url.is_relative_url:
        deployment_url = httpx.URL(get_current_deployment().url.rstrip('/') + '/')
        url = deployment_url.raw_path + url.raw_path.lstrip(b"/")
        return deployment_url.copy_with(raw_path=url)
    return url


class OpenAI(OpenAI_):
    """
    This is a class for the OpenAI API client. It is designed to handle various services provided by OpenAI such as text
     completions, chat, embeddings etc.

    Attributes:
        proxy_client (BaseProxyClient, optional): An instance of a Proxy Client. Defaults to None.

        api_version (str, optional): API version used for OpenAI API calls. Defaults to DEFAULT_API_VERSION.

        completions (Completions): An instance of the Completions class for text generation.

        chat (Chat): An instance of the Chat class for conversation.

        edits: Placeholder for future use. Currently set to None.

        embeddings (Embeddings): An instance of the Embeddings class for getting text embeddings.

        files: Placeholder for future use. Currently set to None.

        images: Placeholder for future use. Currently set to None.

        audio: Placeholder for future use. Currently set to None.

        moderations: Placeholder for future use. Currently set to None.

        models: Placeholder for future use. Currently set to None.

        fine_tuning: Placeholder for future use. Currently set to None.

        fine_tunes: Placeholder for future use. Currently set to None.

        beta: Placeholder for future use. Currently set to None.

        with_raw_response (OpenAIWithRawResponse): An instance of the OpenAIWithRawResponse class for returning raw
        responses from the API.
    """

    def __init__(self,
                 *,
                 proxy_client: Optional[BaseProxyClient] = None,
                 api_version: Optional[str] = DEFAULT_API_VERSION,
                 **kwargs) -> None:
        """Initializes the OpenAI API client with the provided parameters.

        :param proxy_client: An instance of a Proxy Client. Defaults to None.
        :type proxy_client: Optional[BaseProxyClient], optional
        :param api_version: API version used for OpenAI API calls. Defaults to DEFAULT_API_VERSION.
        :type api_version: Optional[str], optional
        """
        self.proxy_client = proxy_client or get_proxy_client()
        for kwarg in ('api_key', 'organization', 'base_url'):
            kwargs.pop(kwarg, None)
        default_query = {'api-version': api_version or DEFAULT_API_VERSION, **kwargs.pop('default_query', {})}
        super().__init__(api_key='???', base_url='???', organization='???', default_query=default_query, **kwargs)

        self.completions = Completions(self)
        self.chat = Chat(self)
        self.edits = None
        self.embeddings = Embeddings(self)
        self.files = None
        self.images = None
        self.audio = None
        self.moderations = None
        self.models = None
        self.fine_tuning = None
        self.fine_tunes = None
        self.beta = self  # required for structure_outputs when using langchain
        self.with_raw_response = OpenAIWithRawResponse(self)
        self.responses = Responses(self)

    @property
    def default_headers(self) -> dict[str, str | Omit]:
        headers = super().default_headers
        headers.update(self.proxy_client.request_header)
        return headers

    def _prepare_url(self, url: str) -> httpx.URL:
        return _prepare_url(url)

    def request(self, cast_to, options, *args, **kwargs):
        options.json_data.update(get_current_deployment().additional_request_body_kwargs())
        return super().request(cast_to, options, *args, **kwargs)


class AsyncOpenAI(AsyncOpenAI_):
    """
    An async version of the OpenAI API client.

    This class is used to interact with the OpenAI API asynchronously. It supports various operations like creating
    completions, generating chat messages, and getting embeddings.

    Attributes:
        proxy_client (BaseProxyClient): A proxy client to make API requests. If not provided, a default one will be
        created.

        api_version (str, optional): The version of the OpenAI API to use. Default is defined by DEFAULT_API_VERSION.

        completions (AsyncCompletions): A client for interacting with the OpenAI API's completions.

        chat (AsyncChat): A client for interacting with the OpenAI API's chat.

        edits (None): Placeholder for future support of "edits" operations.

        embeddings (AsyncEmbeddings): A client for interacting with the OpenAI API's embeddings.

        files (None): Placeholder for future support of "files" operations.

        images (None): Placeholder for future support of "images" operations.

        audio (None): Placeholder for future support of "audio" operations.

        moderations (None): Placeholder for future support of "moderations" operations.

        models (None): Placeholder for future support of "models" operations.

        fine_tuning (None): Placeholder for future support of "fine_tuning" operations.

        fine_tunes (None): Placeholder for future support of "fine_tunes" operations.
        beta (None): Placeholder for future support of "beta" operations.
        with_raw_response (AsyncOpenAIWithRawResponse): A client that returns raw API responses.
    """

    def __init__(self,
                 *,
                 proxy_client: Optional[BaseProxyClient] = None,
                 api_version: Optional[str] = DEFAULT_API_VERSION,
                 **kwargs) -> None:
        """Initializes the AsyncOpenAI client with the provided parameters.

        :param proxy_client: An instance of a Proxy Client. Defaults to None.
        :type proxy_client: Optional[BaseProxyClient], optional
        :param api_version: API version used for OpenAI API calls. Defaults to DEFAULT_API_VERSION.
        :type api_version: Optional[str], optional
        """
        self.proxy_client = proxy_client or get_proxy_client()
        for kwarg in ('api_key', 'organization', 'base_url'):
            kwargs.pop(kwarg, None)
        default_query = {'api-version': api_version or DEFAULT_API_VERSION, **kwargs.pop('default_query', {})}
        super().__init__(api_key='???', base_url='???', organization='???', default_query=default_query, **kwargs)

        self.completions = AsyncCompletions(self)
        self.chat = AsyncChat(self)
        self.edits = None
        self.embeddings = AsyncEmbeddings(self)
        self.files = None
        self.images = None
        self.audio = None
        self.moderations = None
        self.models = None
        self.fine_tuning = None
        self.fine_tunes = None
        self.beta = self  # required for structure_outputs when using langchain
        self.with_raw_response = AsyncOpenAIWithRawResponse(self)
        self.responses = AsyncResponses(self)

    @property
    def default_headers(self) -> dict[str, str | Omit]:
        headers = super().default_headers
        headers.update(self.proxy_client.request_header)
        return headers

    def _prepare_url(self, url: str) -> httpx.URL:
        return _prepare_url(url)

    def request(self, cast_to, options, *args, **kwargs):
        """Overrides the request method to include additional request body kwargs from the current deployment.

        :param cast_to: the type to cast the response to.
        :type cast_to: any
        :param options: the request options.
        :type options: any
        :return: the response from the request.
        :rtype: CoroutineType[Any, Any, ResponseT@request]
        """
        options.json_data.update(get_current_deployment().additional_request_body_kwargs())
        return super().request(cast_to, options, *args, **kwargs)
