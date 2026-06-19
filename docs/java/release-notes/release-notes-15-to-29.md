# release-notes-15-to-29

## 1.20.0 - June 16, 2026[​](#1200---june-16-2026 "Direct link to 1.20.0 - June 16, 2026")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.20.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes "Direct link to 🔧 Compatibility Notes")

* Instead of `PromptTemplatingModuleConfig.create().prompt(prompt).model(model)` you have to use `PromptTemplatingModuleConfig.create().model(model).prompt(prompt)`.

### ✨ New Functionality[​](#-new-functionality "Direct link to ✨ New Functionality")

* \[Batch] Added a new `BatchesApi` client to access the [Batch Service API](https://github.tools.sap/AI/llm-batch-service).
* \[Orchestration] Added `GEMINI_3_1_FLASH_LITE`, `GEMINI_3_5_FLASH`, `GPT_55`, `SONAR_DEEP_RESEARCH`, and `LLAMA_CINDERELLA_DN` to model list in `OrchestrationAiModel`.
* \[OpenAI] Added `GPT_55` to model list in `OpenAiModel`.

### 📈 Improvements[​](#-improvements "Direct link to 📈 Improvements")

* \[Core] Optimized the deployments cache to store only `RUNNING` deployments, ensuring that requests do not resolve to `STOPPED` instances

## 1.19.0 - May 08, 2026[​](#1190---may-08-2026 "Direct link to 1.19.0 - May 08, 2026")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.19.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes-1 "Direct link to 🔧 Compatibility Notes")

* \[Document Grounding] `getAllPipelines()` has additional nullable parameter `metadataConfigId`.
* \[Prompt Registry] The `importPromptTemplate` and `importOrchestrationConfig` accepts `File` instead of `byte[]` to propagate file name in `Content-Disposition` header.

### ✨ New Functionality[​](#-new-functionality-1 "Direct link to ✨ New Functionality")

* \[Orchestration] Added `MISTRAL_SMALL` and `CLAUDE_4_7_OPUS` to model list in `OrchestrationAiModel`.

### 📈 Improvements[​](#-improvements-1 "Direct link to 📈 Improvements")

* Aggregated JavaDocs are now published on our [documentation portal](/ai-sdk/docs/java/overview-cloud-sdk-for-ai-java.md).

## 1.18.0 - April 16, 2026[​](#1180---april-16-2026 "Direct link to 1.18.0 - April 16, 2026")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.18.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes-2 "Direct link to 🔧 Compatibility Notes")

* Remove Spring dependency, by migrating generated API clients from `RestTemplate` (Spring) to `Apache`:

| Aspect                           | Before                                                                                          | After                                                                                                  | Migration                                                                                                |
| -------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| **API Class Base**               | `[...]Api` extends `AbstractOpenApiService`                                                     | `[...]Api` extends `BaseApi`                                                                           | Update inheritance in generated classes                                                                  |
| **Response Object**              | `com.sap.cloud.sdk.services.openapi.core.OpenApiResponse`                                       | `com.sap.cloud.sdk.services.openapi.apache.core.OpenApiResponse`                                       | Update import statements                                                                                 |
| **API Client**                   | `AiCoreService.getApiClient()` returns `com.sap.cloud.sdk.services.openapi.apiclient.ApiClient` | `AiCoreService.getApiClient()` returns `com.sap.cloud.sdk.services.openapi.apache.apiclient.ApiClient` | Update import statements                                                                                 |
| **importPromptTemplate() Input** | `Resource` parameter                                                                            | `byte[]` parameter                                                                                     | Call `Resource.getContentAsByteArray()`                                                                  |
| **Dependencies**                 | Includes `org.springframework`                                                                  | Removed                                                                                                | May need to add to `dependencyManagement`: `spring-core`, `spring-web`, `spring-beans`, `spring-context` |

* \[PromptRegistry] (Breaking) Removed `includeSpec` parameter from `listPromptTemplateHistory` method in `PromptTemplatesApi`
* \[Grounding] (Breaking) `GoogleDriveConfig` now has fields `resourceType` and `resourceId` instead of `folder`. `GoogleDriveFolderDetail` has been renamed to `GoogleDriveResourceDetail` and can now represent both folders and drives using `resourceType` and `resourceId`. `GoogleDrivePipelineCreateRequest` now requires `GoogleDriveConfigurationStruct` to be created
* Deprecated multiple Orchestration and OpenAI models: `MISTRAL_LARGE_INSTRUCT`, `MISTRAL_SMALL_INSTRUCT`, `OPENAI_O1`, and `OPENAI_O3_MINI`.

### ✨ New Functionality[​](#-new-functionality-2 "Direct link to ✨ New Functionality")

* \[Grounding] Added values `CREATING`, `CREATED`, `CREATION_FAILED`, `DELETION_INPROGRESS` and `DELETION_FAILED` for `PipelineExecutionStatus`.
* \[Grounding] New error type `GenericError` added. `ValidationError` now includes additional fields `input` and `ctx` for better debugging and error handling.
* \[Orchestration] Supported (PDF) file uploading feature by local file path via `UserMessage.withFile`, by remote file URL via `UserMessage.withFileUrl` , and by base64 encoded string file via `UserMessage.withFileBase64`.
* \[Orchestration] Added new models `GPT_53_CODEX`, `GPT_54`, and `GPT_54_NANO` for `OrchestrationAiModel`.
* \[OpenAI] Added new models `GPT_53_CODEX`, `GPT_54`, and `GPT_54_NANO` for `OpenAiModel`.

## 1.17.0 - March 27, 2026[​](#1170---march-27-2026 "Direct link to 1.17.0 - March 27, 2026")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.17.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes-3 "Direct link to 🔧 Compatibility Notes")

* Some changes to existing generated API in the *Prompt Registry* module.

* Changes to existing generated API in the *Prompt Registry* module. Generated methods now take additional (nullable) arguments. See full changelog for all details.

* Minor changes to generated API of *SAP Grounding Service*.

  ```
    var chunkMeta;

    var docMeta;

    var chunk =

  -   TextOnlyBaseChunk.create().content("Luna is the Latin word for moon.").metadata(chunkMeta);

  +   TextOnlyBaseChunkCreate.create().content("Luna is the Latin word for moon.").addMetadataItem(chunkMeta);



  - BaseDocument.create().chunks(chunk).metadata(docMeta);

  + BaseDocument.create().chunks(chunk).addMetadataItem(docMeta);
  ```

### ✨ New Functionality[​](#-new-functionality-3 "Direct link to ✨ New Functionality")

* \[Grounding] Added `GroundingClient.withHeader()`.
* \[Orchestration] Added `GPT_52` model for `OrchestrationAiModel`.
* \[OpenAi] Added `GPT_52` model from `OpenAiModel`.
* \[Orchestration] Added `GEMINI_EMBEDDING` model for `OrchestrationEmbeddingModel`.
* \[Orchestration] Added citations for Perplexity `SONAR` model in `client.chatCompletion().getOriginalResponse().getFinalResult().getCitations()`

### 📈 Improvements[​](#-improvements-2 "Direct link to 📈 Improvements")

* \[Orchestration] Added new API `TranslationConfig#applyToPlaceholders` and `TranslationConfig#applyToTemplateRoles` to support partial translation for a message.
* \[RPT] `RptClient.tableCompletion()` GZIP compresses the request payload.

## 1.16.0 - February 20, 2026[​](#1160---february-20-2026 "Direct link to 1.16.0 - February 20, 2026")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.16.0)

### ✨ New Functionality[​](#-new-functionality-4 "Direct link to ✨ New Functionality")

* \[RPT] Introducing `RptClient` for Tabular AI backed by SAP RPT models `SAP_RPT_1_SMALL` and `SAP_RPT_1_LARGE`.
  <!-- -->
  * Added support for Parquet file input with `RptClient#tableCompletion` for larger datasets.
* \[Orchestration] Added new API `OrchestrationTemplateReference#withScope` to support prompt templates with resource-group scope.
* \[Orchestration] Chat completion calls now can have multiple module configs to support [fallback modules](/ai-sdk/docs/java/orchestration/chat-completion.md).
* \[Orchestration] Deprecated `ALEPHALPHA_PHARIA_1_7B_CONTROL` model from `OrchestrationAiModel` with replacement model `MISTRAL_SMALL_INSTRUCT`.
* \[Orchestration] Deprecated `GPT_4O_MINI` model from `OrchestrationAiModel` with replacement model `GPT_5_MINI`.
* \[Orchestration] Deprecated `GPT_4O_MINI` model from `OpenAiModel` with replacement model `GPT_5_MINI`.
* \[Orchestration] Deprecated models `GEMINI_2_0_FLASH`, `GEMINI_2_0_FLASH_LITE` and `CLAUDE_3_7_SONNET` from `OrchestrationAiModel`.
* \[Orchestration] Deprecated `DALL_E_3` model from `OpenAiModel`.
* \[Orchestration] Added new models `CLAUDE_4_6_SONNET` and `CLAUDE_4_6_OPUS` in `OrchestrationAiModel`.

### 📈 Improvements[​](#-improvements-3 "Direct link to 📈 Improvements")

* \[Orchestration] `AzureContentFilter.protectedMaterialCode()` is now supported as an output content filtering module .

## 1.15.0 - January 21, 2026[​](#1150---january-21-2026 "Direct link to 1.15.0 - January 21, 2026")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.15.0)

### ✨ New Functionality[​](#-new-functionality-5 "Direct link to ✨ New Functionality")

* \[Orchestration] Configs stored in prompt registry can now be used for [Orchestration calls via reference](/ai-sdk/docs/java/orchestration/chat-completion.md).
* \[Prompt Registry] Added support to [manage Orchestration configs stored in Prompt Registry](/ai-sdk/docs/java/ai-core/prompt-registry.md).
