# Upgrade Guide

This document guides you through upgrading from version 1 to version 2 of the SAP Cloud SDK for AI packages. It covers all breaking changes and migration steps required for the upgrade.

## Update Dependencies[​](#update-dependencies "Direct link to Update Dependencies")

Search for occurrences of `@sap-ai-sdk/[some module]` in your `package.json` files. Replace the version numbers with `^2`. Run `npm install` or similar to install the dependencies and update the lock file.

Running your tests or deploying your application might fail at this point if you need to adapt to any breaking changes. We recommend updating your applications in one commit or pull request and making sure everything still works using your existing test suite.

## `@sap-ai-sdk/foundation-models`[​](#sap-ai-sdkfoundation-models "Direct link to sap-ai-sdkfoundation-models")

### Type Import[​](#type-import "Direct link to Type Import")

Generated types are no longer exported from `@sap-ai-sdk/foundation-models`. For frequently used types in most cases, they remain available from the public exports. For edge cases where the underlying generated types are used, they must be imported from `@sap-ai-sdk/foundation-models/internal.js`.

Change from **v1:**

```
import type {

  AzureOpenAiCreateChatCompletionRequest,

  AzureOpenAiCreateChatCompletionResponse

} from '@sap-ai-sdk/foundation-models';
```

to **v2:**

```
// Generated types must be imported from internal

import type {

  AzureOpenAiChatCompletionParameters,

  AzureOpenAiCreateChatCompletionResponse

} from '@sap-ai-sdk/foundation-models/internal.js';



// Frequently used types remain available from main package

import type {

  AzureOpenAiChatCompletionTool,

  AzureOpenAiFunctionObject,

  AzureOpenAiChatCompletionRequestMessage,

  AzureOpenAiChatCompletionRequestSystemMessage,

  AzureOpenAiChatCompletionRequestUserMessage,

  AzureOpenAiChatCompletionRequestAssistantMessage,

  AzureOpenAiChatCompletionRequestToolMessage

} from '@sap-ai-sdk/foundation-models';
```

### Stream Controller[​](#stream-controller "Direct link to Stream Controller")

The `stream()` method now accepts an `AbortSignal` instead of an `AbortController` as the second parameter.

Change from **v1:**

```
const controller = new AbortController();

const response = await azureOpenAiChatClient.stream(

  {

    messages: [{ role: 'user', content: 'Hello' }],

    max_tokens: 100

  },

  controller // Pass the controller

);
```

to **v2:**

```
const controller = new AbortController();

const response = await azureOpenAiChatClient.stream(

  {

    messages: [{ role: 'user', content: 'Hello' }],

    max_tokens: 100

  },

  controller.signal // Pass the signal instead

);
```

### Chat Completion Parameter Type[​](#chat-completion-parameter-type "Direct link to Chat Completion Parameter Type")

The `AzureOpenAiCreateChatCompletionRequest` type is no longer exported publicly. Use the new `AzureOpenAiChatCompletionParameters` type instead.

Change from **v1:**

```
import type { AzureOpenAiCreateChatCompletionRequest } from '@sap-ai-sdk/foundation-models';



const request: AzureOpenAiCreateChatCompletionRequest = {

  messages: [{ role: 'user', content: 'Hello' }],

  max_tokens: 100

};
```

to **v2:**

```
import type { AzureOpenAiChatCompletionParameters } from '@sap-ai-sdk/foundation-models';



const request: AzureOpenAiChatCompletionParameters = {

  messages: [{ role: 'user', content: 'Hello' }],

  max_tokens: 100

};
```

### Response Object Data Property[​](#response-object-data-property "Direct link to Response Object Data Property")

The `data` property in response objects is renamed to `_data`. Prefer using the provided getter methods instead of accessing the data object directly.

**Affected Response Classes:**

* `AzureOpenAiChatCompletionResponse`
* `AzureOpenAiChatCompletionStreamChunkResponse`
* `AzureOpenAiEmbeddingResponse`

## `@sap-ai-sdk/orchestration`[​](#sap-ai-sdkorchestration "Direct link to sap-ai-sdkorchestration")

