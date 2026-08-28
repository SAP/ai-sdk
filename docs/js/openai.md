# OpenAI

caution

The `@sap-ai-sdk/openai` package is experimental and may change at any time without prior notice.

If you do not need OpenAI-specific features such as the Responses API, consider using the [`@sap-ai-sdk/orchestration`](/ai-sdk/docs/js/orchestration/chat-completion.md) package instead, which provides a stable interface for chat completion and other AI tasks on SAP AI Core.

caution

This package reuses the types from the official `openai` npm package.

The Azure OpenAI API shape differs from the core OpenAI API shape, and SAP AI Core applies additional platform-specific constraints. As a result, the static types for request parameters and responses are not always an exact match for what is defined at the type-level.

The `@sap-ai-sdk/openai` package is a thin wrapper around the official [`openai`](https://www.npmjs.com/package/openai) npm package, pre-configured for Azure OpenAI deployments on SAP AI Core. It handles deployment resolution, authentication, and SAP-specific headers automatically. The `model` parameter is optional in all request signatures — requests are routed via the deployment URL configured at client initialization by default.

If you need a stable Azure OpenAI integration without recent OpenAI-specific features, consider using the [`@sap-ai-sdk/foundation-models`](/ai-sdk/docs/js/foundation-models.md) package instead. It provides SAP's own client layer, based on a more stable API contract.

For full API reference, see the [official OpenAI documentation](https://platform.openai.com/docs/api-reference).

## Installation[​](#installation "Direct link to Installation")

```
npm install @sap-ai-sdk/openai openai
```

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

See the [prerequisites](/ai-sdk/docs/js/overview.md#prerequisites) section.

## Client Initialization[​](#client-initialization "Direct link to Client Initialization")

Use the `SapOpenAi.createClient()` method to create a pre-configured client. Pass a model name string or a deployment identifier object via the `deployment` option:

```
import { SapOpenAi } from '@sap-ai-sdk/openai';



// By model name (shorthand)

const clientA = await SapOpenAi.createClient('gpt-5.4');



// By model name and version

const clientB = await SapOpenAi.createClient({

  deployment: { modelName: 'gpt-5.4', modelVersion: '2025-04-14' }

});



// By deployment ID

const clientC = await SapOpenAi.createClient({

  deployment: { deploymentId: 'DEPLOYMENT_ID' }

});
```

Use the `resourceGroup` property to target a specific resource group. The resource group defaults to `default`:

```
const client = await SapOpenAi.createClient({

  deployment: { modelName: 'gpt-5.4', resourceGroup: 'my-resource-group' }

});
```

To use a custom SAP AI Core destination, pass the `destination` option:

```
const client = await SapOpenAi.createClient({

  deployment: { modelName: 'gpt-5.4' },

  destination: { destinationName: 'DESTINATION_NAME' }

});
```

## Making Requests[​](#making-requests "Direct link to Making Requests")

`SapOpenAi` exposes three endpoints supported by SAP AI Core: `chat`, `embeddings`, and `responses`. By default, requests are routed via the deployment URL configured at client initialization. You can optionally [pass a `model` parameter](#per-request-model-override) in individual requests to route to a different deployment.

### Chat Completions[​](#chat-completions "Direct link to Chat Completions")

```
const response = await client.chat.completions.create({

  messages: [{ role: 'user', content: 'What is the capital of France?' }]

});
```

Use the `parse()` method for structured output with a Zod schema:

```
import { zodResponseFormat } from 'openai/helpers/zod';

import { z } from 'zod';



const CapitalResponse = z.object({ capital: z.string() });



const response = await client.chat.completions.parse({

  messages: [{ role: 'user', content: 'What is the capital of France?' }],

  response_format: zodResponseFormat(CapitalResponse, 'capital_response')

});
```

### Embeddings[​](#embeddings "Direct link to Embeddings")

```
const embeddingClient = await SapOpenAi.createClient({

  deployment: 'text-embedding-3-small'

});



const response = await embeddingClient.embeddings.create({

  input: 'Hello, world!'

});
```

### Responses API[​](#responses-api "Direct link to Responses API")

```
const response = await client.responses.create({

  instructions: 'You are a helpful assistant.',

  input: 'What is the capital of France?'

});
```

#### Streaming[​](#streaming "Direct link to Streaming")

Pass `stream: true` and iterate over the events with `for await`. The `delta` text is only available when `event.type === 'response.output_text.delta'`.

```
const stream = await client.responses.create({

  instructions: 'You are a helpful assistant.',

  input: 'Give me a short introduction of SAP Cloud SDK.',

  stream: true

});



for await (const event of stream) {

  if (event.type === 'response.output_text.delta') {

    process.stdout.write(event.delta);

  }

}
```

#### Stateful Conversations[​](#stateful-conversations "Direct link to Stateful Conversations")

Pass `previous_response_id` to let the server maintain the conversation history. Each turn only needs to send the new message. Use this when you want simple multi-turn conversations without managing history yourself. Note that responses are stored on the server.

```
const first = await client.responses.create({

  instructions: 'You are a helpful assistant.',

  input: 'What is the capital of France?'

});



const second = await client.responses.create({

  previous_response_id: first.id,

  input: 'What is the population of that city?'

});
```

#### Multi-Turn Conversations[​](#multi-turn-conversations "Direct link to Multi-Turn Conversations")

Manage the context yourself by appending the previous `response.output` to the next `input`. Use this when you need full control over the conversation history, for example to store it in your own database or modify messages between turns.

```
let context: ResponseInputItem[] = [

  { role: 'user' as const, content: 'What is the capital of France?' }

];



const first = await client.responses.create({ input: context });



context = [...context, ...toResponseInputItems(first.output)];

context.push({

  role: 'user' as const,

  content: 'What is the population of that city?'

});



const second = await client.responses.create({ input: context });
```

#### Structured Output[​](#structured-output "Direct link to Structured Output")

Use the `parse()` method for structured output with a Zod schema:

```
import { zodTextFormat } from 'openai/helpers/zod';

import { z } from 'zod';



const CapitalResponse = z.object({ capital: z.string() });



const response = await client.responses.parse({

  instructions: 'You are a helpful assistant.',

  input: 'What is the capital of France?',

  text: { format: zodTextFormat(CapitalResponse, 'capital_response') }

});
```

#### Tool Calling[​](#tool-calling "Direct link to Tool Calling")

Use function tools to let the model call your own functions. The model returns a `function_call` in `response.output`; execute the function and send the result back in a follow-up request.

```
const response = await client.responses.create({

  input: 'What is the weather in Paris?',

  tools: [

    {

      type: 'function',

      name: 'get_weather',

      description: 'Get the current weather for a city.',

      parameters: {

        type: 'object',

        properties: {

          city: { type: 'string', description: 'The city name.' }

        },

        required: ['city'],

        additionalProperties: false

      },

      strict: true

    }

  ]

});



const toolCall = response.output.find(item => item.type === 'function_call');

if (toolCall && toolCall.type === 'function_call') {

  const args = JSON.parse(toolCall.arguments); // { city: 'Paris' }

  // Call your actual function here.

  const result = JSON.stringify({ temperature: '15°C', condition: 'Cloudy' });



  const input = [

    ...toResponseInputItems(response.output),

    {

      type: 'function_call_output' as const,

      call_id: toolCall.call_id,

      output: result

    }

  ];



  const finalResponse = await client.responses.create({ input });

  // finalResponse.output_text contains the final answer.

}
```

## Per-Request Model Override[​](#per-request-model-override "Direct link to Per-Request Model Override")

You can override the model or deployment configuration for individual requests by passing a `model` parameter. This lets a single client instance send requests to different deployments without re-initializing.

Use the client's configured deployment:

```
const client = await SapOpenAi.createClient({ deployment: 'gpt-5.4' });



const response = await client.chat.completions.create({

  messages: [{ role: 'user', content: 'What is the capital of France?' }]

});
```

Override with a different model for this request only:

```
const response = await client.chat.completions.create({

  model: 'gpt-5.4-nano',

  messages: [{ role: 'user', content: 'What is the capital of France?' }]

});
```

Override with a different model and version for this request only:

```
const response = await client.chat.completions.create({

  model: { modelName: 'gpt-5.4-nano', modelVersion: 'latest' },

  messages: [{ role: 'user', content: 'What is the capital of France?' }]

});
```

Override with a different deployment for this request only:

```
const response = await client.chat.completions.create({

  model: { deploymentId: 'DEPLOYMENT_ID' },

  messages: [{ role: 'user', content: 'What is the capital of France?' }]

});
```

note

If the `model` parameter matches the client's configured deployment, no additional deployment resolution is performed. Deployment resolution results are cached, so overriding the model on repeated requests does not incur additional network requests.

## Low-Level Config[​](#low-level-config "Direct link to Low-Level Config")

Use the `createOpenAiConfig()` function to get an `AzureClientOptions` object for direct instantiation of `AzureOpenAI`. This is useful when you need endpoints not exposed by `SapOpenAi`:

```
import { AzureOpenAI } from 'openai';

import { createOpenAiConfig } from '@sap-ai-sdk/openai';



const config = await createOpenAiConfig('gpt-5.4');

const client = new AzureOpenAI(config);
```

## Token Provider[​](#token-provider "Direct link to Token Provider")

Use the `createTokenProvider()` function when you need an `azureADTokenProvider`-compatible function for custom `AzureOpenAI` configurations. It is used internally by `createOpenAiConfig()`.

```
import { AzureOpenAI } from 'openai';

import { createTokenProvider } from '@sap-ai-sdk/openai';



const client = new AzureOpenAI({

  baseURL: 'https://my-deployment-url',

  apiVersion: '2024-10-21',

  azureADTokenProvider: createTokenProvider()

});
```
