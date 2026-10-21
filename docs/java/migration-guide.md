# Migration Guide to v2

Version 2 of the SAP Cloud SDK for AI is here and we highly recommend updating to it as soon as possible.

## Dependency updates[​](#dependency-updates "Direct link to Dependency updates")

**_New required minimum versions_**

`com.github.victools:jsonschema-generator` `5.0.0`

`com.githib.victools:jsonschema-module-jackson` `5.0.0`

`com.github.victools:jsonschema-module-swagger-2` `5.0.0`

`com.networknt:json-schema-validator` `3.0.1`

### MCP[​](#mcp "Direct link to MCP")

If your project uses Spring AI MCP autoconfiguration (i.e. you had `spring-ai-autoconfigure-mcp-client` in your `pom.xml` to register MCP clients from `application.yml`), that artifact was split in Spring AI 2.0.1, replace it:

```
<!-- Remove -->

<dependency>

  <groupId>org.springframework.ai</groupId>

  <artifactId>spring-ai-autoconfigure-mcp-client</artifactId>

</dependency>



<!-- Add -->

<dependency>

  <groupId>org.springframework.ai</groupId>

  <artifactId>spring-ai-autoconfigure-mcp-client-common</artifactId>

  <version>2.0.1</version>

</dependency>
```

If you use MCP clients manually in code (instantiating `SyncMcpToolCallbackProvider` directly), no change is needed, `spring-ai-mcp` already provides those classes.

## OpenAI[​](#openai "Direct link to OpenAI")

The replacement for the legacy OpenAI API (since v1.0.0) is the [new generated API (since v1.4.0)](/ai-sdk/docs/java/foundation-models/openai/chat-completion.md). But we also invite you to use the newer [OpenAI responses client](/ai-sdk/docs/java/foundation-models/openai/responses.md).

| Previous API                                                                         | Replacement                                                                              |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| `OpenAiClient.chatCompletion(String)`                                                | `OpenAiClient.chatCompletion(OpenAiChatCompletionRequest)`                               |
| `OpenAiClient.chatCompletion(OpenAiChatCompletionParameters)`                        | `OpenAiClient.chatCompletion(OpenAiChatCompletionRequest)`                               |
| `OpenAiClient.streamChatCompletionDeltas(OpenAiChatCompletionParameters)`            | `OpenAiClient.streamChatCompletionDeltas(OpenAiChatCompletionRequest)`                   |
| `embedding(OpenAiEmbeddingParameters)`                                               | `embedding(OpenAiEmbeddingRequest)`                                                      |
| legacy `com.sap.ai.sdk.foundationmodels.openai.model` package.                       | Request classes can be found in `com.sap.ai.sdk.foundationmodels.openai.generated.model` |
| `OpenAiClient.withApiVersion(String)` method. The API version is now set internally. | No replacement as targeting a specific API version is no longer supported.               |

### AI models[​](#ai-models "Direct link to AI models")

The following deprecated models were removed:

* `OpenAiModel.DALL_E_3`
* `OpenAiModel.GPT_35_TURBO`
* `OpenAiModel.GPT_35_TURBO_1025`
* `OpenAiModel.GPT_35_TURBO_16K`
* `OpenAiModel.GPT_4`
* `OpenAiModel.GPT_4_32K`
* `OpenAiModel.GPT_4O_MINI`
* `OpenAiModel.O3_MINI`
* `OpenAiModel.O1`
* `OpenAiModel.TEXT_EMBEDDING_ADA_002`

## Spring AI[​](#spring-ai "Direct link to Spring AI")

Spring AI was upgraded to `2.0.1`.

If you use the Spring AI integration (`OrchestrationChatModel`, `OpenAiChatModel`) together with tool calling, the following changes are required:

### Tool execution[​](#tool-execution "Direct link to Tool execution")

Use `ChatClient` instead of `isInternalToolExecutionEnabled`.

The `isInternalToolExecutionEnabled` flag has been removed in Spring AI 2.0.1. To execute tools automatically, route the call through `ChatClient` (which wires in `ToolCallingAdvisor`):

```
-options.setInternalToolExecutionEnabled(true);

-chatModel.call(prompt);



+ChatClient.builder(chatModel).build().prompt(prompt).call().chatResponse();
```

To receive raw tool calls without execution (e.g. to forward them to a client), call the model directly as before, no change needed there.

### Immutable options[​](#immutable-options "Direct link to Immutable options")

Use `.mutate().build()` to configure per-request options.

