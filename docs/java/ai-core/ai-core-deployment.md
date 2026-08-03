# AI Core Deployment

## Introduction[​](#introduction "Direct link to Introduction")

This guide provides examples on how to create and manage deployments in SAP AI Core using the SAP AI SDK for Java.

warning

All classes under any of the `...model` packages are generated from an OpenAPI specification. This means that these model classes are not guaranteed to be stable and may change with future releases. They are safe to use, but may require updates even in minor releases.

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

Before using the AI Core module, ensure that you have met all the general requirements outlined in the [overview](/ai-sdk/docs/java/overview.md#general-requirements). Additionally, include the necessary Maven dependency in your project.

### Maven Dependencies[​](#maven-dependencies "Direct link to Maven Dependencies")

Add the following dependency to your `pom.xml` file:

```
<dependency>

    <groupId>com.sap.ai.sdk</groupId>

    <artifactId>core</artifactId>

    <version>${ai-sdk.version}</version>

</dependency>
```

See [an example pom in our Spring Boot application](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/pom.xml)

## Usage[​](#usage "Direct link to Usage")

In addition to the prerequisites above, we assume you have already set up the following to carry out the examples in this guide:

* **An AI Core Configuration** created in SAP AI Core.

  <!-- -->

  * Example configuration from the AI Core `/configuration` endpoint

    ```
    {

      "createdAt": "2024-07-03T12:44:08Z",

      "executableId": "azure-openai",

      "id": "12345-123-123-123-123456abcdefg",

      "inputArtifactBindings": [],

      "name": "gpt-4o-mini",

      "parameterBindings": [

        {

          "key": "modelName",

          "value": "gpt-4o-mini"

        },

        {

          "key": "modelVersion",

          "value": "latest"

        }

      ],

      "scenarioId": "foundation-models"

    }
    ```

## Create a Deployment[​](#create-a-deployment "Direct link to Create a Deployment")

Use the following code snippet to create a deployment in SAP AI Core:

```
var api = new DeploymentApi();

var resourceGroupId = "default";

var configurationId = "12345-123-123-123-123456abcdefg";



var request = AiDeploymentCreationRequest.create().configurationId(configurationId);

var deployment = api.create(resourceGroupId, request);



String id = deployment.getId();

AiExecutionStatus status = deployment.getStatus();
```

Refer to the [DeploymentController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/DeploymentController.java) in our Spring Boot application for a complete example.

## Delete a Deployment[​](#delete-a-deployment "Direct link to Delete a Deployment")

```
AiDeploymentCreationResponse deployment; // provided

String deploymentId = deployment.getId();



var api = new DeploymentApi();

var resourceGroupId = "default";



if (deployment.getStatus() == AiExecutionStatus.RUNNING) {

  // Only RUNNING deployments can be STOPPED

  api.modify(

    resourceGroupId,

    deploymentId,

    AiDeploymentModificationRequest.create().targetStatus(AiDeploymentTargetStatus.STOPPED));

}

// Wait a few seconds for the deployment to stop

// Only UNKNOWN and STOPPED deployments can be DELETED

api.delete(resourceGroupId, deployment.getId());
```

Refer to the [DeploymentController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/DeploymentController.java) in our Spring Boot application for a complete example.
