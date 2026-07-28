from typing import Optional, Union
import httpx
from google.genai import Client as GoogleClient
from google.genai import types
from google.genai.models import Models as GoogleModels
from google.oauth2.credentials import Credentials

from gen_ai_hub.proxy.core.base import BaseProxyClient
from gen_ai_hub.proxy.core.proxy_clients import get_proxy_client
from gen_ai_hub.proxy.core.utils import kwargs_if_set

_deployment_cache = {}

def _resolve_deployment(transport_instance, requested_model_name: str):
    """
    Finds the appropriate AI Core deployment based on the model name and any filtering kwargs in model_identification.
    """

    if requested_model_name in _deployment_cache:
        return _deployment_cache[requested_model_name]

    model_identification = transport_instance.get_selector_kwargs().copy()

    model_identification['model_name'] = requested_model_name

    if requested_model_name == "gemini-embedding-001":
        model_identification['model_name'] = "gemini-embedding"

    deployment = transport_instance.proxy_client.select_deployment(**model_identification)

    _deployment_cache[requested_model_name] = deployment
    return deployment


def _rewrite_request(transport_instance, request: httpx.Request):
    """Interception and rewriting of the request. Handles dynamic routing, header injection, etc."""

    path = request.url.path

    if "/models/" not in path:
        return request

    _, suffix = path.split("/models/", 1)

    # If the path ends at /models (suffix is empty) or /models? (suffix starts with ?),
    # it is a discovery call, not an inference call, and cannot be routed through SAP AI Core.
    if not suffix or suffix.startswith("/") or suffix.startswith("?"):
        return request

    # Suffix is like "{model_name}:generateContent"
    if ":" in suffix:
        model_name = suffix.split(":")[0]
    else:
        model_name = suffix

    deployment = _resolve_deployment(transport_instance, model_name)

    deployment_url = httpx.URL(deployment.url)

    # Path construction: deployment_url + /models/ + {model_name}:generateContent
    new_path = f"{deployment_url.path.rstrip('/')}/models/{suffix}"

    request.url = request.url.copy_with(
        scheme=deployment_url.scheme,
        host=deployment_url.host,
        port=deployment_url.port,
        path=new_path,
    )

    proxy_headers = transport_instance.proxy_client.request_header

    # Host must always match the resolved deployment URL host
    request.headers["Host"] = deployment_url.host

    # Authorization is handled explicitly to avoid accidental overrides
    auth = proxy_headers.get("Authorization")
    if auth:
        request.headers["Authorization"] = auth

    # Apply remaining proxy headers defensively
    for header_name, header_value in proxy_headers.items():
        if header_name.lower() not in ("host", "authorization"):
            request.headers[header_name] = header_value

    return request


class AICoreDynamicTransport(httpx.BaseTransport):
    """Synchronous transport that dynamically resolves deployment URLs per request."""

    def __init__(self, proxy_client: BaseProxyClient, **deployment_selector_kwargs):
        """Transport constructor.

        :param proxy_client: The proxy client used to select deployments.
        :type proxy_client: BaseProxyClient
        """
        self.proxy_client = proxy_client
        self._inner_transport = httpx.HTTPTransport()
        self._selector_kwargs = kwargs_if_set(**deployment_selector_kwargs)

    def get_selector_kwargs(self):
        """Get the deployment selector kwargs.

        :return: The deployment selector kwargs.
        :rtype: dict
        """
        return self._selector_kwargs

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        """Handles the request by rewriting it to route through the appropriate AI Core deployment.

        :param request: The original HTTPX request.
        :type request: httpx.Request
        :return: The HTTPX response from the AI Core deployment.
        :rtype: httpx.Response
        """
        modified_request = _rewrite_request(self, request)
        return self._inner_transport.handle_request(modified_request)

    def close(self):
        """Closes the inner transport.""" 
        self._inner_transport.close()