`OrchestrationChatOptions` and `DefaultToolCallingChatOptions` are now immutable. Use the builder to set per-request options such as tool callbacks:

```
-OrchestrationChatOptions options = new OrchestrationChatOptions(config);

-options.setToolCallbacks(...);  // no longer available



+OrchestrationChatOptions options = new OrchestrationChatOptions(config)

+    .mutate()

+    .toolCallbacks(ToolCallbacks.from(new MyTool()))

+    .build();
```

### Spring AI callbacks[​](#spring-ai-callbacks "Direct link to Spring AI callbacks")

`OrchestrationChatModel` applies registered tool callbacks automatically. Native SDK callers using the helper must pass `options.withCallbacks(template)` to `.promptTemplate(...)` and use `options.getConfig()` for the config. The helper adds tool definitions; it does not execute callbacks.

## Orchestration[​](#orchestration "Direct link to Orchestration")

| Previous API                                                                  | Replacement                                                                     |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `new OrchestrationModuleConfig().withLlmConfig(GPT_5)`                        | `new OrchestrationModuleConfig(GPT_5)`                                          |
| `TemplateConfig` / `OrchestrationTemplate` / `OrchestrationTemplateReference` | `PromptTemplate` / `LocalPromptTemplate` / `PromptTemplateReference`            |
| `OrchestrationPrompt`                                                         | `PromptTemplate.create(String)` or `PromptTemplate.create(Message, Message...)` |
| `OrchestrationTemplate.withTemplate(List<ChatMessage>)`                       | `LocalPromptTemplate.withMessages(Message...)`                                  |
| `OrchestrationPrompt.messageHistory(...)`                                     | `LocalPromptTemplate.withMessageHistory(...)`                                   |
| `OrchestrationConfigReference.withTemplateParameters(...)`                    | `withInputParameters(...)` on a completed reference                             |
| `OrchestrationChatOptions.getConfigWithCallbacks()`                           | `withCallbacks(LocalPromptTemplate)`, returning an enriched template            |
| `client.executeRequest(request)`                                              | `client.chatCompletion().lowLevel().request(request).execute()`                 |
| `client.streamChatCompletionDeltas(request)`                                  | `client.chatCompletion().lowLevel().request(request).executeStreamDeltas()`     |
| `client.embed(orchestrationEmbeddingRequest)`                                 | `client.embeddings().request(orchestrationEmbeddingRequest).execute()`          |
| `client.embed(embeddingsPostRequest)`                                         | `client.embeddings().lowLevel().request(embeddingsPostRequest).execute()`       |
| `OrchestrationClient.executeRequestFromJsonModuleConfig`                      | Removed without replacement                                                     |
| \[Internal] `createInputFilterConfig`                                         | Removed method without replacement                                              |
| \[Internal] `createOutputFilterConfig`                                        | Removed method without replacement                                              |
| \[Internal] `GroundingProvider.createConfig`                                  | Removed method without replacement                                              |
| \[Internal] `MaskingProvider.createConfig`                                    | Removed method without replacement                                              |
| \[Internal] `Message.createMessage`                                           | Removed method without replacement                                              |
| \[Internal] `AssistantMessage(List<MessageToolCall> toolCalls)`               | `AssistantMessage.withToolCalls(List)`                                          |

### Templates and execution[​](#templates-and-execution "Direct link to Templates and execution")

Templates are no longer stored in `OrchestrationModuleConfig`. Combine the former template and prompt messages in order, then pass the result separately:

```
-var template = TemplateConfig.create()

-    .withMessages(Message.system("Translate into {{?language}}"));

-var prompt = new OrchestrationPrompt(parameters, Message.user("Hello"))

-    .messageHistory(history);

-var response = client.chatCompletion(prompt, config.withTemplateConfig(template));

+var template = PromptTemplate.create(

+    Message.system("Translate into {{?language}}"), Message.user("Hello"))

+    .withInputParameters(parameters)

+    .withMessageHistory(history);

+var response = client.chatCompletion()

+    .config(config)

+    .promptTemplate(template)

+    .execute();
```

* Replace `streamChatCompletion(prompt, config)` with the same builder ending in `executeStream()` (`Stream<String>`). Use `executeStreamDeltas()` for full deltas, including reasoning, tool calls, usage, and intermediate results. Close both kinds of streams with try-with-resources.
* Set defaults, tools, and response formats on the local template using `withDefaults(...)`, `withTools(...)`, `withJsonResponse()`, or `withJsonSchemaResponse(...)`. All `with...` methods return updated instances; retain their results.
* Supply at least one template message. Import templates with `PromptTemplate.fromJson(...)` or `fromYaml(...)`, handling `IOException` and nullable results.

