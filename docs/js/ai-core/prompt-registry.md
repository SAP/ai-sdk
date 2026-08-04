# Prompt Registry

The `@sap-ai-sdk/prompt-registry` package incorporates generative AI prompt registry capabilities into your AI activities in SAP AI Core and SAP AI Launchpad.

## Installation[​](#installation "Direct link to Installation")

```
npm install @sap-ai-sdk/prompt-registry
```

important

This package contains generated code. Updates to this package may include breaking changes.

To ensure compatibility and manage updates effectively, we strongly recommend using the tilde (`~`) version range in your project instead of the caret (`^`). This approach will allow patch-level updates while preventing potentially breaking minor version changes.

## Usage[​](#usage "Direct link to Usage")

The example below demonstrate a sample usage of APIs in SAP AI Core prompt registry service. In addition, you can find more sample code [here](https://github.com/SAP/ai-sdk-js/blob/main/sample-code/src/prompt-registry.ts).

### List Prompt Templates[​](#list-prompt-templates "Direct link to List Prompt Templates")

```
const response: PromptTemplateListResponse =

  await PromptTemplatesApi.listPromptTemplates({

    scenario: 'test'

  }).execute();
```

### Custom Destination[​](#custom-destination "Direct link to Custom Destination")

When calling the `execute()` method, it is possible to provide a custom destination for your SAP AI Core instance. For example, when querying deployments targeting a destination with the name `my-destination`, the following code can be used:

```
const response: PromptTemplateListResponse =

  await PromptTemplatesApi.listPromptTemplates({

    scenario: 'test'

  }).execute({

    destinationName: 'my-destination'

  });
```

By default, the fetched destination is cached. To disable caching, set the `useCache` parameter to `false` together with the `destinationName` parameter.

For more information about configuring a destination, refer to the [Using a Destination](/ai-sdk/docs/js/connecting-to-ai-core.md#using-a-destination) section.

## Custom Request Configuration[​](#custom-request-configuration "Direct link to Custom Request Configuration")

Set custom request configuration in the `requestConfig` parameter when calling the `.execute()` method.

```
const response: PromptTemplateListResponse =

  await PromptTemplatesApi.listPromptTemplates({

    scenario: 'test'

  }).execute(

    { destinationName: 'my-destination' },

    {

      requestConfig: {

        headers: {

          'x-custom-header': 'custom-value'

          // Add more headers here

        },

        params: {

          // Add more parameters here

        }

        // Add more request configuration here

      }

    }

  );
```

## Orchestration Configuration[​](#orchestration-configuration "Direct link to Orchestration Configuration")

The orchestration config API available as part of the prompt registry package allows to persist orchestration configurations. These configurations can include prompt templating, content filtering, data masking, grounding, and translation settings. Once stored, you can reference them when initializing an `OrchestrationClient` instance instead of defining the configuration inline.

For more details about orchestration configuration management, refer to the [SAP AI Core documentation](https://help.sap.com/docs/sap-ai-core/generative-ai/orchestration-config-management).

### Create an Orchestration Configuration[​](#create-an-orchestration-configuration "Direct link to Create an Orchestration Configuration")

Use the `createUpdateOrchestrationConfig()` method to create or update an orchestration configuration:

```
import { OrchestrationConfigsApi } from '@sap-ai-sdk/prompt-registry';



const orchestrationConfig = {

  name: 'my-orchestration-config',

  scenario: 'customer-support',

  version: '0.0.1',

  spec: {

    modules: {

      prompt_templating: {

        model: {

          name: 'gpt-5',

          version: 'latest'

        },

        prompt: {

          template: [

            {

              role: 'system' as const,

              content:

                'You are a helpful customer support assistant. Answer customer questions professionally and accurately.'

            },

            { role: 'user' as const, content: '{{?customerQuestion}}' }

          ]

        }

      }

    }

  }

};



const response =

  await OrchestrationConfigsApi.createUpdateOrchestrationConfig(

    orchestrationConfig

  ).execute();



console.log(response.id);
```

The response contains the generated `id` property, which uniquely identifies the orchestration configuration.

note

To use [streaming](/ai-sdk/docs/js/orchestration/chat-completion.md#streaming) with an orchestration configuration, include streaming settings in the `spec` property when creating the configuration.

### List Orchestration Configurations[​](#list-orchestration-configurations "Direct link to List Orchestration Configurations")

Use the `listOrchestrationConfigs()` method to retrieve existing orchestration configurations:

```
const configs = await OrchestrationConfigsApi.listOrchestrationConfigs({

  scenario: 'customer-support'

}).execute();
```

To use a stored orchestration configuration with the `OrchestrationClient`, refer to the [Initialization with Orchestration Configuration](/ai-sdk/docs/js/orchestration/chat-completion.md#initialization-with-orchestration-configuration) section in the chat completion guide.
