# Prompt Registry

The `@sap-ai-sdk/prompt-registry` package incorporates generative AI prompt registry capabilities into your AI activities in SAP AI Core and SAP AI Launchpad.

## Installation[​](#installation "Direct link to Installation")

```
$ npm install @sap-ai-sdk/prompt-registry
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

For more information about configuring a destination, refer to the [Using a Destination](/ai-sdk/docs/js/v1/connecting-to-ai-core.md#using-a-destination) section.