### Context Registry references[​](#context-registry-references "Direct link to Context Registry references")

Complete prompt-template references with `andInputParameters(...)` and pass them to the same `.promptTemplate(template)` step:

```
var template = PromptTemplate.reference().byId("template-id")

	.andInputParameters(parameters);

// Alternatively: reference().byScenario("translation").name("translator")

//     .version("0.0.1").andInputParameters(parameters)
```

Use `Map.of()` when no parameters are needed. Tenant scope is the default; set `.withScope(PromptTemplateReference.ScopeEnum.RESOURCE_GROUP)` after completing the reference if required.

For a stored orchestration configuration, replace `chatCompletionUsingReference(...)` with `configReference(...)`; no separate config or template is needed:

```
 var reference = OrchestrationConfigReference.fromScenario("translation")

	 .name("translator-config").version("0.0.1")

-    .withTemplateParameters(parameters);

+    .andInputParameters(parameters);

-var response = client.chatCompletionUsingReference(reference);

+var response = client.chatCompletion().configReference(reference).execute();
```

For ID-based configs, use `OrchestrationConfigReference.fromId(id).withInputParameters(parameters)`. Both config-reference forms support `withMessageHistory(...)`, `executeStream()`, and `executeStreamDeltas()`.

### AI models[​](#ai-models-1 "Direct link to AI models")

The following deprecated models were removed:

* `OrchestrationAiModel.IBM_GRANITE_13B_CHAT`
* `OrchestrationAiModel.MISTRAL_LARGE_INSTRUCT`
* `OrchestrationAiModel.MISTRAL_SMALL_INSTRUCT`
* `OrchestrationAiModel.MIXTRAL_8X7B_INSTRUCT_V01`
* `OrchestrationAiModel.LLAMA3_70B_INSTRUCT`
* `OrchestrationAiModel.LLAMA3_1_70B_INSTRUCT`
* `OrchestrationAiModel.CLAUDE_3_SONNET`
* `OrchestrationAiModel.CLAUDE_3_HAIKU`
* `OrchestrationAiModel.CLAUDE_3_OPUS`
* `OrchestrationAiModel.CLAUDE_3_5_SONNET`
* `OrchestrationAiModel.CLAUDE_3_7_SONNET`
* `OrchestrationAiModel.CLAUDE_4_SONNET`
* `OrchestrationAiModel.TITAN_TEXT_LITE`
* `OrchestrationAiModel.TITAN_TEXT_EXPRESS`
* `OrchestrationAiModel.GPT_35_TURBO`
* `OrchestrationAiModel.GPT_35_TURBO_16K`
* `OrchestrationAiModel.GPT_35_TURBO_0125`
* `OrchestrationAiModel.GPT_4`
* `OrchestrationAiModel.GPT_4_32K`
* `OrchestrationAiModel.GPT_4_0613`
* `OrchestrationAiModel.GPT_4O_MINI`
* `OrchestrationAiModel.OPENAI_O1`
* `OrchestrationAiModel.OPENAI_O3_MINI`
* `OrchestrationAiModel.GEMINI_1_0_PRO`
* `OrchestrationAiModel.GEMINI_1_5_PRO`
* `OrchestrationAiModel.GEMINI_1_5_FLASH`
* `OrchestrationAiModel.GEMINI_2_0_FLASH`
* `OrchestrationAiModel.GEMINI_2_0_FLASH_LITE`
* `OrchestrationAiModel.ALEPHALPHA_PHARIA_1_7B_CONTROL`
* `OrchestrationAiModel.DEEPSEEK_R1`

## Prompt registry client Migration Guide[​](#prompt-registry-client-migration-guide "Direct link to Prompt registry client Migration Guide")

`OrchestrationConfigClient` and `PromptClient` were replaced with unified `PromptRegistryClient`,

OrchestrationConfigClient:

```
-var orchestrationConfigsClient = new OrchestrationConfigClient();

-var configs = orchestrationConfigsClient.listOrchestrationConfigs();



+var orchestractionConfigsClient = new PromptRegistryClient().orchestrationConfig();

+var configs = orchestractionConfigsClient.listOrchestrationConfigs();
```

PromptRegistryClient:

```
-var promptClient = new PromptClient();

-var templates = promptClient.listPromptTemplates();



+var promptClient = new PromptRegistryClient().prompt();

+var templates = promptClient.listPromptTemplates();
```
