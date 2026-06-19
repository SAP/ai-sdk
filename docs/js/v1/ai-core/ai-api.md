# AI API

The `@sap-ai-sdk/ai-api` package provides tools to manage scenarios and workflows in SAP AI Core.

* Streamline data preprocessing and model training pipelines.
* Execute batch inference jobs.
* Deploy inference endpoints for trained models.
* Register custom Docker registries, sync AI content from Git repositories, and register object storage for training data and model artifacts.

We maintain a list of [currently available and tested AI Core APIs](https://github.com/SAP/ai-sdk-js/blob/main/docs/list-tested-APIs.md).

## Installation[​](#installation "Direct link to Installation")

```
$ npm install @sap-ai-sdk/ai-api
```

important

This package contains generated code. Updates to this package may include breaking changes.

To ensure compatibility and manage updates effectively, we strongly recommend using the tilde (`~`) version range in your project instead of the caret (`^`). This approach will allow patch-level updates while preventing potentially breaking minor version changes.

## Usage[​](#usage "Direct link to Usage")

The examples below demonstrate the usage of the most commonly used APIs in SAP AI Core. In addition to the examples below, you can find more sample code [here](https://github.com/SAP/ai-sdk-js/blob/main/sample-code/src/ai-api).

### Create an Artifact[​](#create-an-artifact "Direct link to Create an Artifact")

```
async function createArtifact() {

  const requestBody: ArtifactPostData = {

    name: 'training-test-dataset',

    kind: 'dataset',

    url: 'https://ai.example.com',

    scenarioId: 'foundation-models'

  };



  const responseData: ArtifactCreationResponse =

    await ArtifactApi.artifactCreate(requestBody, {

      'AI-Resource-Group': 'default'

    }).execute();

  return responseData;

}
```

### Create a Configuration[​](#create-a-configuration "Direct link to Create a Configuration")

```
async function createConfiguration() {

  const requestBody: ConfigurationBaseData = {

    name: 'gpt-4o',

    executableId: 'azure-openai',

    scenarioId: 'foundation-models',

    parameterBindings: [

      {

        key: 'modelName',

        value: 'gpt-4o'

      },

      {

        key: 'modelVersion',

        value: 'latest'

      }

    ],

    inputArtifactBindings: []

  };



  const responseData: ConfigurationCreationResponse =

    await ConfigurationApi.configurationCreate(requestBody, {

      'AI-Resource-Group': 'default'

    }).execute();

  return responseData;

}
```

### Create a Deployment[​](#create-a-deployment "Direct link to Create a Deployment")

```
async function createDeployment() {

  const requestBody: DeploymentCreationRequest = {

    configurationId: '0a1b2c3d-4e5f6g7h'

  };

  const responseData: DeploymentCreationResponse =

    await DeploymentApi.deploymentCreate(requestBody, {

      'AI-Resource-Group': 'default'

    }).execute();

  return responseData;

}
```

### Delete a Deployment[​](#delete-a-deployment "Direct link to Delete a Deployment")

Only deployments with `targetStatus: STOPPED` can be deleted. Thus, a modification request must be sent before deletion can occur.

```
async function modifyDeployment() {

  let deploymentId: string = '0a1b2c3d4e5f';



  const deployment: DeploymentResponseWithDetails =

    await DeploymentApi.deploymentGet(

      deploymentId,

      {},

      { 'AI-Resource-Group': 'default' }

    ).execute();



  if (deployment.targetStatus === 'RUNNING') {

    // Only RUNNING deployments can be STOPPED.

    const requestBody: DeploymentModificationRequest = {

      targetStatus: 'STOPPED'

    };



    await DeploymentApi.deploymentModify(deploymentId, requestBody, {

      'AI-Resource-Group': 'default'

    }).execute();

  }

  // Wait a few seconds for the deployment to stop

  return DeploymentApi.deploymentDelete(deploymentId, {

    'AI-Resource-Group': 'default'

  }).execute();

}
```

### Custom Destination[​](#custom-destination "Direct link to Custom Destination")

When calling the `execute()` method, it is possible to provide a custom destination for your SAP AI Core instance. For example, when querying deployments targeting a destination with the name `my-destination`, the following code can be used:

```
const queryParams = status ? { status } : {};

return DeploymentApi.deploymentQuery(queryParams, {

  'AI-Resource-Group': resourceGroup

}).execute({

  destinationName: 'my-destination'

});
```

By default, the fetched destination is cached. To disable caching, set the `useCache` parameter to `false` together with the `destinationName` parameter.

For more information about configuring a destination, refer to the [Using a Destination](/ai-sdk/docs/js/v1/connecting-to-ai-core.md#using-a-destination) section.
