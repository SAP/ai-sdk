# Release Notes
## 7.2.0

### Features
- Added Support for LLM Batch Service, see [](batch_service)

### Bugfixes
- Upgraded langchain
- Upgraded langchain-aws
- Upgraded langchain-google-genai
- Upgraded langchain-openai
- Upgraded google-genai to v2
- Fixed OrchestrationV2 response handling
- Removed hard-coded model lists. New versions of existing models will be automatically supported.

## 6.10.0

### Features
- Added model_version as model identifier
- Updated Prompt Registry Client to align with API changes
- Added support for OpenAI Responses API, see [](responses_api)
- Enabled flat import for Model/Client classes
- Added support for newly added models to the AI Core, see [](supported_models)

### Bugfixes
- Upgraded google-genai
- Upgraded langchain

## 6.7.0

### Features
- Added support for Orchestration Config API of Prompt Registry, see [](orchestration_config_api)
- Added retry logic for token retrieval

### Bugfixes
- Upgraded langchain-aws

## 6.6.0

### Bugfixes
- Replaced the lingua-language-detector library, which was causing version conflict issues. 

## 6.5.0

### Features
- Enabled providing additional headers for Grounding Clients (Pipeline API Client, Retrieval API Client & Vector API Client)
- Added support for Orchestration V2 API /embeddings endpoint, see [](orchestration2)
- Added Evaluations Client, see [](evaluations)
- Added support for RPT-1 models, see [](rpt_models)

### Bugfixes
- Fixed the issue regarding the handling of large streaming responses in AsyncSSEClient
- Upgraded langchain version
- Adjusted to the changes in Orchestration V2 API
- Removed aiboto3 dependency in favor of aibotocore

## 6.1.2

### Breaking Changes

