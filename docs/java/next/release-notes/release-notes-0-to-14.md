# release-notes-0-to-14

## 1.14.0 - January 08, 2026[​](#1140---january-08-2026 "Direct link to 1.14.0 - January 08, 2026")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.14.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes "Direct link to 🔧 Compatibility Notes")

* \[PromptRegistry] Export methods (`exportPromptTemplate`, `exportOrchestrationConfig`) now return `byte[]` instead of `File`. Import methods (`importPromptTemplate`, `importOrchestrationConfig`) now accept `org.springframework.core.io.Resource` instead of `File`.

### ✨ New Functionality[​](#-new-functionality "Direct link to ✨ New Functionality")

* \[Orchestration] Added new models for `OrchestrationAiModel`: `SAP_ABAP_1`, `SONAR`,`SONAR_PRO`, `GEMINI_2_5_FLASH_LITE`, `CLAUDE_4_5_HAIKU`, `CLAUDE_4_5_OPUS`, `GPT_REALTIME`.
* \[Orchestration] Convenience for adding the `metadata_params` option to grounding calls.
* \[Orchestration] Added new models for `OrchestrationAiModel`: `COHERE_COMMAND_A_REASONING`, `NOVA_PREMIER`, `COHERE_RERANKER`.
* \[Orchestration] Deprecated `DEEPSEEK_R1` model from `OrchestrationAiModel` with no replacement.

### 📈 Improvements[​](#-improvements "Direct link to 📈 Improvements")

* \[Orchestration] Added new API `TranslationConfig#translateInputTo` to extract input config.
* \[Orchestration] Added new API `TranslationConfig#translateOutputTo` to extract output config.

### 🐛 Fixed Issues[​](#-fixed-issues "Direct link to 🐛 Fixed Issues")

* \[PromptRegistry] Fix deserialization of `response_format` in retrieved prompt templates.

## 1.13.0 - October 30, 2025[​](#1130---october-30-2025 "Direct link to 1.13.0 - October 30, 2025")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.13.0)

### ✨ New Functionality[​](#-new-functionality-1 "Direct link to ✨ New Functionality")

* \[Orchestration] Introduced Spring AI integration for embeddings generation with the new `OrchestrationSpringAiEmbeddingModel` class.

### 📈 Improvements[​](#-improvements-1 "Direct link to 📈 Improvements")

* \[Core] If the AI Core credentials used are missing an explicit `credential-type` but `clientid` and `clientsecret` are present then `"credential-type": "binding-secret"` is inferred automatically.
* \[Core] Log message about "service key in environment variable" to `INFO` level only once.

## 1.12.0 - October 17, 2025[​](#1120---october-17-2025 "Direct link to 1.12.0 - October 17, 2025")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.12.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes-1 "Direct link to 🔧 Compatibility Notes")

* Breaking change:

  <!-- -->

  * `CompletionPostRequest` is now an interface instead of a class. For all previous use-cases, it should be substitutable with the new class `CompletionRequestConfiguration`.

    <!-- -->

    * `OrchestrationClient.toCompletionPostRequest()` now returns `CompletionRequestConfiguration`.
    * `OrchestrationClient.streamChatCompletionDeltas()` takes `CompletionRequestConfiguration` as an input now.

  * Two fields in `OrchestrationModuleConfig` changed:

    <!-- -->

    * `inputTranslationConfig` is now of type `SAPDocumentTranslationInput`
    * `outputTranslationConfig` is now of type `SAPDocumentTranslationOutput`

  * When using `OrchestrationModuleConfig.withInputTranslationConfig()` and `OrchestrationModuleConfig.withOutputTranslationConfig()` consider the following diff (note, especially, that setting `.applyTo()` to either `null` or to an actual value is necessary):
    <!-- -->
    ```
    var config = new OrchestrationModuleConfig("some prompt");

    config

           .withInputTranslationConfig(

    -          SAPDocumentTranslation.create()

    -              .type(SAP_DOCUMENT_TRANSLATION)

    -              .config(SAPDocumentTranslationConfig.create().targetLanguage("en-US")))

    +          SAPDocumentTranslationInput.create()

    +              .type(SAPDocumentTranslationInput.TypeEnum.SAP_DOCUMENT_TRANSLATION)

    +              .config(

    +                    SAPDocumentTranslationInputConfig.create()

    +                        .targetLanguage("en-US")

    +                        .applyTo(null)))

            .withOutputTranslationConfig(

    -          SAPDocumentTranslation.create()

    -              .type(SAP_DOCUMENT_TRANSLATION)

    +          SAPDocumentTranslationOutput.create()

    +              .type(SAPDocumentTranslationOutput.TypeEnum.SAP_DOCUMENT_TRANSLATION)

                   .config(

    -                  SAPDocumentTranslationConfig.create()

    -                      .targetLanguage("de-DE")

    +                  SAPDocumentTranslationOutputConfig.create()

    +                      .targetLanguage(

    +                          SAPDocumentTranslationOutputTargetLanguage.create("de-DE"))

                           .sourceLanguage("en-US")));
    ```

