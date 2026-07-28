---
id: chat-completion
title: Chat Completion
description: How to use the SAP Cloud SDK for AI to perform chat completion tasks using Azure OpenAI models deployed through SAP AI Core.
---

# Chat Completion


Initialize the `AzureOpenAiChatClient` by following the instructions in the [Client Initialization](../../foundation-models#client-initialization) section.

Currently, the client sends request with Azure OpenAI API version `2024-10-21`.
We are continuously updating the client to match the latest API specification.
You can overwrite the API version by setting the `api-version` parameter in the `CustomRequestConfig` object.
Refer to the [Custom Request Configuration](../../foundation-models#custom-request-configuration) section for more details.

## Making Requests

```ts twoslash
import { AzureOpenAiChatClient } from '@sap-ai-sdk/foundation-models';
const client = new AzureOpenAiChatClient('gpt-5');
// ---cut---
const response = await client.run({
  messages: [
    {
      role: 'user',
      content: 'Where is the deepest place on earth located?'
    }
  ]
});
console.log(response.getContent());
```

### Message History

Multiple messages can be sent in a single request, enabling the model to reference the conversation history.
Include `max_tokens` and `temperature` in the request to control the completion behavior:

```ts twoslash
import { AzureOpenAiChatClient } from '@sap-ai-sdk/foundation-models';
const client = new AzureOpenAiChatClient('gpt-5');
// ---cut---
const response = await client.run({
  messages: [
    {
      role: 'system',
      content: 'You are a friendly chatbot.'
    },
    {
      role: 'user',
      content: 'Hi, my name is Isa'
    },
    {
      role: 'assistant',
      content:
        'Hi Isa! It is nice to meet you. Is there anything I can help you with today?'
    },
    {
      role: 'user',
      content: 'Can you remind me, What is my name?'
    }
  ],
  max_tokens: 100,
  temperature: 0.0
});
console.log(response.getContent());

const tokenUsage = response.getTokenUsage();
console.log(
  `Total tokens consumed by the request: ${tokenUsage?.total_tokens}\n` +
    `Input prompt tokens consumed: ${tokenUsage?.prompt_tokens}\n` +
    `Output text completion tokens consumed: ${tokenUsage?.completion_tokens}\n`
);
```

Use the autocompletion feature to see other possible parameters.

## Streaming

The `AzureOpenAiChatClient` supports streaming response for chat completion requests based on the [Server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events) standard.

Use the `stream()` method to receive a stream of chunk responses from the model.
After consuming the stream, call the helper methods to get the finish reason and token usage information.

```ts twoslash
import { AzureOpenAiChatClient } from '@sap-ai-sdk/foundation-models';
const client = new AzureOpenAiChatClient('gpt-5');
// ---cut---
const response = await client.stream({
  messages: [
    {
      role: 'user',
      content: 'Give me a very long introduction of SAP Cloud SDK.'
    }
  ]
});

for await (const chunk of response.stream) {
  console.log(JSON.stringify(chunk));
}

const finishReason = response.getFinishReason();
const tokenUsage = response.getTokenUsage();

console.log(`Finish reason: ${finishReason}\n`);
console.log(`Token usage: ${JSON.stringify(tokenUsage)}\n`);
```

### Streaming the Delta Content

Use `toContentStream()` method to create a stream generating delta content string.

```ts twoslash
import { AzureOpenAiChatClient } from '@sap-ai-sdk/foundation-models';
const client = new AzureOpenAiChatClient('gpt-5');
const response = await client.stream({
  messages: [{ role: 'user', content: '' }]
});
// ---cut---
for await (const chunk of response.stream.toContentStream()) {
  console.log(chunk); // will log the delta content
}
```

### Streaming with Tool Calls

Use `getToolCalls()` method to get the tool calls at the end of a stream.
While `getDeltaToolCalls()` method can be called on individual chunks, partial tool calls are typically not useful.
Therefore, it is recommended to use the `getToolCalls()` method on the full response instead.

```ts twoslash
import { AzureOpenAiChatClient } from '@sap-ai-sdk/foundation-models';
const client = new AzureOpenAiChatClient('gpt-5');
const response = await client.stream({
  messages: [{ role: 'user', content: '' }]
});
// ---cut---
for await (const _ of response.stream) {
  console.log('Waiting for the stream to end ...');
}

const toolCalls = response.getToolCalls();
```

### Streaming with Abort Controller

Streaming request can be aborted using the `AbortController` API.
In case of an error, SAP Cloud SDK for AI will automatically close the stream.
Additionally, it can be aborted manually by calling the `stream()` method with an `AbortSignal` object.

```ts twoslash
import { AzureOpenAiChatClient } from '@sap-ai-sdk/foundation-models';
const client = new AzureOpenAiChatClient('gpt-5');
// ---cut---
const controller = new AbortController();
const streamResponse = await client.stream(
  {
    messages: [
      {
        role: 'user',
        content: 'Give me a very long introduction of SAP Cloud SDK.'
      }
    ]
  },
  controller.signal
);

// Abort the streaming request after one second
setTimeout(() => {
  controller.abort();
}, 1000);

for await (const chunk of streamResponse.stream) {
  console.log(JSON.stringify(chunk));
}
```

In this example, streaming request will be aborted after one second.
Abort controller can be useful, e.g., when end-user wants to stop the stream or refreshes the page.

## Response Format

For general response formatting, use the `response_format` parameter.
It is useful when model is not calling a tool and should still return a structured response.

The example below returns a JSON Schema with `strict: true` to let the response adhere to the schema definition.

```ts twoslash
import { AzureOpenAiChatClient } from '@sap-ai-sdk/foundation-models';
const client = new AzureOpenAiChatClient('gpt-5');
// ---cut---
const response = await client.run({
  messages: [
    {
      role: 'user',
      content: 'What is the capital of France?'
    }
  ],
  response_format: {
    type: 'json_schema',
    json_schema: {
      description: 'Response format for the capital of France.',
      name: 'capital_of_france',
      schema: {
        type: 'object',
        properties: {
          capital: {
            type: 'string',
            description: 'The capital city of France.'
          },
          population: {
            type: 'number',
            description: 'The population of the capital city.'
          }
        },
        additionalProperties: false, // Ensures no additional properties are allowed
        required: ['capital', 'population']
      },
      strict: true
    }
  }
});
console.log(response.getContent());
```

You can also define JSON schema using [Zod](https://zod.dev/) schema.
We recommend using Zod v4 for full compatibility with this package.
If you're upgrading from an earlier version, refer to the [Zod v4 migration guide](https://zod.dev/v4/changelog) and pay attention to breaking changes like the switch from `describe('...')` to `meta({ description: '...' })`.

```ts
import * as z from 'zod';
import { toJsonSchema } from '@langchain/core/utils/json_schema';
import { AzureOpenAiResponseFormatJsonSchema } from '@sap-ai-sdk/foundation-models';

const countryCapitalSchema = z.strictObject({
  population: z.number(),
  capital: z.string()
});

const response_format: AzureOpenAiResponseFormatJsonSchema = {
  type: 'json_schema',
  json_schema: {
    name: 'capital_response',
    strict: true,
    schema: toJsonSchema(countryCapitalSchema)
  }
};
```

## Function Calling

Define and pass [tool definitions](https://platform.openai.com/docs/guides/function-calling) to enable the model to call specific functions.
Here's an example of temperature conversion using tool calls:

First, define the tool with `name`, `description` and `parameters` properties:

```ts twoslash
import { AzureOpenAiChatCompletionTool } from '@sap-ai-sdk/foundation-models';
// ---cut---
const convertTemperatureTool: AzureOpenAiChatCompletionTool = {
  type: 'function',
  function: {
    name: 'convert_temperature_to_fahrenheit',
    description: 'Converts temperature from Celsius to Fahrenheit',
    parameters: {
      type: 'object',
      properties: {
        temperature: {
          type: 'number',
          description: 'The temperature value in Celsius to convert.'
        }
      },
      required: ['temperature']
    }
  }
};
```

Set `strict` to `true` to ensure function calls adhere to the function schema.
For more information refer to the [OpenAI documentation](https://platform.openai.com/docs/guides/function-calling?api-mode=chat#strict-mode).

Initialize the client and send the initial request with the tool definition:

```ts twoslash
import {
  AzureOpenAiChatClient,
  AzureOpenAiChatCompletionTool,
  AzureOpenAiChatCompletionRequestMessage
} from '@sap-ai-sdk/foundation-models';
declare const convertTemperatureTool: AzureOpenAiChatCompletionTool;
// ---cut---
const client = new AzureOpenAiChatClient('gpt-5');
const messages: AzureOpenAiChatCompletionRequestMessage[] = [
  {
    role: 'user',
    content: 'Convert 20 degrees Celsius to Fahrenheit.'
  }
];

const response = await client.run({
  messages,
  tools: [convertTemperatureTool]
});
```

When the model decides to use a tool, it returns the function name and input arguments in the response.
Use the model response to execute the function.

```ts twoslash
import {
  AzureOpenAiChatClient,
  AzureOpenAiChatCompletionTool,
  AzureOpenAiChatCompletionRequestToolMessage,
  AzureOpenAiChatCompletionRequestMessage
} from '@sap-ai-sdk/foundation-models';
declare const convertTemperatureTool: AzureOpenAiChatCompletionTool;
declare function callFunction(name: string, args: any): string;

const client = new AzureOpenAiChatClient('gpt-5');
const messages: AzureOpenAiChatCompletionRequestMessage[] = [
  {
    role: 'user',
    content: 'Convert 20 degrees Celsius to Fahrenheit.'
  }
];
const response = await client.run({
  messages,
  tools: [convertTemperatureTool]
});
// ---cut---
const initialResponse = response._data.choices[0].message;
messages.push(initialResponse);
let toolMessage: AzureOpenAiChatCompletionRequestToolMessage;

if (initialResponse.tool_calls) {
  const toolCall = initialResponse.tool_calls[0];
  const name = toolCall.function.name;
  const args = JSON.parse(toolCall.function.arguments);

  // Execute the function with the provided arguments
  const toolResult = callFunction(name, args);

  toolMessage = {
    role: 'tool',
    content: toolResult,
    tool_call_id: toolCall.id
  };
}
```

The `callFunction` function routes the calls to the actual implementations.

```ts twoslash
function callFunction(name: string, args: any): string {
  switch (name) {
    case 'convert_temperature_to_fahrenheit':
      return convertTemperatureToFahrenheit(args.temperature);
    default:
      throw new Error(`Function: ${name} not found!`);
  }
}

function convertTemperatureToFahrenheit(temperature: number): string {
  return `The temperature in Fahrenheit is ${(temperature * 9) / 5 + 32}°F.`;
}
```

Send the function result back to the model to get it's final response:

```ts twoslash
import {
  AzureOpenAiChatClient,
  AzureOpenAiChatCompletionTool,
  AzureOpenAiChatCompletionRequestToolMessage
} from '@sap-ai-sdk/foundation-models';
declare const convertTemperatureTool: AzureOpenAiChatCompletionTool;
declare const messages: { role: 'user'; content: string }[];
declare const toolMessage: AzureOpenAiChatCompletionRequestToolMessage;
const client = new AzureOpenAiChatClient('gpt-5');
// ---cut---
const finalResponse = await client.run({
  messages: [...messages, toolMessage],
  tools: [convertTemperatureTool]
});

console.log(finalResponse.getContent());
```

### Access to Raw HTTP Response

The SAP Cloud SDK for AI provides access to the underlying HTTP response through the `rawResponse` property on response objects.
Use this for advanced scenarios such as accessing response headers, inspecting HTTP status codes, or debugging.

```ts twoslash
import { AzureOpenAiChatClient } from '@sap-ai-sdk/foundation-models';
const client = new AzureOpenAiChatClient('gpt-5');
// ---cut---
const response = await client.run({
  messages: [{ role: 'user', content: 'Hello World!' }]
});

// Recommended: Use convenience methods for typical use cases
console.log(response.getContent());

// Advanced: Access HTTP response details when needed
console.log(response.rawResponse.status); // HTTP status code
console.log(response.rawResponse.headers); // Response headers
console.log(response.rawResponse.data); // Raw response data
```

:::tip
For most use cases, prefer the convenience methods like `getContent()` and `getTokenUsage()`.
Use `rawResponse` only when you need direct access to HTTP-level details.
:::

The `rawResponse` property is available on chat completion response objects, but not on the streaming response object returned by the `stream()` method.
If you need access to the raw HTTP response for streaming requests, please open a feature request on our [GitHub repository](https://github.com/SAP/ai-sdk-js/issues/new).

## Resilience

Use the `resilience()` function from `@sap-cloud-sdk/resilience` to add resilience to requests.
By default, it enables a circuit breaker and a 10-second timeout.

```ts twoslash
import { AzureOpenAiChatClient } from '@sap-ai-sdk/foundation-models';
const client = new AzureOpenAiChatClient('gpt-5');
// ---cut---
import { resilience } from '@sap-cloud-sdk/resilience';

const request = {
  messages: [
    {
      role: 'user' as const,
      content: 'Where is the deepest place on earth located?'
    }
  ]
};

const response = await client.run(request, {
  middleware: resilience()
});
```

:::tip
`resilience()` returns an array of middleware.
You can pass it directly to `middleware` or combine it with other middleware: `[...resilience(), myMiddleware]`.
:::

Customize the behavior by passing options:

<!-- vale off -->

```ts twoslash
import { resilience } from '@sap-cloud-sdk/resilience';
import { AzureOpenAiChatClient } from '@sap-ai-sdk/foundation-models';
const client = new AzureOpenAiChatClient('gpt-5');
const request = { messages: [{ role: 'user' as const, content: '' }] };
// ---cut---
const response = await client.run(request, {
  middleware: resilience({
    timeout: 5000, // 5 seconds; true for default 10s, false to disable
    circuitBreaker: true, // true by default, false to disable
    retry: 3 // false by default; true for 3 retries, or pass a number
  })
});
```

<!-- vale on -->

For advanced resilience patterns, refer to the [SAP Cloud SDK documentation on resilience](https://sap.github.io/cloud-sdk/docs/js/guides/resilience).

### Request Cancellation

Cancel HTTP requests using the `AbortSignal` API to stop in-flight requests when they are no longer needed.
This is useful when end-users navigate away from a page, close a dialog, or explicitly cancel an operation.
Pass an `AbortSignal` through the `signal` property of the request configuration parameter and call the `abort()` method on the controller when you want to cancel the request.

```ts twoslash
import { AzureOpenAiChatClient } from '@sap-ai-sdk/foundation-models';
const client = new AzureOpenAiChatClient('gpt-5');
// ---cut---
const controller = new AbortController();

const response = client.run(
  {
    messages: [
      {
        role: 'user',
        content: 'What is the capital of France?'
      }
    ]
  },
  { signal: controller.signal }
);

// Cancel the request after one second
setTimeout(() => {
  controller.abort();
}, 1000);

try {
  await response;
} catch (error: any) {
  console.error('Request was cancelled:', error.message);
}
```

:::info
HTTP request cancellation may not cancel the request on the AI service.
The cancellation stops the HTTP connection from the client side, but the service may continue processing the request.
Metering information may not be available for cancelled requests.
:::
