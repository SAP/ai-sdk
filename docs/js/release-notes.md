# Release Notes

## 2.16.0 - September 18, 2026[​](#2160---september-18-2026 "Direct link to 2.16.0 - September 18, 2026")

### Compatibility Notes[​](#compatibility-notes "Direct link to Compatibility Notes")

* \[openai] Raise the minimum required openai package version to 7.5.0. ([875e285](https://github.com/SAP/ai-sdk-js/commit/875e2850257cb46da4b83aebfda13be1bd0d698a))
* \[rpt] Deprecate `sap-rpt-1-small` and `sap-rpt-1-large`. These model names remain functional until their retirement date (2026-12-31). ([ba5b1b4](https://github.com/SAP/ai-sdk-js/commit/ba5b1b49e24f7a13256a92faf3d29904ec327472))
* \[rpt] The server default changed from for `parse_data_types` changed from `true` to `false`. Pass `parse_data_types: true` explicitly if you relied on the old default. ([ba5b1b4](https://github.com/SAP/ai-sdk-js/commit/ba5b1b49e24f7a13256a92faf3d29904ec327472))
* \[rpt] The `RptClient` constructor no longer has a default model name. Pass one of the known model names explicitly, e.g. `'sap-rpt-1.5'`. ([ba5b1b4](https://github.com/SAP/ai-sdk-js/commit/ba5b1b49e24f7a13256a92faf3d29904ec327472))
* \[rpt] Widen `TargetColumnConfig.prediction_placeholder` to accept `null`. The type is now `string | number | null` (was `string | number`). ([ba5b1b4](https://github.com/SAP/ai-sdk-js/commit/ba5b1b49e24f7a13256a92faf3d29904ec327472))

### New Features[​](#new-features "Direct link to New Features")

* \[core, llm-batch] Add `LlmBatchModel` type for models supported in LLM batch processing. `BatchCreateRequest.spec.model` now uses this type for IDE autocomplete. ([0da56e2](https://github.com/SAP/ai-sdk-js/commit/0da56e271930d1ed966e53b3664a413878d202f0))
* \[core] Add `gemini-3.5-flash-lite` to the available model list. Remove deprecated model `mistralai--mistral-large-instruct` (retirement date: 2026-09-30). ([4b2c014](https://github.com/SAP/ai-sdk-js/commit/4b2c014fe6837c91a078b3841d7205e351e745d4))
* \[rpt] Add a `confidence_interval` field to `PredictResponsePayload` predictions for regression tasks. ([ba5b1b4](https://github.com/SAP/ai-sdk-js/commit/ba5b1b49e24f7a13256a92faf3d29904ec327472))
* \[rpt] Default gzip compression level to 1 for RPT predict requests. ([ba5b1b4](https://github.com/SAP/ai-sdk-js/commit/ba5b1b49e24f7a13256a92faf3d29904ec327472))
* \[rpt] Add an `explanations` field to `prediction_config`; read feature importance scores per query row from the response. ([ba5b1b4](https://github.com/SAP/ai-sdk-js/commit/ba5b1b49e24f7a13256a92faf3d29904ec327472))
* \[rpt] Expand `ColumnType` from 3 to 16 values (`integer`, `int16`, `int32`, `int64`, `uint8`, `decimal`, `double`, `boolean`, `largestring`, `uuid`, `time`, `datetime`, `timestamp`). Map the new numeric variants to `number`; all other new variants (including `datetime` and `timestamp`, which are full ISO strings) map to `string`. ([ba5b1b4](https://github.com/SAP/ai-sdk-js/commit/ba5b1b49e24f7a13256a92faf3d29904ec327472))
* \[rpt] Add `context_mode` to `PredictionConfig` and `PredictResponseMetadata` (from RPT spec v1.6.0). ([21556db](https://github.com/SAP/ai-sdk-js/commit/21556dbd11c84f37d7bcc706564c48ac82ad664d))

### Fixed Issues[​](#fixed-issues "Direct link to Fixed Issues")

* \[core] Set the default http agent socket timeout for AI Core requests to 1201 seconds (1201000 ms). This overrides the Cloud SDK default of 5 seconds, which is too short for chat and streaming completions. The value covers the orchestration server-side maximum of 1200 seconds plus 1 second of leeway. Keep-alive is now disabled on these requests. This avoids reusing stale sockets that a load balancer may have closed during the longer timeout. Both settings apply only to the service-binding destination. You can still override them with a custom destination's `agentOptions` or `CustomRequestConfig.httpsAgent`. ([3483acb](https://github.com/SAP/ai-sdk-js/commit/3483acb2bda79ebe6a777497eb7ad74776dd982c))
* \[langchain] Normalize invalid tool message content to empty string to prevent AI Core 400 errors when MCP tools return empty results. ([4cda527](https://github.com/SAP/ai-sdk-js/commit/4cda527415974b9d70b5a902110f2ab597149927))

### Improvements[​](#improvements "Direct link to Improvements")

* \[core] Added `mistralai--mistral-medium`, `sap-rpt-1.5`, `sap-rpt-1.5-large`, `sap-rpt-1.6`, `sap-rpt-1.6-large`, `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna` to the available model list. Remove deprecated models `gpt-4.1-nano` (retirement date: 2026-10-14), `gemini-2.5-flash` (retirement date: 2026-10-16) and `gemini-2.5-pro` (retirement date: 2026-10-16). ([94b36e5](https://github.com/SAP/ai-sdk-js/commit/94b36e52e20693998b6f2e8cca1b7229efc01585))
* \[document-grounding] Update document grounding specification. ([478fc53](https://github.com/SAP/ai-sdk-js/commit/478fc5396a686e9799c66b848f490cffb09a3475))

## 2.15.0 - August 18, 2026[​](#2150---august-18-2026 "Direct link to 2.15.0 - August 18, 2026")

### Compatibility Notes[​](#compatibility-notes-1 "Direct link to Compatibility Notes")

* \[orchestration] Deprecate `OrchestrationConfigRef` — use `OrchestrationConfigRefById` or `OrchestrationConfigRefByName` instead. ([b61cb53](https://github.com/SAP/ai-sdk-js/commit/b61cb5315b7b9e725c611168342a37dd0e69bb4f))

### New Features[​](#new-features-1 "Direct link to New Features")

* \[core, openai] Add experimental OpenAI Realtime API (speech-to-speech) support for `gpt-realtime` via the `@sap-ai-sdk/openai/realtime` sub-path export. ([a5407c8](https://github.com/SAP/ai-sdk-js/commit/a5407c80e60c39c1dbbb24a265869d88be933b9e))
* \[langchain] Add `orchestrationPromptCachingMiddleware()` middleware for the LangChain Orchestration client, exported from `@sap-ai-sdk/langchain/orchestration/prompt-caching-middleware`. It enables automatic cache control for orchestration requests. The middleware requires the optional `langchain` peer dependency to be installed. ([070b309](https://github.com/SAP/ai-sdk-js/commit/070b3095f94d6a9a7a1622be4033e8382076eb4e))
* \[orchestration] Split `OrchestrationConfigRef` into `OrchestrationConfigRefById` and `OrchestrationConfigRefByName`. ([b61cb53](https://github.com/SAP/ai-sdk-js/commit/b61cb5315b7b9e725c611168342a37dd0e69bb4f))

## 2.14.0 - August 06, 2026[​](#2140---august-06-2026 "Direct link to 2.14.0 - August 06, 2026")

### New Features[​](#new-features-2 "Direct link to New Features")

* \[core, orchestration] Add `GcpVertexAiEmbeddingModel` type with `gemini-embedding` to `@sap-ai-sdk/core`. Add `GcpVertexAiEmbeddingModel` to the `EmbeddingModel` union in `@sap-ai-sdk/orchestration`. ([cca7edd](https://github.com/SAP/ai-sdk-js/commit/cca7edd3c41f8cd36f23f8702e36f76143d16bae))
* \[orchestration] Add reasoning content support to the Orchestration client. `reasoning_content` fields were added on response, streaming delta, and assistant message types. The `getReasoningContent()` and `getDeltaReasoningContent()` convenience functions return the reasoning text from model responses. ([b986b70](https://github.com/SAP/ai-sdk-js/commit/b986b708075101fb721e53c5cbe31fa7915ae69b))
* \[orchestration] Added `overrideConfig` field to `OrchestrationConfigRef` to pass a `PartialOrchestrationConfig` that overrides parts of the stored orchestration configuration at request time. Streaming via `.stream()` now automatically sets `stream.enabled = true` in the partial configuration override, so clients using a stored orchestration configuration reference no longer require streaming to be pre-configured in the stored configuration. ([b986b70](https://github.com/SAP/ai-sdk-js/commit/b986b708075101fb721e53c5cbe31fa7915ae69b))
* \[prompt-registry] prompt-registry: Update generated client to latest specification. ([a268597](https://github.com/SAP/ai-sdk-js/commit/a26859733486d5c3282322794cdd20e2cd6fd9c9))

### Fixed Issues[​](#fixed-issues-1 "Direct link to Fixed Issues")

* \[langchain] Skip tool and assistant messages when applying `cache_control`, using the last applicable message (system, user, or developer) instead. Some models do not support `cache_control` on `tool` messages. ([4003a12](https://github.com/SAP/ai-sdk-js/commit/4003a1212bae77921ffe9450c3c886a7d17db77b))
* \[openai] Fix OpenAI client types to allow passing objects with model deployment details (model name + model version, deployment ID and/or resource group) instead of just model names. ([016edcd](https://github.com/SAP/ai-sdk-js/commit/016edcd2f50b32ab2c7a7c24f8ea92b82d90534c))

### Improvements[​](#improvements-1 "Direct link to Improvements")

* \[core] Add `anthropic--claude-4.5-opus`, `anthropic--claude-4.8-opus`, `gemini-3.5-flash`, `gemini-embedding` to the available model list. ([cca7edd](https://github.com/SAP/ai-sdk-js/commit/cca7edd3c41f8cd36f23f8702e36f76143d16bae))

## 2.13.0 - July 14, 2026[​](#2130---july-14-2026 "Direct link to 2.13.0 - July 14, 2026")

### New Features[​](#new-features-3 "Direct link to New Features")

* \[core] Add `toReadableStream()` method to `SseStream`. The new method converts the asynchronous iterable stream to a pull-based `ReadableStream` of newline-delimited JSON, enabling composable transformations via the Web Streams API `pipeThrough()` pattern with native flow control. ([6542a2a](https://github.com/SAP/ai-sdk-js/commit/6542a2a3a6740277b61c820c8f70a37b71c4e75a))
* \[langchain] Add `cache_control` call option to the LangChain orchestration client. When the `cache_control` option is set, a cache breakpoint is automatically applied to the request. ([fafd99e](https://github.com/SAP/ai-sdk-js/commit/fafd99e43f8bc1879a896862eccb93cf8827a77e))
* \[langchain] Expose `cached_tokens` and `cache_creation_tokens` in `usage_metadata.input_token_details` for LangChain orchestration responses. ([fafd99e](https://github.com/SAP/ai-sdk-js/commit/fafd99e43f8bc1879a896862eccb93cf8827a77e))
* \[openai] Allow setting a model configuration per request. ([fea1c3f](https://github.com/SAP/ai-sdk-js/commit/fea1c3ff75a87621e800ae7bdae3d51f07dacbb7))

### Improvements[​](#improvements-2 "Direct link to Improvements")

* \[core] Remove deprecated models `mistralai--mistral-small-instruct` (retirement date: not earlier than 2026-09-30) — use `mistralai--mistral-small` instead, `amazon--nova-premier` (retirement date: 2026-09-10) — use `amazon--nova-lite` (version: 2) instead, `anthropic--claude-3-haiku` (retirement date: 2026-09-10) — use `anthropic--claude-4.5-haiku` instead and `anthropic--claude-4-sonnet` (retirement date: 2026-10-14) — use `anthropic--claude-4.5-sonnet` instead. ([11baf52](https://github.com/SAP/ai-sdk-js/commit/11baf52487ecdb14062223a74a3f94938def5910))
* \[core] Added `gpt-5.1` to the available model list. ([cb8ffe7](https://github.com/SAP/ai-sdk-js/commit/cb8ffe7f133ea15aba2ef01baf4d64d0bba0d59f))
* \[core] Remove deprecated models `gpt-4.1` (retirement date: 2026-10-14), `gpt-4.1-mini` (retirement date: 2026-10-14), `o3` (retirement date: 2026-10-16) and `o4-mini` (retirement date: 2026-10-16). ([a8c9b29](https://github.com/SAP/ai-sdk-js/commit/a8c9b291a09ac812f24007b6a5f4139d8a3ef71b))

## 2.12.0 - June 24, 2026[​](#2120---june-24-2026 "Direct link to 2.12.0 - June 24, 2026")

### New Features[​](#new-features-4 "Direct link to New Features")

* \[core] Add `AzureOpenAiResponsesModel` type for Azure OpenAI models that exclusively support the Responses API. ([0f10482](https://github.com/SAP/ai-sdk-js/commit/0f104825fb37f3518acb8cf4389b69e48e973182))
* \[document-grounding, prompt-registry] Update document grounding specification. ([d984914](https://github.com/SAP/ai-sdk-js/commit/d984914f17767a458f1c2b4dae2aa6a8837dee62))
* \[foundation-models] Add `createBatchInput()` and `parseBatchOutput()` helpers for building and parsing LLM batch requests and responses. ([0b41bea](https://github.com/SAP/ai-sdk-js/commit/0b41bea8cb572fdb8d1ea849bd31f87aef3341ea))
* \[llm-batch] Add new experimental `@sap-ai-sdk/llm-batch` package for asynchronous batch processing of LLM requests via SAP AI Core LLM Batch Service. ([0b41bea](https://github.com/SAP/ai-sdk-js/commit/0b41bea8cb572fdb8d1ea849bd31f87aef3341ea))
* \[openai] Add new experimental `@sap-ai-sdk/openai` package with a SAP AI Core-aware OpenAI client. The client wraps the OpenAI SDK and handles authentication and deployment resolution against SAP AI Core. ([0f10482](https://github.com/SAP/ai-sdk-js/commit/0f104825fb37f3518acb8cf4389b69e48e973182))

### Fixed Issues[​](#fixed-issues-2 "Direct link to Fixed Issues")

* \[core] Improve error message when server sends a non-JSON response during streaming. ([2faf4a8](https://github.com/SAP/ai-sdk-js/commit/2faf4a8e0211f5d356e5aa0164c739c7160a212f))
* \[langchain] Fixed duplicate tools accumulating in LangChain orchestration client in some configurations on repeated invocations. ([311dc08](https://github.com/SAP/ai-sdk-js/commit/311dc08e45ee7f7f897a9dc227fb22d078e28356))

### Improvements[​](#improvements-3 "Direct link to Improvements")

* \[core] Added `gpt-5.5` to the available model list. Remove retired model `anthropic--claude-4-opus` — use `anthropic--claude-4.7-opus` instead. Remove deprecated model `o3-mini` (retirement date: 2026-08-02). ([e944aa1](https://github.com/SAP/ai-sdk-js/commit/e944aa1083c56d04bdef210870641b35ab17794c))

## 2.11.0 - May 26, 2026[​](#2110---may-26-2026 "Direct link to 2.11.0 - May 26, 2026")

### New Features[​](#new-features-5 "Direct link to New Features")

* \[langchain] Support orchestration prompt module fallbacks. (dc2f5b1)
* \[orchestration] Update orchestration specification to v0.131.3 (f72bb58)

### Fixed Issues[​](#fixed-issues-3 "Direct link to Fixed Issues")

* \[orchestration] Route messages to `messages_history` when using an orchestration config reference or prompt template reference. (cbcefb9)
* \[orchestration] Disallow providing both orchestration config reference and config object at the same time. (7db7237)

### Improvements[​](#improvements-4 "Direct link to Improvements")

* \[core] Add `gpt-5.4`, `gpt-5.4-nano` to the available model list. Remove deprecated model `o1` (retirement date: 2026-06-18). (c8c0e41)
* \[core] Added `mistralai--mistral-small`, `anthropic--claude-4.7-opus`, `gemini-3.1-flash-lite` to the available model list. (75bb9a9)

## 2.10.0 - April 19, 2026[​](#2100---april-19-2026 "Direct link to 2.10.0 - April 19, 2026")

### Compatibility Notes[​](#compatibility-notes-2 "Direct link to Compatibility Notes")

* \[document-grounding] `DocumentKeyValueListPair`, `RetrievalDocumentKeyValueListPair`, `VectorDocumentKeyValueListPair`: the `matchMode` property type was narrowed from an open union (`'ANY' | 'ALL' | any`) to the strict `FilterMatchModeEnum` (`'ANY' | 'ALL'`). (029f091)
* \[document-grounding] `CollectionPendingResponse`: fields `Location` and `status` were removed. A new `monitorURL` property was added instead. (029f091)
* \[document-grounding] `GoogleDrivePipelineCreateRequest`: the `configuration` property is now required (was optional). Code constructing this request without `configuration` must be updated to provide it. (94546e6)
* \[document-grounding] `GoogleDriveFolderDetail` type was removed. Code referencing `GoogleDriveFolderDetail` must be updated to use `GoogleDriveResourceDetail` instead. (94546e6)
* \[document-grounding] `DataRepositoryType`, `RetrievalSearchSelectOptionEnum`, `VectorSearchSelectOptionEnum`: previously open (`| any`) unions are now strictly typed. Only the specified string literals are accepted. (029f091)
* \[document-grounding] `S3PipelineMinimalResponse`, `SFTPPipelineMinimalResponse`: the `configuration` property is now optional. (029f091)
* \[document-grounding] `GoogleDriveFolder` type was removed and replaced by `GoogleDriveResourceDetail`. The properties `id`, `driveId`, and `driverType` were replaced by `resourceType` and `resourceId`. Code referencing `GoogleDriveFolder` or its properties must be updated to use `GoogleDriveResourceDetail` with the new property names. (94546e6)
* \[document-grounding] `TextOnlyBaseChunk`: new required field `id: string` added and `metadata` is now optional. (029f091)
* \[document-grounding] `GoogleDriveConfig`: the `folder` property was removed and replaced by a new required `resourceType: 'SHARED_FOLDER' | 'SHARED_DRIVE'` property, plus optional `resourceId` and `includePaths` properties. Code constructing `GoogleDriveConfig` objects must be updated to use the new shape. (94546e6)
* \[document-grounding] `BaseDocument` / `DocumentInput`: `chunks` type changed from `TextOnlyBaseChunk[]` to `TextOnlyBaseChunkCreate[]`. The `metadata` property is now optional. (029f091)
* \[foundation-models] Support for constructing an `AzureOpenAiChatCompletionStreamResponse` without an `HttpResponse` has been deprecated, and will be removed in the next major release. Code directly instantiating this class should be updated to provide an `HttpResponse` object as the first parameter to allow reading from raw HTTP response. (a722171)
* \[prompt-registry] `listPromptTemplateHistory()`: the `includeSpec` query parameter has been removed. (dce18df)
* \[prompt-registry] The `include_spec` parameter is deprecated in favor of `includeSpec` and `resolve_template_ref` is deprecated in favor of `resolveTemplateRef`. (cc9e80c)
* \[prompt-registry] `PromptTemplateSubstitutionRequest` now requires the `inputParams` property. (cc9e80c)

### New Features[​](#new-features-6 "Direct link to New Features")

* \[document-grounding] Update document grounding specification. (029f091)
* \[foundation-models] Add `getRequestId()` method to `AzureOpenAiChatCompletionResponse`, `AzureOpenAiChatCompletionStreamResponse` and `AzureOpenAiEmbeddingResponse`. The new method retrieves the request ID from the `x-aicore-request-id` response header, useful for debugging and tracking requests. (a722171)
* \[foundation-models] Add `rawResponse` property to `AzureOpenAiChatCompletionStreamResponse`. The new property exposes the raw HTTP response for advanced use cases such as accessing response headers. (a722171)
* \[orchestration] Update orchestration specification to 0.115.19. Multiple embedding output formats are not yet supported in the orchestration embedding client. (cf767a9)
* \[prompt-registry] Update prompt registry specification. (cc9e80c)

### Improvements[​](#improvements-5 "Direct link to Improvements")

* \[core] Remove deprecated models `amazon--titan-embed-image` and `anthropic--claude-4.5-opus`. (8cb466a)

## 2.9.0 - March 20, 2026[​](#290---march-20-2026 "Direct link to 2.9.0 - March 20, 2026")

### New Features[​](#new-features-7 "Direct link to New Features")

* \[orchestration] Add `getCitations()` method to retrieve source citations from models like Perplexity Sonar. (8de0013)

### Improvements[​](#improvements-6 "Direct link to Improvements")

* \[core] Add `gpt-5.2`, `anthropic--claude-4.5-opus`, `anthropic--claude-4.6-opus`, `anthropic--claude-4.6-sonnet` and `amazon-titan-embed-image` to the available model list. Removed deprecated `gpt-4o` model. (cd3d8ed)
* \[orchestration] Support file input for user messages. File inputs have a `type` of `file` and include a `file_data` field with a URL such as a HTTP URL or a data URL. Local files must be provided as `data:MEDIATYPE;base64,DATA` with a non-empty media type and valid base64 content. Availability of different file types depends on the capabilities of the underlying model and tools. GPT-models do not support file inputs with the orchestration API at this time. (b822da9)
* \[rpt] Align parquet endpoint types with the RPT API types. (08c6137)

## 2.8.0 - March 03, 2026[​](#280---march-03-2026 "Direct link to 2.8.0 - March 03, 2026")

### New Features[​](#new-features-8 "Direct link to New Features")

* \[orchestration] Support streaming with orchestration prompt module fallback. (3d12d4c)
* \[orchestration] Support orchestration prompt module fallback for non-streaming requests When constructing an `OrchestrationClient` it is now possible to provide a list of module configurations to support module fallback. (5501e7c)
* \[rpt] Add generic HTTP request configuration support. The `predictWithSchema()` and `predictWithoutSchema()` methods now accept an optional `customRequest` parameter of type `RptRequestOptions`, allowing configuration of custom HTTP request options such as headers, timeout, and middlewares. (e0ef84c)
* \[rpt] Add predict request compression support. All requests with a body of 1024 bytes or larger will be automatically compressed with `gzip` by default, unless configured otherwise. Compression configuration is available via the `requestCompression` property on the `RptClientConfig` object. (e0ef84c)

## 2.7.0 - February 16, 2026[​](#270---february-16-2026 "Direct link to 2.7.0 - February 16, 2026")

### Compatibility Notes[​](#compatibility-notes-3 "Direct link to Compatibility Notes")

* \[ai-api] Extract functionality around execution scheduling from the `ExecutionApi` to `ExecutionScheduleApi`. (8616d5e)
* \[ai-api] Remove the `BckndEvent` type. (8616d5e)
* \[ai-api] Split the `BckndArgoCDApplicationData` into `BckndArgoCDApplicationDataResponse` and `BckndArgoCDApplicationDataRequest`. (8616d5e)
* \[core] Remove deprecated and retired models from model list. Remove retired model `anthropic--claude-3-sonnet` from model list, use suggested replacement `anthropic--claude-4.5-sonnet` instead. Remove retired model `anthropic--claude-3-opus` from model list. Remove deprecated model `gpt-4o-mini`, use suggested replacement `gpt-5-mini` instead. Remove deprecated models `anthropic--claude-3.5-sonnet` and `anthropic--claude-3.7-sonnet`. (b12626b)
* \[orchestration] Support for constructing an `OrchestrationStreamResponse` without an `HttpResponse` has been deprecated, and will be removed in the next major release. Code directly instantiating this class should be updated to provide an `HttpResponse` object as the first parameter to allow reading from raw HTTP response. (6b49479)

### New Features[​](#new-features-9 "Direct link to New Features")

* \[core] Advertise AbortSignal support for HTTP request cancellation. This change adds typings, documentation and examples for using AbortSignal with the HTTP client to enable request cancellation. (b11b00c)
* \[langchain] Support the `withStructuredOutput()` method in the Orchestration LangChain client. (4fce347)
* \[orchestration] Add `rawResponse` property to `OrchestrationStreamResponse`. The new property exposes the raw HTTP response from the orchestration service for advanced use cases. (6b49479)
* \[orchestration] Add `getRequestId()` method to `OrchestrationResponse`, `OrchestrationStreamResponse` and `OrchestrationEmbeddingResponse`. The new method allows retrieving the request ID from the orchestration service responses, which can be useful for debugging and tracking requests. (6b49479)

### Improvements[​](#improvements-7 "Direct link to Improvements")

* \[core] Combine 'ai-client-type' headers if a custom 'ai-client-type' header is set. (56e9c3f)
* \[rpt] Restrict the `task_type` property in the `PredictionConfig` type. (12b4129)

## 2.6.0 - February 04, 2026[​](#260---february-04-2026 "Direct link to 2.6.0 - February 04, 2026")

### New Features[​](#new-features-10 "Direct link to New Features")

* \[rpt] Release Beta version of a client for the SAP-RPT-1 model. (790ad05)

### Fixed Issues[​](#fixed-issues-4 "Direct link to Fixed Issues")

* \[orchestration] Export `isConfigReference()` method as a value instead of type-only export. This function can now be imported and used at runtime to check if a configuration is an orchestration configuration reference type. (f3b6dc5)

## 2.5.0 - January 13, 2026[​](#250---january-13-2026 "Direct link to 2.5.0 - January 13, 2026")

### Compatibility Notes[​](#compatibility-notes-4 "Direct link to Compatibility Notes")

* \[langchain] The `@langchain/core` package is now a peer dependency. You now have to install the `@langchain/core` package as a direct dependency of your project. (5b88f6f)

### New Features[​](#new-features-11 "Direct link to New Features")

* \[langchain] Support disabling streaming completely via the langchain option `disableStreaming`. (b91e0a7)
* \[langchain] Support auto-streaming via the langchain option `streaming`. When enabled (e.g., transparently by LangGraph), responses are automatically streamed in `invoke()` calls. (b91e0a7)
* \[orchestration] Add support for orchestration configuration references in the orchestration client. (2f19a40)

### Fixed Issues[​](#fixed-issues-5 "Direct link to Fixed Issues")

* \[langchain] Pin `@langchain/core` to v1.1.8 to avoid a regression. (9ff7cec)

### Improvements[​](#improvements-8 "Direct link to Improvements")

* \[langchain] Move the `@langchain/core` package from dependencies to peer dependencies. This reduces the chance of version incompatibilities between langchain-related packages. (5b88f6f)

## 2.4.0 - December 23, 2025[​](#240---december-23-2025 "Direct link to 2.4.0 - December 23, 2025")

### Compatibility Notes[​](#compatibility-notes-5 "Direct link to Compatibility Notes")

* \[prompt-registry] In the prompt-registry client schema, the `Template` type was renamed to `PromptTemplate`. (a3cbc6e)

### New Features[​](#new-features-12 "Direct link to New Features")

* \[orchestration] Added support for `applyTo` and `translateMessagesHistory` in order to enable selective input translation and automatic inference of target language for output translation parameters. (aa097da)
* \[prompt-registry] Update prompt-registry specification adding support for resource group scoped prompt templates. (a3cbc6e)

### Improvements[​](#improvements-9 "Direct link to Improvements")

* \[core] Added `anthropic--claude-4.5-sonnet` , `anthropic--claude-4.5-haiku` , `gemini-2.5-flash-lite` and `sap-abap-1` to the available model list. Removed deprecated models `gemini-2.0-flash` and `gemini-2.0-flash-lite` scheduled for retirement. (2e1d2c2)

## 2.3.0 - November 27, 2025[​](#230---november-27-2025 "Direct link to 2.3.0 - November 27, 2025")

### Compatibility Notes[​](#compatibility-notes-6 "Direct link to Compatibility Notes")

* \[langchain, orchestration, prompt-registry] `zod` was upgraded to v4 (7c9605d)

### New Features[​](#new-features-13 "Direct link to New Features")

* \[langchain] Bump langchain to v1 (7c9605d)
* \[orchestration] Added support for `protected_material_code` property to `buildAzureContentSafetyFilter()` function for output filter configuration to allow detecting protected code content from known github repositories. (485e21b)

## 2.2.0 - November 17, 2025[​](#220---november-17-2025 "Direct link to 2.2.0 - November 17, 2025")

### Compatibility Notes[​](#compatibility-notes-7 "Direct link to Compatibility Notes")

* \[document-grounding] `MSSharePointConfigurationGetResponse` now requires the `sharePoint` property (e2c34f3)

* \[document-grounding] `CommonConfiguration` was replaced with backend-specific types: `SFTPConfiguration` and `S3Configuration` (e2c34f3)

* \[document-grounding] Some types have been renamed to include endpoint-specific prefixes. Some instances of the prior names may still exist:

  <!-- -->

  * `SearchResults` was renamed to `VectorSearchResults` / `RetrievalSearchResults`
  * `Chunk` was renamed to `VectorChunk` / `RetrievalChunk`
  * `SearchFilter` was renamed to `VectorSearchFilter`
  * `KeyValueListPair` was renamed to `VectorKeyValueListPair` / `RetrievalKeyValueListPair`
  * `DocumentKeyValueListPair` was renamed to `VectorDocumentKeyValueListPair` / `RetrievalDocumentKeyValueListPair`
  * `SearchConfiguration` was renamed to `VectorSearchConfiguration` / `RetrievalSearchConfiguration`
  * `SearchSelectOptionEnum` was renamed to `VectorSearchSelectOptionEnum` / `RetrievalSearchSelectOptionEnum`
  * `PerFilterSearchResult` was renamed to `RetrievalPerFilterSearchResult`
  * `PerFilterSearchError` was renamed to `RetrievalPerFilterSearchError`
  * `DataRepositorySearchResult` was renamed to `RetrievalDataRepositorySearchResult`
  * `SearchInput` was renamed to `RetrievalSearchInput` (e2c34f3)

* \[langchain] Remove structured ouput handling for deprecated gpt-4 & gpt-3 models (6100bca)

### New Features[​](#new-features-14 "Direct link to New Features")

* \[ai-api] Update `ai-api` package with the new specification (2509b). (58464e9)
* \[core, orchestration] Introduce orchestration embedding client for consuming embedding feature of the orchestration service. (347eac1)
* \[document-grounding] Update document-grounding specification (e2c34f3)

### Fixed Issues[​](#fixed-issues-6 "Direct link to Fixed Issues")

* \[core] Replace active logging during streaming with error throwing to avoid logging the response payload. (5225275)

### Improvements[​](#improvements-10 "Direct link to Improvements")

* \[core, orchestration] Add `cohere--command-a-reasoning`, `mistralai--mistral-medium-instruct` and perplexity-ai `sonar` and `sonar-pro` to model list (6100bca)

## 2.1.0 - October 17, 2025[​](#210---october-17-2025 "Direct link to 2.1.0 - October 17, 2025")

### Fixed Issues[​](#fixed-issues-7 "Direct link to Fixed Issues")

* \[orchestration] Fix JSDoc example of `buildAzureContentSafetyFilter()` function. (0cf7d80)

### Improvements[​](#improvements-11 "Direct link to Improvements")

* \[core] Remove `alephalpha-pharia-1-7b-control` and `deepseek-ai--deepseek-r1` from available model list. (0cf7d80)

## 2.0.0 - September 22, 2025[​](#200---september-22-2025 "Direct link to 2.0.0 - September 22, 2025")

### Compatibility Notes[​](#compatibility-notes-8 "Direct link to Compatibility Notes")

* \[foundation-models, orchestration] Change stream method parameter from `AbortController` to `AbortSignal`. The `stream()` method now accepts an `AbortSignal` instead of an `AbortController` as the second parameter in both Azure OpenAI and Orchestration clients. (4c00c27)

* \[foundation-models, orchestration] Response object `data` property is renamed to `_data`. Use getter methods like `getContent()`, `getTokenUsage()`, `getAssistantMessage()` instead of direct data access. (5c52cb6)

* \[foundation-models] Move generated types to internal exports while keeping frequently used types in main exports.

  <!-- -->

  * Generated types are no longer exported from `@sap-ai-sdk/foundation-models` and must be imported from `@sap-ai-sdk/foundation-models/internal.js` instead.
  * Frequently used types (`AzureOpenAiChatCompletionTool`, `AzureOpenAiFunctionObject`, `AzureOpenAiChatCompletionRequestMessage`, `AzureOpenAiChatCompletionRequestSystemMessage`, `AzureOpenAiChatCompletionRequestUserMessage`, `AzureOpenAiChatCompletionRequestAssistantMessage`, `AzureOpenAiChatCompletionRequestToolMessage`) remain available from main package exports.
  * Add new type `AzureOpenAiChatCompletionParameters` to replace `AzureOpenAiCreateChatCompletionRequest` which is no longer exported publicly. (5c52cb6)

* \[langchain] Major breaking changes for LangChain orchestration v2:

  <!-- -->

  * Update LangChain orchestration configuration structure to use `promptTemplating` instead of separate `llm` and `templating` properties.
  * Replace `llm.model_name` with `promptTemplating.model.name` and `llm.model_params` with `promptTemplating.model.params`.
  * The `templating.template` property is now `promptTemplating.prompt.template`.
  * Rename `inputParams` parameter to `placeholderValues` in LangChain orchestration client methods.
  * Update message response property names from `module_results` to `intermediate_results` in additional kwargs. (86e6370)

* \[langchain] Update imports to use new API facade from foundation-models package.

  <!-- -->

  * Some generated types now need to be imported from `@sap-ai-sdk/foundation-models/internal.js` instead of `@sap-ai-sdk/foundation-models`.
  * Update to use new `AzureOpenAiChatCompletionParameters` type to replace `AzureOpenAiCreateChatCompletionRequest` which is no longer exported publicly. (5c52cb6)

* \[orchestration] `buildTranslationConfig()` function now requires `type` parameter to distinguish between `input` and `output` translation configuration. (740ba78)

* \[orchestration] `buildLlamaGuardFilter()` function has been renamed to `buildLlamaGuard38BFilter()`. It now requires a type parameter to distinguish between `input` and `output` filter configurations, and accepts filter categories as an array. (740ba78)

* \[orchestration] Move generated types to internal exports while keeping frequently used types in main exports.

  <!-- -->

  * Generated types are no longer exported from `@sap-ai-sdk/orchestration` and must be imported from `@sap-ai-sdk/orchestration/internal.js` instead.
  * Frequently used types (`ChatMessage`, `SystemChatMessage`, `UserChatMessage`, `AssistantChatMessage`, `ToolChatMessage`, `DeveloperChatMessage`, `ChatCompletionTool`, `FunctionObject`) remain available from main package exports. (5c52cb6)

* \[orchestration] `buildAzureContentSafetyFilter()` function now requires `type` parameter to distinguish between `input` and `output` filter configuration. (997e8ec)

* \[orchestration] Major breaking changes for orchestration v2:

  <!-- -->

  * Consolidate `llm` and `templating` modules into a single `promptTemplating` module.
  * The `llm.model_name` property is now `promptTemplating.model.name` and `llm.model_params` is now `promptTemplating.model.params`.
  * The `templating.template` property is now `promptTemplating.prompt.template`.
  * Rename `inputParams` parameter to `placeholderValues` in orchestration client methods.
  * Update response property names from `orchestration_result` to `final_result` and `module_results` to `intermediate_results`.
  * Replace top-level `stream` property with `streamOptions.enabled` and update streaming module options from `llm` to `promptTemplating`.
  * Update grounding configuration to use `placeholders.input` and `placeholders.output` instead of separate `input_params` and `output_param`.
  * Update Azure content filter property names to lowercase with underscores: `Hate` to `hate`, `SelfHarm` to `self_harm`, `Sexual` to `sexual`, and `Violence` to `violence`.
  * Remove deprecated `buildAzureContentFilter()` function and use `buildAzureContentSafetyFilter()` instead. (86e6370)

### New Features[​](#new-features-15 "Direct link to New Features")

* \[ai-api] Add `resolveDeploymentUrl()` function to resolve the deployment URL that matches the given criteria. (14745de)
* \[foundation-models] Add `getTokenUsage()`, `getFinishReason()`, `getContent()`, `getToolCalls()`, `getRefusal()`, `getAssistantMessage()`, `findChoiceByIndex()` methods to Azure OpenAI chat completion response. (5c52cb6)
* \[orchestration] Add `prompt_shield` property to `buildAzureContentSafetyFilter()` function for input filter configuration to allow enabling prompt attack detection. (997e8ec)
* \[orchestration] Add `getIntermediateResults()` method to `OrchestrationResponse`, `OrchestrationStreamResponse`, `OrchestrationStreamChunkResponse` classes for accessing intermediate processing results from orchestration modules. (5c52cb6)
* \[orchestration] Add `deploymentId` as the optional parameter for OrchestrationClient initialization. (0a418d0)
* \[orchestration] Add `findChoiceByIndex()` method to find specific choices by index in streaming responses. (5c52cb6)

### Improvements[​](#improvements-12 "Direct link to Improvements")

* \[core] Add `gpt-5`,`gpt-5-mini` and `gpt-5-nano` to and remove `gemini-1.5-flash`, `gemini-1.5-pro` and `ibm--granite-13b-chat` from the available model list. (500c0dd)
* \[core] Add `anthropic--claude-4-opus`, `anthropic--claude-4-sonnet`, `amazon--nova-premier`, `gemini-2.5-flash` and `gemini-2.5-pro` to and remove `mistralai--mixtral-8x7b-instruct-v01`, `meta--llama3.1-70b-instruct`, `nvidia--llama-3.2-nv-embedqa-1b`, `amazon--titan-embed-text`, `gpt-4`, `amazon--titan-text-express` and `amazon--titan-text-lite` from the available model list. (9e1c43a)