In v2, the orchestration package targets v2 of the [Orchestration service](https://api.sap.com/api/ORCHESTRATION_API_v2/overview).

### Type Import[​](#type-import-1 "Direct link to Type Import")

Generated types are no longer exported from `@sap-ai-sdk/orchestration`. For frequently used types in most cases, they remain available from the public exports. For edge cases where the underlying generated types are used, they must be imported from `@sap-ai-sdk/orchestration/internal.js`.

Change from **v1:**

```
import type {

  CompletionPostResponse,

  LlmChoice

} from '@sap-ai-sdk/orchestration';
```

to **v2:**

```
// Generated types must be imported from internal

import type {

  CompletionPostResponse,

  LlmChoice

} from '@sap-ai-sdk/orchestration/internal.js';



// Frequently used types remain available from main package

import type {

  ChatMessage,

  SystemChatMessage,

  UserChatMessage,

  AssistantChatMessage,

  ToolChatMessage,

  DeveloperChatMessage,

  ChatCompletionTool,

  FunctionObject

} from '@sap-ai-sdk/orchestration';
```

### Stream Controller[​](#stream-controller-1 "Direct link to Stream Controller")

The `stream()` method now accepts an `AbortSignal` instead of an `AbortController` as the second parameter.

Change from **v1:**

```
const controller = new AbortController();

const response = await orchestrationClient.stream(

  { messages: [{ role: 'user', content: 'Hello' }] },

  controller // Pass the controller

);
```

to **v2:**

```
const controller = new AbortController();

const response = await orchestrationClient.stream(

  { messages: [{ role: 'user', content: 'Hello' }] },

  controller.signal // Pass the signal instead

);
```

### Response Object Data Property[​](#response-object-data-property-1 "Direct link to Response Object Data Property")

The `data` property in response objects is renamed to `_data`. Prefer using the provided getter methods instead of accessing the data object directly.

**Affected Response Classes:**

* `OrchestrationResponse`
* `OrchestrationStreamResponse`
* `OrchestrationStreamChunkResponse`

### Module Configuration Structure[​](#module-configuration-structure "Direct link to Module Configuration Structure")

The most significant change is the consolidation of `llm` and `templating` modules into a single `promptTemplating` module as `model` and `prompt` properties respectively.

Change from **v1:**

```
const config = {

  llm: {

    model_name: 'gpt-5',

    model_params: {}

  },

  templating: {

    template: [

      { role: 'user', content: 'What is the capital of {{?country}}?' }

    ]

  }

};
```

to **v2:**

```
const config = {

  promptTemplating: {

    model: {

      name: 'gpt-5',

      params: {}

    },

    prompt: {

      template: [

        { role: 'user', content: 'What is the capital of {{?country}}?' }

      ]

    }

  }

};
```

### Chat Completion Parameter[​](#chat-completion-parameter "Direct link to Chat Completion Parameter")

The `inputParams` property for chat completion calls has been renamed to `placeholderValues`.

Change from **v1:**

```
orchestrationClient.chatCompletion({

  inputParams: { country: 'France' }

});
```

to **v2:**

```
orchestrationClient.chatCompletion({

  placeholderValues: { country: 'France' }

});
```

### Global Streaming Configuration[​](#global-streaming-configuration "Direct link to Global Streaming Configuration")

The global streaming configuration has been updated to use an `enabled` flag instead of a top-level `stream` property.

Change from **v1:**

```
const config = {

  stream: true,

  streamOptions: {

    llm: { include_usage: true }

  }

};
```

to **v2:**

```
const config = {

  streamOptions: {

    enabled: true,

    promptTemplating: { include_usage: true }

  }

};
```

### Response Structure[​](#response-structure "Direct link to Response Structure")

The response structure has been updated with new property names.

Change from **v1:**

```
// Response properties

response.orchestration_result;

response.module_results;
```

to **v2:**

```
// Response properties

response.final_result;

response.intermediate_results;
```

### Grounding Configuration[​](#grounding-configuration "Direct link to Grounding Configuration")

The grounding configuration structure has been updated to use `placeholders` instead of separate `input_params` and `output_param`.

Change from **v1:**

```
buildDocumentGroundingConfig({

  input_params: ['groundingInput'],

  output_param: 'groundingOutput',

  filters: [...]

});
```

to **v2:**

```
buildDocumentGroundingConfig({

  placeholders: {

    input: ['groundingInput'],

    output: 'groundingOutput'

  },

  filters: [...]

});
```

### Removed Functions[​](#removed-functions "Direct link to Removed Functions")

The deprecated `buildAzureContentFilter()` function has been removed in v2. Use `buildAzureContentSafetyFilter()` instead.

Change from **v1:**

```
// This function is deprecated and removed in v2

const filter = buildAzureContentFilter({

  Hate: 'ALLOW_SAFE',

  Violence: 'ALLOW_SAFE_LOW_MEDIUM'

});
```

to **v2:**

```
// Use this function instead

const filter = buildAzureContentSafetyFilter('input', {

  // For output filter, use type 'output'

  hate: 'ALLOW_SAFE',

  violence: 'ALLOW_SAFE_LOW_MEDIUM'

});
```

### Azure Content Filter[​](#azure-content-filter "Direct link to Azure Content Filter")

The `buildAzureContentSafetyFilter()` function now requires a `type` parameter as the first argument to distinguish between input and output filter configurations. Additionally, the Azure content filter property names have been updated to use lowercase with underscores.

Change from **v1:**

```
buildAzureContentSafetyFilter({

  Hate: 'ALLOW_SAFE',

  SelfHarm: 'ALLOW_SAFE_LOW',

  Sexual: 'ALLOW_SAFE_LOW_MEDIUM',

  Violence: 'ALLOW_ALL'

});
```

to **v2:**

```
// For input filters

buildAzureContentSafetyFilter('input', {

  hate: 'ALLOW_SAFE',

  self_harm: 'ALLOW_SAFE_LOW',

  sexual: 'ALLOW_SAFE_LOW_MEDIUM',

  violence: 'ALLOW_ALL'

});



// For output filters

buildAzureContentSafetyFilter('output', {

  hate: 'ALLOW_SAFE',

  self_harm: 'ALLOW_SAFE_LOW',

  sexual: 'ALLOW_SAFE_LOW_MEDIUM',

  violence: 'ALLOW_ALL'

});
```

### Llama Guard Filter[​](#llama-guard-filter "Direct link to Llama Guard Filter")

The `buildLlamaGuardFilter()` function has been renamed to `buildLlamaGuard38BFilter()` function. It now requires a `type` parameter as the first argument to distinguish between `input` and `output` filter configurations, and accepts categories as an array instead of individual parameters.

Change from **v1:**

```
buildLlamaGuardFilter('self_harm');
```

to **v2:**

```
// For input filters

buildLlamaGuard38BFilter('input', ['self_harm', 'violence']);



// For output filters

buildLlamaGuard38BFilter('output', ['self_harm', 'violence']);
```

### Translation Configuration[​](#translation-configuration "Direct link to Translation Configuration")

The `buildTranslationConfig()` function now requires a `type` parameter as the first argument to distinguish between input and output translation configurations.

Change from **v1:**

```
buildTranslationConfig({

  sourceLanguage: 'en-US',

  targetLanguage: 'de-DE'

});
```

to **v2:**

```
// For input translation

buildTranslationConfig('input', {

  sourceLanguage: 'en-US',

  targetLanguage: 'de-DE'

});



// For output translation

buildTranslationConfig('output', {

  sourceLanguage: 'de-DE',

  targetLanguage: 'fr-FR'

});
```

## `@sap-ai-sdk/langchain`[​](#sap-ai-sdklangchain "Direct link to sap-ai-sdklangchain")

### Configuration Structure[​](#configuration-structure "Direct link to Configuration Structure")

The LangChain orchestration configuration follows the same structural changes as the core orchestration package.

Change from **v1:**

```
const config: LangChainOrchestrationModuleConfig = {

  llm: {

    model_name: 'gpt-5',

    model_params: {}

  },

  templating: {

    template: messages

  }

};
```

to **v2:**

```
const config: LangChainOrchestrationModuleConfig = {

  promptTemplating: {

    model: {

      name: 'gpt-5',

      params: {}

    },

    prompt: {

      template: messages

    }

  }

};
```

### Invoke Parameter[​](#invoke-parameter "Direct link to Invoke Parameter")

Input parameters for LangChain orchestration calls have been updated.

Change from **v1:**

```
await orchestrationClient.invoke(messages, {

  inputParams: { country: 'France' }

});
```

to **v2:**

```
await orchestrationClient.invoke(messages, {

  placeholderValues: { country: 'France' }

});
```

### Response Property[​](#response-property "Direct link to Response Property")

LangChain message responses now use updated property names for intermediate results.

Change from **v1:**

```
// Access module results in response

message.additional_kwargs.module_results;
```

to **v2:**

```
// Access intermediate results in response

message.additional_kwargs.intermediate_results;
```
