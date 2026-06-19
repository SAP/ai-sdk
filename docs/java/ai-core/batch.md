# Batch

## Introduction[​](#introduction "Direct link to Introduction")

This guide provides examples on how to manage LLM batch jobs using the [Batch API](https://github.tools.sap/AI/llm-batch-service). It allows you to submit large numbers of requests asynchronously, which is useful for workloads that don't require immediate responses.

warning

All classes in the `...generated..` packages are generated from an OpenAPI specification. These classes can be used, but no API stability guarantees are provided, even for minor releases. Maintenance and support are limited to ensuring consistency with the service specification. No additional convenience API layer is provided.

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

Before using the Batch module, ensure that you have met all the general requirements outlined in the [overview](/ai-sdk/docs/java/overview-cloud-sdk-for-ai-java.md#general-requirements). Additionally, include the necessary Maven dependency in your project.

### Maven Dependencies[​](#maven-dependencies "Direct link to Maven Dependencies")

Add the following dependency to your `pom.xml` file:

```
<dependency>

    <groupId>com.sap.ai.sdk</groupId>

    <artifactId>batch</artifactId>

    <version>${ai-sdk.version}</version>

</dependency>
```

See [an example pom in our Spring Boot application](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/pom.xml)

### Object Store Setup[​](#object-store-setup "Direct link to Object Store Setup")

Batch requires an S3-compatible object store to be configured:

* Create an object store secret in **AI Launchpad > AI Core Administration > Object Store Secrets**.
* The credentials can be accessed from the **BTP Cockpit > Instances > Object Store**.
* [The input file must be a `.jsonl` file uploaded to the object store before creating a batch job.](#upload-batch-input)
* The output directory in the object store will receive the results once the batch job completes.

## Create a Batch Job[​](#create-a-batch-job "Direct link to Create a Batch Job")

Submit a new batch job by specifying the input file, output directory, and the model to use.

```
BatchesApi client = new BatchesApi();



BatchCreateResponse response = client.createBatch(

    "my-resource-group",

    BatchCreateRequest.create()

        .type(TypeEnum.LLM_NATIVE)

        .input(BatchCreateRequestInput.create().uri("ai://s3secret/input-batch.jsonl"))

        .output(BatchCreateRequestOutput.create().uri("ai://s3secret/batch-output/"))

        .spec(BatchCreateRequestSpec.create().provider("azure-openai").model("gpt-4.1")));
```

Refer to the [BatchController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/BatchController.java) in our Spring Boot application for a complete example.

## List Batch Jobs[​](#list-batch-jobs "Direct link to List Batch Jobs")

Retrieve all batch jobs for a given resource group.

```
BatchesApi client = new BatchesApi();



BatchListResponse response = client.listBatches("my-resource-group");
```

Refer to the [BatchController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/BatchController.java) in our Spring Boot application for a complete example.

## Get a Batch Job[​](#get-a-batch-job "Direct link to Get a Batch Job")

Retrieve the details and status of a specific batch job by its ID.

```
BatchesApi client = new BatchesApi();



BatchDetailResponse response = client.getBatchById(

    "my-resource-group",

    UUID.fromString("your-batch-job-id"));
```

Refer to the [BatchController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/BatchController.java) in our Spring Boot application for a complete example.

## Delete a Batch Job[​](#delete-a-batch-job "Direct link to Delete a Batch Job")

Delete a specific batch job by its ID.

```
BatchesApi client = new BatchesApi();



BatchDeleteResponse response = client.deleteBatch(

    "my-resource-group",

    UUID.fromString("your-batch-job-id"));
```

Refer to the [BatchController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/BatchController.java) in our Spring Boot application for a complete example.

## Upload Batch Input[​](#upload-batch-input "Direct link to Upload Batch Input")

Before creating a batch job, you need to upload the input file to the object store.

**Prerequisite:** Add the following dependency to your `pom.xml` file:

```
<dependency>

  <groupId>com.sap.ai.sdk.foundationmodels</groupId>

  <artifactId>openai</artifactId>

    <version>${ai-sdk.version}</version>

</dependency>

<dependency>

    <groupId>com.sap.ai.sdk</groupId>

    <artifactId>core</artifactId>

    <version>${ai-sdk.version}</version>

</dependency>
```

**Example:**

```
FileApi fileClient = new FileApi().withDefaultHeaders(Map.of("Content-Type", "text/csv"));



var batchInput =

    new OpenAiBatchInput(

        new OpenAiChatCompletionRequest("What is machine learning?"),

        new OpenAiChatCompletionRequest("Explain neural networks in simple terms"));



fileClient.upload("s3secret/input-batch.jsonl", "my-resource-group", true, batchInput);
```

Refer to the [BatchController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/BatchController.java) in our Spring Boot application for a complete example.

## Read Batch Output[​](#read-batch-output "Direct link to Read Batch Output")

Once a batch job has completed, you can download and read the output file from the object store using the `FileApi`.

**Prerequisite:** Add the following dependency to your `pom.xml` file:

```
<dependency>

    <groupId>com.sap.ai.sdk</groupId>

    <artifactId>core</artifactId>

    <version>${ai-sdk.version}</version>

</dependency>
```

**Example:**

```
FileApi fileClient = new FileApi();



String filePath = "s3secret/batch-output/" + batchJobId + "/output.jsonl";



try {

    File downloadedFile = fileClient.download(filePath, "my-resource-group");

    byte[] content = Files.readAllBytes(downloadedFile.toPath());

    downloadedFile.delete();



    if (content.length == 0) {

        System.out.println("No file found");

    } else {

        System.out.println(new String(content, StandardCharsets.UTF_8));

    }

} catch (OpenApiRequestException e) {

    System.err.println("Error downloading file");

} catch (Exception e) {

    System.err.println("Error reading file");

}
```

Refer to the [BatchController.java](https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/controllers/BatchController.java) in our Spring Boot application for a complete example.