* \[Orchestration] Deprecated models `OrchestrationAiModel.CLAUDE_3_OPUS` and `OrchestrationAiModel.CLAUDE_3_5_SONNET`.
  <!-- -->
  * Replacement are respectively `OrchestrationAiModel.CLAUDE_4_OPUS` and `OrchestrationAiModel.CLAUDE_4_SONNET`.

* Inner record classes and their creator methods in model interfaces are renamed to be more descriptive and type-specific.
  <!-- -->
  * eg: `InnerString` -> `ListOfStrings`, `create()` -> `createListOfStrings()`

### ✨ New Functionality[​](#-new-functionality-2 "Direct link to ✨ New Functionality")

* \[Orchestration] For streaming, add convenience configuration for output-filter-overlap, chunk-size, and delimiters via `OrchestrationModuleConfig#withStreamConfig`.

* \[Orchestration] Added embedding generation support with new `OrchestrationClient#embed()` methods.

  <!-- -->

  * Added `OrchestrationEmbeddingModel` with `TEXT_EMBEDDING_3_SMALL`, `TEXT_EMBEDDING_3_LARGE`, `AMAZON_TITAN_EMBED_TEXT` and `NVIDIA_LLAMA_32_NV_EMBEDQA_1B` embedding models.
  * Introduced `OrchestrationEmbeddingRequest` for building requests fluently and `OrchestrationEmbeddingResponse#getEmbeddingVectors()` to retrieve embeddings.

* \[Orchestration] Added new model `OrchestrationAiModel.MISTRAL_MEDIUM_INSTRUCT`.

### 📈 Improvements[​](#-improvements-2 "Direct link to 📈 Improvements")

* \[Orchestration] Added new API `DpiMasking#withRegex` to apply custom masking patterns.

### 🐛 Fixed Issues[​](#-fixed-issues-1 "Direct link to 🐛 Fixed Issues")

* \[Orchestration] Tool calling works on all models

## 1.11.0 - September 12, 2025[​](#1110---september-12-2025 "Direct link to 1.11.0 - September 12, 2025")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.11.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes-2 "Direct link to 🔧 Compatibility Notes")

