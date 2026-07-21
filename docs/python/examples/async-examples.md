# Async Examples

## Async Amazon Native[​](#async-amazon-native "Direct link to Async Amazon Native")

### Invoke Model[​](#invoke-model "Direct link to Invoke Model")

```
import json

from gen_ai_hub.proxy.native.amazon import AsyncSession



async def async_bedrock_invoke_model():

    session = AsyncSession()

    bedrock = await session.async_client(model_name="amazon--nova-premier")

    body = json.dumps({

        "inputText": "Explain black holes to 8th graders.",

        "textGenerationConfig": {"maxTokenCount": 300, "stopSequences": [], "temperature": 0.0, "topP": 0.9},

    })

    response = await bedrock.invoke_model(body=body)

    response_body = json.loads(await response.get("body").read())

    print("Response:", response_body)

    await bedrock.close()



await async_bedrock_invoke_model()
```

### Streaming[​](#streaming "Direct link to Streaming")

```
async def async_bedrock_invoke_with_stream():

    session = AsyncSession()

    bedrock = await session.async_client(model_name="amazon--nova-premier")

    body = json.dumps({

        "inputText": "You are a story teller. Tell me a short story about boats.",

        "textGenerationConfig": {"maxTokenCount": 300, "stopSequences": [], "temperature": 0.0, "topP": 0.9},

    })

    async for event in bedrock.invoke_model_with_response_stream(body=body):

        for line in event["chunk"]["bytes"].splitlines():

            if line and line.startswith(b"data: "):

                chunk = json.loads(line[6:])

                if "outputText" in chunk:

                    print("Chunk Output:", chunk["outputText"])



await async_bedrock_invoke_with_stream()
```

### Converse[​](#converse "Direct link to Converse")

```
async def async_amazon_bedrock_converse(model_name):

    session = AsyncSession()

    bedrock = await session.async_client(model_name=model_name)

    conversation = [{"role": "user", "content": [{"text": "Describe the purpose of a 'hello world' program in one line."}]}]

    response = await bedrock.converse(

        messages=conversation,

        inferenceConfig={"maxTokens": 512, "temperature": 0.0, "topP": 0.9},

    )

    print("Response:", response["output"]["message"]["content"][0]["text"])

    await bedrock.close()



await async_amazon_bedrock_converse("amazon--nova-premier")
```

### Embeddings[​](#embeddings "Direct link to Embeddings")

```
async def async_amazon_titan_embedding(model_name):

    session = AsyncSession()

    bedrock = await session.async_client(model_name=model_name)

    body = json.dumps({"inputText": "Please recommend books with a theme similar to the movie 'Inception'."})

    response = await bedrock.invoke_model(body=body)

    response_body = json.loads(await response.get("body").read())

    print("Embedding:", response_body["embedding"])

    await bedrock.close()



await async_amazon_titan_embedding("amazon--titan-embed-text")
```

## Async Google GenAI Native[​](#async-google-genai-native "Direct link to Async Google GenAI Native")

### Generate Content[​](#generate-content "Direct link to Generate Content")

```
from gen_ai_hub.proxy.native.google_genai import Client

from gen_ai_hub.proxy import get_proxy_client



proxy_client = get_proxy_client('gen-ai-hub')

async with Client(proxy_client=proxy_client).aio as aclient:

    response = await aclient.models.generate_content(

        model="gemini-2.5-flash",

        contents="Explain the relativity theory in simple terms."

    )

print(response)
```

### Chat[​](#chat "Direct link to Chat")

```
async with Client(proxy_client=proxy_client).aio as aclient:

    chat_session = aclient.chats.create(model="gemini-2.5-flash")

    response1 = await chat_session.send_message("Hello.")

    print("Response 1:", response1.text)

    response2 = await chat_session.send_message("What is your opinion about the latest Gemini model?")

    print("Response 2:", response2.text)
```

### Streaming[​](#streaming-1 "Direct link to Streaming")

```
from google.genai.types import GenerateContentConfig, Content, Part



proxy_client = get_proxy_client('gen-ai-hub')

async with Client(proxy_client=proxy_client).aio as aclient:

    async_response_stream = await aclient.models.generate_content_stream(

        model="gemini-2.5-flash",

        contents=[Content(role="user", parts=[Part(text="Write a paragraph about a magic kingdom.")])],

        config=GenerateContentConfig(temperature=0),

    )

    async for chunk in async_response_stream:

        print("Chunk:", chunk.text)
```

## LangChain Async Examples[​](#langchain-async-examples "Direct link to LangChain Async Examples")

### Async Chat (Amazon Bedrock)[​](#async-chat-amazon-bedrock "Direct link to Async Chat (Amazon Bedrock)")

```
from langchain_core.messages import HumanMessage, AIMessage

from gen_ai_hub.proxy.langchain import ChatBedrock



async def async_amazon_chat_model():

    chat_model = ChatBedrock(model_name="anthropic--claude-3-haiku", model_kwargs={"temperature": 0.0})

    response = await chat_model.ainvoke([HumanMessage(content="Write me a song about sparkling water.")])

    if isinstance(response, AIMessage):

        print("Response:", response.content)



await async_amazon_chat_model()
```

### Async Streaming (Amazon Bedrock)[​](#async-streaming-amazon-bedrock "Direct link to Async Streaming (Amazon Bedrock)")

```
from langchain_core.messages import AIMessageChunk

from gen_ai_hub.proxy.langchain import ChatBedrock



async def async_chat_streaming():

    chat_model = ChatBedrock(

        model_name="anthropic--claude-3-haiku",

        model_kwargs={"temperature": 0.0},

        streaming=True

    )

    async for chunk in chat_model.astream([HumanMessage(content="Write me a song about sparkling water in 20 words.")]):

        print(chunk.content)



await async_chat_streaming()
```

### Async Chat (Amazon Bedrock Converse)[​](#async-chat-amazon-bedrock-converse "Direct link to Async Chat (Amazon Bedrock Converse)")

```
from gen_ai_hub.proxy.langchain import ChatBedrockConverse



async def chat_converse_model_example(model_name):

    chat_model = ChatBedrockConverse(model_name=model_name, model_kwargs={"temperature": 0.0})

    response = await chat_model.ainvoke([HumanMessage(content="Write me a song about sparkling water.")])

    if isinstance(response, AIMessage):

        print("Response:", response.content)



await chat_converse_model_example("anthropic--claude-3-haiku")
```

### Async Gemini[​](#async-gemini "Direct link to Async Gemini")

```
from gen_ai_hub.proxy.langchain import init_llm



async def gemini_ainvoke_example():

    llm = init_llm(model_name="gemini-2.0-flash", max_tokens=300)

    response = await llm.ainvoke("Write a ballad about LangChain")

    print(response)



await gemini_ainvoke_example()
```

### Async Gemini Streaming[​](#async-gemini-streaming "Direct link to Async Gemini Streaming")

```
from gen_ai_hub.proxy.langchain import ChatGoogleGenerativeAI



async def gemini_astream_example():

    chat_model = ChatGoogleGenerativeAI(proxy_model_name="gemini-2.0-flash", temperature=0)

    async for chunk in chat_model.astream("Write a story about a magic backpack."):

        print("Chunk:", chunk.content)



await gemini_astream_example()
```
