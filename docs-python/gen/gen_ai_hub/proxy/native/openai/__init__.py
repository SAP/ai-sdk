from typing import Any

import openai
from packaging import version

from gen_ai_hub.proxy.core import get_proxy_version
from .clients import AsyncOpenAI, OpenAI

if version.parse(openai.__version__) < version.parse('1.0.0'):
    raise ImportError(
        f'Found openai=={openai.__version__}. Since v0.2.0 it only supports openai>=1.0.0! Update openai or run `pip install -U openai<1`'
    )
# TODO: Adjust error message


class GlobalClient:
    """A global client to manage OpenAI clients based on proxy version."""

    def __init__(self) -> None:
        self._client = {}

    @property
    def client(self):
        """Get the OpenAI client based on the current proxy version.

        :return: The OpenAI client instance.
        :rtype: OpenAI
        """
        proxy_version = get_proxy_version()
        client = self._client.get(proxy_version, None)
        if not client:
            self._client[proxy_version] = OpenAI()
        return self._client[proxy_version]


_global_client = GlobalClient()


def __getattr__(name: str) -> Any:
    if name in ('completions', 'chat', 'embeddings', "responses"):
        return getattr(_global_client.client, name)
    else:
        return locals().get(name)