class AsyncAICoreDynamicTransport(httpx.AsyncBaseTransport):
    """Asynchronous transport that dynamically resolves deployment URLs per request."""

    def __init__(self, proxy_client: BaseProxyClient, **deployment_selector_kwargs):
        """Transport constructor.

        :param proxy_client: The proxy client used to select deployments.
        :type proxy_client: BaseProxyClient
        """
        self.proxy_client = proxy_client
        self._inner_transport = httpx.AsyncHTTPTransport()
        self._selector_kwargs = kwargs_if_set(**deployment_selector_kwargs)

    def get_selector_kwargs(self):
        """get the deployment selector kwargs.

        :return: The deployment selector kwargs.
        :rtype: dict
        """
        return self._selector_kwargs

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        """Handles the request by rewriting it to route through the appropriate AI Core deployment.

        :param request: The original HTTPX request.
        :type request: httpx.Request
        :return: The HTTPX response from the AI Core deployment.
        :rtype: httpx.Response
        """
        modified_request = _rewrite_request(self, request)
        return await self._inner_transport.handle_async_request(modified_request)

    async def aclose(self):
        """Closes the inner transport."""
        await self._inner_transport.aclose()

class Models(GoogleModels):
    """
    Class that extends the original Google Models class for patch embed_content method.
    """
    def embed_content(
            self,
            *,
            model: str,
            contents: Union[types.ContentListUnion, types.ContentListUnionDict],
            config: Optional[types.EmbedContentConfigOrDict] = None,
    ) -> types.EmbedContentResponse:
        """Need for add model version for "gemini-embedding" model."""
        if model == "gemini-embedding":
            model = "gemini-embedding-001"
        return super().embed_content(model=model, contents=contents, config=config)

class Client(GoogleClient):
    """
    Unified, native-feeling client that dynamically routes requests
    through SAP AI Core deployments based on the requested identifiers e.g. model name.
    """

    def __init__(
            self,
            # Standard Google Args (kept for compatibility, though placeholders used)
            vertexai: bool = True,
            project: str = "placeholder",
            location: str = "placeholder",
            # AI Core Filtering Args
            deployment_id: str = "",
            config_id: str = "",
            config_name: str = "",
            proxy_client: BaseProxyClient = None,
            timeout: int = None,
            **kwargs
    ):
        """Initializes the Client.

        :param vertexai: to indicate Vertex AI usage, defaults to True
        :type vertexai: bool, optional
        :param project: the GCP project, defaults to "placeholder"
        :type project: str, optional
        :param location: the GCP location, defaults to "placeholder"
        :type location: str, optional
        :param deployment_id: the deployment identifier, defaults to ""
        :type deployment_id: str, optional
        :param config_id: the configuration identifier, defaults to ""
        :type config_id: str, optional
        :param config_name: the configuration name, defaults to ""
        :type config_name: str, optional
        :param proxy_client: the proxy client to use, defaults to None
        :type proxy_client: BaseProxyClient, optional
        :param timeout: the request timeout, defaults to None
        :type timeout: int, optional
        """
        self.proxy_client = proxy_client or get_proxy_client()

        deployment_selector_kwargs = kwargs_if_set(
            deployment_id=deployment_id,
            config_id=config_id,
            config_name=config_name,
        )

        sync_transport = AICoreDynamicTransport(
            proxy_client=self.proxy_client,
            **deployment_selector_kwargs
        )
        async_transport = AsyncAICoreDynamicTransport(
            proxy_client=self.proxy_client,
            **deployment_selector_kwargs
        )

        super().__init__(
            vertexai=True,
            project=project,
            location=location,
            credentials=Credentials(token="dummy-token-placeholder"),
            http_options=types.HttpOptions(
                client_args={
                    "transport": sync_transport
                    },
                async_client_args={
                    "transport": async_transport
                    },
                timeout=timeout,
            ),
            **kwargs
        )
        self._models = Models(self._api_client)
