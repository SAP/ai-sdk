# Streaming

Streaming in AI models enables real-time data generation. With native SDKs, invocation and response formats vary by provider and model. LangChain simplifies this by offering a unified `stream` method.

## Native SDKs[​](#native-sdks "Direct link to Native SDKs")

### OpenAI[​](#openai "Direct link to OpenAI")

```
from gen_ai_hub.proxy.native.openai import chat



def stream_openai(prompt, model_name='gpt-4o-mini'):

    messages = [

        {"role": "system", "content": "You are a helpful assistant."},

        {"role": "user", "content": prompt}

    ]

    kwargs = dict(model_name=model_name, messages=messages, max_tokens=500, stream=True)

    stream = chat.completions.create(**kwargs)

    for chunk in stream:

        if chunk.choices:

            content = chunk.choices[0].delta.content

            if content:

                print(content, end='')



stream_openai("Why is the sky blue?")
```

#### Structured model outputs[​](#structured-model-outputs "Direct link to Structured model outputs")

```
from gen_ai_hub.proxy import get_proxy_client

from gen_ai_hub.proxy.native.openai import chat, OpenAI

from pydantic import BaseModel



class Person(BaseModel):

    name: str

    age: int



messages = [{"role": "user", "content": "Tell me about John Doe, aged 30."}]



def stream_openai_structured_outputs(messages, response_object, model_name):

    with chat.completions.with_streaming_response.parse(

        model=model_name,

        messages=messages,

        response_format=Person

    ) as stream:

        response = stream.parse()

    return response.choices[0].message.parsed



print(stream_openai_structured_outputs(messages, Person, "gpt-4o-mini"))
```

```
def stream_beta_openai_structured_outputs(messages, response_object, model_name):

    chat = OpenAI(proxy_client=get_proxy_client())

    with chat.beta.chat.completions.stream(

        model=model_name,

        messages=messages,

        response_format=Person

    ) as stream:

        response = stream.get_final_completion()

    return response.choices[0].message.parsed



print(stream_beta_openai_structured_outputs(messages, Person, "gpt-4o-mini"))
```

### Google GenAI[​](#google-genai "Direct link to Google GenAI")

```
from gen_ai_hub.proxy import get_proxy_client

from gen_ai_hub.proxy.native.google_genai import Client

from google.genai.types import GenerateContentConfig



def stream_genai(prompt, model_name='gemini-2.0-flash'):

    proxy_client = get_proxy_client('gen-ai-hub')

    client = Client(proxy_client=proxy_client)

    response = client.models.generate_content_stream(

        model=model_name,

        contents=prompt,

        config=GenerateContentConfig(max_output_tokens=500),

    )

    for chunk in response:

        print(chunk.text, end='')



stream_genai("Why is the sky blue?")
```

### Anthropic (via Amazon)[​](#anthropic-via-amazon "Direct link to Anthropic (via Amazon)")

```
import json

from gen_ai_hub.proxy.native.amazon import Session



def stream_claude(prompt, model_name='anthropic--claude-3-haiku'):

    bedrock = Session().client(model_name=model_name)

    body = json.dumps({

        "max_tokens": 500,

        "messages": [{"role": "user", "content": prompt}],

        "anthropic_version": "bedrock-2023-05-31"

    })

    response = bedrock.invoke_model_with_response_stream(body=body)

    stream = response.get("body")

    for event in stream:

        chunk = json.loads(event["chunk"]["bytes"])

        if chunk["type"] == "content_block_delta":

            print(chunk["delta"].get("text", ""), end="")



stream_claude("Why is the sky blue?")
```

### Amazon Bedrock[​](#amazon-bedrock "Direct link to Amazon Bedrock")

```
import json

from gen_ai_hub.proxy.native.amazon import Session



def stream_bedrock(prompt, model_name='amazon--nova-pro'):

    bedrock = Session().client(model_name=model_name)

    body = json.dumps({

        "schemaVersion": "messages-v1",

        "messages": [{"role": "user", "content": [{"text": prompt}]}],

        "system": [{"text": "Act as a creative writing assistant."}],

        "inferenceConfig": {"maxTokens": 500, "topP": 0.9, "topK": 20, "temperature": 0.7},

    })

    response = bedrock.invoke_model_with_response_stream(body=body)

    stream = response.get("body")

    answer = ""

    if stream:

        for event in stream:

            chunk = event.get("chunk")

            if chunk:

                chunk_json = json.loads(chunk.get("bytes").decode())

                content_block_delta = chunk_json.get("contentBlockDelta")

                if content_block_delta:

                    answer += content_block_delta.get("delta").get("text")

        print("Final answer:", answer)



stream_bedrock("Why is the sky blue?")
```

## LangChain[​](#langchain "Direct link to LangChain")

```
from gen_ai_hub.proxy.langchain import init_llm



def stream_langchain(prompt, model_name):

    llm = init_llm(model_name=model_name, max_tokens=500)

    for chunk in llm.stream(prompt):

        print(chunk.content, end='')



stream_langchain("How do airplanes stay in the air?", model_name='gpt-4o-mini')

stream_langchain("How do airplanes stay in the air?", model_name='gemini-2.0-flash')

stream_langchain("How do airplanes stay in the air?", model_name='anthropic--claude-3-haiku')

stream_langchain("How do airplanes stay in the air?", model_name='amazon--nova-premier')
```
