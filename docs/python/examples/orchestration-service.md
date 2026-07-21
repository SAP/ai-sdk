# Orchestration Service (Deprecated)

warning

Version 1 of the orchestration service API is deprecated and will be decommissioned October 2026. See [SAP Note 3634540](https://me.sap.com/notes/3634540). Use the [Orchestration Service V2 API](/ai-sdk/docs/python/examples/orchestration-service2.md) instead.

This page demonstrates how to use the SDK to interact with the Orchestration Service, enabling the creation of AI-driven workflows by integrating modules such as templating, LLMs, data masking, and content filtering.

## Prerequisite[​](#prerequisite "Direct link to Prerequisite")

Before you begin, make sure to set up a virtual deployment of the Orchestration Service. See the [setup guide](https://help.sap.com/docs/ai-launchpad/sap-ai-launchpad/create-deployment-for-orchestration).

## Basic Orchestration Pipeline[​](#basic-orchestration-pipeline "Direct link to Basic Orchestration Pipeline")

### Step 1: Define the Template[​](#step-1-define-the-template "Direct link to Step 1: Define the Template")

```
from gen_ai_hub.orchestration.models.message import SystemMessage, UserMessage

from gen_ai_hub.orchestration.models.template import Template, TemplateValue



template = Template(

    messages=[

        SystemMessage("You are a helpful translation assistant."),

        UserMessage("Translate the following text to {{?to_lang}}: {{?user_query}}"),

    ],

    defaults=[

        TemplateValue(name="to_lang", value="German"),

    ],

)
```

### Step 2: Define the LLM[​](#step-2-define-the-llm "Direct link to Step 2: Define the LLM")

```
from gen_ai_hub.orchestration.models.llm import LLM



llm = LLM(name="gpt-5-nano", parameters={"max_completion_tokens": 512})
```

### Step 3: Create the Configuration[​](#step-3-create-the-configuration "Direct link to Step 3: Create the Configuration")

```
from gen_ai_hub.orchestration.models.config import OrchestrationConfig



config = OrchestrationConfig(template=template, llm=llm)
```

### Step 4: Run the Request[​](#step-4-run-the-request "Direct link to Step 4: Run the Request")

```
from gen_ai_hub.orchestration.service import OrchestrationService



orchestration_service = OrchestrationService(config=config)

result = orchestration_service.run(template_values=[

    TemplateValue(name="user_query", value="The Orchestration Service is working!"),

])

print(result.orchestration_result.choices[0].message.content)
```

#### Referencing Templates from the Prompt Registry[​](#referencing-templates-from-the-prompt-registry "Direct link to Referencing Templates from the Prompt Registry")

```
from gen_ai_hub.orchestration.models.template_ref import TemplateRef



template_by_id = TemplateRef.from_id(prompt_template_id="648871d9-b207-441c-8c13-afee71b0dbec")

template_by_names = TemplateRef.from_tuple(scenario="translation", name="translate_text", version="0.1.0")
```

#### Response Format Options[​](#response-format-options "Direct link to Response Format Options")

**Text:**

```
from gen_ai_hub.orchestration.models.message import SystemMessage, UserMessage

from gen_ai_hub.orchestration.models.template import Template, TemplateValue



template = Template(

    messages=[

        SystemMessage("You are a helpful translation assistant."),

        UserMessage("{{?user_query}}")

    ],

    response_format="text",

    defaults=[TemplateValue(name="user_query", value="Who was the first person on the moon?")]

)
```

**JSON Object:**

```
template = Template(

    messages=[

        SystemMessage("You are a helpful translation assistant. Format the response as json."),

        UserMessage("{{?user_query}}")

    ],

    response_format="json_object",

    defaults=[TemplateValue(name="user_query", value="Who was the first person on the moon?")]

)
```

**JSON Schema:**

```
from gen_ai_hub.orchestration.models.response_format import ResponseFormatJsonSchema



json_schema = {

    "title": "Person",

    "type": "object",

    "properties": {

        "firstName": {"type": "string", "description": "The person's first name."},

        "lastName": {"type": "string", "description": "The person's last name."}

    }

}

template = Template(

    messages=[

        SystemMessage("You are a helpful translation assistant."),

        UserMessage("{{?user_query}}")

    ],

    response_format=ResponseFormatJsonSchema(name="person", description="person mapping", schema=json_schema),

    defaults=[TemplateValue(name="user_query", value="Who was the first person on the moon?")]

)
```

## Optional Modules[​](#optional-modules "Direct link to Optional Modules")

### Data Masking[​](#data-masking "Direct link to Data Masking")

```
from gen_ai_hub.orchestration.utils import load_text_file

from gen_ai_hub.orchestration.models.data_masking import DataMasking

from gen_ai_hub.orchestration.models.sap_data_privacy_integration import (

    SAPDataPrivacyIntegration, MaskingMethod, ProfileEntity

)



data_masking = DataMasking(

    providers=[

        SAPDataPrivacyIntegration(

            method=MaskingMethod.ANONYMIZATION,

            entities=[ProfileEntity.EMAIL, ProfileEntity.PHONE, ProfileEntity.PERSON,

                      ProfileEntity.ORG, ProfileEntity.LOCATION],

            allowlist=["M&K Group"],

        )

    ]

)



config = OrchestrationConfig(

    template=Template(

        messages=[

            SystemMessage("You are a helpful AI assistant."),

            UserMessage("Summarize the following CV in 10 sentences: {{?orgCV}}"),

        ]

    ),

    llm=LLM(name="gpt-4o"),

    data_masking=data_masking

)



cv_as_string = load_text_file("data/cv.txt")

result = orchestration_service.run(

    config=config,

    template_values=[TemplateValue(name="orgCV", value=cv_as_string)]

)

print(result.orchestration_result.choices[0].message.content)
```

### Content Filtering[​](#content-filtering "Direct link to Content Filtering")

```
from gen_ai_hub.orchestration.models.content_filtering import ContentFiltering, InputFiltering, OutputFiltering

from gen_ai_hub.orchestration.models.azure_content_filter import AzureContentFilter, AzureThreshold

from gen_ai_hub.orchestration.models.llama_guard_3_filter import LlamaGuard38bFilter



input_filter = AzureContentFilter(hate=AzureThreshold.ALLOW_SAFE, violence=AzureThreshold.ALLOW_SAFE,

                                   self_harm=AzureThreshold.ALLOW_SAFE, sexual=AzureThreshold.ALLOW_SAFE)

input_filter_llama = LlamaGuard38bFilter(hate=True)

output_filter = AzureContentFilter(hate=AzureThreshold.ALLOW_SAFE, violence=AzureThreshold.ALLOW_SAFE_LOW,

                                    self_harm=AzureThreshold.ALLOW_SAFE_LOW_MEDIUM, sexual=AzureThreshold.ALLOW_ALL)

output_filter_llama = LlamaGuard38bFilter(hate=True)



config = OrchestrationConfig(

    template=Template(

        messages=[SystemMessage("You are a helpful AI assistant."), UserMessage("{{?text}}")]),

    llm=LLM(name="gpt-4o"),

    filtering=ContentFiltering(

        input_filtering=InputFiltering(filters=[input_filter, input_filter_llama]),

        output_filtering=OutputFiltering(filters=[output_filter, output_filter_llama])

    )

)



from gen_ai_hub.orchestration.exceptions import OrchestrationError



try:

    result = orchestration_service.run(config=config, template_values=[

        TemplateValue(name="text", value="I hate you")

    ])

except OrchestrationError as error:

    print(error.message)
```

## Streaming[​](#streaming "Direct link to Streaming")

```
config = OrchestrationConfig(

    template=Template(

        messages=[SystemMessage("You are a helpful AI assistant."), UserMessage("{{?text}}")]),

    llm=LLM(name="gpt-4o-mini", parameters={"max_completion_tokens": 256, "temperature": 0.0}),

)



service = OrchestrationService()

response = service.stream(

    config=config,

    template_values=[TemplateValue(name="text", value="Which color is the sky? Answer in one sentence.")]

)



for chunk in response:

    print(chunk.orchestration_result)
```

With `chunk_size`:

```
response = service.stream(

    config=config,

    template_values=[TemplateValue(name="text", value="Which color is the sky? Answer in one sentence.")],

    stream_options={'chunk_size': 25}

)

for chunk in response:

    print(chunk.orchestration_result)
```

## Tool Calling[​](#tool-calling "Direct link to Tool Calling")

### Defining Tools[​](#defining-tools "Direct link to Defining Tools")

Using the Python decorator:

```
from gen_ai_hub.orchestration.models.tools import function_tool



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
from gen_ai_hub.orchestration.models.tools import FunctionTool



def get_weather(location: str) -> str:

    """Get current temperature for a given location."""

    return "22°C"



weather_tool = FunctionTool(

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
```

From function:

```
weather_tool = FunctionTool.from_function(get_weather, strict=True)
```

### Synchronous Tool Call Workflow[​](#synchronous-tool-call-workflow "Direct link to Synchronous Tool Call Workflow")

```
from typing import List

from gen_ai_hub.orchestration.models.config import OrchestrationConfig

from gen_ai_hub.orchestration.models.template import Template, TemplateValue

from gen_ai_hub.orchestration.models.message import Message, ToolMessage

from gen_ai_hub.orchestration.models.llm import LLM

from gen_ai_hub.orchestration.service import OrchestrationService



llm = LLM(name="gpt-4o-mini", parameters={"max_completion_tokens": 200, "temperature": 0.0})

config = OrchestrationConfig(template=template, llm=llm)

template_values = [TemplateValue(name="location", value="Bogotá, Colombia")]



service = OrchestrationService()

response = service.run(config=config, template_values=template_values)

tool_calls = response.orchestration_result.choices[0].message.tool_calls



history: List[Message] = []

history.extend(response.module_results.templating)

history.append(response.orchestration_result.choices[0].message)



for tool_call in tool_calls:

    result = weather_tool.execute(**tool_call.function.parse_arguments())

    history.append(ToolMessage(content=str(result), tool_call_id=tool_call.id))



response2 = service.run(config=config, template_values=template_values, history=history)

print(response2.orchestration_result.choices[0].message.content)
```

## Using Images as Input[​](#using-images-as-input "Direct link to Using Images as Input")

```
from gen_ai_hub.orchestration.models.multimodal_items import ImageItem



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
from gen_ai_hub.orchestration.models.message import UserMessage

from gen_ai_hub.orchestration.models.template import Template



content_vqa = [image_from_web, "What objects are prominent in this image?"]

user_message = UserMessage(content=content_vqa)

prompt_template = Template(messages=[user_message])



orchestration_service = OrchestrationService(config=OrchestrationConfig(template=prompt_template, llm=llm))

result = orchestration_service.run()

print(result.orchestration_result.choices[0].message.content)
```

## Translation[​](#translation "Direct link to Translation")

```
from gen_ai_hub.orchestration.models.translation.translation import InputTranslationConfig, OutputTranslationConfig

from gen_ai_hub.orchestration.models.translation.sap_document_translation import SAPDocumentTranslation



input_config = InputTranslationConfig(source_language="en-US", target_language="de-DE")

output_config = OutputTranslationConfig(source_language="de-DE", target_language="en-US")



translation_module = SAPDocumentTranslation(

    input_translation_config=input_config,

    output_translation_config=output_config

)



config = OrchestrationConfig(

    template=Template(

        messages=[SystemMessage("You are a helpful AI assistant."), UserMessage("{{?text}}")]),

    llm=LLM(name="gpt-4o"),

    translation=translation_module

)



result = orchestration_service.run(

    config=config,

    template_values=[TemplateValue(name="text", value="What is the capital of Germany?")]

)

print(result.orchestration_result.choices[0].message.content)
```

## Advanced Examples[​](#advanced-examples "Direct link to Advanced Examples")

### Translation Service[​](#translation-service "Direct link to Translation Service")

```
from gen_ai_hub.orchestration.models.config import OrchestrationConfig

from gen_ai_hub.orchestration.models.llm import LLM

from gen_ai_hub.orchestration.models.message import SystemMessage, UserMessage

from gen_ai_hub.orchestration.models.template import Template, TemplateValue

from gen_ai_hub.orchestration.service import OrchestrationService





class TranslationService:

    def __init__(self, orchestration_service: OrchestrationService):

        self.service = orchestration_service

        self.config = OrchestrationConfig(

            template=Template(

                messages=[

                    SystemMessage("You are a helpful translation assistant."),

                    UserMessage("Translate the following text to {{?to_lang}}: {{?text}}"),

                ],

                defaults=[TemplateValue(name="to_lang", value="English")],

            ),

            llm=LLM(name="gpt-4o"),

        )



    def translate(self, text, to_lang):

        response = self.service.run(

            config=self.config,

            template_values=[

                TemplateValue(name="to_lang", value=to_lang),

                TemplateValue(name="text", value=text),

            ],

        )

        return response.orchestration_result.choices[0].message.content





service = OrchestrationService(api_url=YOUR_API_URL)

translator = TranslationService(orchestration_service=service)

print(translator.translate(text="Hello, world!", to_lang="French"))

print(translator.translate(text="Hello, world!", to_lang="Spanish"))
```

### Chatbot with Memory[​](#chatbot-with-memory "Direct link to Chatbot with Memory")

```
from typing import List

from gen_ai_hub.orchestration.models.config import OrchestrationConfig

from gen_ai_hub.orchestration.models.llm import LLM

from gen_ai_hub.orchestration.models.message import Message, SystemMessage, UserMessage

from gen_ai_hub.orchestration.models.template import Template, TemplateValue

from gen_ai_hub.orchestration.service import OrchestrationService





class ChatBot:

    def __init__(self, orchestration_service: OrchestrationService):

        self.service = orchestration_service

        self.config = OrchestrationConfig(

            template=Template(

                messages=[SystemMessage("You are a helpful chatbot assistant."), UserMessage("{{?user_query}}")]),

            llm=LLM(name="gpt-4o"),

        )

        self.history: List[Message] = []



    def chat(self, user_input):

        response = self.service.run(

            config=self.config,

            template_values=[TemplateValue(name="user_query", value=user_input)],

            history=self.history,

        )

        message = response.orchestration_result.choices[0].message

        self.history = response.module_results.templating

        self.history.append(message)

        return message.content



    def reset(self):

        self.history = []





bot = ChatBot(orchestration_service=service)

print(bot.chat("Hello, how are you?"))

print(bot.chat("What's the weather like today?"))

print(bot.chat("Can you remember what I first asked you?"))

bot.reset()
```

### Sentiment Analysis with Few-Shot Learning[​](#sentiment-analysis-with-few-shot-learning "Direct link to Sentiment Analysis with Few-Shot Learning")

```
from typing import List, Tuple

from gen_ai_hub.orchestration.models.config import OrchestrationConfig

from gen_ai_hub.orchestration.models.llm import LLM

from gen_ai_hub.orchestration.models.message import SystemMessage, UserMessage, AssistantMessage

from gen_ai_hub.orchestration.models.template import Template, TemplateValue

from gen_ai_hub.orchestration.service import OrchestrationService





class FewShotLearner:

    def __init__(self, orchestration_service, system_message, examples):

        self.service = orchestration_service

        self.config = OrchestrationConfig(

            template=self._create_few_shot_template(system_message, examples),

            llm=LLM(name="gpt-4o-mini"),

        )



    @staticmethod

    def _create_few_shot_template(system_message, examples):

        messages = [system_message]

        for example in examples:

            messages.append(example[0])

            messages.append(example[1])

        messages.append(UserMessage("{{?user_input}}"))

        return Template(messages=messages)



    def predict(self, user_input):

        response = self.service.run(

            config=self.config,

            template_values=[TemplateValue(name="user_input", value=user_input)],

        )

        return response.orchestration_result.choices[0].message.content





sentiment_examples = [

    (UserMessage("I love this product!"), AssistantMessage("Positive")),

    (UserMessage("This is terrible service."), AssistantMessage("Negative")),

    (UserMessage("The weather is okay today."), AssistantMessage("Neutral")),

]



sentiment_analyzer = FewShotLearner(

    orchestration_service=service,

    system_message=SystemMessage(

        "You are a sentiment analysis assistant. Classify the sentiment as Positive, Negative, or Neutral."

    ),

    examples=sentiment_examples,

)

print(sentiment_analyzer.predict("The movie was a complete waste of time!"))
```

## Async Support[​](#async-support "Direct link to Async Support")

```
import asyncio

from gen_ai_hub.orchestration.models.message import SystemMessage, UserMessage

from gen_ai_hub.orchestration.models.template import Template

from gen_ai_hub.orchestration.models.llm import LLM

from gen_ai_hub.orchestration.models.config import OrchestrationConfig

from gen_ai_hub.orchestration.service import OrchestrationService



config = OrchestrationConfig(

    llm=LLM(name="gemini-2.0-flash"),

    template=Template(messages=[

        SystemMessage("This is a system message."),

        UserMessage("Write a markdown cheatsheet!"),

    ]),

)

orchestration_service = OrchestrationService(config=config)



async def test_async():

    async_result = await orchestration_service.arun()

    print(async_result.orchestration_result.choices[0].message.content)



await test_async()
```

Async streaming:

```
async def test_streaming_async():

    streamed_content = ""

    async for chunk in await orchestration_service.astream():

        if chunk.orchestration_result.choices:

            streamed_content += chunk.orchestration_result.choices[0].delta.content

    print(streamed_content)



await test_streaming_async()
```
