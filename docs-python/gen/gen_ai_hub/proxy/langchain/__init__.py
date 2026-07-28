from .init_models import init_embedding_model, init_llm
from .openai import OpenAI, OpenAIEmbeddings, OpenAIClient, AsyncOpenAIClient, ChatOpenAI
from .amazon import BedrockEmbeddings, AICoreBedrockBaseModel, ChatBedrock, ChatBedrockConverse
from .google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Make sure that the user has a recent version of langchain installed
_langchain_is_below_0_1_0 = None
try:
    import langchain
except ImportError:
    pass
else:
    from packaging import version
    _langchain_is_below_0_1_0 = version.parse(langchain.__version__) < version.parse('0.1.0')
    if _langchain_is_below_0_1_0:
        raise ImportError('langchain<0.1.0 is no longer supported. Please upgrade to version 0.1.0 or higher.')


__all__ = [
    'init_llm',
    'init_embedding_model',
    'OpenAIClient',
    'OpenAIEmbeddings',
    'AsyncOpenAIClient',
    'ChatOpenAI',
    'BedrockEmbeddings',
    'AICoreBedrockBaseModel',
    'ChatBedrock',
    'ChatBedrockConverse',
    'ChatGoogleGenerativeAI',
    'GoogleGenerativeAIEmbeddings',
    'OpenAI'
]

try:
    from .openai import ChatOpenAI, OpenAI, OpenAIEmbeddings
    __all__.extend(['ChatOpenAI', 'OpenAI', 'OpenAIEmbeddings'])
except ImportError:
    pass

try:
    from .amazon import ChatBedrock
    __all__.append('ChatBedrock')
except ImportError:
    pass

try:
    from .google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
    __all__.extend(['ChatGoogleGenerativeAI', 'GoogleGenerativeAIEmbeddings'])
except ImportError:
    pass
