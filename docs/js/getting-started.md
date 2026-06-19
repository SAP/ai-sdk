# Getting Started

### What You'll Build[​](#what-youll-build "Direct link to What You'll Build")

In this quickstart, you'll use the OpenAI GPT-5 model via the [Orchestration Service of AI Core](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/orchestration) to generate text. The application will send a prompt to the AI model and display the generated response.

### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

Refer to prerequisites outlined [here](/ai-sdk/docs/js/overview-cloud-sdk-for-ai-js.md#prerequisites).

This quickstart assumes you are using the `default` resource group of your AI Core instance. If you need to [use a different resource group](/ai-sdk/docs/js/orchestration/chat-completion.md#custom-deployment-configuration), make sure it has an [orchestration deployment](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-deployment-for-orchestration) available.

### Add `@sap-ai-sdk/orchestration` as a Dependency[​](#add-sap-ai-sdkorchestration-as-a-dependency "Direct link to add-sap-ai-sdkorchestration-as-a-dependency")

```
npm install @sap-ai-sdk/orchestration
```

### Use the Orchestration API[​](#use-the-orchestration-api "Direct link to Use the Orchestration API")

Initialize an orchestration client with an LLM model and a prompt template.

```
import { OrchestrationClient } from '@sap-ai-sdk/orchestration';



const orchestrationClient = new OrchestrationClient({

  promptTemplating: {

    model: {

      name: 'gpt-5'

    },

    prompt: {

      template: [

        { role: 'user', content: 'Answer the question: {{?question}}' }

      ]

    }

  }

});
```

Next, send a chat completion request with a value defined for the `question` input parameter. The value replaces the `{{?question}}` placeholder in the template.

```
const response = await orchestrationClient.chatCompletion({

  placeholderValues: {

    question: 'Why is the phrase "Hello world!" so famous?'

  }

});

console.log(response.getContent());
```

Use `getContent()` method to get the generated text.

### Run the Application Locally[​](#run-the-application-locally "Direct link to Run the Application Locally")

Define the `AICORE_SERVICE_KEY` environment variable with your AI Core service key in a `.env` file.

```
AICORE_SERVICE_KEY='{

  "clientid": "...",

  ...

}'
```

Load the `.env` file by using [dotenv](https://www.npmjs.com/package/dotenv) or running `node --env-file=.env ...`.

Refer to [Providing a Service Binding Locally](/ai-sdk/docs/js/connecting-to-ai-core.md#providing-a-service-binding-locally) section for more information.
