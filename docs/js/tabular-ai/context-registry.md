# Context Registry

important

This package is in **beta** and subject to breaking changes. Do not use in production.

This package contains generated code, so updates may include breaking changes. We strongly recommend using the tilde (`~`) version range instead of the caret (`^`) to allow patch updates while preventing potentially breaking minor version changes.

The `@sap-ai-sdk/context-registry` package provides a client for the SAP Context Registry service. Before you can request predictions from the Tabular Orchestration service, you need to configure three resources in the Context Registry. For an overview of the design-time setup process, see the [SAP AI Core documentation](https://help.sap.com/docs/sap-ai-core/generative-ai/design-time-setup?locale=en-US).

<!-- -->

The three resources serve the following purposes:

* **Data Destination**: stores the connection details and credentials for an external data store such as HANA Data Lake, Azure Blob Storage, S3, or GCS.
* **Tabular Artifact**: references a file within a Data Destination (for example, a Parquet file) and carries the schema metadata the prediction service needs.
* **Scenario Configuration**: groups one or more Tabular Artifacts under a single name. You pass that name to the Tabular Orchestration service when requesting a prediction.

## Installation[​](#installation "Direct link to Installation")

```
npm install @sap-ai-sdk/context-registry
```

## Usage[​](#usage "Direct link to Usage")

The examples below cover the most common operations for each resource. You can find additional sample code [here](https://github.com/SAP/ai-sdk-js/blob/main/sample-code/src/tabular-orchestration.ts).

### Data Destinations[​](#data-destinations "Direct link to Data Destinations")

For service-level details, see the [Data Destination documentation](https://help.sap.com/docs/sap-ai-core/generative-ai/data-destination?locale=en-US). Create and delete operations are asynchronous. The API returns `202 Accepted` with a `Location` header pointing to the new resource. Poll the `getDataDestinationByName()` method and check `status` until it reaches `ACTIVE`.

#### List Data Destinations[​](#list-data-destinations "Direct link to List Data Destinations")

```
import { DataDestinationsApi } from '@sap-ai-sdk/context-registry';



const response: GetDataDestinations =

  await DataDestinationsApi.getAllDataDestinations(

    {},

    { 'AI-Resource-Group': 'default' }

  ).execute();
```

#### Create or Update a Data Destination[​](#create-or-update-a-data-destination "Direct link to Create or Update a Data Destination")

Use the `createUpdateDataDestination()` method to upsert a destination. Use `executeRaw()` to access the `Location` header for polling.

```
const response = await DataDestinationsApi.createUpdateDataDestination(

  'my-hdl-destination',

  {

    type: 'HDL',

    config: {

      host: 'my-hdl-instance.hanacloud.ondemand.com'

    }

  },

  { 'AI-Resource-Group': 'default' }

).executeRaw();



// response.status === 202

// response.headers.location points to the new resource
```

#### Validate a Data Destination[​](#validate-a-data-destination "Direct link to Validate a Data Destination")

Use the `validateDataDestination()` method to test provider connectivity before saving. Nothing is persisted.

```
const result: ValidateDataDestinationResponse =

  await DataDestinationsApi.validateDataDestination(

    {

      type: 'S3',

      config: {

        bucket: 'my-bucket',

        region: 'eu-central-1',

        access_key_id: 'MY_ACCESS_KEY_ID',

        secret_access_key: 'MY_SECRET_ACCESS_KEY'

      }

    },

    { 'AI-Resource-Group': 'default' }

  ).execute();
```

#### Delete a Data Destination[​](#delete-a-data-destination "Direct link to Delete a Data Destination")

The API checks for dependent Tabular Artifacts synchronously, then returns `202 Accepted` and marks the destination as `DELETING`. A background task handles the actual removal.

```
await DataDestinationsApi.deleteDataDestinationByName('my-hdl-destination', {

  'AI-Resource-Group': 'default'

}).execute();
```

### Tabular Artifacts[​](#tabular-artifacts "Direct link to Tabular Artifacts")

For service-level details, see the [Tabular Artifact documentation](https://help.sap.com/docs/sap-ai-core/generative-ai/tabular-artifact?locale=en-US). A Tabular Artifact references a file within a Data Destination and carries the schema metadata the prediction service needs. Creation is asynchronous; poll the `getTabularArtifactByName()` method until `status` is `ACTIVE`.

#### List Tabular Artifacts[​](#list-tabular-artifacts "Direct link to List Tabular Artifacts")

```
import { TabularArtifactsApi } from '@sap-ai-sdk/context-registry';



const response: TabularArtifactListResponse =

  await TabularArtifactsApi.getAllTabularArtifacts(

    {},

    { 'AI-Resource-Group': 'default' }

  ).execute();
```

#### Create a Tabular Artifact[​](#create-a-tabular-artifact "Direct link to Create a Tabular Artifact")

```
const response = await TabularArtifactsApi.createTabularArtifact(

  'my-tabular-artifact',

  {

    dataDestinationName: 'my-hdl-destination',

    type: 'PARQUET',

    path: '/data/product_data.parquet',

    csnMetadata: { definition: { definitionType: 'AUTO' } }

  },

  { 'AI-Resource-Group': 'default' }

).executeRaw();



// response.status === 202

// response.headers.location points to the new resource
```

#### Preview Tabular Artifact Data[​](#preview-tabular-artifact-data "Direct link to Preview Tabular Artifact Data")

Use the `getTabularArtifactData()` method to retrieve the first 10 rows of the artifact. This is useful for verifying the data is readable before creating a Scenario Configuration.

```
import { TabularArtifactsApi } from '@sap-ai-sdk/context-registry';



const preview: TabularArtifactDataPreview =

  await TabularArtifactsApi.getTabularArtifactData('my-tabular-artifact', {

    'AI-Resource-Group': 'default'

  }).execute();
```

### Scenario Configurations[​](#scenario-configurations "Direct link to Scenario Configurations")

For service-level details, see the [Scenario Configuration documentation](https://help.sap.com/docs/sap-ai-core/generative-ai/scenario-configuration?locale=en-US). A Scenario Configuration groups one or more Tabular Artifacts under a single name. Pass that name to the Tabular Orchestration service when requesting a prediction.

#### List Scenario Configurations[​](#list-scenario-configurations "Direct link to List Scenario Configurations")

```
import { ScenarioConfigurationManagerApi } from '@sap-ai-sdk/context-registry';



const response: GetScenarioConfigurations =

  await ScenarioConfigurationManagerApi.getAllScenarioConfigurations(

    {},

    { 'AI-Resource-Group': 'default' }

  ).execute();
```

#### Create a Scenario Configuration[​](#create-a-scenario-configuration "Direct link to Create a Scenario Configuration")

```
await ScenarioConfigurationManagerApi.createScenarioConfiguration(

  'my-scenario-config',

  {

    description: 'Product prediction scenario',

    contextSelectionStrategy: 'random',

    tabularArtifacts: [{ name: 'my-tabular-artifact' }]

  },

  { 'AI-Resource-Group': 'default' }

).execute();
```

#### Update a Scenario Configuration[​](#update-a-scenario-configuration "Direct link to Update a Scenario Configuration")

Use the `patchScenarioConfigurationByName()` method to update individual fields without replacing the entire resource.

```
await ScenarioConfigurationManagerApi.patchScenarioConfigurationByName(

  'my-scenario-config',

  {

    description: 'Updated description',

    tabularArtifacts: [

      { name: 'my-tabular-artifact' },

      { name: 'my-other-artifact' }

    ]

  },

  { 'AI-Resource-Group': 'default' }

).execute();
```

#### Delete a Scenario Configuration[​](#delete-a-scenario-configuration "Direct link to Delete a Scenario Configuration")

```
await ScenarioConfigurationManagerApi.deleteScenarioConfigurationByName(

  'my-scenario-config',

  { 'AI-Resource-Group': 'default' }

).execute();
```

### Polling for Async Operations[​](#polling-for-async-operations "Direct link to Polling for Async Operations")

Create and delete operations return `202 Accepted` and complete in the background. Poll the corresponding `GET` endpoint and wait until `status` is `ACTIVE`, or until the endpoint returns 404 for deletions. The following example polls until a Tabular Artifact is ready:

```
import { setTimeout } from 'node:timers/promises';



async function pollUntilActive(name: string): Promise<TabularArtifactDetails> {

  for (let attempt = 0; attempt < 60; attempt++) {

    const artifact = await TabularArtifactsApi.getTabularArtifactByName(name, {

      'AI-Resource-Group': 'default'

    }).execute();



    if (artifact.status === 'ACTIVE') {

      return artifact;

    }

    if (artifact.status === 'ERROR') {

      throw new Error(

        artifact.errorMessage ?? 'Tabular artifact creation failed'

      );

    }



    await setTimeout(2000);

  }

  throw new Error('Timed out waiting for tabular artifact to become active');

}
```

The same pattern applies to Data Destinations and Scenario Configurations.

## Custom Destination[​](#custom-destination "Direct link to Custom Destination")

Pass a `destinationName` to the `execute()` method to target a specific SAP AI Core instance.

```
const response = await DataDestinationsApi.getAllDataDestinations(

  {},

  { 'AI-Resource-Group': 'default' }

).execute({ destinationName: 'my-destination' });
```

By default, the fetched destination is cached. To disable caching, set `useCache` to `false` together with `destinationName`.

For more information about configuring a destination, refer to the [Using a Destination](/ai-sdk/docs/js/connecting-to-ai-core.md#using-a-destination) section.

## Custom Request Configuration[​](#custom-request-configuration "Direct link to Custom Request Configuration")

Pass request configuration as a second argument to the `execute()` method.

```
const response = await DataDestinationsApi.getAllDataDestinations(

  {},

  { 'AI-Resource-Group': 'default' }

).execute(undefined, {

  headers: {

    'x-custom-header': 'custom-value'

  }

});
```
