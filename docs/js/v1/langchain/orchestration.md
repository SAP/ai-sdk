# Orchestration Integration

The `@sap-ai-sdk/langchain` packages provides `OrchestrationClient` client for LangChain integration with orchestration service.

## Client Initialization[​](#client-initialization "Direct link to Client Initialization")

The client reuses the orchestration client from `@sap-ai-sdk/orchestration` and implements [LangChain's interface](https://js.langchain.com/docs/introduction). Therefore, the client initialization combines the configuration of the orchestration client and LangChain options.

Similar to the orchestration client, the `OrchestrationClient` LangChain client can be initialized with an orchestration configuration. Refer to [Orchestration Chat Completion](/ai-sdk/docs/js/v1/orchestration/chat-completion.md) for more information about the configuration.

```
import { OrchestrationClient } from '@sap-ai-sdk/langchain';



const config: OrchestrationModuleConfig = {

  llm: {

    model_name: 'gpt-4o'

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

For more information about configuring a destination, refer to the [Using a Destination](/ai-sdk/docs/js/v1/connecting-to-ai-core.md#using-a-destination) section.

## Chat Completion[​](#chat-completion "Direct link to Chat Completion")

Pass a message history and, in most cases, input parameters for the orchestration templating module.

```
const systemMessage = new SystemMessage('Be a helpful assistant!');

const history = [systemMessage];

const response = await client.invoke(history, {

  inputParams: { subject: 'Paris' }

});
```

### Streaming[​](#streaming "Direct link to Streaming")

The client supports streaming responses for chat completion requests. Use the `stream()` method to receive a stream of chunk responses from the model.

By default, the last chunk contains the finish reason and token usage information.

warning

The orchestration service currently doesn't support multiple choices during streaming.

```
const orchestrationConfig: LangchainOrchestrationModuleConfig = {

  llm: {

    model_name: 'gpt-4o'

  }

};



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
const orchestrationConfig: LangchainOrchestrationModuleConfig = {

  llm: {

    model_name: 'gpt-4o'

  }

};



const client = new OrchestrationClient(orchestrationConfig);

const controller = new AbortController();

const { signal } = controller;

const response = await client.stream([

  {

    role: 'user',

    content:

      'Write a 100 word explanation about SAP Cloud SDK and its capabilities'

  },

  { signal }

]);



// Abort the streaming request after one second

setTimeout(() => {

  controller.abort();

}, 1000);



for await (const chunk of response) {

  console.log(chunk.content);

}
```

In this example, streaming request will be aborted after one second. Abort controller can be useful, e.g., when end-user wants to stop the stream or refreshes the page.

### Tool Calling[​](#tool-calling "Direct link to Tool Calling")

LangChain offers a unified way to connect tools to language models. Use the `bindTools()` method to define the set of tools a model can access. For more details, see the [official LangChain documentation on tool binding](https://js.langchain.com/docs/concepts/tool_calling/#tool-binding). For a usage example, refer to the [getting started with agents tutorial](/ai-sdk/docs/js/v1/tutorials/getting-started-with-agents.md#define-tools).

## Resilience[​](#resilience "Direct link to Resilience")

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
