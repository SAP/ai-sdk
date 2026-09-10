# Connecting to AI Core

The SAP AI SDK uses the [`Destination` concept of the SAP Cloud SDK](https://sap.github.io/cloud-sdk/docs/java/features/connectivity/destination-service) to connect to AI Core. This allows for a seamless integration in BTP and offers a wide variety of managing the credentials for the connection.

## Using a Service Binding[​](#using-a-service-binding "Direct link to Using a Service Binding")

By default, the SAP AI SDK will look for an `aicore` service binding in the environment of the application.

When running on SAP BTP, [create an instance of the AI Core service](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-service-instance) and bind it to your application. The SAP AI SDK will automatically detect the service binding and use it to connect to AI Core.

If no service binding could be found (and no other destination has been given), the SAP AI SDK will throw an exception:

> Could not find any matching service bindings for service identifier 'aicore'

To run your code outside SAP BTP (e.g. locally), you will have to provide the credentials manually.

### Providing a Service Binding Locally[​](#providing-a-service-binding-locally "Direct link to Providing a Service Binding Locally")

For local development, you can provide the service credentials locally in various ways.

#### Using CAP Hybrid Testing[​](#using-cap-hybrid-testing "Direct link to Using CAP Hybrid Testing")

When developing a [CAP application](https://cap.cloud.sap/docs/), you can use the [hybrid testing](https://cap.cloud.sap/docs/advanced/hybrid-testing#services-on-cloud-foundry) approach. Assuming your AI Core service instance is called `aicore`, the following command runs a Maven command with the credentials of the service instance:

```
cds bind --to aicore --exec mvn spring-boot:run
```

#### Using the `AICORE_SERVICE_KEY` Environment Variable[​](#using-the-aicore_service_key-environment-variable "Direct link to using-the-aicore_service_key-environment-variable")

You can also provide the service credentials in the `AICORE_SERVICE_KEY` environment variable. First, click on the SAP AI Core service instance in the SAP BTP Cockpit, press on the **View Credentials** tab on the top right corner. Copy the resulting JSON object. (JSON text copied will be used as shown in the examples in the next steps)

Then set the environment variable `AICORE_SERVICE_KEY` to be defined for however you want to run your code. How exactly to set this depends on how you run your code (e.g. via IDE, command line etc.) and potentially on your operating system.

Here are three examples of how this can be done:

1. Using a `.env` file

   Create a `.env` file in the **working directory** from which you run your code as shown in the image below. Add the copied JSON object in the file as the value of the `AICORE_SERVICE_KEY` variable as shown in the image below.

   ![AICORE\_SERVICE\_KEY environment variable in .env file](/ai-sdk/img/JSON-Object-Steps.png)

   info

   The value of `AICORE_SERVICE_KEY` must be a single line, so remove any line breaks from the service key JSON.

2. Using the command line on Mac OS

   Run your code with the following command:

   ```
   export AICORE_SERVICE_KEY='{ "clientid": "...", "clientsecret": "...", "url": "...", "serviceurls": { "AI_API_URL": "..." } }'

   mvn ...
   ```

3. Using PowerShell on Windows

   Run your code with the following command:

   ```
   $env:AICORE_SERVICE_KEY='{ "clientid": "...", "clientsecret": "...", "url": "...", "serviceurls": { "AI_API_URL": "..." } }'

   mvn ...
   ```

4. Using an IntelliJ run configuration

   In IntelliJ, go to `Run` > `Edit Configurations...` > `Environment variables`. Add a new environment variable with the name `AICORE_SERVICE_KEY` and paste the service key as value.

   For more information, see the [official IntelliJ documentation](https://www.jetbrains.com/help/idea/run-debug-configuration-application.html#configure-environment-variables).

## Using a Destination from the BTP Destination Service[​](#using-a-destination-from-the-btp-destination-service "Direct link to Using a Destination from the BTP Destination Service")

You can define a destination in the BTP Destination Service and use that to connect to AI Core.

How to create a Destination in the SAP BTP Cockpit

1. [Create a service key for your AI Core service instance](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-service-key).

2. Create a new Destination in the SAP BTP Cockpit with the following properties:

* **Name**: `my-aicore`

* **Type**: `HTTP`

* **URL**: `[serviceurls.AI_API_URL]`

* **Proxy Type**: `Internet`

* **Authentication**: `OAuth2ClientCredentials`

* **Client ID**: `[clientid]`

* **Client Secret**: `[clientsecret]`

* **Token Service URL Type**: `Dedicated`

* **Token Service URL**: `[url]/oauth/token`

  Fill in the values for URL, client ID, client secret, and token service URL from the service key JSON. Make sure to add `/oauth/token` in the token service URL.

To use the destination, ensure you have created an instance of the BTP Destination Service and bound it to your application.

tip

If you are using CAP, you can again use Hybrid Testing to bind the destination service to your application when running **locally**.

```
Destination destination = DestinationAccessor.getDestination("my-aicore").asHttp();

AiCoreService aiCoreService = new AiCoreService().withBaseDestination(destination);
```

Now you can use the `AiCoreService` as follows:

```
// To create an OpenAiClient:

var openAiDestination = aiCoreService.getInferenceDestination().forModel(OpenAiModel.TEXT_EMBEDDING_3_LARGE);

var client = OpenAiClient.withCustomDestination(openAiDestination);



// To create an OrchestrationClient:

var orchestrationDestination = aiCoreService.getInferenceDestination().forScenario("orchestration");

var client = new OrchestrationClient(orchestrationDestination);



// To create any of the com.sap.ai.sdk.core.client.* classes (e.g. DeploymentApi):

new DeploymentApi(aiCoreService);
```

info

The `destination` obtained from BTP destination service will expire once the contained OAuth2 token expires. Please run the above code for each request to ensure the destination is up-to-date. Destinations are cached by default, so this does not come with a performance penalty. To learn more, see the [SAP Cloud SDK documentation](https://sap.github.io/cloud-sdk/docs/java/features/connectivity/destination-service).

## Creating a Custom Destination[​](#creating-a-custom-destination "Direct link to Creating a Custom Destination")

If the above options are not suitable for your use case (e.g. because you are obtaining the credentials in a completely different way), you can also use a custom-built destination:

```
var destination = OAuth2DestinationBuilder

    .forTargetUrl("https://<ai-api-url>")

    .withTokenEndpoint("https://<xsuaa-url>/oauth/token")

    .withClient(new ClientCertificate("<cert>", "<key>", "<clientid>"), OnBehalfOf.TECHNICAL_USER_PROVIDER)

    .build();



AiCoreService aiCoreService = new AiCoreService().withBaseDestination(destination);
```

The above example assumes you are using a client certificate for authentication and have stored the relevant credentials somewhere. You are free to use X509 certificates (also via the Zero Trust Identity Service) or a client secret.

For more details, refer to the [SAP Cloud SDK documentation](https://sap.github.io/cloud-sdk/docs/java/features/connectivity/destination-service).
