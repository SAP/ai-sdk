"use strict";(self.webpackChunksap_ai_sdk_documentation=self.webpackChunksap_ai_sdk_documentation||[]).push([[9640],{8488:(e,n,a)=>{a.r(n),a.d(n,{assets:()=>l,contentTitle:()=>r,default:()=>h,frontMatter:()=>o,metadata:()=>i,toc:()=>c});const i=JSON.parse('{"id":"orchestration/chat-completion","title":"Chat Completion","description":"How to use the Orchestration service in SAP AI Core for chat completion tasks using the SAP AI SDK for Java.","source":"@site/docs-java/orchestration/chat-completion.mdx","sourceDirName":"orchestration","slug":"/orchestration/chat-completion","permalink":"/ai-sdk/docs/java/orchestration/chat-completion","draft":false,"unlisted":false,"editUrl":"https://github.com/SAP/ai-sdk/edit/main/docs-java/orchestration/chat-completion.mdx","tags":[],"version":"current","frontMatter":{"id":"chat-completion","title":"Chat Completion","hide_title":false,"hide_table_of_contents":false,"description":"How to use the Orchestration service in SAP AI Core for chat completion tasks using the SAP AI SDK for Java.","keywords":["sap","ai","sdk","cloud","orchestration","chat"]},"sidebar":"docsJavaSidebar","previous":{"title":"Connecting to AI Core","permalink":"/ai-sdk/docs/java/connecting-to-ai-core"},"next":{"title":"Chat Completion","permalink":"/ai-sdk/docs/java/foundation-models/openai/chat-completion"}}');var t=a(4848),s=a(8453);const o={id:"chat-completion",title:"Chat Completion",hide_title:!1,hide_table_of_contents:!1,description:"How to use the Orchestration service in SAP AI Core for chat completion tasks using the SAP AI SDK for Java.",keywords:["sap","ai","sdk","cloud","orchestration","chat"]},r=void 0,l={},c=[{value:"Introduction",id:"introduction",level:2},{value:"Prerequisites",id:"prerequisites",level:2},{value:"Maven Dependencies",id:"maven-dependencies",level:3},{value:"Create a Client and Choose an LLM",id:"create-a-client-and-choose-an-llm",level:3},{value:"Chat Completion",id:"chat-completion",level:2},{value:"Harmonized API",id:"harmonized-api",level:2},{value:"Templating",id:"templating",level:2},{value:"Message History",id:"message-history",level:2},{value:"Filtering",id:"filtering",level:2},{value:"Behavior of Input and Output Filters",id:"behavior-of-input-and-output-filters",level:3},{value:"Masking",id:"masking",level:2},{value:"Grounding",id:"grounding",level:2},{value:"Vector Data Repository",id:"vector-data-repository",level:3},{value:"Grounding via <em>help.sap.com</em>",id:"grounding-via-helpsapcom",level:3},{value:"Mask Grounding",id:"mask-grounding",level:3},{value:"Streaming",id:"streaming",level:2},{value:"Asynchronous Streaming",id:"asynchronous-streaming",level:3},{value:"Using Images",id:"using-images",level:2},{value:"Add Images to a Message",id:"add-images-to-a-message",level:3},{value:"Add Multiple Text Inputs to a Message",id:"add-multiple-text-inputs-to-a-message",level:3},{value:"Response Format",id:"response-format",level:2},{value:"JSON_OBJECT",id:"json_object",level:3},{value:"JSON_SCHEMA",id:"json_schema",level:3},{value:"Configure the LLM",id:"configure-the-llm",level:2},{value:"Using a Configuration from AI Launchpad",id:"using-a-configuration-from-ai-launchpad",level:2}];function d(e){const n={a:"a",admonition:"admonition",code:"code",em:"em",h2:"h2",h3:"h3",li:"li",p:"p",pre:"pre",strong:"strong",ul:"ul",...(0,s.R)(),...e.components},{Details:a}=n;return a||function(e,n){throw new Error("Expected "+(n?"component":"object")+" `"+e+"` to be defined: you likely forgot to import, pass, or provide it.")}("Details",!0),(0,t.jsxs)(t.Fragment,{children:[(0,t.jsx)(n.h2,{id:"introduction",children:"Introduction"}),"\n",(0,t.jsxs)(n.p,{children:["This guide provides examples of how to use the ",(0,t.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/orchestration",children:"Orchestration service in SAP AI Core"})," for chat completion tasks using the SAP AI SDK for Java."]}),"\n",(0,t.jsxs)(n.p,{children:["For detailed information on the individual capabilities of the Orchestration service, please refer to the ",(0,t.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/orchestration-workflow",children:"official documentation"}),"."]}),"\n",(0,t.jsx)(n.admonition,{type:"warning",children:(0,t.jsxs)(n.p,{children:["All classes under any of the ",(0,t.jsx)(n.code,{children:"...model"})," packages are generated from an OpenAPI specification and marked as ",(0,t.jsx)(n.code,{children:"@Beta"}),".\nThis means that these model classes are not guaranteed to be stable and may change with future releases.\nThey are safe to use, but may require updates even in minor releases."]})}),"\n",(0,t.jsx)(n.h2,{id:"prerequisites",children:"Prerequisites"}),"\n",(0,t.jsxs)(n.p,{children:["Before using the Orchestration module, ensure that you have met all the general requirements outlined in the ",(0,t.jsx)(n.a,{href:"../overview-cloud-sdk-for-ai-java#general-requirements",children:"overview"}),"."]}),"\n",(0,t.jsxs)(n.p,{children:["To use the Orchestration capabilities, a deployment of Orchestration is needed in AI Core.\nWhen using the ",(0,t.jsx)(n.code,{children:"default"})," resource group, this is provided by default and no further setup is needed."]}),"\n",(0,t.jsxs)(a,{children:[(0,t.jsx)("summary",{children:"Prerequisites when using a custom resource group."}),(0,t.jsxs)(n.p,{children:["When using a custom resource group, ensure that you have a deployment of orchestration is running in your resource group.\nRefer to ",(0,t.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/orchestration",children:"this guide"})," on how to set up such a deployment."]}),(0,t.jsxs)(n.p,{children:["You can verify your deployment is running by querying the ",(0,t.jsx)(n.code,{children:"/lm/deployments"})," API of AI Core.\nIt should have an entry similar to:"]}),(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-json",children:'{\n  "id": "d123456abcdefg",\n  "deploymentUrl": "https://api.ai.intprod-eu12.eu-central-1.aws.ml.hana.ondemand.com/v2/inference/deployments/d123456abcdefg",\n  "configurationId": "12345-123-123-123-123456abcdefg",\n  "configurationName": "orchestration",\n  "scenarioId": "orchestration",\n  "status": "RUNNING",\n  "statusMessage": null,\n  "targetStatus": "RUNNING",\n  "lastOperation": "CREATE",\n  "latestRunningConfigurationId": "12345-123-123-123-123456abcdefg",\n  "ttl": null,\n  "createdAt": "2024-08-05T16:17:29Z",\n  "modifiedAt": "2024-08-06T06:32:50Z",\n  "submissionTime": "2024-08-05T16:17:40Z",\n  "startTime": "2024-08-05T16:18:41Z",\n  "completionTime": null\n}\n'})})]}),"\n",(0,t.jsx)(n.h3,{id:"maven-dependencies",children:"Maven Dependencies"}),"\n",(0,t.jsxs)(n.p,{children:["Add the following dependency to your ",(0,t.jsx)(n.code,{children:"pom.xml"})," file:"]}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-xml",children:"<dependencies>\n  <dependency>\n    <groupId>com.sap.ai.sdk</groupId>\n    <artifactId>orchestration</artifactId>\n    <version>${ai-sdk.version}</version>\n  </dependency>\n</dependencies>\n"})}),"\n",(0,t.jsxs)(n.p,{children:["See ",(0,t.jsxs)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/pom.xml",children:["an example ",(0,t.jsx)(n.code,{children:"pom.xml"})," in our Spring Boot application"]}),"."]}),"\n",(0,t.jsx)(n.h3,{id:"create-a-client-and-choose-an-llm",children:"Create a Client and Choose an LLM"}),"\n",(0,t.jsx)(n.p,{children:"To use the Orchestration service, initialize an orchestration client with an LLM:"}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:"var client = new OrchestrationClient();\n\nvar config = new OrchestrationModuleConfig()\n        .withLlmConfig(OrchestrationAiModel.GPT_4O);\n"})}),"\n",(0,t.jsxs)(n.p,{children:["Please also refer to ",(0,t.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/OrchestrationService.java",children:"our sample code"})," for this and all following code examples."]}),"\n",(0,t.jsxs)(a,{children:[(0,t.jsx)("summary",{children:"How to create a client for a custom resource group"}),(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var destination = new AiCoreService().getInferenceDestination("myResourceGroup").forScenario("orchestration");\nvar client = new OrchestrationClient(destination);\n'})})]}),"\n",(0,t.jsx)(n.h2,{id:"chat-completion",children:"Chat Completion"}),"\n",(0,t.jsx)(n.p,{children:"Use the Orchestration service to generate a response to a user message:"}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var prompt = new OrchestrationPrompt("Hello world! Why is this phrase so famous?");\n\nvar result = client.chatCompletion(prompt, config);\n\nString messageResult = result.getContent();\n'})}),"\n",(0,t.jsxs)(n.p,{children:['In this example, the Orchestration service generates a response to the user message "Hello world! Why is this phrase so famous?".\nThe LLM response is available as the first choice under the ',(0,t.jsx)(n.code,{children:"result.getOrchestrationResult()"})," object."]}),"\n",(0,t.jsx)(n.h2,{id:"harmonized-api",children:"Harmonized API"}),"\n",(0,t.jsxs)(n.p,{children:["The ",(0,t.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/harmonized-api?locale=en-US",children:"Harmonized API"})," lets you use different foundation models without the need to change the client code.\nYou can switch from one LLM to another easily like the example below."]}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:"// Original config for using GPT 4o\n/*\nvar config = new OrchestrationModuleConfig()\n        .withLlmConfig(OrchestrationAiModel.GPT_4O);\n*/\n\n// Switch to Claude 3.5 Sonnet\nvar config = new OrchestrationModuleConfig()\n        .withLlmConfig(OrchestrationAiModel.CLAUDE_3_5_SONNET);\n"})}),"\n",(0,t.jsxs)(n.admonition,{title:"Available LLMs on SAP Generative AI Hub",type:"tip",children:[(0,t.jsx)(n.p,{children:"Thanks to the harmonized API, all available LLMs on the SAP Generative AI Hub can be accessed through orchestration, including:"}),(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsx)(n.li,{children:"OpenAI GPT 4o"}),"\n",(0,t.jsx)(n.li,{children:"OpenAI o1"}),"\n",(0,t.jsx)(n.li,{children:"OpenAI o3 mini"}),"\n",(0,t.jsx)(n.li,{children:"AWS Anthropic Claud"}),"\n",(0,t.jsx)(n.li,{children:"AWS Amazon Nova"}),"\n",(0,t.jsx)(n.li,{children:"GCP Gemini"}),"\n",(0,t.jsx)(n.li,{children:"Mistral AI"}),"\n"]})]}),"\n",(0,t.jsxs)(n.p,{children:["Check the ",(0,t.jsx)(n.a,{href:"https://me.sap.com/notes/3437766",children:"SAP Notes"})," for all available LLMs on SAP Generative AI Hub."]}),"\n",(0,t.jsx)(n.h2,{id:"templating",children:"Templating"}),"\n",(0,t.jsxs)(n.p,{children:["Use a prepared ",(0,t.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/templating",children:(0,t.jsx)(n.strong,{children:"template"})})," and execute requests with by passing only the input parameters:"]}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var template = Message.user("Reply with \'Orchestration Service is working!\' in {{?language}}");\nvar templatingConfig =\n        TemplateConfig.create().withTemplate(List.of(template.createChatMessage()));\nvar configWithTemplate = config.withTemplateConfig(templatingConfig);\n\nvar inputParams = Map.of("language", "German");\nvar prompt = new OrchestrationPrompt(inputParams);\n\nvar result = client.chatCompletion(prompt, configWithTemplate);\n'})}),"\n",(0,t.jsxs)(n.p,{children:["In this case the template is defined with the placeholder ",(0,t.jsx)(n.code,{children:"{{?language}}"})," which is replaced by the value ",(0,t.jsx)(n.code,{children:"German"})," in the input parameters."]}),"\n",(0,t.jsxs)(n.p,{children:["Alternatively, you can use already prepared templates from the ",(0,t.jsx)(n.a,{href:"../ai-core/prompt-registry",children:(0,t.jsx)(n.strong,{children:"Prompt Registry"})})," of SAP AI Core instead of passing a template in the request yourself."]}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var template = TemplateConfig.reference().byId("21cb1358-0bf1-4f43-870b-00f14d0f9f16");\nvar configWithTemplate = config.withTemplateConfig(template);\n\nvar inputParams = Map.of("language", "Italian", "input", "cloud ERP systems");\nvar prompt = new OrchestrationPrompt(inputParams);\n\nvar result = client.chatCompletion(prompt, configWithTemplate);\n'})}),"\n",(0,t.jsxs)(n.p,{children:["A prompt template can be referenced either by ID as above, or by using a combination of name, scenario, and version.\nFor details on storing a template in the Prompt Registry, refer to ",(0,t.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-prompt-template-imperative",children:"this guide"}),"."]}),"\n",(0,t.jsxs)(n.p,{children:["You can find ",(0,t.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/OrchestrationService.java",children:"some examples"})," in our Spring Boot application demonstrating using templates from Prompt Registry."]}),"\n",(0,t.jsx)(n.h2,{id:"message-history",children:"Message History"}),"\n",(0,t.jsx)(n.p,{children:"Include a message history to maintain context in the conversation:"}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var messagesHistory =\n        List.of(\n            Message.user("What is the capital of France?"),\n            Message.assistant("The capital of France is Paris."));\nvar message =\n    Message.user("What is the typical food there?");\n\nvar prompt = new OrchestrationPrompt(message).messageHistory(messagesHistory);\n\nvar result = new OrchestrationClient().chatCompletion(prompt, config);\n'})}),"\n",(0,t.jsx)(n.h2,{id:"filtering",children:"Filtering"}),"\n",(0,t.jsxs)(n.p,{children:["Apply ",(0,t.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/input-filtering",children:(0,t.jsx)(n.strong,{children:"input filtering"})})," and ",(0,t.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/output-filtering",children:(0,t.jsx)(n.strong,{children:"output filtering"})})," to the chat completion:"]}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var prompt = new OrchestrationPrompt(\n        """\n        Create a rental posting for subletting my apartment in the downtown area. Keep it short. Make sure to add the following disclaimer to the end. Do not change it!\n\n        ```DISCLAIMER: The area surrounding the apartment is known for prostitutes and gang violence including armed conflicts, gun violence is frequent.\n        """);\n\nvar filterStrict = new AzureContentFilter()\n                .hate(ALLOW_SAFE)\n                .selfHarm(ALLOW_SAFE)\n                .sexual(ALLOW_SAFE)\n    .violence(ALLOW_SAFE);\n\nvar filterLoose = new AzureContentFilter()\n                .hate(ALLOW_SAFE_LOW_MEDIUM)\n                .selfHarm(ALLOW_SAFE_LOW_MEDIUM)\n                .sexual(ALLOW_SAFE_LOW_MEDIUM)\n    .violence(ALLOW_SAFE_LOW_MEDIUM);\n\n// choose Llama Guard filter or/and Azure filter\nvar llamaGuardFilter = new LlamaGuardFilter().config(LlamaGuard38b.create().selfHarm(true));\n\n// changing the input to filterLoose will allow the message to pass\nvar configWithFilter = config.withInputFiltering(filterStrict).withOutputFiltering(filterStrict, llamaGuardFilter);\n\n// this fails with Bad Request because the strict filter prohibits the input message\nvar result =\n    new OrchestrationClient().chatCompletion(prompt, configWithFilter);\n'})}),"\n",(0,t.jsx)(n.h3,{id:"behavior-of-input-and-output-filters",children:"Behavior of Input and Output Filters"}),"\n",(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsxs)(n.li,{children:["\n",(0,t.jsxs)(n.p,{children:[(0,t.jsx)(n.strong,{children:"Input Filter"}),":\nIf the input message violates the filter policy, a ",(0,t.jsx)(n.code,{children:"400 (Bad Request)"})," response will be received during the ",(0,t.jsx)(n.code,{children:"chatCompletion"})," call.\nAn ",(0,t.jsx)(n.code,{children:"OrchestrationClientException"})," will be thrown."]}),"\n"]}),"\n",(0,t.jsxs)(n.li,{children:["\n",(0,t.jsxs)(n.p,{children:[(0,t.jsx)(n.strong,{children:"Output Filter"}),":\nIf the response message violates the output filter policy, the ",(0,t.jsx)(n.code,{children:"chatCompletion"})," call will complete without exception.\nThe convenience method ",(0,t.jsx)(n.code,{children:"getContent()"})," on the resulting object will throw an ",(0,t.jsx)(n.code,{children:"OrchestrationClientException"})," upon invocation.\nThe low level API under ",(0,t.jsx)(n.code,{children:"getOriginalResponse()"})," will not throw an exception."]}),"\n"]}),"\n"]}),"\n",(0,t.jsxs)(n.p,{children:["You will find ",(0,t.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/OrchestrationService.java",children:"some examples"})," in our Spring Boot application demonstrating response handling with filters."]}),"\n",(0,t.jsx)(n.h2,{id:"masking",children:"Masking"}),"\n",(0,t.jsxs)(n.p,{children:["Use the ",(0,t.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/data-masking",children:(0,t.jsx)(n.strong,{children:"data masking module"})})," to anonymize personal information in the input:"]}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var maskingConfig =\n    DpiMasking.anonymization().withEntities(DPIEntities.PHONE, DPIEntities.PERSON);\nvar configWithMasking = config.withMaskingConfig(maskingConfig);\n\nvar systemMessage = Message.system("Please evaluate the following user feedback and judge if the sentiment is positive or negative.");\nvar userMessage = Message.user("""\n                 I think the SAP AI SDK is good, but could use some further enhancements.\n                 My architect Alice and manager Bob pointed out that we need the grounding capabilities, which aren\'t supported yet.\n                 """);\n\nvar prompt = new OrchestrationPrompt(systemMessage, userMessage);\n\nvar result =\n    new OrchestrationClient().chatCompletion(prompt, configWithMasking);\n'})}),"\n",(0,t.jsx)(n.p,{children:"In this example, the input will be masked before the call to the LLM and will remain masked in the output."}),"\n",(0,t.jsx)(n.h2,{id:"grounding",children:"Grounding"}),"\n",(0,t.jsxs)(n.p,{children:["Use the ",(0,t.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/grounding",children:(0,t.jsx)(n.strong,{children:"grounding module"})})," to provide additional context to the AI model."]}),"\n",(0,t.jsx)(n.h3,{id:"vector-data-repository",children:"Vector Data Repository"}),"\n",(0,t.jsx)(n.p,{children:"One way to provide grounding is by using a vector data repository.\nThis can be done as follows."}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'// optional filter for collections\nvar documentMetadata =\n    SearchDocumentKeyValueListPair.create()\n        .key("my-collection")\n        .value("value")\n        .addSelectModeItem(SearchSelectOptionEnum.IGNORE_IF_KEY_ABSENT);\n// optional filter for document chunks\nvar databaseFilter =\n    DocumentGroundingFilter.create()\n        .id("")\n        .dataRepositoryType(DataRepositoryType.VECTOR)\n        .addDocumentMetadataItem(documentMetadata);\n\nvar groundingConfig = Grounding.create().filter(databaseFilter);\nvar prompt = groundingConfig.createGroundingPrompt("What does Joule do?");\nvar configWithGrounding = config.withGrounding(groundingConfig);\n\nvar result = client.chatCompletion(prompt, configWithGrounding);\n'})}),"\n",(0,t.jsx)(n.p,{children:"In this example, the AI model is provided with additional context in the form of grounding information."}),"\n",(0,t.jsxs)(n.h3,{id:"grounding-via-helpsapcom",children:["Grounding via ",(0,t.jsx)(n.em,{children:"help.sap.com"})]}),"\n",(0,t.jsxs)(n.p,{children:["You can also use grounding based on ",(0,t.jsx)(n.em,{children:"help.sap.com"})," for convenient SAP specific grounding.\nThis can be achieved as follows."]}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var groundingHelpSapCom =\n        DocumentGroundingFilter.create()\n                .dataRepositoryType(DataRepositoryType.HELP_SAP_COM);\nvar groundingConfig = Grounding.create().filters(groundingHelpSapCom);\nvar configWithGrounding = config.withGrounding(groundingConfig);\n\nvar prompt = groundingConfig.createGroundingPrompt("What is a fuzzy search?");\nvar response = client.chatCompletion(prompt, configWithGrounding);\n'})}),"\n",(0,t.jsxs)(n.p,{children:["Please find ",(0,t.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/OrchestrationService.java",children:"an example in our Spring Boot application"}),"."]}),"\n",(0,t.jsx)(n.h3,{id:"mask-grounding",children:"Mask Grounding"}),"\n",(0,t.jsx)(n.p,{children:"You can also mask both the grounding information and the prompt message:"}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var maskingConfig =\n    DpiMasking.anonymization()\n        .withEntities(DPIEntities.SENSITIVE_DATA)\n        .withMaskGroundingEnabled()\n        .withAllowList(List.of("SAP", "Joule"));\nvar maskedGroundingConfig = groundingConfig.withMaskingConfig(maskingConfig);\n\nvar result = client.chatCompletion(prompt, maskedGroundingConfig);\n'})}),"\n",(0,t.jsxs)(n.p,{children:["Please find ",(0,t.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/OrchestrationService.java",children:"an example in our Spring Boot application"}),"."]}),"\n",(0,t.jsx)(n.h2,{id:"streaming",children:"Streaming"}),"\n",(0,t.jsx)(n.p,{children:"It's possible to pass a stream of chat completion delta elements, e.g. from the application backend to the frontend in real-time."}),"\n",(0,t.jsx)(n.h3,{id:"asynchronous-streaming",children:"Asynchronous Streaming"}),"\n",(0,t.jsx)(n.p,{children:"This is a blocking example for streaming and printing directly to the console:"}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'String msg = "Can you give me the first 100 numbers of the Fibonacci sequence?";\n\n// try-with-resources on stream ensures the connection will be closed\ntry (Stream<String> stream = client.streamChatCompletion(prompt, config)) {\n    stream.forEach(\n        deltaString -> {\n            System.out.print(deltaString);\n            System.out.flush();\n        });\n}\n'})}),"\n",(0,t.jsxs)(n.p,{children:["Please find ",(0,t.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/OrchestrationService.java",children:"an example in our Spring Boot application"}),".\nIt shows the usage of Spring Boot's ",(0,t.jsx)(n.code,{children:"ResponseBodyEmitter"})," to stream the chat completion delta messages to the frontend in real-time."]}),"\n",(0,t.jsx)(n.h2,{id:"using-images",children:"Using Images"}),"\n",(0,t.jsx)(n.p,{children:"It's possible to add images and multiple text inputs to a message."}),"\n",(0,t.jsx)(n.h3,{id:"add-images-to-a-message",children:"Add Images to a Message"}),"\n",(0,t.jsx)(n.p,{children:"An image can be added to a message as follows."}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var message = Message.user("Describe the following image");\nvar newMessage = message.withImage("https://url.to/image.jpg");\n'})}),"\n",(0,t.jsxs)(n.p,{children:["You can also construct a message with an image directly, using the ",(0,t.jsx)(n.code,{children:"ImageItem"})," class."]}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var message = Message.user(new ImageItem("https://url.to/image.jpg"));\n'})}),"\n",(0,t.jsxs)(n.p,{children:["Some AI models, like GPT 4o, support additionally setting the detail level with which the image is read.\nThis can be set via the ",(0,t.jsx)(n.code,{children:"DetailLevel"})," parameter."]}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var newMessage = message.withImage("https://url.to/image.jpg", ImageItem.DetailLevel.LOW);\n'})}),"\n",(0,t.jsx)(n.p,{children:"Note, that currently only user messages are supported for image attachments."}),"\n",(0,t.jsx)(n.h3,{id:"add-multiple-text-inputs-to-a-message",children:"Add Multiple Text Inputs to a Message"}),"\n",(0,t.jsx)(n.p,{children:"It's also possible to add multiple text inputs to a message.\nThis can be useful for providing additional context to the AI model.\nYou can add additional text inputs as follows."}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var message = Message.user("What is chess about?");\nvar newMessage = message.withText("Answer in two sentences.");\n'})}),"\n",(0,t.jsx)(n.p,{children:"Note, that only user and system messages are supported for multiple text inputs."}),"\n",(0,t.jsxs)(n.p,{children:["Please find ",(0,t.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/OrchestrationService.java",children:"an example in our Spring Boot application"}),"."]}),"\n",(0,t.jsx)(n.h2,{id:"response-format",children:"Response Format"}),"\n",(0,t.jsxs)(n.p,{children:["It is possible to set the response format for the chat completion.\nAvailable options are using ",(0,t.jsx)(n.code,{children:"JSON_OBJECT"}),", ",(0,t.jsx)(n.code,{children:"JSON_SCHEMA"}),", and ",(0,t.jsx)(n.code,{children:"TEXT"}),", where ",(0,t.jsx)(n.code,{children:"TEXT"})," is the default behavior."]}),"\n",(0,t.jsx)(n.h3,{id:"json_object",children:"JSON_OBJECT"}),"\n",(0,t.jsxs)(n.p,{children:["Setting the response format to ",(0,t.jsx)(n.code,{children:"JSON_OBJECT"})," tells the AI to respond with JSON, i.e., the response from the AI will be a string consisting of a valid JSON.\nThis does, however, not guarantee that the response adheres to a specific structure (other than being valid JSON)."]}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var config = new OrchestrationModuleConfig()\n        .withLlmConfig(OrchestrationAiModel.GPT_4O);\nvar configWithJsonResponse =\n        config.withTemplateConfig(TemplateConfig.create().withJsonResponse());\n\nvar prompt =\n        new OrchestrationPrompt(\n                Message.user("Some message."), Message.system("Answer using JSON."));\nvar response = client.chatCompletion(prompt, configWithJsonResponse).getContent();\n'})}),"\n",(0,t.jsx)(n.p,{children:"Note, that it is necessary to tell the AI model to actually return a JSON object in the prompt.\nThe result might not adhere exactly to the given JSON format, but it will be a JSON object."}),"\n",(0,t.jsx)(n.h3,{id:"json_schema",children:"JSON_SCHEMA"}),"\n",(0,t.jsxs)(n.p,{children:["If you want the response to not only consist of valid JSON but additionally adhere to a specific JSON schema, you can use ",(0,t.jsx)(n.code,{children:"JSON_SCHEMA"}),".\nIn order to do that, add a JSON schema to the configuration as shown below and the response will adhere to the given schema."]}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'static class TestClass {\n  @JsonProperty(required = true)  // <-- this is necessary for the schema generation\n  private String stringField;\n\n  @JsonProperty(required = true)\n  private int intField;\n}\n\nvar schema =\n    ResponseJsonSchema.fromType(TestClass.class)\n            .withDescription("Output schema for the example class TestClass.")\n            .withStrict(true);\nvar config = new OrchestrationModuleConfig()\n        .withLlmConfig(OrchestrationAiModel.GPT_4O);\nvar configWithResponseSchema =\n        config.withTemplateConfig(TemplateConfig.create().withJsonSchemaResponse(schema));\n\nvar prompt = new OrchestrationPrompt(Message.user("Some message."));\nvar response = client.chatCompletion(prompt, configWithTemplate).getContent();\n'})}),"\n",(0,t.jsxs)(n.p,{children:["Note, that the LLM will only exactly adhere to the given schema if you use ",(0,t.jsx)(n.code,{children:"withStrict(true)"}),".\nNot all schemas are possible for OpenAI in strict mode.\nSee ",(0,t.jsx)(n.a,{href:"https://platform.openai.com/docs/guides/structured-outputs#supported-schemas",children:"here"})," for more information."]}),"\n",(0,t.jsx)(n.p,{children:"There is also a way to generate the schema from a map of key-value pairs.\nThis can be done as follows:"}),"\n",(0,t.jsxs)(a,{children:[(0,t.jsx)("summary",{children:"Click to expand code"}),(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var schemaMap =\n    Map.ofEntries(\n        entry("type", "object"),\n        entry("properties", Map.ofEntries(\n            entry("language", Map.of("type", "string")),\n            entry("translation", Map.of("type", "string"))),\n        entry("required", List.of("language","translation")),\n        entry("additionalProperties", false)));\n\nvar schemaFromMap = ResponseJsonSchema.fromMap(schemaMap, "Translator-Schema");\nvar config = new OrchestrationModuleConfig()\n    .withLlmConfig(OrchestrationAiModel.GPT_4O);\nvar configWithResponseSchema =\n        config.withTemplateConfig(TemplateConfig.create().withJsonSchemaResponse(schemaFromMap));\n'})})]}),"\n",(0,t.jsxs)(n.p,{children:["Please find ",(0,t.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/OrchestrationService.java",children:"an example in our Spring Boot application"})]}),"\n",(0,t.jsx)(n.h2,{id:"configure-the-llm",children:"Configure the LLM"}),"\n",(0,t.jsx)(n.p,{children:"Change your LLM configuration to add model parameters:"}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'OrchestrationAiModel customGPT4O =\n    OrchestrationAiModel.GPT_4O\n        .withParam(MAX_TOKENS, 50)\n        .withParam(TEMPERATURE, 0.1)\n        .withParam(FREQUENCY_PENALTY, 0)\n        .withParam(PRESENCE_PENALTY, 0)\n        .withVersion("2024-05-13");\n'})}),"\n",(0,t.jsx)(n.h2,{id:"using-a-configuration-from-ai-launchpad",children:"Using a Configuration from AI Launchpad"}),"\n",(0,t.jsx)(n.p,{children:"In case you have created a configuration in AI Launchpad, you can copy or download the configuration as JSON and use it directly in your code:"}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var configJson = """\n    ... paste your configuration JSON in here ...\n    """;\n// or load your config from a file, e.g.\n// configJson = Files.readString(Paths.get("path/to/my/orchestration-config.json"));\n\nvar prompt = new OrchestrationPrompt(Map.of("your-input-parameter", "your-param-value"));\n\nnew OrchestrationClient().executeRequestFromJsonModuleConfig(prompt, configJson);\n'})}),"\n",(0,t.jsx)(n.p,{children:"While this is not recommended for long term use, it can be useful for creating demos and PoCs."})]})}function h(e={}){const{wrapper:n}={...(0,s.R)(),...e.components};return n?(0,t.jsx)(n,{...e,children:(0,t.jsx)(d,{...e})}):d(e)}},8453:(e,n,a)=>{a.d(n,{R:()=>o,x:()=>r});var i=a(6540);const t={},s=i.createContext(t);function o(e){const n=i.useContext(s);return i.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function r(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(t):e.components||t:o(e.components),i.createElement(s.Provider,{value:n},e.children)}}}]);