* \[Prompt Registry] breaking changes:

  * `Template` has been renamed to `PromptTemplate`.
  * Some endpoints have a new parameter `String aiResourceGroupScope` which can be set to `null`.

  For more details please refer to the [sample code](https://github.com/SAP/ai-sdk-java/blob/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/PromptRegistryController.java).

### ✨ New Functionality[​](#-new-functionality-3 "Direct link to ✨ New Functionality")

* Extend `OpenAiClientException` and `OrchestrationClientException` to retrieve error diagnostics information received from remote service. New available accessors for troubleshooting: `getErrorResponse()`, `getHttpResponse()` and, `getHttpRequest()`. Please note: depending on the error response, these methods may return `null` if the information is not available.
* \[OpenAI] Added new models for `OpenAiModel`: `GPT_5`, `GPT_5_MINI` and `GPT_5_NANO`.
* \[Orchestration] Added new models for `OrchestrationAiModel`: `GPT_5`, `GPT_5_MINI` and `GPT_5_NANO`.
* \[Orchestration] Deprecated models for `OrchestrationAiModel`: `GEMINI_1_5_PRO` and `OrchestrationAiModel.GEMINI_1_5_FLASH`
  * Replacement are `GEMINI_2_5_PRO` and `GEMINI_2_5_FLASH`.
* \[Orchestration] Deprecated `OrchestrationAiModel.IBM_GRANITE_13B_CHAT` with no replacement.
* \[OpenAI] [Introduced SpringAI integration with our OpenAI client.](/ai-sdk/docs/java/spring-ai/openai.md)
  * Added `OpenAiChatModel`
* \[Prompt Registry] [Using Prompt Registry Templates in SpringAI.](/ai-sdk/docs/java/ai-core/prompt-registry.md#using-templates-in-springai)
  * Added `SpringAiConverter`
* \[Orchestration] [Added convenience to add custom headers to individual orchestration calls.](/ai-sdk/docs/java/orchestration/chat-completion.md#custom-headers)
* \[OpenAI] [Added convenience to add custom headers to individual LLM calls.](/ai-sdk/docs/java/foundation-models/openai/chat-completion.md#custom-headers)

### 🐛 Fixed Issues[​](#-fixed-issues-2 "Direct link to 🐛 Fixed Issues")

* \[Orchestration] Fixed getting `OrchestrationFilterException.Input` for bad requests with input filter.

## 1.10.0 - August 08, 2025[​](#1100---august-08-2025 "Direct link to 1.10.0 - August 08, 2025")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.10.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes-3 "Direct link to 🔧 Compatibility Notes")

* The **Spring AI** version has been increased from `1.0.0-M6` to the GA release `1.0.0`.

  <!-- -->

  * The `OrchestrationChatOptions` have been, replacing all references to `FunctionCallback` with `ToolCallback`.
  * Please follow the [official Spring AI upgrade guide](https://docs.spring.io/spring-ai/reference/upgrade-notes.html#upgrading-to-1-0-0-RC1) for further details.
  * The `@Beta` annotations on all classes related to Spring AI have been removed.

* \[Orchestration] The `completion` endpoint have been moved to the latest version `/v2/completion`

  * `LLMModuleConfig` is replaced by `LLMModelDetails` in `withLLmConfig` method of `OrchestrationModuleConfig` class.
  * `PromptTemplatingModuleConfigPrompt` replaces `TemplatingModuleConfig` in the `withTemplateConfig` method of `OrchestrationModuleConfig` class.
  * The generated model classes will reflect payload updates including restructuring of the module configurations and renaming of several fields.

* \[Document Grounding] Breaking: The `message` field in `RetrievalPerFilterSearchResultWithError` is replaced by `error` and `filterId` with more specific error details.

* \[Document Grounding] Extensive generated model class renaming for better specificity due to API spec changes.

  <!-- -->

  * `SearchResults` → `VectorSearchResults`

  * `KeyValueListPair` split into context-specific classes:

    <!-- -->

    * `VectorKeyValueListPair` for vector operations
    * `RetrievalKeyValueListPair` for retrieval operations
    * `VectorDocumentKeyValueListPair` for vector document operations
    * `RetrievalDocumentKeyValueListPair` for retrieval document operations

  * `Chunk` → `VectorChunk` and `RetrievalChunk` for different contexts

  * `SearchFilter` → `VectorSearchFilter` and `RetrievalSearchFilter`

  * `SearchConfiguration` → `VectorSearchConfiguration` and `RetrievalSearchConfiguration`

### ✨ New Functionality[​](#-new-functionality-4 "Direct link to ✨ New Functionality")

* \[Core] Added `ClientExceptionFactory` interface to provide custom exception mapping logic for different service clients.

* Extend `OpenAiClientException` and `OrchestrationClientException` to retrieve error diagnostics information received from remote service using `getErrorResponse`.

* \[Orchestration] Introduced filtering related exceptions along with convenience methods to obtain additional contextual information.

  <!-- -->

  * `OrchestrationInputFilterException` for prompt filtering and `OrchestrationOutputFilterException` for response filtering.

    <!-- -->

    * `getFilterDetails()`: Returns a map of all filter details.
    * `getAzureContentSafetyInput()` and `getAzureContentSafetyInput()` : Returns Azure Content Safety filter scores
    * `getLlamaGuard38b()`: Returns LlamaGuard filter scores

* \[Document Grounding] Extend `PipelineApi` operations, notably:

  <!-- -->

  * Added new pipeline creation requests for SDM and WorkZone with `SDMPipelineCreateRequest` and `WorkZonePipelineCreateRequest`.
  * S3 and SFTP pipeline configurations extended with `S3Configuration` and `SFTPConfiguration` for including data sources.
  * Support `/pipelines/trigger` endpoint to trigger pipelines on-demand via `PipelinesApi#manualTriggerPipeline()`.

### 📈 Improvements[​](#-improvements-3 "Direct link to 📈 Improvements")

* Update AI Core client to 2.40.1
* \[Document Grounding] Enhanced pipeline status reporting with additional metadata such as `createdAt`, `modifiedAt`, `lastCompletedAt`.

### 🐛 Fixed Issues[​](#-fixed-issues-3 "Direct link to 🐛 Fixed Issues")

* OpenAi: Fix AssistantMessage Bug by now being able to send Assistant Messages using our API Client.

## 1.9.0 - July 22, 2025[​](#190---july-22-2025 "Direct link to 1.9.0 - July 22, 2025")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.9.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes-4 "Direct link to 🔧 Compatibility Notes")

* The old OpenAI client (v1.0.0) is being deprecated in favor of the new OpenAI client (v1.4.0). [See the documentation for more details](/ai-sdk/docs/java/foundation-models/openai/chat-completion.md)

* Generated classes for the following service specifications are subject to change:

  * core
  * openai
  * orchestration
  * document grounding

* \[Orchestration] Interfaces with only one implementation were reduced.

  * As a result, the accessors for fields `OrchestrationModuleConfig.inputTranslationConfig` and `OrchestrationModuleConfig.outputTranslationConfig` now handle the implementing class explicitly.
  * The same applies to helper methods `DpiMasking#createConfig()` and `MaskingProvider#createConfig()`.

* \[Orchestration] `OrchestrationTemplate.withTemplate()` has been deprecated. Please use `OrchestrationTemplate.withTemplateMessages()` instead.

* \[Orchestration] The method `createConfig()` is removed from `ContentFilter`, `AzureContentFilter` and `LlamaGuardFilter` and is replaced by `createInputFilterConfig()` and `createOutputFilterConfig()`.

* \[Orchestration] Deprecated : `LLAMA3_1_70B_INSTRUCT`, `CLAUDE_3_SONNET`, `TITAN_TEXT_LITE`, `TITAN_TEXT_EXPRESS`, `GPT_4`, `GPT_4_0613`, `MIXTRAL_8X7B_INSTRUCT_V01`.

  * `GPT_4` and `GPT_4_0613` are replaced by : `GPT_40`or `GPT_41`.
  * `CLAUDE_3_SONNET` is replaced by `CLAUDE_4_SONNET`.
  * `MIXTRAL_8X7B_INSTRUCT_V01` is replaced by `MISTRAL_SMALL_INSTRUCT`.

* \[OpenAI] Deprecated : `GPT_4`.

  * `GPT_4`is replaced by : `GPT_40`or `GPT_41`.

* \[Prompt Registry] Resource group has been added as a optional parameter to all endpoints. Set it to `"default"` if it was not set before. Examples:

  * `client.importPromptTemplate(File)` --> `client.importPromptTemplate("default", File)`.
  * `client.parsePromptTemplateById(id, false, inputParams)` --> `client.parsePromptTemplateById(id, "default", false, inputParams)`.

* \[Document Grounding] All classes with `Retrieval` have been renamed to fix the typo

  * for example: `RetievalSearchResults` has been renamed to `RetrievalSearchResults`

* \[Document Grounding] `PipelinesApi#getAllPipelines()` and `PipelinesApi#getPipelineById()` now any of these 3 classes implementing the `GetPipeline` interface:

  * `MSSharePointPipelineGetResponse`, `S3PipelineGetResponse` and `SFTPPipelineGetResponse`

### ✨ New Functionality[​](#-new-functionality-5 "Direct link to ✨ New Functionality")

* \[Orchestration] Added support for [transforming a JSON output into an entity](/ai-sdk/docs/java/orchestration/chat-completion.md#json_schema)
* \[Orchestration] Added `AzureContentFilter#promptShield()` available for input filtering.
* \[Orchestration] Added new models for `OrchestrationAiModel`: `GEMINI_2_5_FLASH`, `GEMINI_2_5_PRO`, `ALEPHALPHA_PHARIA_1_7B_CONTROL`, `OPENAI_O4_MINI`, `CLAUDE_4_OPUS`, `CLAUDE_4_SONNET`, `OPENAI_O3`.

### 🐛 Fixed Issues[​](#-fixed-issues-4 "Direct link to 🐛 Fixed Issues")

* \[Orchestration] Resolved duplicate JSON property issue, enabling Anthropic Claude chat completions.
* Remove logging of any request/response payloads to avoid potential exposure of sensitive data.

## 1.8.0 - May 26, 2025[​](#180---may-26-2025 "Direct link to 1.8.0 - May 26, 2025")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.8.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes-5 "Direct link to 🔧 Compatibility Notes")

* The constructor of the `AssistantMessage` class now takes `List<MessageToolCall>` as input instead of `List<ResponseMessageToolCall>` (the generated class got renamed).

### ✨ New Functionality[​](#-new-functionality-6 "Direct link to ✨ New Functionality")

* \[OpenAI] [Add convenience for tool definition, parsing function calls and tool execution](/ai-sdk/docs/java/foundation-models/openai/chat-completion.md#executing-tool-calls)
* \[OpenAI] Added the following new models: `o4-mini`, `o3`, `gpt-4.1`, `gpt-4.1-nano`, and `gpt-4.1-mini`
* \[Orchestration] Added new model DeepSeek-R1: `OrchestrationAiModel.DEEPSEEK_R1`
* \[Orchestration] [Tool execution fully enabled](/ai-sdk/docs/java/spring-ai/orchestration.md#tool-calling)
* \[Orchestration] [Added translation](/ai-sdk/docs/java/orchestration/chat-completion.md#translation)

### 🐛 Fixed Issues[​](#-fixed-issues-5 "Direct link to 🐛 Fixed Issues")

* \[Orchestration] Fixed `OrchestrationAiModel.CLAUDE_3_7_SONNET`.

## 1.7.0 - April 30, 2025[​](#170---april-30-2025 "Direct link to 1.7.0 - April 30, 2025")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.7.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes-6 "Direct link to 🔧 Compatibility Notes")

* \[Orchestration] Deprecated `OrchestrationAiModel.GEMINI_1_0_PRO`. The replacements are either:

  <!-- -->

  * `OrchestrationAiModel.GEMINI_2_0_FLASH`
  * `OrchestrationAiModel.GEMINI_2_0_FLASH_LITE`.

### ✨ New Functionality[​](#-new-functionality-7 "Direct link to ✨ New Functionality")

* \[Orchestration] [Added support to locally test prompt template files](/ai-sdk/docs/java/orchestration/chat-completion.md#locally-test-a-prompt-template)

* \[Orchestration] Added new models:

  <!-- -->

  * `OrchestrationAiModel.CLAUDE_3_7_SONNET`
  * `OrchestrationAiModel.GEMINI_2_0_FLASH`
  * `OrchestrationAiModel.GEMINI_2_0_FLASH_LITE`

## 1.6.0 - April 03, 2025[​](#160---april-03-2025 "Direct link to 1.6.0 - April 03, 2025")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.6.0)

### ✨ New Functionality[​](#-new-functionality-8 "Direct link to ✨ New Functionality")

* \[Prompt Registry] [Add Prompt Registry client](/ai-sdk/docs/java/ai-core/prompt-registry.md)
  * `com.sap.ai.sdk:prompt-registry:1.6.0`
* \[OpenAI] [Add convenience for tool call execution](/ai-sdk/docs/java/foundation-models/openai/chat-completion.md#executing-tool-calls)

## 1.5.0 - March 13, 2025[​](#150---march-13-2025 "Direct link to 1.5.0 - March 13, 2025")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.5.0)

### ✨ New Functionality[​](#-new-functionality-9 "Direct link to ✨ New Functionality")

* \[Orchestration] [Add Spring AI Chat Memory support](/ai-sdk/docs/java/spring-ai/orchestration.md#chat-memory)
* \[Orchestration] [Prompt templates can be consumed from registry.](/ai-sdk/docs/java/orchestration/chat-completion.md#templating)
* \[Orchestration] [Masking is now available on grounding.](/ai-sdk/docs/java/orchestration/chat-completion.md#mask-grounding)
* \[Orchestration] [Grounding via *help.sap.com* is enabled.](/ai-sdk/docs/java/orchestration/chat-completion.md#grounding-via-helpsapcom)
* \[OpenAI] [Spring AI integration for embedding calls.](/ai-sdk/docs/java/spring-ai/openai.md#embedding)

## 1.4.0 - February 28, 2025[​](#140---february-28-2025 "Direct link to 1.4.0 - February 28, 2025")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.4.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes-7 "Direct link to 🔧 Compatibility Notes")

* \[Orchestration] The constructors `UserMessage(MessageContent)` and `SystemMessage(MessageContent)` are removed. Use `Message.user(String)`, `Message.user(ImageItem)`, or `Message.system(String)` instead.

* Deprecate `getCustomField(String)` in favor of `toMap()` on generated model classes.

  <!-- -->

  * `com.sap.ai.sdk.core.model.*`
  * `com.sap.ai.sdk.orchestration.model.*`

### ✨ New Functionality[​](#-new-functionality-10 "Direct link to ✨ New Functionality")

* \[Orchestration] [Add Spring AI tool calling](/ai-sdk/docs/java/spring-ai/orchestration.md#tool-calling).

* \[Orchestration] [Add new convenient methods to set the response format for Orchestration.](/ai-sdk/docs/java/orchestration/chat-completion.md#response-format)

* \[Document Grounding] [Add Document Grounding Client](/ai-sdk/docs/java/ai-core/document-grounding.md)
  * `com.sap.ai.sdk:document-grounding:1.4.0`

* \[OpenAI] New generated model classes introduced for *AzureOpenAI* specification dated 2024-10-21.

* \[OpenAI] Introducing [new user interface](/ai-sdk/docs/java/foundation-models/openai/chat-completion.md) for chat completion wrapping the generated model classes.

  <!-- -->

  * `OpenAiChatCompletionRequest` and `OpenAiChatCompletionResponse`' for high level request and response handling.
  * `OpenAiUserMessage`, `OpenAiSystemMessage`, `OpenAiAssistantMessage` and `OpenAiToolMessage` for message creation for different content types.
  * `OpenAiToolChoice` for configuring chat completion requests with tool selection strategy.

* \[OpenAI] Introducing new user interface for embedding calls using `OpenAiEmbeddingRequest` and `OpenAiEmbeddingResponse`.

## 1.3.0 - February 13, 2025[​](#130---february-13-2025 "Direct link to 1.3.0 - February 13, 2025")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.3.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes-8 "Direct link to 🔧 Compatibility Notes")

* `Message.content()` returns a `ContentItem` now instead of a `String`. Use `((TextItem) Message.content().items().get(0)).text()` if the corresponding `ContentItem` is a `TextItem` and the string representation is needed.

### ✨ New Functionality[​](#-new-functionality-11 "Direct link to ✨ New Functionality")

* Upgrade to release 2502a of AI Core.

* Orchestration:

  <!-- -->

  * [Add `LlamaGuardFilter`](/ai-sdk/docs/java/orchestration/chat-completion.md#filtering).
  * [Convenient methods to create messages containing images and multiple text inputs](/ai-sdk/docs/java/orchestration/chat-completion.md#using-images)
  * [Enable setting the response format](/ai-sdk/docs/java/orchestration/chat-completion.md#response-format)

## 1.2.0 - January 30, 2025[​](#120---january-30-2025 "Direct link to 1.2.0 - January 30, 2025")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.2.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes-9 "Direct link to 🔧 Compatibility Notes")

* `SingleChatMessage`, as well as new `MultiChatMessage`, are now subtypes of new interface `ChatMessage`. Most variables or methods previously typed as `ChatMessage` in `model` package are now typed as `SingleChatMessage`.
* Add missing `@Beta` annotations to all `com.sap.ai.sdk.core.client` and `com.sap.ai.sdk.core.model` classes.

### ✨ New Functionality[​](#-new-functionality-12 "Direct link to ✨ New Functionality")

* New Orchestration features:

  <!-- -->

  * [Spring AI integration](/ai-sdk/docs/java/spring-ai/orchestration.md)
  * [Add Grounding configuration convenience](/ai-sdk/docs/java/orchestration/chat-completion.md#grounding)
  * Images are now supported as input in newly introduced `MultiChatMessage`.
  * `MultiChatMessage` also allows for multiple content items (text or image) in one object.
  * Grounding input can be masked with `DPIConfig`.
  * LLama Guard can now be used for content filtering.
  * Support for tool calling and response format
  * Updated the list for supported models (e.g., added amazon nova models).

### 📈 Improvements[​](#-improvements-4 "Direct link to 📈 Improvements")

* Update Orchestration client to version 0.48.2 (2501a)

## 1.1.0 - January 07, 2025[​](#110---january-07-2025 "Direct link to 1.1.0 - January 07, 2025")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.1.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes-10 "Direct link to 🔧 Compatibility Notes")

* Changed return type of `List<Double> getEmbedding()` from experimental API `OpenAiEmbeddingData` to `float[]` to match recent Spring AI change.

### ✨ New Functionality[​](#-new-functionality-13 "Direct link to ✨ New Functionality")

* Added `streamChatCompletion()` and `streamChatCompletionDeltas()` to the `OrchestrationClient`.

### 📈 Improvements[​](#-improvements-5 "Direct link to 📈 Improvements")

* Update AI Core client to 2.37.0

## 1.0.0 - December 03, 2024[​](#100---december-03-2024 "Direct link to 1.0.0 - December 03, 2024")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.0.0)

### ✨ New Functionality[​](#-new-functionality-14 "Direct link to ✨ New Functionality")

* Introduce AI Core client to consume the [AI Core Rest APIs](https://api.sap.com/api/AI_CORE_API/overview). Here are a few features:

  <!-- -->

  * Artifact management: register and organize datasets and model artifacts.
  * Configuration management: set up configurations for various models and use cases.
  * Deployment management: deploy AI models and manage their lifecycle within SAP AI Core.

* Introduce Orchestration client for consuming the following features of the orchestration service:

  <!-- -->

  * Harmonized LLM access via orchestration
  * Prompt templates
  * Content filtering
  * Masking

* Introduce the OpenAI client to consume the following features:

  <!-- -->

  * Chat completion and streaming chat completion

    <!-- -->

    * Text
    * Images
    * Tools

  * Generate embeddings for input text.

warning

All classes under any of the `...model` packages are generated from an OpenAPI specification. This means that these model classes are not guaranteed to be stable and may change with future releases. They are safe to use, but may require updates even in minor releases.
