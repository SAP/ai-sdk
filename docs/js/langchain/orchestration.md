# Orchestration Integration

The `@sap-ai-sdk/langchain` packages provides `OrchestrationClient` client for LangChain integration with orchestration service.

## Client Initialization[​](#client-initialization "Direct link to Client Initialization")

The client reuses the orchestration client from `@sap-ai-sdk/orchestration` and implements [LangChain's interface](https://docs.langchain.com/oss/javascript/langchain/models). Therefore, the client initialization combines the configuration of the orchestration client and LangChain options.

Similar to the orchestration client, the `OrchestrationClient` LangChain client can be initialized with an orchestration configuration. Refer to [Orchestration Chat Completion](/ai-sdk/docs/js/orchestration/chat-completion.md) for more information about the configuration.

```
import { OrchestrationClient } from '@sap-ai-sdk/langchain';

import type { LangChainOrchestrationModuleConfig } from '@sap-ai-sdk/langchain';



const config: LangChainOrchestrationModuleConfig = {

  promptTemplating: {

    model: {

      name: 'gpt-5'

    }

  }

};

const client = new OrchestrationClient(config);
```

Optionally, you can also specify LangChain options, resource group in deployment config, and a custom destination.

### Custom Destination[​](#custom-destination "Direct link to Custom Destination")

When initializing the client, it is possible to provide a custom destination for your SAP AI Core instance.

```
const client = new OrchestrationClient(

  orchestrationConfig,

  langchainOptions,

  deploymentConfig,

  { destinationName: 'my-destination' }

);
```

By default, the fetched destination is cached. To disable caching, set the `useCache` parameter to `false` together with the `destinationName` parameter.

For more information about configuring a destination, refer to the [Using a Destination](/ai-sdk/docs/js/connecting-to-ai-core.md#using-a-destination) section.

## Chat Completion[​](#chat-completion "Direct link to Chat Completion")

Pass a message history and, in most cases, input parameters for the orchestration templating module.

```
const systemMessage = new SystemMessage('Be a helpful assistant!');

const history = [systemMessage];

const response = await client.invoke(history, {

  placeholderValues: { subject: 'Paris' }

});
```

### Module Fallback[​](#module-fallback "Direct link to Module Fallback")

The [`OrchestrationClient`](/ai-sdk/api/v2/classes/langchain_src.OrchestrationClient.html) supports module fallback, which allows you to provide multiple orchestration configurations that are tried in sequence until one succeeds. Pass a non-empty array of [`LangChainOrchestrationModuleConfig`](/ai-sdk/api/v2/types/langchain_src.LangChainOrchestrationModuleConfig.html) objects when initializing the client, using the [`LangChainOrchestrationModuleConfigList`](/ai-sdk/api/v2/types/langchain_src.LangChainOrchestrationModuleConfigList.html) type.

For a full explanation of when fallback is triggered and how it works with the orchestration service, refer to [Module Fallback](/ai-sdk/docs/js/orchestration/chat-completion.md#module-fallback) in the orchestration documentation.

```
import type { LangChainOrchestrationModuleConfigList } from '@sap-ai-sdk/langchain';



const orchestrationConfigs: LangChainOrchestrationModuleConfigList = [

  {

    // Primary configuration — fails if the model is unavailable

    promptTemplating: {

      model: {

        name: 'gpt-5',

        timeout: 10 // seconds; triggers fallback on timeout (non-streaming only)

      }

    }

  },

  {

    // Fallback configuration

    promptTemplating: {

      model: {

        name: 'anthropic--claude-4.5-haiku'

      }

    }

  }

];



const response = await new OrchestrationClient(orchestrationConfigs).invoke([

  { role: 'user', content: 'Tell me about SAP Cloud SDK.' }

]);
```

Module fallback also works with the `stream()` method. Note that in streaming scenarios, only model unavailability triggers fallback. Unlike non-streaming requests, timeouts will not trigger fallback during streaming.

```
import type { AIMessageChunk } from '@langchain/core/messages';



const client = new OrchestrationClient(orchestrationConfigs);

const stream = await client.stream([

  { role: 'user', content: 'Tell me about SAP Cloud SDK.' }

]);



let finalOutput: AIMessageChunk | undefined;

for await (const chunk of stream) {

  finalOutput = finalOutput ? finalOutput.concat(chunk) : chunk;

}
```

### Streaming[​](#streaming "Direct link to Streaming")

The client supports streaming responses for chat completion requests. Use the `stream()` method to receive a stream of chunk responses from the model.

By default, the last chunk contains the finish reason and token usage information.

warning

The orchestration service currently doesn't support multiple choices during streaming.

```
const client = new OrchestrationClient(orchestrationConfig);

const response = await client.stream([

  {

    role: 'user',

    content:

      'Write a 100 word explanation about SAP Cloud SDK and its capabilities'

  }

]);



let finalResult: AIMessageChunk | undefined;



for await (const chunk of response) {

  console.log(chunk.content);

  finalResult = finalResult ? finalResult.concat(chunk) : chunk;

}



console.log(finalResult?.response_metadata?.finish_reason);



console.log(finalResult?.usage_metadata);

/*

  { input_tokens: 13, output_tokens: 30, total_tokens: 43 }

*/



// Token usage is also available in `response_metadata` property

console.log(finalResult?.response_metadata?.token_usage);

/*

  { completion_tokens: 30, prompt_tokens: 13, total_tokens: 43 }

*/
```

#### Streaming with Abort Controller[​](#streaming-with-abort-controller "Direct link to Streaming with Abort Controller")

The client supports aborting streaming requests using the `AbortController` API. In case of an error, SAP Cloud SDK for AI will automatically close the stream. It can also be manually aborted if an `AbortSignal` object associated with an `AbortController` was provided when calling the `stream()` method.

```
const client = new OrchestrationClient(orchestrationConfig);

const controller = new AbortController();

const { signal } = controller;

const response = await client.stream(

  [

    {

      role: 'user',

      content:

        'Write a 100 word explanation about SAP Cloud SDK and its capabilities'

    }

  ],

  { signal }

);



// Abort the streaming request after one second

setTimeout(() => {

  controller.abort();

}, 1000);



for await (const chunk of response) {

  console.log(chunk.content);

}
```

In this example, streaming request will be aborted after one second. Abort controller can be useful, e.g., when end-user wants to stop the stream or refreshes the page.

#### Streaming Configuration[​](#streaming-configuration "Direct link to Streaming Configuration")

By default, the `stream()` method supports streaming, while the `invoke()` method uses non-streaming requests.

##### Auto-Streaming[​](#auto-streaming "Direct link to Auto-Streaming")

Set the `streaming` option to `true` to enable automatic streaming for all requests made with the `invoke()` method:

```
const client = new OrchestrationClient(orchestrationConfig, {

  streaming: true

});



const response = await client.invoke(messageHistory);
```

With auto-streaming enabled, the `invoke()` method uses streaming to retrieve responses, returning the complete result upon completion. This option is automatically enabled by LangGraph when a LangGraph-based agent is used with a [streaming mode](https://docs.langchain.com/oss/javascript/langgraph/streaming#supported-stream-modes) that can output partial responses, such as "updates".

##### Disabling Streaming[​](#disabling-streaming "Direct link to Disabling Streaming")

Set the `disableStreaming` option to turn off streaming entirely.

```
const client = new OrchestrationClient(orchestrationConfig, {

  disableStreaming: true

});



const response = await client.stream(messageHistory);
```

When streaming is disabled, both the `invoke()` and `stream()` methods use non-streaming requests internally. The `stream()` method will still return an iterable, but it will yield a single chunk containing the complete response.

### Tool Calling[​](#tool-calling "Direct link to Tool Calling")

LangChain offers a unified way to connect tools to language models. Use the `bindTools()` method to define the set of tools a model can access. For more details, see the [official LangChain documentation on tool binding](https://docs.langchain.com/oss/javascript/langchain/models#tool-calling). For a usage example, refer to the [getting started with agents tutorial](/ai-sdk/docs/js/tutorials/getting-started-agents.md#define-tools).

### Basic Agent Usage[​](#basic-agent-usage "Direct link to Basic Agent Usage")

The `OrchestrationClient` can be used with LangChain's agent framework through the `createAgent()` function.

note

In LangChain v1, the function `createReactAgent` was replaced by `createAgent`.

Create an agent by providing the orchestration client as the model, along with any tools you want the agent to use:

```
import { createAgent } from 'langchain';

import { OrchestrationClient } from '@sap-ai-sdk/langchain';



const model = new OrchestrationClient({

  promptTemplating: {

    model: {

      name: 'gpt-5'

    }

  }

});



const agent = createAgent({

  model,

  tools: []

});



const agentInputs = {

  messages: [{ role: 'user', content: 'What is SAP?' }]

};



const result = await agent.invoke(agentInputs);
```

### Prompt Caching[​](#prompt-caching "Direct link to Prompt Caching")

note

Prompt caching is supported by Anthropic Claude and Amazon Nova model families served through orchestration. Other models ignore the `cache_control` directive without error. For a full overview, refer to the [prompt caching documentation](https://help.sap.com/docs/sap-ai-core/generative-ai/prompt-caching?locale=en-US).

Prompt caching reduces latency and cost by reusing cached content at the model provider level. The SDK offers two approaches: a per-call option and an agent middleware.

#### Per-Call Cache Control[​](#per-call-cache-control "Direct link to Per-Call Cache Control")

Pass `cache_control` as a call option to `invoke()` or `stream()`. The SDK automatically places a cache breakpoint on the last cacheable block of the last message, so the breakpoint advances naturally as the conversation grows.

```
import { OrchestrationClient } from '@sap-ai-sdk/langchain';



const client = new OrchestrationClient({

  promptTemplating: {

    model: {

      name: 'anthropic--claude-4.5-haiku'

    }

  }

});



const response = await client.invoke(

  [{ role: 'user', content: 'What is the speed of light?' }],

  { cache_control: { type: 'ephemeral' } }

);



console.log(response.usage_metadata?.input_token_details);

/*

  { cache_read: 0, cache_creation: TOKEN_COUNT }   // first call: tokens written to cache

  { cache_read: TOKEN_COUNT, cache_creation: 0 }   // identical repeated call: tokens read from cache

*/
```

#### Prompt Caching Middleware[​](#prompt-caching-middleware "Direct link to Prompt Caching Middleware")

For agents, use `orchestrationPromptCachingMiddleware()` to manage cache breakpoints automatically across turns. Pass it to `createAgent()` via the `middleware` option.

note

The middleware is exported from a sub-path that requires the `langchain` package to be installed as a direct dependency. You can install it with `npm install langchain`.

```
import { createAgent } from 'langchain';

import { OrchestrationClient } from '@sap-ai-sdk/langchain';

import { orchestrationPromptCachingMiddleware } from '@sap-ai-sdk/langchain/orchestration/prompt-caching-middleware';



const model = new OrchestrationClient({

  promptTemplating: {

    model: {

      name: 'anthropic--claude-4.5-haiku'

    }

  }

});



const agent = createAgent({

  model,

  middleware: [orchestrationPromptCachingMiddleware({ ttl: '5m' })],

  tools: []

});



const result = await agent.invoke({

  messages: [{ role: 'user', content: 'What is the speed of light?' }]

});
```

For configuration options such as `minMessagesToCache` and `unsupportedModelBehavior`, refer to the [LangChain `anthropicPromptCachingMiddleware()` middleware documentation](https://reference.langchain.com/javascript/langchain/browser/anthropicPromptCachingMiddleware).

### Structured Output[​](#structured-output "Direct link to Structured Output")

It is often useful to have a model return output that matches a specific schema. This schema can be defined using either a [Zod](https://zod.dev/) schema or a JSON schema. We recommend using Zod v4 for full compatibility with this package. If you're upgrading from an earlier version, refer to the [Zod v4 migration guide](https://zod.dev/v4/changelog) and pay attention to breaking changes like the switch from `describe('...')` to `meta({ description: '...' })`. For more details on structured output, refer to the [official LangChain documentation on structured output](https://docs.langchain.com/oss/javascript/langchain/models#structured-outputs). Below is an example using `json_schema` response type and passing in a Zod schema.

```
import * as z from 'zod';

import { OrchestrationClient } from '@sap-ai-sdk/langchain';



const llm = new OrchestrationClient({

  promptTemplating: {

    model: {

      name: 'gpt-5'

    }

  }

});



const joke = z.object({

  setup: z.string().meta({ description: 'The setup of the joke' }),

  punchline: z.string().meta({ description: 'The punchline to the joke' }),

  rating: z

    .number()

    .meta({ description: 'How funny the joke is, from 1 to 10' })

});



const structuredLlm = llm.withStructuredOutput(joke, {

  name: 'joke',

  strict: true

});



const finalResponse = await structuredLlm.invoke('Tell me a joke about cats');
```

## Resilience[​](#resilience "Direct link to Resilience")

warning

The Langchain, Orchestration layer and the SAP Cloud SDK resilience mechanisms should not be combined, or should be integrated only with careful consideration.

Use LangChain options such as `maxRetries` and `timeout` to provide resilience.

### Retry[​](#retry "Direct link to Retry")

By default, LangChain client retries up to six times with exponential delay. To modify this behavior, set the `maxRetries` option during the client initialization.

```
const client = new OrchestrationClient(orchestrationConfig, {

  maxRetries: 0

});
```

note

If the error is caused by input content filtering, the client will throw immediately without retrying.

### Timeout[​](#timeout "Direct link to Timeout")

By default, no timeout is set in the client. To limit the maximum duration for the entire request including retries, specify a timeout in milliseconds when calling the `invoke` method. A request that times out will be [retried](#retry) by default.

```
const response = await client.invoke(messageHistory, { timeout: 10000 });
```

Timeout can also be set for streaming requests.

```
const response = await client.stream(

  [

    {

      role: 'user',

      content: 'Hello world! Why is this phrase so famous?'

    }

  ],

  { timeout: 1000 }

);
```