- Switch to [langchain 1.x](https://docs.langchain.com/oss/python/langchain/overview) This also results in upgrading of dependent langchain libraries. You need to ensure your code works with the upgraded dependencies. Langchain 0.3.x is no longer supported in the SDK. Please refer to [](package_dependencies) for details on the dependencies.
- Switch from langchain-google-vertexai to langchain-google-genai and google-cloud-aiplatform to google-genai due to [deprecation of these libraries](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/deprecations/genai-vertexai-sdk)

### Features
- Added support for additional embedding models: Amazon Titan Embedding, Llama 3.2 Embedding, Google Gemini Embedding

## 5.11.0

### Features
- Added support for orchestration V2 API. For details, see [](orchestration2).
- Added API reference documentation
- Added support for new models: Claude 4.5 Sonnet, Claude 4.5 Haiku, Cohere Command-a-reasoning, Cohere reranker, Gemini 2.5 Flash Lite, Perplexity Sonar, Perplexity Sonar-Pro, Mistral Medium
- Removed decomissioned models: IBM granite 13b, Meta Llama 3.1, Claude 3 Opus

## 5.10.0

### Features

- Added retry logic for orchestration service with exponential backoff. Use method "run_with_retries" instead of "run" for your orchestration service instance.

## 5.9.0

### Bugfixes

- Upgraded boto3 and langchain-aws dependencies and relaxed the dependecy to pydantic libary, see [](package_dependencies) for details.

## 5.8.0

### Features 

- Added additional apis for document grounding: vector api and retrieval api support and additional methods for pipelines api.

## 5.7.5

### Features

- Added support for new models: Amazon Nova Premier, Claude 4 Opus, Gemini 2.5-flash, Gemini 2.5-pro, GPT-5, GPT-5-mini, GPT-5-nano, Mistral Small Instruct. See [](supported_models) for a comprehensive overview of supported models.
- Removed old models: Amazon Titan Text Express/Lite, Gemini 1.5-flash, Gemini 1.5-pro, Claude 3 Sonnet 
- Allow botocore.config as input for Amazon Bedrock to set additional parameters, e.g. connect_timeout

### Bugfixes

- Upgraded langchain-google-vertexai to fix a [bug in ChatVertexAI](https://github.com/langchain-ai/langchain-google/issues/1057)
- Upgraded boto3 and langchain-aws dependencies to allow tool binding with Claude 4

## 5.6.3

### Features

- Added support for converse_stream for aws models and event streams

### Bugfixes

- Display deployment not found error in orchestration
- Return http headers from orchestration in case of error

## 5.5.0

### Features

- Added support for Claude 4 Sonnet

### Bugfixes 

- Upgraded langchain-google-vertexai to fix a bug with streaming on newer gemini models
- Fix issue where template input parameters would be converted to CamelCase when sending to prompt registry API

## 5.4.5

### Features

- Added support for additional storage types (S3/SFTP) for the Grounding module of the Orchestration Service.


## 5.4.1

### Features

- Added support for images in the orchestration service. See [](input_images) for details.
- Added timeout parameter for amazon native streaming calls in method `invoke_model_with_response_stream`.

## 5.3.4

### Breaking Changes

- Switch to different distribution name as part of a rebranding to `SAP Cloud SDK for AI (Python) - generative`. See [](installation) for details. The package and subpackage names are unchanged, therefore no code adjustment is necessary, only the installation of the SDK has changed.

### Features

- Added support for the translation module in the orchestration service. See [](translation) for details.
- Added support for function calling in the orchestration service. See [](tool_calling) for details.
- Added support for OpenAI o3, o4-mini, gpt-4.1, gpt-4.1-mini, gpt-4.1-nano models.
- Reworked the langchain dependency chain, only installing the vendor specific langchain libraries on demand, see [](installation) for details.

### Bugfixes

- Set the dependency to h11 library and relaxed the dependecy to pydantic libary, see [](package_dependencies) for details.

## 4.12.1

### Features
- Added support for Anthropic Claude 3.7 Sonnet model.
- Added support for gemini-2.0 and gemini-2.0-flash models.
- Retirement of Gemini 1.0 Pro.
- Added async examples for bedrock and vertex models. See [](async_examples) for details.
- Deprecation of SAP Generative AI Hub SDK, as it will be rebranded to sap-ai-sdk-gen.

## 4.10.2

### Features

- Added support for OpenAI o1 and o3-mini models.
- Added support for AWS amazon--nova-micro, amazon--nova-lite, and amazon--nova-pro models.
- Added support for asynchronous calls to Bedrock models.
- Added support for asynchronous calls to Vertex models.
- Added support for `masked_grounding_input` and `allowlist` also for the grounding output in the orchestration service. See [](allow_list) for details.
- Deprecation of `input_filters` and `output_filters` in the orchestration configuration, use `ContentFiltering` instead. See [](content_filtering) for details.

## 4.4.3

### Features

- Add support for LlamaGuard38b content filtering in the orchestration service. You can use LlamaGuard38b filters for filtering input and output along different content categories, see [SAP AI Core help documentation](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/input-filtering?locale=en-US). For usage examples, see [](content_filtering)
- Add support for grounding metadata parameters, see [SAP AI Core help documentation](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/metadata?locale=en-US)
- Add support for asynchronous calls to orchestration service. See [](orchestration_async) for details.

## 4.3.1

### Features

- Add support for prompt registry APIs. You can create, retrieve and modify prompt templates from the prompt repository. For example usage, see [](prompt_registry_notebook)
- Add support for grounding in orchestration. You can now configure the grounding module in the orchestration service.
- Add support for structured output in the orchestration service by specifying the response format, for instance text or json. See [](response_format) for details.
- Add autodiscovery for orchestration deployments. See [](orchestration_deployment) for details.

### Bugfixes

- OpenAI deprecated max_tokens in favor of max_completion_tokens parameter. This was now also included in the generative AI Hub SDK and the dependency of the langchain-openai version could be relaxed.

## 4.1.1

### Features

- Add support for prompt registry templates in orchestration. You can now configure a prompt registry template in the orchestration service call by referencing the ID or scenario, template name, and version. See [](prompt_registry)

### Bugfixes

- Set langchain-openai==0.2.9 due to max_completion_token issues with later versions.

## 4.0.0

### Breaking Changes

- Switch to [langchain 0.3.x](https://python.langchain.com/docs/versions/v0_3/) This also results in upgrading of dependent langchain libraries and a transition to pydantic v2. You need to ensure your code works with the upgraded dependencies. Langchain 0.2.x is no longer supported in the SDK. Please refer to [](package_dependencies) for details on the dependencies.

### Features

- Add support for streaming in orchestration service. See the example notebook here: [](orchestration_streaming).
- Add enhanced debug logging: When log level debug is enabled the source of configuration will be logged to support troubleshooting.

## 3.8.0

### Features

- Add support for mistralai--mistral-large-instruct model
- Add support for ibm--granite-13b-chat model
- Add capability to access unsupported models, see the example notebook [](unsupported_models) for details.
- Add enhanced logging for API calls
  - By setting the environment variable `DEBUG_LOG_API_CALLS` to `true`, all calls to the backend are logged for better error diagnosis

## 3.2.6

### Features

- Add support for orchestration service: data masking. See the example notebook section [](content_filtering) for details.
 
### Bugfixes

- Bugfix for x509 certificate authentication support

## 3.1.1

### Features

- Add support for gpt-4o model

## 3.1.0

### Breaking Changes

- Switch to vertexAI SDK for native Google model access. The previous library 'google-generativeai' is no longer supported by the generative AI Hub SDK.

### Features

- Add support for orchestration service: templating, content safety, inference. See the example notebook [](orchestration) for details.
- Add support for anthropic--claude-3.5-sonnet model
