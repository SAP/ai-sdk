# Orchestration Service V2 API

This page demonstrates how to use the SDK with the Orchestration Service V2, enabling AI-driven workflows with modules such as templating, LLMs, data masking, and content filtering.

## Prerequisite[​](#prerequisite "Direct link to Prerequisite")

Before you begin, set up a virtual deployment of the Orchestration Service. See the [setup guide](https://help.sap.com/docs/ai-launchpad/sap-ai-launchpad/create-deployment-for-orchestration).

## Basic Orchestration Pipeline[​](#basic-orchestration-pipeline "Direct link to Basic Orchestration Pipeline")

### Step 1: Define the Template[​](#step-1-define-the-template "Direct link to Step 1: Define the Template")

```
from gen_ai_hub.orchestration_v2 import Template, SystemMessage, UserMessage



template = Template(

    template=[

        SystemMessage(content="You are a helpful translation assistant."),

        UserMessage(content="Translate the following text to {{?to_lang}}: {{?user_query}}"),

    ],

    defaults={"to_lang": "German"}

)
```

### Step 2: Define the LLM[​](#step-2-define-the-llm "Direct link to Step 2: Define the LLM")

```
from gen_ai_hub.orchestration_v2 import LLMModelDetails



llm = LLMModelDetails(name="gpt-5-nano", params={"max_completion_tokens": 512})
```

### Step 3: Create the Configuration[​](#step-3-create-the-configuration "Direct link to Step 3: Create the Configuration")

```
from gen_ai_hub.orchestration_v2 import PromptTemplatingModuleConfig, ModuleConfig, OrchestrationConfig



prompt_template = PromptTemplatingModuleConfig(prompt=template, model=llm)

module_config = ModuleConfig(prompt_templating=prompt_template)

config = OrchestrationConfig(modules=module_config)
```

### Step 4: Run the Request[​](#step-4-run-the-request "Direct link to Step 4: Run the Request")

```
from gen_ai_hub.orchestration_v2 import OrchestrationService



orchestration_service = OrchestrationService(config=config)

result = orchestration_service.run(placeholder_values={"user_query": "The Orchestration Service is working!"})

print(result.final_result.choices[0].message.content)
```

#### Referencing Templates from the Prompt Registry[​](#referencing-templates-from-the-prompt-registry "Direct link to Referencing Templates from the Prompt Registry")

```
from gen_ai_hub.orchestration_v2 import TemplateRefByID, TemplateRefByScenarioNameVersion



template_by_id = TemplateRefByID(id="648871d9-b207-441c-8c13-afee71b0dbec")

template_by_names = TemplateRefByScenarioNameVersion(scenario="translation", name="translate_text", version="0.1.0")
```

#### Response Format Options[​](#response-format-options "Direct link to Response Format Options")

**Text:**

```
from gen_ai_hub.orchestration_v2 import SystemMessage, UserMessage, Template, ResponseFormatText



template = Template(

    template=[SystemMessage(content="You are a helpful assistant."), UserMessage(content="{{?user_query}}")],

    response_format=ResponseFormatText(),

    defaults={"user_query": "Who was the first person on the moon?"}

)
```

**JSON Object:**

```
from gen_ai_hub.orchestration_v2 import ResponseFormatJsonObject



template = Template(

    template=[

        SystemMessage(content="You are a helpful assistant. Format the response as json."),

        UserMessage(content="{{?user_query}}")

    ],

    response_format=ResponseFormatJsonObject(),

    defaults={"user_query": "Who was the first person on the moon?"}

)
```

**JSON Schema:**

```
from gen_ai_hub.orchestration_v2 import ResponseFormatJsonSchema, JSONResponseSchema



json_schema = {

    "title": "Person", "type": "object",

    "properties": {

        "firstName": {"type": "string", "description": "The person's first name."},

        "lastName": {"type": "string", "description": "The person's last name."}

    }

}

template = Template(

    template=[SystemMessage(content="You are a helpful assistant."), UserMessage(content="{{?user_query}}")],

    response_format=ResponseFormatJsonSchema(

        json_schema=JSONResponseSchema(name="person", description="person mapping", schema=json_schema)

    ),

    defaults={"user_query": "Who was the first person on the moon?"}

)
```

## Optional Modules[​](#optional-modules "Direct link to Optional Modules")

### Data Masking[​](#data-masking "Direct link to Data Masking")

```
from gen_ai_hub.orchestration_v2.utils import load_text_file

from gen_ai_hub.orchestration_v2 import (

    SystemMessage, UserMessage, Template, PromptTemplatingModuleConfig,

    LLMModelDetails, ModuleConfig, OrchestrationConfig, OrchestrationService,

    MaskingModuleConfig, MaskingProviderConfig, MaskingMethod, DPIStandardEntity, ProfileEntity

)



data_masking_config = MaskingModuleConfig(

    providers=[MaskingProviderConfig(

        method=MaskingMethod.ANONYMIZATION,

        entities=[

            DPIStandardEntity(type=ProfileEntity.ADDRESS),

            DPIStandardEntity(type=ProfileEntity.EMAIL),

            DPIStandardEntity(type=ProfileEntity.PHONE),

            DPIStandardEntity(type=ProfileEntity.PERSON),

        ],

        allowlist=["M&K Group"],

    )],

)



template = Template(template=[

    SystemMessage(content="You are a helpful AI assistant."),

    UserMessage(content="Summarize the following CV in 10 sentences: {{?orgCV}}"),

])

llm = LLMModelDetails(name="gpt-4o")

module_config = ModuleConfig(

    prompt_templating=PromptTemplatingModuleConfig(prompt=template, model=llm),

    masking=data_masking_config

)

config = OrchestrationConfig(modules=module_config)



cv_as_string = load_text_file("data/cv.txt")

result = OrchestrationService().run(config=config, placeholder_values={"orgCV": cv_as_string})

print(result.final_result.choices[0].message.content)
```

### Content Filtering[​](#content-filtering "Direct link to Content Filtering")

```
from gen_ai_hub.orchestration_v2 import (

    AzureContentSafetyInput, AzureContentSafetyOutput, AzureThreshold,

    LlamaGuard38bFilter, FilteringModuleConfig, InputFiltering, OutputFiltering,

    AzureContentSafetyInputFilterConfig, AzureContentSafetyOutputFilterConfig, LlamaGuard38bFilterConfig

)



content_filter_config = FilteringModuleConfig(

    input=InputFiltering(filters=[

        AzureContentSafetyInputFilterConfig(config=AzureContentSafetyInput(

            hate=AzureThreshold.ALLOW_SAFE, violence=AzureThreshold.ALLOW_SAFE,

            self_harm=AzureThreshold.ALLOW_SAFE, sexual=AzureThreshold.ALLOW_SAFE)),

        LlamaGuard38bFilterConfig(config=LlamaGuard38bFilter(hate=True))

    ]),

    output=OutputFiltering(filters=[

        AzureContentSafetyOutputFilterConfig(config=AzureContentSafetyOutput(

            hate=AzureThreshold.ALLOW_SAFE, violence=AzureThreshold.ALLOW_SAFE,

            self_harm=AzureThreshold.ALLOW_SAFE, sexual=AzureThreshold.ALLOW_SAFE)),

        LlamaGuard38bFilterConfig(config=LlamaGuard38bFilter(hate=True))

    ])

)



from gen_ai_hub.orchestration_v2 import OrchestrationError



try:

    result = client.run(placeholder_values={"text": "I hate you"})

    print(result.final_result.choices[0].message.content)

except OrchestrationError as er:

    print(er.message)
```

## Streaming[​](#streaming "Direct link to Streaming")

```
from gen_ai_hub.orchestration_v2 import GlobalStreamOptions



config = OrchestrationConfig(modules=module_config, stream=GlobalStreamOptions(enabled=True))

client = OrchestrationService(config=config)



result = client.stream(placeholder_values={"text": "Which color is the sky? Answer in one sentence."})

for part in result:

    print(part.final_result.choices[0].delta.content)
```

With `chunk_size`:

```
config = OrchestrationConfig(modules=module_config, stream=GlobalStreamOptions(enabled=True, chunk_size=25))

client = OrchestrationService(config=config)



result = client.stream(placeholder_values={"text": "Which color is the sky? Answer in one sentence."})

for part in result:

    print(part.final_result.choices[0].delta.content)
```

## Tool Calling[​](#tool-calling "Direct link to Tool Calling")

### Defining Tools[​](#defining-tools "Direct link to Defining Tools")

Using the Python decorator:

```
from gen_ai_hub.orchestration_v2 import function_tool



@function_tool()

def multiply(a: int, b: int) -> int:

    """Multiply two numbers."""

    return a * b



@function_tool()

def add(a: int, b: int) -> int:

    """Add two numbers."""

    return a + b



tools = [multiply, add]
```

Using `FunctionTool`:

```
from gen_ai_hub.orchestration_v2 import FunctionTool, FunctionObject



def get_weather(location: str) -> str:

    """Get current temperature for a given location."""

    return "22°C"



weather_tool_func = FunctionObject(

    name="get_weather",

    description="Get current temperature for a given location.",

    parameters={

        "type": "object",

        "properties": {"location": {"type": "string", "description": "City and country e.g. Bogotá, Colombia"}},

        "required": ["location"],

        "additionalProperties": False

    },

    strict=True,

    function=get_weather

)

weather_tool = FunctionTool(function=weather_tool_func)
```

From function:

```
weather_tool = FunctionTool.from_function(get_weather, strict=True)
```

### Synchronous Tool Call Workflow[​](#synchronous-tool-call-workflow "Direct link to Synchronous Tool Call Workflow")

```
from typing import List

from gen_ai_hub.orchestration_v2 import ChatMessage, ToolChatMessage



llm = LLMModelDetails(name="gpt-4o-mini", params={"max_completion_tokens": 200, "temperature": 0.0})

prompt_template = PromptTemplatingModuleConfig(prompt=template, model=llm)

module_config = ModuleConfig(prompt_templating=prompt_template)

config = OrchestrationConfig(modules=module_config)



service = OrchestrationService()

template_values = {"location": "Bogotá, Colombia"}



response = service.run(config=config, placeholder_values=template_values)

tool_calls = response.final_result.choices[0].message.tool_calls



history: List[ChatMessage] = []

history.extend(response.intermediate_results.templating)

history.append(response.final_result.choices[0].message)



for tool_call in tool_calls:

    result = weather_tool.execute(**tool_call.function.parse_arguments())

    history.append(ToolChatMessage(content=str(result), tool_call_id=tool_call.id))



response2 = service.run(config=config, placeholder_values=template_values, history=history)

print(response2.final_result.choices[0].message.content)
```

## Using Images as Input[​](#using-images-as-input "Direct link to Using Images as Input")

```
from gen_ai_hub.orchestration_v2 import ImageItem



# From URL

image_from_web = ImageItem(url="https://picsum.photos/id/1/200/300")



# From Data URL

image_from_data_url = ImageItem(

    url="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAIAAAACUFjqAAAAE0lEQVR4nGP8z4APMOGVZRip0gBBLAETee26JgAAAABJRU5ErkJggg=="

)



# From local file

try:

    image_from_local_file = ImageItem.from_file("path/to/your/local/image.jpeg")

except FileNotFoundError:

    print("Error: The specified image file was not found.")
```

```
from gen_ai_hub.orchestration_v2 import UserMessage



content_vqa = [image_from_web, "What objects are prominent in this image?"]

user_message = UserMessage(content=content_vqa)
```

## Translation[​](#translation "Direct link to Translation")

```
from gen_ai_hub.orchestration_v2 import (

    TranslationModuleConfig, SAPDocumentTranslationInput, SAPDocumentTranslationOutput,

    InputTranslationConfig, OutputTranslationConfig

)



translation_config = TranslationModuleConfig(

    input=SAPDocumentTranslationInput(config=InputTranslationConfig(source_language="en-US", target_language="de-DE")),

    output=SAPDocumentTranslationOutput(config=OutputTranslationConfig(source_language="de-DE", target_language="fr-FR"))

)



module_config = ModuleConfig(prompt_templating=prompt_template, translation=translation_config)

config = OrchestrationConfig(modules=module_config)



result = OrchestrationService().run(config=config, placeholder_values={"text": "What is the capital of Germany?"})

print(result.final_result.choices[0].message.content)
```

## Embeddings[​](#embeddings "Direct link to Embeddings")

### Basic Usage[​](#basic-usage "Direct link to Basic Usage")

```
from gen_ai_hub.orchestration_v2 import (

    OrchestrationService, EmbeddingsOrchestrationConfig, EmbeddingsModuleConfigs,

    EmbeddingsModelConfig, EmbeddingsModelDetails, EmbeddingsInput

)



service = OrchestrationService()

embeddings_config = EmbeddingsOrchestrationConfig(

    modules=EmbeddingsModuleConfigs(

        embeddings=EmbeddingsModelConfig(model=EmbeddingsModelDetails(name="text-embedding-3-large"))

    )

)

response = service.embed(config=embeddings_config, input=EmbeddingsInput(text="Hello World!"))

embedding = response.final_result.data[0].embedding

print(f"Embedding dimensions: {len(embedding)}")
```

### Customizing Parameters[​](#customizing-parameters "Direct link to Customizing Parameters")

```
from gen_ai_hub.orchestration_v2 import EmbeddingsModelParams, EmbeddingsEncodingFormat



embeddings_config_custom = EmbeddingsOrchestrationConfig(

    modules=EmbeddingsModuleConfigs(

        embeddings=EmbeddingsModelConfig(

            model=EmbeddingsModelDetails(

                name="text-embedding-3-large",

                params=EmbeddingsModelParams(dimensions=256, encoding_format=EmbeddingsEncodingFormat.FLOAT, normalize=True)

            )

        )

    )

)

response = service.embed(config=embeddings_config_custom, input=EmbeddingsInput(text="Hello World!"))

print(f"Embedding dimensions: {len(response.final_result.data[0].embedding)}")
```

### Batch Embeddings[​](#batch-embeddings "Direct link to Batch Embeddings")

```
documents = [

    "Artificial intelligence is transforming industries worldwide.",

    "Machine learning models require large amounts of training data.",

    "Neural networks are inspired by the human brain structure.",

    "Deep learning has achieved breakthroughs in image recognition."

]

response = service.embed(config=embeddings_config, input=EmbeddingsInput(text=documents))

print(f"Generated {len(response.final_result.data)} embeddings")
```

### Async Embeddings[​](#async-embeddings "Direct link to Async Embeddings")

```
async def embed_async():

    async_service = OrchestrationService()

    response = await async_service.aembed(config=embeddings_config, input=EmbeddingsInput(text="Hello async world!"))

    print(f"Async embedding dimensions: {len(response.final_result.data[0].embedding)}")

    await async_service.aclose_http_connection()



await embed_async()
```

## Advanced Examples[​](#advanced-examples "Direct link to Advanced Examples")

### Translation Service[​](#translation-service "Direct link to Translation Service")

```
from gen_ai_hub.orchestration_v2 import (

    OrchestrationConfig, ModuleConfig, LLMModelDetails, SystemMessage, UserMessage,

    Template, PromptTemplatingModuleConfig, OrchestrationService

)





class TranslationService:

    def __init__(self, orchestration_service: OrchestrationService):

        self.service = orchestration_service

        self.template = Template(

            template=[

                SystemMessage(content="You are a helpful AI assistant."),

                UserMessage(content="Translate the following text to {{?to_lang}}: {{?text}}"),

            ],

            defaults={"to_lang": "en-US"}

        )

        self.llm = LLMModelDetails(name="gpt-4o")

        self.config = OrchestrationConfig(modules=ModuleConfig(

            prompt_templating=PromptTemplatingModuleConfig(prompt=self.template, model=self.llm)

        ))



    def translate(self, text, to_lang):

        response = self.service.run(config=self.config, placeholder_values={"to_lang": to_lang, "text": text})

        return response.final_result.choices[0].message.content





service = OrchestrationService(api_url=YOUR_API_URL)

translator = TranslationService(orchestration_service=service)

print(translator.translate(text="Hello, world!", to_lang="French"))

print(translator.translate(text="Hello, world!", to_lang="Spanish"))
```

### Chatbot with Memory[​](#chatbot-with-memory "Direct link to Chatbot with Memory")

```
from typing import List

from gen_ai_hub.orchestration_v2 import (

    OrchestrationConfig, ModuleConfig, LLMModelDetails, ChatMessage, SystemMessage,

    UserMessage, Template, PromptTemplatingModuleConfig, OrchestrationService

)





class ChatBot:

    def __init__(self, orchestration_service: OrchestrationService):

        self.service = orchestration_service

        self.template = Template(template=[

            SystemMessage(content="You are a helpful chatbot assistant."),

            UserMessage(content="{{?user_query}}")

        ])

        self.llm = LLMModelDetails(name="gpt-4o")

        self.config = OrchestrationConfig(modules=ModuleConfig(

            prompt_templating=PromptTemplatingModuleConfig(prompt=self.template, model=self.llm)

        ))

        self.history: List[ChatMessage] = []



    def chat(self, user_input):

        response = self.service.run(

            config=self.config,

            placeholder_values={"user_query": user_input},

            history=self.history,

        )

        message = response.final_result.choices[0].message

        self.history = response.intermediate_results.templating

        self.history.append(message)

        return message.content



    def reset(self):

        self.history = []





bot = ChatBot(orchestration_service=OrchestrationService())

print(bot.chat("Hello, how are you?"))

print(bot.chat("What's the weather like today?"))

bot.reset()
```

### Sentiment Analysis with Few-Shot Learning[​](#sentiment-analysis-with-few-shot-learning "Direct link to Sentiment Analysis with Few-Shot Learning")

```
from typing import List, Tuple

from gen_ai_hub.orchestration_v2 import (

    OrchestrationConfig, ModuleConfig, LLMModelDetails, SystemMessage, UserMessage,

    AssistantMessage, Template, PromptTemplatingModuleConfig, OrchestrationService

)





class FewShotLearner:

    def __init__(self, orchestration_service, system_message, examples):

        self.service = orchestration_service

        self.llm = LLMModelDetails(name="gpt-4o-mini")

        self.config = OrchestrationConfig(modules=ModuleConfig(

            prompt_templating=PromptTemplatingModuleConfig(

                prompt=self._create_few_shot_template(system_message, examples),

                model=self.llm

            )

        ))



    @staticmethod

    def _create_few_shot_template(system_message, examples):

        messages = [system_message]

        for example in examples:

            messages.append(example[0])

            messages.append(example[1])

        messages.append(UserMessage(content="{{?user_input}}"))

        return Template(template=messages)



    def predict(self, user_input):

        response = self.service.run(config=self.config, placeholder_values={"user_input": user_input})

        return response.final_result.choices[0].message.content





sentiment_examples = [

    (UserMessage(content="I love this product!"), AssistantMessage(content="Positive")),

    (UserMessage(content="This is terrible service."), AssistantMessage(content="Negative")),

    (UserMessage(content="The weather is okay today."), AssistantMessage(content="Neutral")),

]

sentiment_analyzer = FewShotLearner(

    orchestration_service=OrchestrationService(),

    system_message=SystemMessage(

        content="You are a sentiment analysis assistant. Classify the sentiment as Positive, Negative, or Neutral."

    ),

    examples=sentiment_examples,

)

print(sentiment_analyzer.predict("The movie was a complete waste of time!"))
```

## Async Support[​](#async-support "Direct link to Async Support")

```
from gen_ai_hub.orchestration_v2 import (

    SystemMessage, UserMessage, Template, PromptTemplatingModuleConfig,

    LLMModelDetails, OrchestrationConfig, ModuleConfig, OrchestrationService, GlobalStreamOptions

)



template = Template(template=[

    SystemMessage(content="This is a system message."),

    UserMessage(content="Write a markdown cheatsheet!"),

])

llm = LLMModelDetails(name="gemini-2.0-flash")

config = OrchestrationConfig(modules=ModuleConfig(

    prompt_templating=PromptTemplatingModuleConfig(prompt=template, model=llm)

))

orchestration_service = OrchestrationService(config=config)



async def test_async():

    result = await orchestration_service.arun()

    print(result.final_result.choices[0].message.content)



await test_async()
```

Async streaming:

```
config_stream = OrchestrationConfig(modules=module_config, stream=GlobalStreamOptions(enabled=True))



async def test_streaming_async():

    streamed_content = ""

    async for chunk in await orchestration_service.astream(config=config_stream):

        streamed_content += chunk.final_result.choices[0].delta.content

    print(streamed_content)



await test_streaming_async()
```
