"use strict";(self.webpackChunksap_ai_sdk_documentation=self.webpackChunksap_ai_sdk_documentation||[]).push([[227],{4709:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>l,contentTitle:()=>r,default:()=>h,frontMatter:()=>i,metadata:()=>s,toc:()=>c});const s=JSON.parse('{"id":"foundation-models/openai/chat-completion","title":"Chat Completion","description":"How to use the SAP AI SDK for Java to perform chat completion tasks using OpenAI models deployed on SAP AI Core.","source":"@site/docs-java/foundation-models/openai/chat-completion.mdx","sourceDirName":"foundation-models/openai","slug":"/foundation-models/openai/chat-completion","permalink":"/ai-sdk/docs/java/foundation-models/openai/chat-completion","draft":false,"unlisted":false,"editUrl":"https://github.com/SAP/ai-sdk/edit/main/docs-java/foundation-models/openai/chat-completion.mdx","tags":[],"version":"current","frontMatter":{"id":"chat-completion","title":"Chat Completion","hide_title":false,"hide_table_of_contents":false,"description":"How to use the SAP AI SDK for Java to perform chat completion tasks using OpenAI models deployed on SAP AI Core.","keywords":["sap","cloud","sdk","ai"]},"sidebar":"docsJavaSidebar","previous":{"title":"Chat Completion","permalink":"/ai-sdk/docs/java/orchestration/chat-completion"},"next":{"title":"Embedding","permalink":"/ai-sdk/docs/java/foundation-models/openai/embedding"}}');var o=t(4848),a=t(8453);const i={id:"chat-completion",title:"Chat Completion",hide_title:!1,hide_table_of_contents:!1,description:"How to use the SAP AI SDK for Java to perform chat completion tasks using OpenAI models deployed on SAP AI Core.",keywords:["sap","cloud","sdk","ai"]},r=void 0,l={},c=[{value:"Introduction",id:"introduction",level:2},{value:"Prerequisites",id:"prerequisites",level:2},{value:"Maven Dependencies",id:"maven-dependencies",level:3},{value:"Usage",id:"usage",level:2},{value:"Simple chat completion",id:"simple-chat-completion",level:2},{value:"Using a Custom Resource Group",id:"using-a-custom-resource-group",level:2},{value:"Message history",id:"message-history",level:2},{value:"Chat Completion with Specific Model Version",id:"chat-completion-with-specific-model-version",level:2},{value:"Chat completion with Custom Model",id:"chat-completion-with-custom-model",level:2},{value:"Stream chat completion",id:"stream-chat-completion",level:2},{value:"Asynchronous Streaming - Blocking",id:"asynchronous-streaming---blocking",level:3},{value:"Asynchronous Streaming - Non-blocking",id:"asynchronous-streaming---non-blocking",level:3},{value:"Executing Tool Calls",id:"executing-tool-calls",level:2}];function d(e){const n={a:"a",admonition:"admonition",code:"code",h2:"h2",h3:"h3",li:"li",p:"p",pre:"pre",strong:"strong",ul:"ul",...(0,a.R)(),...e.components},{Details:t}=n;return t||function(e,n){throw new Error("Expected "+(n?"component":"object")+" `"+e+"` to be defined: you likely forgot to import, pass, or provide it.")}("Details",!0),(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)(n.h2,{id:"introduction",children:"Introduction"}),"\n",(0,o.jsx)(n.p,{children:"This guide demonstrates how to use the SAP AI SDK for Java to perform chat completion tasks using OpenAI models deployed on SAP AI Core."}),"\n",(0,o.jsx)(n.admonition,{type:"warning",children:(0,o.jsxs)(n.p,{children:["All classes under any of the ",(0,o.jsx)(n.code,{children:"...model"})," packages are generated from an OpenAPI specification and marked as ",(0,o.jsx)(n.code,{children:"@Beta"}),".\nThis means that these model classes are not guaranteed to be stable and may change with future releases.\nThey are safe to use, but may require updates even in minor releases."]})}),"\n",(0,o.jsxs)(t,{children:[(0,o.jsx)("summary",{children:"New User Interface (v1.4.0)"}),(0,o.jsxs)(n.p,{children:["We're excited to introduce a new user interface for OpenAI chat completions starting with ",(0,o.jsx)(n.strong,{children:"version 1.4.0"}),". This update is designed to improve the SAP AI SDK by:"]}),(0,o.jsxs)(n.ul,{children:["\n",(0,o.jsxs)(n.li,{children:[(0,o.jsx)(n.strong,{children:"Decoupling Layers:"})," Separating the convenience layer from the model classes to deliver a more stable and maintainable experience."]}),"\n",(0,o.jsxs)(n.li,{children:[(0,o.jsx)(n.strong,{children:"Staying Current:"})," Making it easier for the SAP AI SDK to adapt to the latest changes in the OpenAI API specification."]}),"\n",(0,o.jsxs)(n.li,{children:[(0,o.jsx)(n.strong,{children:"Consistent Design:"})," Aligning with the Orchestrator convenience API for a smoother transition and easier adoption."]}),"\n"]}),(0,o.jsx)(n.p,{children:(0,o.jsx)(n.strong,{children:"Please Note:"})}),(0,o.jsxs)(n.ul,{children:["\n",(0,o.jsx)(n.li,{children:"The new interface is gradually being rolled out across the SAP AI SDK."}),"\n",(0,o.jsx)(n.li,{children:"We welcome your feedback to help us refine this interface."}),"\n",(0,o.jsx)(n.li,{children:"The existing interface (v1.0.0) remains available for compatibility."}),"\n"]})]}),"\n",(0,o.jsx)(n.h2,{id:"prerequisites",children:"Prerequisites"}),"\n",(0,o.jsxs)(n.p,{children:["Before using the AI Core module, ensure that you have met all the general requirements outlined in the ",(0,o.jsx)(n.a,{href:"../../overview-cloud-sdk-for-ai-java#general-requirements",children:"overview"}),".\nAdditionally, include the necessary Maven dependency in your project."]}),"\n",(0,o.jsx)(n.h3,{id:"maven-dependencies",children:"Maven Dependencies"}),"\n",(0,o.jsxs)(n.p,{children:["Add the following dependency to your ",(0,o.jsx)(n.code,{children:"pom.xml"})," file:"]}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-xml",children:"<dependencies>\n    <dependency>\n        <groupId>com.sap.ai.sdk.foundationmodels</groupId>\n        <artifactId>openai</artifactId>\n        <version>${ai-sdk.version}</version>\n    </dependency>\n</dependencies>\n"})}),"\n",(0,o.jsxs)(n.p,{children:["See ",(0,o.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/pom.xml",children:"an example pom in our Spring Boot application"})]}),"\n",(0,o.jsx)(n.h2,{id:"usage",children:"Usage"}),"\n",(0,o.jsx)(n.p,{children:"In addition to the prerequisites above, we assume you have already set up the following to carry out the examples in this guide:"}),"\n",(0,o.jsxs)(n.ul,{children:["\n",(0,o.jsxs)(n.li,{children:["\n",(0,o.jsx)(n.p,{children:(0,o.jsx)(n.strong,{children:"A Deployed OpenAI Model in SAP AI Core"})}),"\n",(0,o.jsxs)(n.ul,{children:["\n",(0,o.jsxs)(n.li,{children:["\n",(0,o.jsxs)(n.p,{children:["Refer\nto ",(0,o.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-deployment-for-generative-ai-model-in-sap-ai-core",children:"How to deploy a model to AI Core"}),"\nfor setup instructions."]}),"\n"]}),"\n",(0,o.jsxs)(n.li,{children:["\n",(0,o.jsxs)(n.p,{children:["In case the model is deployed in a custom resource group, refer to ",(0,o.jsx)(n.a,{href:"#using-a-custom-resource-group",children:"this section"}),"."]}),"\n"]}),"\n",(0,o.jsxs)(n.li,{children:["\n",(0,o.jsxs)(t,{children:[(0,o.jsxs)("summary",{children:["Example deployed model from the AI Core ",(0,o.jsx)("code",{children:"/deployments"})," endpoint"]}),(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-json",children:'{\n  "id": "d123456abcdefg",\n  "deploymentUrl": "https://api.ai.region.aws.ml.hana.ondemand.com/v2/inference/deployments/d123456abcdefg",\n  "configurationId": "12345-123-123-123-123456abcdefg",\n  "configurationName": "gpt-4o-mini",\n  "scenarioId": "foundation-models",\n  "status": "RUNNING",\n  "statusMessage": null,\n  "targetStatus": "RUNNING",\n  "lastOperation": "CREATE",\n  "latestRunningConfigurationId": "12345-123-123-123-123456abcdefg",\n  "ttl": null,\n  "details": {\n    "scaling": {\n      "backendDetails": {}\n    },\n    "resources": {\n      "backendDetails": {\n        "model": {\n          "name": "gpt-4o-mini",\n          "version": "latest"\n        }\n      }\n    }\n  },\n  "createdAt": "2024-07-03T12:44:22Z",\n  "modifiedAt": "2024-07-16T12:44:19Z",\n  "submissionTime": "2024-07-03T12:44:51Z",\n  "startTime": "2024-07-03T12:45:56Z",\n  "completionTime": null\n}\n'})})]}),"\n"]}),"\n"]}),"\n"]}),"\n"]}),"\n",(0,o.jsx)(n.h2,{id:"simple-chat-completion",children:"Simple chat completion"}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:'var result =\n    OpenAiClient.forModel(GPT_4O_MINI)\n        .withSystemPrompt("You are a helpful AI")\n        .chatCompletion("Hello World! Why is this phrase so famous?");\n\nString resultMessage = result.getContent();\n'})}),"\n",(0,o.jsx)(n.h2,{id:"using-a-custom-resource-group",children:"Using a Custom Resource Group"}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:'var destination = new AiCoreService()\n    .getInferenceDestination("custom-rg")\n    .forModel(GPT_4O);\nOpenAiClient.withCustomDestination(destination);\n'})}),"\n",(0,o.jsx)(n.h2,{id:"message-history",children:"Message history"}),"\n",(0,o.jsx)(n.p,{children:(0,o.jsx)(n.strong,{children:"Since v1.4.0"})}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:'var request =\n    new OpenAiChatCompletionRequest(\n        OpenAiMessage.system("You are a helpful assistant"),\n        OpenAiMessage.user("Hello World! Why is this phrase so famous?"));\n\nvar response = OpenAiClient.forModel(GPT_4O).chatCompletion(request).getContent();\n'})}),"\n",(0,o.jsxs)(t,{children:[(0,o.jsx)("summary",{children:(0,o.jsx)("b",{children:"Since v1.0.0"})}),(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:'var systemMessage =\n    new OpenAiChatSystemMessage().setContent("You are a helpful assistant");\nvar userMessage =\n    new OpenAiChatUserMessage().addText("Hello World! Why is this phrase so famous?");\nvar request =\n    new OpenAiChatCompletionParameters().addMessages(systemMessage, userMessage);\n\nvar result = OpenAiClient.forModel(GPT_4O_MINI).chatCompletion(request);\n\nString resultMessage = result.getContent();\n'})}),(0,o.jsxs)(n.p,{children:["See ",(0,o.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/OpenAiService.java",children:"an example in our Spring Boot application"})]})]}),"\n",(0,o.jsx)(n.h2,{id:"chat-completion-with-specific-model-version",children:"Chat Completion with Specific Model Version"}),"\n",(0,o.jsx)(n.p,{children:"By default, when no version is specified, the system selects one of the available deployments of the specified model, regardless of its version.\nTo target a specific version, you can specify the model version along with the model."}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:'OpenAiChatCompletionOutput result =\n    OpenAiClient.forModel(GPT_4O_MINI.withVersion("1106")).chatCompletion(request);\n'})}),"\n",(0,o.jsx)(n.h2,{id:"chat-completion-with-custom-model",children:"Chat completion with Custom Model"}),"\n",(0,o.jsxs)(n.p,{children:["You can also use a custom OpenAI model for chat completion by creating an ",(0,o.jsx)(n.code,{children:"OpenAiModel"})," object."]}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:'OpenAiChatCompletionOutput result =\n    OpenAiClient.forModel(new OpenAiModel("custom-model", "v1")).chatCompletion(request);\n'})}),"\n",(0,o.jsx)(n.p,{children:"Ensure that the custom model is deployed in SAP AI Core."}),"\n",(0,o.jsx)(n.h2,{id:"stream-chat-completion",children:"Stream chat completion"}),"\n",(0,o.jsx)(n.p,{children:"It's possible to pass a stream of chat completion delta elements, e.g. from the application backend to the frontend in real-time."}),"\n",(0,o.jsx)(n.h3,{id:"asynchronous-streaming---blocking",children:"Asynchronous Streaming - Blocking"}),"\n",(0,o.jsx)(n.p,{children:"This is a blocking example for streaming and printing directly to the console:"}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:'String msg = "Can you give me the first 100 numbers of the Fibonacci sequence?";\n\nOpenAiClient client = OpenAiClient.forModel(GPT_4O_MINI);\n\n// try-with-resources on stream ensures the connection will be closed\ntry (Stream<String> stream = client.streamChatCompletion(msg)) {\n    stream.forEach(\n        deltaString -> {\n            System.out.print(deltaString);\n            System.out.flush();\n        });\n}\n'})}),"\n",(0,o.jsx)(n.h3,{id:"asynchronous-streaming---non-blocking",children:"Asynchronous Streaming - Non-blocking"}),"\n",(0,o.jsx)(n.p,{children:(0,o.jsx)(n.strong,{children:"Since v1.4.0"})}),"\n",(0,o.jsx)(n.p,{children:'The following example demonstrate how you can leverage a concurrency-safe container (like an AtomicReference) to "listen" for usage information in any incoming delta.'}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:'String question = "Can you give me the first 100 numbers of the Fibonacci sequence?";\nvar userMessage = OpenAiMessage.user(question);\nvar request = new OpenAiChatCompletionRequest(userMessage);\n\nOpenAiClient client = OpenAiClient.forModel(GPT_4O);\nvar usageRef = new AtomicReference<CompletionUsage>();\n\n// Prepare the stream before starting the thread to handle any initialization exceptions\nStream<OpenAiChatCompletionDelta> stream = client.streamChatCompletionDeltas(request);\n\n// Create a new thread for asynchronous, non-blocking processing\nThread streamProcessor =\n    new Thread(\n        () -> {\n            // try-with-resources ensures the stream is closed after processing\n            try (stream) {\n                stream.forEach(\n                    delta -> {\n                        usageRef.compareAndExchange(null, delta.getCompletionUsage());\n                        System.out.println("Content: " + delta.getDeltaContent());\n                    });\n            }\n        });\n\n// Start the processing thread; the main thread remains free (non-blocking)\nstreamProcessor.start();\n// Wait for the thread to finish (blocking)\nstreamProcessor.join();\n\n// Access information caught from completion usage\nInteger tokensUsed = usageRef.get().getCompletionTokens();\nSystem.out.println("Tokens used: " + tokensUsed);\n'})}),"\n",(0,o.jsxs)(t,{children:[(0,o.jsx)("summary",{children:(0,o.jsx)("b",{children:"Since v1.0.0"})}),(0,o.jsx)(n.p,{children:"The following example is non-blocking and demonstrates how to aggregate the complete response.\nAny asynchronous library can be used, such as the classic Thread API."}),(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:'var question = "Can you give me the first 100 numbers of the Fibonacci sequence?";\n\nvar userMessage =\n    new OpenAiChatMessage.OpenAiChatUserMessage().addText(question);\nvar requestParameters =\n    new OpenAiChatCompletionParameters().addMessages(userMessage);\n\nvar client = OpenAiClient.forModel(GPT_4O_MINI);\nvar totalOutput = new OpenAiChatCompletionOutput();\n\n// Prepare the stream before starting the thread to handle any initialization exceptions\nStream<OpenAiChatCompletionDelta> stream =\n    client.streamChatCompletionDeltas(requestParameters);\n\nvar streamProcessor =\n    new Thread(\n        () -> {\n          // try-with-resources ensures the stream is closed after processing\n          try (stream) {\n            stream.peek(totalOutput::addDelta).forEach(System.out::println);\n          }\n        });\n\nstreamProcessor.start(); // Start processing in a separate thread (non-blocking)\nstreamProcessor.join(); // Wait for the thread to finish (blocking)\n\n// Access aggregated information from total output\nInteger tokensUsed = totalOutput.getUsage().getCompletionTokens();\nSystem.out.println("Tokens used: " + tokensUsed);\n'})}),(0,o.jsxs)(n.p,{children:["Please find ",(0,o.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/OpenAiService.java",children:"an example in our Spring Boot application"}),". It shows the usage of Spring\nBoot's ",(0,o.jsx)(n.code,{children:"ResponseBodyEmitter"})," to stream the chat completion delta messages to the frontend in real-time."]})]}),"\n",(0,o.jsx)(n.h2,{id:"executing-tool-calls",children:"Executing Tool Calls"}),"\n",(0,o.jsx)(n.p,{children:(0,o.jsx)(n.strong,{children:"Since v1.6.0"})}),"\n",(0,o.jsxs)(n.p,{children:["You can pass ",(0,o.jsx)(n.a,{href:"https://platform.openai.com/docs/guides/function-calling?api-mode=chat#overview",children:"tool definitions"})," to the model to enable tool calling."]}),"\n",(0,o.jsxs)(n.p,{children:["Below is a ",(0,o.jsxs)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/WeatherMethod.java",children:["sample tool named ",(0,o.jsx)(n.code,{children:"WeatherMethod"})]})," with parameters location and temperature unit."]}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:"class WeatherMethod {\n  enum Unit {C,F}\n  record Request(String location, Unit unit) {}\n  record Response(double temp, Unit unit) {}\n\n  static Response getCurrentWeather(Request request) {\n    int temperature = request.location.hashCode() % 30;\n    return new Response(temperature, request.unit);\n  }\n}\n"})}),"\n",(0,o.jsx)(n.p,{children:"You can define the function and pass it to the model as follows."}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:'var question = "What\'s the weather in Berlin in Celsius";\n\n // 1. Define the function\n // Find generateSchema in the sample application\nMap<String, Object> schemaMap = generateSchema(WeatherMethod.Request.class);\nvar function =\n    new FunctionObject()\n        .name("weather")\n        .description("Get the weather for the given location")\n        .parameters(schemaMap);\nvar tool = new ChatCompletionTool().type(FUNCTION).function(function);\n\nvar messages = new ArrayList<OpenAiMessage>();\nmessages.add(OpenAiMessage.user(question));\n\n// Assistant will call the function\nvar request = new OpenAiChatCompletionRequest(messages).withTools(List.of(tool));\nOpenAiChatCompletionResponse response =\n    OpenAiClient.forModel(GPT_4O_MINI).chatCompletion(request);\n'})}),"\n",(0,o.jsx)(n.p,{children:"Optionally, you can execute the tool call and request the LLM to format the result in a user-friendly way."}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:'OpenAiAssistantMessage assistantMessage = response.getMessage();\nmessages.add(assistantMessage);\n\nOpenAiToolCall toolCall = assistantMessage.toolCalls().get(0);\nif (!(toolCall instanceof OpenAiFunctionCall functionCall)) {\n  throw new IllegalArgumentException(\n      "Expected a function call, but got: %s".formatted(assistantMessage));\n}\n\n// Find parseJson is in the sample application\nWeatherMethod.Request arguments =\n    parseJson(functionCall.getArguments(), WeatherMethod.Request.class);\nWeatherMethod.Response weatherMethod = WeatherMethod.getCurrentWeather(arguments);\n\nmessages.add(OpenAiMessage.tool(weatherMethod.toString(), functionCall.getId()));\n\n// Send back the results, and the model will incorporate them into its final response.\nOpenAiChatCompletionResponse finalResponse =\n    OpenAiClient.forModel(GPT_4O_MINI).chatCompletion(request.withMessages(messages));\n\nString content = finalResponse.getContent();\n'})}),"\n",(0,o.jsxs)(n.p,{children:["Please find more to the example in ",(0,o.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/OpenAiServiceV2.java",children:"the sample application"})," including the definition for ",(0,o.jsx)(n.code,{children:"generateSchema"})," and ",(0,o.jsx)(n.code,{children:"parseJson"}),"."]})]})}function h(e={}){const{wrapper:n}={...(0,a.R)(),...e.components};return n?(0,o.jsx)(n,{...e,children:(0,o.jsx)(d,{...e})}):d(e)}},8453:(e,n,t)=>{t.d(n,{R:()=>i,x:()=>r});var s=t(6540);const o={},a=s.createContext(o);function i(e){const n=s.useContext(a);return s.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function r(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(o):e.components||o:i(e.components),s.createElement(a.Provider,{value:n},e.children)}}}]);