# Prompt Registry

## Introduction[​](#introduction "Direct link to Introduction")

This guide provides examples on how to manage the life cycle of your prompts, from design to runtime in [Prompt Registry](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/prompt-registry).

warning

All classes in the `...model` and `...client` packages are generated from an OpenAPI specification. These classes can be used, but no API stability guarantees are provided, even for minor releases. Maintenance and support are limited to ensuring consistency with the service specification. No additional convenience API layer is provided.

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

Before using the Prompt Registry module, ensure that you have met all the general requirements outlined in the [overview](/ai-sdk/docs/java/overview-cloud-sdk-for-ai-java.md#general-requirements). Additionally, include the necessary Maven dependency in your project.

### Maven Dependencies[​](#maven-dependencies "Direct link to Maven Dependencies")

Add the following dependency to your `pom.xml` file:

```
<dependency>

    <groupId>com.sap.ai.sdk</groupId>

    <artifactId>prompt-registry</artifactId>

    <version>${ai-sdk.version}</version>

</dependency>
```

See [an example pom in our Spring Boot application](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/pom.xml)

## Create a Prompt Template[​](#create-a-prompt-template "Direct link to Create a Prompt Template")

### Tenant Scope Approach[​](#tenant-scope-approach "Direct link to Tenant Scope Approach")

You can create a reusable prompt for a specific use case, including placeholders that are filled later.

```
PromptClient client = new PromptClient();



var spec =

    PromptTemplateSpec.create()

        .template(

            SingleChatTemplate.create()

                .role("system")

                .content(

                    "You classify input text into the two following categories: {{?categories}}"),

            SingleChatTemplate.create().role("user").content("{{?inputExample}}"))

        .defaults(Map.of("categories", "Finance, Tech, Sports"));



var template = PromptTemplatePostRequest.create()

    .name("template-name")

    .version("0.0.1")

    .scenario("categorization")

    .spec(spec);



PromptTemplatePostResponse response = client.createUpdatePromptTemplate(template);
```

Refer to the [PromptRegistryController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/PromptRegistryController.java) in our Spring Boot application for a complete example.

### Resource Group Scope Approach[​](#resource-group-scope-approach "Direct link to Resource Group Scope Approach")

```
PromptClient client = new PromptClient();



var spec =

    PromptTemplateSpec.create()

        .template(

            SingleChatTemplate.create()

                .role("system")

                .content(

                    "You classify input text into the two following categories: {{?categories}}"),

            SingleChatTemplate.create().role("user").content("{{?inputExample}}"))

        .defaults(Map.of("categories", "Finance, Tech, Sports"));



var template = PromptTemplatePostRequest.create()

    .name("template-name")

    .version("0.0.1")

    .scenario("categorization")

    .spec(spec);



var resourceGroupId = "ai-sdk-java-e2e"; // your resource group id

var resourceGroupScope = "true";



PromptTemplatePostResponse response = client.createUpdatePromptTemplate(template, resourceGroupId, resourceGroupScope);
```

## Update a Prompt Template[​](#update-a-prompt-template "Direct link to Update a Prompt Template")

To update an existing prompt template, you can use the same `createUpdatePromptTemplate` method with the updated template details:

```
var updatedSpec = spec.defaults(Map.of("categories", "Finance, Tech, Sports, Politics"));



// using the same version will save the old prompt in the history

// using a new version will create a new prompt with a clean history

var updatedTemplate = template.spec(updatedSpec);



PromptTemplatePostResponse response = client.createUpdatePromptTemplate(updatedTemplate);
```

Refer to the [PromptRegistryController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/PromptRegistryController.java) in our Spring Boot application for a complete example.

### Resource Group Scope Approach[​](#resource-group-scope-approach-1 "Direct link to Resource Group Scope Approach")

```
var updatedSpec = spec.defaults(Map.of("categories", "Finance, Tech, Sports, Politics"));



// using the same version will save the old prompt in the history

// using a new version will create a new prompt with a clean history

var updatedTemplate = template.spec(updatedSpec);



var resourceGroupId = "ai-sdk-java-e2e"; // your resource group id

var resourceGroupScope = "true";



PromptTemplatePostResponse response = client.createUpdatePromptTemplate(updatedTemplate, resourceGroupId, resourceGroupScope);
```

## Get a Prompt Template[​](#get-a-prompt-template "Direct link to Get a Prompt Template")

You can retrieve a prompt template by ID, or by the combination of name, scenario, and version.

Prompt templates can also be retrieved and consumed in orchestration. For more information, see [Templating](/ai-sdk/docs/java/orchestration/chat-completion.md#templating).

```
PromptClient client = new PromptClient();



PromptTemplateListResponse templates = client.listPromptTemplates();
```

Refer to the [PromptRegistryController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/PromptRegistryController.java) in our Spring Boot application for a complete example.

## Get a Prompt Template History[​](#get-a-prompt-template-history "Direct link to Get a Prompt Template History")

You can list the history of edits to prompt templates, for imperatively managed prompt templates only.

```
PromptClient client = new PromptClient();



PromptTemplateListResponse history = client.listPromptTemplateHistory("categorization", "0.0.1", NAME);
```

Refer to the [PromptRegistryController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/PromptRegistryController.java) in our Spring Boot application for a complete example.

## Use a Prompt Template[​](#use-a-prompt-template "Direct link to Use a Prompt Template")

You can fill a prompt template by ID, or by the combination of name, scenario, and version.

### Tenant Scope Approach[​](#tenant-scope-approach-1 "Direct link to Tenant Scope Approach")

```
PromptClient client = new PromptClient();



PromptTemplateSubstitutionResponse substitution = client.parsePromptTemplateById(

    "212a9b9b-a532-4c1c-8852-bf75de853d74",

    false,

    PromptTemplateSubstitutionRequest.create()

        .inputParams(Map.of("inputExample", "I love football")));
```

Refer to the [PromptRegistryController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/PromptRegistryController.java) in our Spring Boot application for a complete example.

### Resource Group Scope Approach[​](#resource-group-scope-approach-2 "Direct link to Resource Group Scope Approach")

```
PromptClient client = new PromptClient();



var resourceGroupId = "ai-sdk-java-e2e"; // your resource group id

var resourceGroupScope = "true";



PromptTemplateSubstitutionResponse substitution = client.parsePromptTemplateById(

    "212a9b9b-a532-4c1c-8852-bf75de853d74",

    resourceGroupId,

    resourceGroupScope,

    false,

    PromptTemplateSubstitutionRequest.create()

        .inputParams(Map.of("inputExample", "I love football")));
```

## Import a Prompt Template[​](#import-a-prompt-template "Direct link to Import a Prompt Template")

You can import a declarative prompt template as a single file export in yaml format.

### Tenant Scope Approach[​](#tenant-scope-approach-2 "Direct link to Tenant Scope Approach")

```
PromptClient client = new PromptClient();



File template = new ClassPathResource("prompt-template.yaml").getFile();

PromptTemplatePostResponse response = promptClient.importPromptTemplate("default", null, template);
```

Refer to the [PromptRegistryController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/PromptRegistryController.java) in our Spring Boot application for a complete example.

### Resource Group Scope Approach[​](#resource-group-scope-approach-3 "Direct link to Resource Group Scope Approach")

```
PromptClient client = new PromptClient();



var resourceGroupId = "ai-sdk-java-e2e"; // your resource group id

var resourceGroupScope = "true";



Resource template = new ClassPathResource("prompt-template.yaml");

PromptTemplatePostResponse response = client.importPromptTemplate(resourceGroupId, resourceGroupScope, template.getFile());
```

## Export a Prompt Template[​](#export-a-prompt-template "Direct link to Export a Prompt Template")

You can export a prompt template as a single file export in declarative compatible yaml format.

warning

Currently not working

## Delete a Prompt Template[​](#delete-a-prompt-template "Direct link to Delete a Prompt Template")

### Tenant Scope Approach[​](#tenant-scope-approach-3 "Direct link to Tenant Scope Approach")

Delete a specific version of the prompt template, for imperatively managed prompt templates only.

```
PromptClient client = new PromptClient();



PromptTemplateDeleteResponse response = client.deletePromptTemplate(template.getId())
```

Refer to the [PromptRegistryController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/PromptRegistryController.java) in our Spring Boot application for a complete example.

### Resource Group Scope Approach[​](#resource-group-scope-approach-4 "Direct link to Resource Group Scope Approach")

```
PromptClient client = new PromptClient();



var resourceGroupId = "ai-sdk-java-e2e"; // your resource group id

var resourceGroupScope = "true";



PromptTemplateDeleteResponse response = client.deletePromptTemplate(template.getId(), resourceGroupId, resourceGroupScope);
```

## Using Templates in SpringAI[​](#using-templates-in-springai "Direct link to Using Templates in SpringAI")

You can use prompt templates with input parameters in your Spring AI application.

Add the following dependency to your `pom.xml` file:

```
<dependency>

    <groupId>org.springframework.ai</groupId>

    <artifactId>spring-ai-model</artifactId>

</dependency>
```

```
OpenAiClient openAiClient = OpenAiClient.forModel(OpenAiModel.GPT_4O_MINI);

ChatModel client = new OpenAiChatModel(openAiClient);



var repository = new InMemoryChatMemoryRepository();

var memory = MessageWindowChatMemory.builder().chatMemoryRepository(repository).build();

var advisor = MessageChatMemoryAdvisor.builder(memory).build();

var cl = ChatClient.builder(client).defaultAdvisors(advisor).build();



var promptResponse =

        new PromptClient()

            .parsePromptTemplateByNameVersion(

                "scenario",

                "0.0.1",

                "template_name",

                "resource-group",// usually "default"

                false,

                PromptTemplateSubstitutionRequest.create()

                    .inputParams(Map.of("parameter1", "value1")));



List<Message> messages = SpringAiConverter.promptTemplateToMessages(promptResponse);

var prompt = new Prompt(messages);



Generation response = cl.prompt(prompt).call().chatResponse().getResult();
```

Refer to the [PromptRegistryController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/PromptRegistryController.java) in our Spring Boot application for a complete example.

## Locally Test a Prompt Template[​](#locally-test-a-prompt-template "Direct link to Locally Test a Prompt Template")

Note that you can also locally test a prompt, without needing it to be deployed in the Prompt Registry. For more information, see [the Orchestration documentation](/ai-sdk/docs/java/orchestration/chat-completion.md#locally-test-a-prompt-template).

## Orchestration Configurations in Prompt Registry[​](#orchestration-configurations-in-prompt-registry "Direct link to Orchestration Configurations in Prompt Registry")

The orchestration config API available as part of Prompt Registry allows to persist Orchestration configurations. Once stored, you can reference and use them through your `OrchestrationClient` instead of defining the configuration during runtime.

Please refer to the [chapter on chat completion](/ai-sdk/docs/java/orchestration/chat-completion.md#using-a-prepared-configuration) for details on how to use a stored Orchestration configuration with your `OrchestrationClient`.

For more details about orchestration configuration management, refer to the [SAP AI Core documentation](https://help.sap.com/docs/sap-ai-core/generative-ai/orchestration-config-management).

### Create an Orchestration Configuration[​](#create-an-orchestration-configuration "Direct link to Create an Orchestration Configuration")

You can create a new Orchestration configuration in Prompt Registry as follows.

```
var orchConfigClient = new OrchestrationConfigClient();

var orchConfig = OrchestrationConfig.create()

        .modules(

            OrchestrationConfigModules.createInnerModuleConfigs(

                ModuleConfigs.create()

                    .promptTemplating(

                        PromptTemplatingModuleConfig.create()

                            .prompt(

                                Template.create()

                                    .template(

                                        UserChatMessage.create()

                                            .content(

                                                new UserChatMessageContent.InnerString("message"))

                                            .role(UserChatMessage.RoleEnum.USER)))

                            .model(LLMModelDetails.create().name("model-name")))));

var postRequest =

      OrchestrationConfigPostRequest.create()

          .name("name")

          .version("0.0.1")

          .scenario("scenario")

          .spec(buildOrchestrationConfig());

OrchestrationConfigPostResponse response = orchConfigClient.createUpdateOrchestrationConfig(postRequest);
```

### List Orchestration Configurations[​](#list-orchestration-configurations "Direct link to List Orchestration Configurations")

You can list the saved Orchestration configurations as follows.

```
var orchConfigClient = new OrchestrationConfigClient();

OrchestrationConfigListResponse response = orchConfigClient.listOrchestrationConfigs();
```
