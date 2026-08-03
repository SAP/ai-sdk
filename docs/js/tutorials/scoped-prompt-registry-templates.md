# Using Scoped Prompt Registry Templates

## Introduction[​](#introduction "Direct link to Introduction")

This tutorial demonstrates how to use scoped prompt registry templates with custom headers in the SAP AI Core orchestration service. Scoped templates isolate prompt templates within specific resource groups, improving security and organizational control. Follow these steps to create an orchestration deployment and configure prompt templates with resource-group scoping using custom headers.

## Create a Configuration[​](#create-a-configuration "Direct link to Create a Configuration")

If no configuration exists, create a configuration with the following code:

```
const configurationPostData: AiConfigurationBaseData = {

  name: 'CONFIG_EXAMPLE',

  executableId: 'orchestration',

  scenarioId: 'orchestration'

};



const result: AiConfigurationCreationResponse =

  await ConfigurationApi.configurationCreate(configurationPostData, {

    'AI-Resource-Group': 'MY_RESOURCE_GROUP'

  }).execute();
```

## Create an Orchestration Deployment[​](#create-an-orchestration-deployment "Direct link to Create an Orchestration Deployment")

Create an orchestration deployment for the target resource group if it does not exist already with the following code:

```
const deploymentPostData: AiDeploymentCreationRequest = {

  configurationId: '3d2c1b0a'

};



const deploymentResponse = await createDeployment(deploymentPostData, {

  'AI-Resource-Group': 'MY_RESOURCE_GROUP'

});
```

## Create Prompt Template with Specific Resource Group Scope[​](#create-prompt-template-with-specific-resource-group-scope "Direct link to Create Prompt Template with Specific Resource Group Scope")

Create the prompt template with resource group scoping:

```
const promptTemplate = await PromptTemplatesApi.createUpdatePromptTemplate(

  {

    name: 'MY_SCOPED_TEMPLATE',

    scenario: 'MY_SCENARIO',

    version: '0.0.1',

    spec: {

      template: [

        {

          content: 'Hello, world!',

          role: 'user'

        }

      ]

    }

  },

  {

    'AI-Resource-Group-Scope': 'true',

    'AI-Resource-Group': 'MY_RESOURCE_GROUP'

  }

).execute();
```

## Consume Scoped Prompt Template in Orchestration client[​](#consume-scoped-prompt-template-in-orchestration-client "Direct link to Consume Scoped Prompt Template in Orchestration client")

Create the orchestration client with custom headers for resource group scoping:

```
import { OrchestrationClient } from '@sap-ai-sdk/orchestration';



const orchestrationClient = new OrchestrationClient(

  {

    promptTemplating: {

      model: {

        name: 'gpt-5'

      },

      prompt: {

        template_ref: {

          name: 'MY_SCOPED_TEMPLATE',

          scenario: 'MY_SCENARIO',

          version: '1.0.0',

          scope: 'resource_group'

        }

      }

    }

  },

  {

    resourceGroup: 'MY_RESOURCE_GROUP'

  }

);



const response = await orchestrationClient.chatCompletion({

  messages: [{ role: 'user', content: 'Hello, how can I help you?' }]

});
```

This configuration scopes the prompt template to the specified resource group and uses the appropriate headers for access control.

## Summary[​](#summary "Direct link to Summary")

This tutorial demonstrates how to use scoped prompt registry templates with resource group isolation:

* Creating a configuration with `AI-Resource-Group` and `AI-Resource-Group-Scope` headers for resource group scoping.
* Creating an orchestration deployment for a specific resource group.
* Creating a scoped prompt template in the prompt registry with resource group headers.
* Consuming the scoped template using the `OrchestrationClient` instance with `resourceGroup` header configuration.

Explore additional orchestration capabilities in the [Orchestration documentation](/ai-sdk/docs/js/orchestration/chat-completion.md).
