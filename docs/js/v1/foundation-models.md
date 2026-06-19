# Foundation Models

The `@sap-ai-sdk/foundation-models` package incorporates generative AI foundation models into your AI activities in SAP AI Core and SAP AI Launchpad.

## Installation[​](#installation "Direct link to Installation")

```
$ npm install @sap-ai-sdk/foundation-models
```

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

Refer to prerequisites outlined [here](/ai-sdk/docs/js/overview-cloud-sdk-for-ai-js.md#prerequisites).

## Client Initialization[​](#client-initialization "Direct link to Client Initialization")

Initialize a client with the model name. If model version is not specified, it is set to `latest`.

The current available clients are: - `AzureOpenAiChatClient` - `AzureOpenAiEmbeddingClient`

Take the `AzureOpenAiChatClient` as an example, use the following code to initialize a client:

```
import { AzureOpenAiChatClient } from '@sap-ai-sdk/foundation-models';



const client = new AzureOpenAiChatClient('gpt-4o');
```

The deployment ID will be implicitly fetched from the `default` resource group. By default, the deployment information is cached for five minutes, including deployment ID, model name, and model version.

When using other resource groups, you can specify the `resourceGroup` parameter.

```
const client = new AzureOpenAiChatClient({

  modelName: 'gpt-4o',

  // modelVersion: '2024-08-06', // optional

  resourceGroup: 'my-resource-group'

});
```

Alternatively, you can also provide a deployment ID instead of model name (and model version).

```
const client = new AzureOpenAiChatClient({

  // resourceGroup: 'my-resource-group', // optional

  deploymentId: 'd1234'

});
```

tip

When initializing a client for using a foundation model, it is equivalent to provide - a combination of model name and model version - or deployment ID

to identify a model within a [Resource Group](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/resource-groups?q=resource+group). If multiple deployments were created with the same model name and version, the first deployment will be used.

### Custom Destination[​](#custom-destination "Direct link to Custom Destination")

When initializing the client, it is possible to provide a custom destination for your SAP AI Core instance.

```
const client = await new AzureOpenAiChatClient('gpt-4o', {

  destinationName: 'my-destination'

});
```

By default, the fetched destination is cached. To disable caching, set the `useCache` parameter to `false` together with the `destinationName` parameter.

For more information about configuring a destination, refer to the [Using a Destination](/ai-sdk/docs/js/connecting-to-ai-core.md#using-a-destination) section.

## Custom Request Configuration[​](#custom-request-configuration "Direct link to Custom Request Configuration")

Set custom request configuration in the `requestConfig` parameter when calling the `run()` method of a client.

```
const response = await client.run(

  {

    ...

  },

  {

    headers: {

      'x-custom-header': 'custom-value'

      // Add more headers here

    },

    params: {

      // Add more parameters here

    }

    // Add more request configuration here

  }

);
```

This can be useful, e.g., to overwrite the API version of Azure OpenAI by defining the `api-version` parameter in the `params` object.

```
{

  params: {

    'api-version': 'AZURE_OPENAI_API_VERSION'

  }

}
```
