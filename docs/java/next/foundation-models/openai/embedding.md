# Embedding

## Introduction[​](#introduction "Direct link to Introduction")

This guide demonstrates how to use the SAP AI SDK for Java to perform embedding tasks using OpenAI models deployed on SAP AI Core.

warning

All classes under any of the `...model` packages are generated from an OpenAPI specification. This means that these model classes are not guaranteed to be stable and may change with future releases. They are safe to use, but may require updates even in minor releases.

New User Interface (v1.4.0)

Starting with **version 2.0.0**, the old OpenAI client interface (v1.0.0) has been removed. The new interface introduced in v1.4.0 provides a more stable and maintainable experience, stays current with the latest OpenAI API specification, and aligns with the Orchestration convenience API.

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

Before using the AI Core module, ensure that you have met all the general requirements outlined in the [overview](/ai-sdk/docs/java/next/overview.md#general-requirements). Additionally, include the necessary Maven dependency in your project.

### Maven Dependencies[​](#maven-dependencies "Direct link to Maven Dependencies")

Add the following dependency to your `pom.xml` file:

```
<dependencies>

    <dependency>

        <groupId>com.sap.ai.sdk.foundationmodels</groupId>

        <artifactId>openai</artifactId>

        <version>${ai-sdk.version}</version>

    </dependency>

</dependencies>
```

See [an example pom in our Spring Boot application](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/pom.xml)

## Usage[​](#usage "Direct link to Usage")

In addition to the prerequisites above, we assume you have already set up the following to carry out the examples in this guide:

* **A Deployed OpenAI Model in SAP AI Core**

  * Refer to [How to deploy a model to AI Core](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-deployment-for-generative-ai-model-in-sap-ai-core) for setup instructions.

  * In case the model is deployed in a custom resource group, refer to [this section](/ai-sdk/docs/java/next/foundation-models/openai/chat-completion.md#using-a-custom-resource-group).

  * Example deployed model from the AI Core `/deployments` endpoint

    ```
    {

      "id": "d123456abcdefg",

      "deploymentUrl": "https://api.ai.region.aws.ml.hana.ondemand.com/v2/inference/deployments/d123456abcdefg",

      "configurationId": "12345-123-123-123-123456abcdefg",

      "configurationName": "gpt-4o-mini",

      "scenarioId": "foundation-models",

      "status": "RUNNING",

      "statusMessage": null,

      "targetStatus": "RUNNING",

      "lastOperation": "CREATE",

      "latestRunningConfigurationId": "12345-123-123-123-123456abcdefg",

      "ttl": null,

      "details": {

        "scaling": {

          "backendDetails": {}

        },

        "resources": {

          "backendDetails": {

            "model": {

              "name": "gpt-4o-mini",

              "version": "latest"

            }

          }

        }

      },

      "createdAt": "2024-07-03T12:44:22Z",

      "modifiedAt": "2024-07-16T12:44:19Z",

      "submissionTime": "2024-07-03T12:44:51Z",

      "startTime": "2024-07-03T12:45:56Z",

      "completionTime": null

    }
    ```

## Embedding[​](#embedding "Direct link to Embedding")

**Since v1.4.0**

Get the embeddings of a text input in list of float values:

```
var request = new OpenAiEmbeddingRequest(List.of("Hello World"));



OpenAiEmbeddingResponse response = OpenAiClient.forModel(TEXT_EMBEDDING_3_SMALL).embedding(request);

float[] embedding = embedding.getEmbeddingVectors().get(0);
```

**Since v1.0.0**

This interface has been removed in v2.0.0. Please use `OpenAiEmbeddingRequest` instead.
