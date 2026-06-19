# OpenAI Integration

The `@sap-ai-sdk/langchain` packages provides `AzureOpenAiChatClient` and `AzureOpenAiEmbeddingClient` clients for LangChain integration with Azure OpenAI.

## Client Initialization[​](#client-initialization "Direct link to Client Initialization")

Both clients reuse the Azure OpenAI clients from `@sap-ai-sdk/foundation-models` and implement [LangChain's interface](https://js.langchain.com/docs/introduction). Therefore, the client initialization combines the configuration of the foundation model and LangChain options.

Similar to the foundation model clients, the `AzureOpenAiChatClient` and `AzureOpenAiEmbeddingClient` LangChain clients can be initialized with model name and, by default, the latest model version.

```
import {

  AzureOpenAiChatClient,

  AzureOpenAiEmbeddingClient

} from '@sap-ai-sdk/langchain';



const chatClient = new AzureOpenAiChatClient({ modelName: 'gpt-4o' });

const embeddingClient = new AzureOpenAiEmbeddingClient({

  modelName: 'text-embedding-3-small'

});
```

Optionally, you can also specify model version, resource group and other parameters such as `max_tokens`, `temperature` and more.

note

Providing a deployment ID is currently not supported.

### Custom Destination[​](#custom-destination "Direct link to Custom Destination")

When initializing the client, it is possible to provide a custom destination for your SAP AI Core instance.

```
const chatClient = new AzureOpenAiChatClient(

  {

    modelName: 'gpt-4o'

  },

  {

    destinationName: 'my-destination'

  }

);
```

By default, the fetched destination is cached. To disable caching, set the `useCache` parameter to `false` together with the `destinationName` parameter.

For more information about configuring a destination, refer to the [Using a Destination](/ai-sdk/docs/js/v1/connecting-to-ai-core.md#using-a-destination) section.

## Chat Completion[​](#chat-completion "Direct link to Chat Completion")

The `AzureOpenAiChatClient` allows interaction with Azure OpenAI chat models on SAP AI Core. Pass a prompt to invoke the client.

```
const response = await chatClient.invoke("What's the capital of France?");
```

Below is an advanced example demonstrating the usage of templating and output parsing.

```
import { AzureOpenAiChatClient } from '@sap-ai-sdk/langchain';

import { StringOutputParser } from '@langchain/core/output_parsers';

import { ChatPromptTemplate } from '@langchain/core/prompts';



// Initialize the client

const chatClient = new AzureOpenAiChatClient({ modelName: 'gpt-4o' });



// Create a prompt template

const promptTemplate = ChatPromptTemplate.fromMessages([

  ['system', 'Answer the following in {language}:'],

  ['user', '{text}']

]);



// Create an output parser

const parser = new StringOutputParser();



// Chain together template, client and parser

const llmChain = promptTemplate.pipe(chatClient).pipe(parser);



// Invoke the chain

return llmChain.invoke({

  language: 'german',

  text: 'What is the capital of France?'

});
```

### Streaming[​](#streaming "Direct link to Streaming")

The client supports streaming responses for chat completion requests. Use the `stream()` method to receive a stream of chunk responses from the model.

By default, the last chunk contains the finish reason and token usage information.

```
const client = new AzureOpenAiChatClient({ modelName: 'gpt-4o' });

const response = await client.stream([

  {

    role: 'user',

    content:

      'Write a 100 word explanation about SAP Cloud SDK and its capabilities'

  }

]);



let finalResult: AIMessageChunk | undefined;



for await (const chunk of stream) {

  console.log(chunk.content);

  finalResult = finalResult ? finalResult.concat(chunk) : chunk;

}



console.log(finalResult?.response_metadata?.finish_reason);



console.log(finalResult?.usage_metadata);

/*

  { input_tokens: 20, output_tokens: 126, total_tokens: 146 }

*/



// Token usage is also available in `response_metadata` property

console.log(finalResult?.response_metadata?.token_usage);

/*

  {

    completion_tokens: 126,

    completion_tokens_details: {

      accepted_prediction_tokens: 0,

      audio_tokens: 0,

      reasoning_tokens: 0,

      rejected_prediction_tokens: 0

    },

    prompt_tokens: 20,

    prompt_tokens_details: { audio_tokens: 0, cached_tokens: 0 },

    total_tokens: 146

  }

*/
```

#### Streaming with Abort Controller[​](#streaming-with-abort-controller "Direct link to Streaming with Abort Controller")

The client supports aborting streaming requests using the `AbortController` API. In case of an error, SAP Cloud SDK for AI will automatically close the stream. It can also be manually aborted if an `AbortSignal` object associated with an `AbortController` was provided when calling the `stream()` method.

```
const client = new AzureOpenAiChatClient({ modelName: 'gpt-4o' });

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

### Structured Output[​](#structured-output "Direct link to Structured Output")

It is often useful to have a model return output that matches a specific schema. This schema can be defined using either a [Zod](https://zod.dev/) schema or an OpenAI-style JSON schema. For more details on structured output, refer to the [official LangChain documentation on structured output](https://js.langchain.com/docs/how_to/structured_output/#the-.withstructuredoutput-method). Below is an example using `json_schema` response type and passing in a Zod schema.

```
import * as z from 'zod';

import { AzureOpenAiChatClient } from '@sap-ai-sdk/langchain';



const llm = new AzureOpenAiChatClient({ modelName: 'gpt-4o' });



const joke = z.object({

  setup: z.string().describe('The setup of the joke'),

  punchline: z.string().describe('The punchline to the joke'),

  rating: z.number().describe('How funny the joke is, from 1 to 10')

});



const structuredLlm = llm.withStructuredOutput(joke, {

  name: 'joke',

  strict: true

});



const finalResponse = await structuredLlm.invoke('Tell me a joke about cats');
```

## Embedding[​](#embedding "Direct link to Embedding")

The `AzureOpenAiEmbeddingClient` allows embedding text or document chunks (represented as arrays of strings). While the embedding client can be used standalone, it is typically combined with other LangChain utilities, such as a text splitter for preprocessing and a vector store for storing and retrieving relevant embeddings. For a complete example of how to implement RAG with the LangChain client, refer to the [sample code](https://github.com/SAP/ai-sdk-js/blob/main/sample-code/src/langchain-azure-openai.ts).

### Embed Text[​](#embed-text "Direct link to Embed Text")

```
const embeddedText = await embeddingClient.embedQuery(

  'Paris is the capital of France.'

);
```

### Embed Document Chunks[​](#embed-document-chunks "Direct link to Embed Document Chunks")

```
const embeddedDocuments = await embeddingClient.embedDocuments([

  'Page 1: Paris is the capital of France.',

  'Page 2: It is a beautiful city.'

]);
```

### Preprocess, embed, and store documents[​](#preprocess-embed-and-store-documents "Direct link to Preprocess, embed, and store documents")

```
// Create a text splitter and split the document

const textSplitter = new RecursiveCharacterTextSplitter({

  chunkSize: 2000,

  chunkOverlap: 200

});

const splits = await textSplitter.splitDocuments(docs);



// Initialize the embedding client

const embeddingClient = new AzureOpenAiEmbeddingClient({

  modelName: 'text-embedding-3-small'

});



// Create a vector store from the document

const vectorStore = await MemoryVectorStore.fromDocuments(

  splits,

  embeddingClient

);



// Create a retriever for the vector store

const retriever = vectorStore.asRetriever();
```

## Resilience[​](#resilience "Direct link to Resilience")

Use LangChain options such as `maxRetries` and `timeout` to provide resilience.

### Retry[​](#retry "Direct link to Retry")

By default, LangChain client retries up to six times with exponential delay. To modify this behavior, set the `maxRetries` option during the client initialization.

```
const client = new AzureOpenAiChatClient({

  modelName: 'gpt-4o',

  maxRetries: 0

});
```

### Timeout[​](#timeout "Direct link to Timeout")

By default, no timeout is set in the client. To limit the maximum duration for the entire request including retries, specify a timeout in milliseconds when calling the `invoke` method.

```
const response = await client.invoke(messageHistory, { timeout: 10000 });
```
