# Embedding

## Introduction[​](#introduction "Direct link to Introduction")

This guide demonstrates how to use the SAP AI SDK for Java to perform embedding tasks using Orchestration models deployed on SAP AI Core.

warning

All classes under any of the `...model` packages are generated from an OpenAPI specification. This means that these model classes are not guaranteed to be stable and may change with future releases. They are safe to use, but may require updates even in minor releases.

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

Before using the AI Core module, ensure that you have met all the general requirements outlined in the [overview](/ai-sdk/docs/java/overview.md#general-requirements). Additionally, include the necessary Maven dependency in your project.

### Maven Dependencies[​](#maven-dependencies "Direct link to Maven Dependencies")

Add the following dependency to your `pom.xml` file:

```
<dependencies>

    <dependency>

        <groupId>com.sap.ai.sdk</groupId>

        <artifactId>orchestration</artifactId>

        <version>${ai-sdk.version}</version>

    </dependency>

</dependencies>
```

See [an example pom in our Spring Boot application](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/pom.xml)

## Usage[​](#usage "Direct link to Usage")

In addition to the prerequisites above, we assume you have already set up the following to carry out the examples in this guide:

* **A Deployed Orchestration Model in SAP AI Core**

  * Refer to [How to deploy a model to AI Core](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-deployment-for-orchestration) for setup instructions.

  * In case the model is deployed in a custom resource group, refer to [this section](/ai-sdk/docs/java/orchestration/chat-completion.md#create-a-client-and-choose-an-llm).

  * Example deployed model from the AI Core `/deployments` endpoint

    ```
    {

      "id": "d123456abcdefg",

      "deploymentUrl": "https://api.ai.intprod-eu12.eu-central-1.aws.ml.hana.ondemand.com/v2/inference/deployments/d123456abcdefg",

      "configurationId": "12345-123-123-123-123456abcdefg",

      "configurationName": "orchestration",

      "scenarioId": "orchestration",

      "status": "RUNNING",

      "statusMessage": null,

      "targetStatus": "RUNNING",

      "lastOperation": "CREATE",

      "latestRunningConfigurationId": "12345-123-123-123-123456abcdefg",

      "ttl": null,

      "createdAt": "2024-08-05T16:17:29Z",

      "modifiedAt": "2024-08-06T06:32:50Z",

      "submissionTime": "2024-08-05T16:17:40Z",

      "startTime": "2024-08-05T16:18:41Z",

      "completionTime": null

    }
    ```

## Embedding[​](#embedding "Direct link to Embedding")

**Since v1.11.0**

Get the embeddings of a text input in list of float values:

```
var request = OrchestrationEmbeddingRequest

    .forModel(TEXT_EMBEDDING_3_SMALL)

    .forInputs("I am John Doe")

    .asDocument() // Optionally optimize for document content



OrchestrationEmbeddingResponse response = client.embed(request);

float[] embedding = response.getEmbeddingVectors().get(0);
```

See [an example in our Spring Boot application](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/OrchestrationService.java) for more features including masking of sensitive data.

Integration with CAP

In case you are using CAP, you can use the above code together with the native support for the [HANA Vector Store](https://cap.cloud.sap/docs/guides/databases-hana#vector-embeddings).
