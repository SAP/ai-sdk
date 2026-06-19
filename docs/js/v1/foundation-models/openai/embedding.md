# Embedding

Initialize the `AzureOpenAiEmbeddingClient` by following the instructions in the [Client Initialization](/ai-sdk/docs/js/v1/foundation-models.md#client-initialization) section.

Currently, the client sends request with Azure OpenAI API version `2024-10-21`. We are continuously updating the client to match the latest API specification. You can overwrite the API version by setting the `api-version` parameter in the `CustomRequestConfig` object. Refer to the [Custom Request Configuration](/ai-sdk/docs/js/v1/foundation-models.md#custom-request-configuration) section for more details.

## Making Requests[​](#making-requests "Direct link to Making Requests")

```
const response = await client.run({

  input: 'AI is fascinating'

});

const embedding = response.getEmbedding();
```
