"use strict";(self.webpackChunksap_ai_sdk_documentation=self.webpackChunksap_ai_sdk_documentation||[]).push([[933],{6594:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>l,contentTitle:()=>r,default:()=>h,frontMatter:()=>s,metadata:()=>i,toc:()=>c});const i=JSON.parse('{"id":"guides/spring-ai-integration","title":"Spring AI Integration","description":"How to use our Spring AI integration with our clients in SAP AI Core for chat completion tasks using the SAP AI SDK for Java.","source":"@site/docs-java/guides/spring-ai-integration.mdx","sourceDirName":"guides","slug":"/guides/spring-ai-integration","permalink":"/ai-sdk/docs/java/guides/spring-ai-integration","draft":false,"unlisted":false,"editUrl":"https://github.com/SAP/ai-sdk/edit/main/docs-java/guides/spring-ai-integration.mdx","tags":[],"version":"current","frontMatter":{"id":"spring-ai-integration","title":"Spring AI Integration","hide_title":false,"hide_table_of_contents":false,"description":"How to use our Spring AI integration with our clients in SAP AI Core for chat completion tasks using the SAP AI SDK for Java.","keywords":["sap","cloud","sdk","ai"]},"sidebar":"docsJavaSidebar","previous":{"title":"Orchestration Chat Completion","permalink":"/ai-sdk/docs/java/guides/orchestration-chat-completion"},"next":{"title":"Release Notes","permalink":"/ai-sdk/docs/java/release-notes"}}');var o=t(4848),a=t(8453);const s={id:"spring-ai-integration",title:"Spring AI Integration",hide_title:!1,hide_table_of_contents:!1,description:"How to use our Spring AI integration with our clients in SAP AI Core for chat completion tasks using the SAP AI SDK for Java.",keywords:["sap","cloud","sdk","ai"]},r=void 0,l={},c=[{value:"Table of Contents",id:"table-of-contents",level:2},{value:"Introduction",id:"introduction",level:2},{value:"Orchestration Chat Completion",id:"orchestration-chat-completion",level:2},{value:"Orchestration Masking",id:"orchestration-masking",level:2},{value:"Stream chat completion",id:"stream-chat-completion",level:2},{value:"Tool Calling",id:"tool-calling",level:2}];function p(e){const n={a:"a",admonition:"admonition",code:"code",em:"em",h2:"h2",li:"li",p:"p",pre:"pre",ul:"ul",...(0,a.R)(),...e.components};return(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)(n.h2,{id:"table-of-contents",children:"Table of Contents"}),"\n",(0,o.jsxs)(n.ul,{children:["\n",(0,o.jsx)(n.li,{children:(0,o.jsx)(n.a,{href:"#introduction",children:"Introduction"})}),"\n",(0,o.jsx)(n.li,{children:(0,o.jsx)(n.a,{href:"#orchestration-chat-completion",children:"Orchestration Chat Completion"})}),"\n",(0,o.jsx)(n.li,{children:(0,o.jsx)(n.a,{href:"#orchestration-masking",children:"Orchestration Masking"})}),"\n",(0,o.jsx)(n.li,{children:(0,o.jsx)(n.a,{href:"#stream-chat-completion",children:"Stream chat completion"})}),"\n",(0,o.jsx)(n.li,{children:(0,o.jsx)(n.a,{href:"#tool-calling",children:"Tool Calling"})}),"\n"]}),"\n",(0,o.jsx)(n.h2,{id:"introduction",children:"Introduction"}),"\n",(0,o.jsx)(n.p,{children:"This guide provides examples of how to use our Spring AI integration with our clients in SAP AI Core\nfor chat completion tasks using the SAP AI SDK for Java."}),"\n",(0,o.jsxs)(n.p,{children:["First, add the Spring AI dependency to your ",(0,o.jsx)(n.code,{children:"pom.xml"}),":"]}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-xml",children:"<dependency>\n    <groupId>org.springframework.ai</groupId>\n    <artifactId>spring-ai-core</artifactId>\n    <version>1.0.0-M5</version>\n</dependency>\n...\n<repository>\n    <snapshots>\n        <enabled>true</enabled>\n    </snapshots>\n    <id>spring-milestones</id>\n    <name>Spring Milestones</name>\n    <url>https://repo.spring.io/milestone</url>\n</repository>\n"})}),"\n",(0,o.jsxs)(n.admonition,{title:"Spring AI Milestone Version",type:"note",children:[(0,o.jsxs)(n.p,{children:["Note that currently no stable version of Spring AI exists just yet.\nThe AI SDK currently uses the ",(0,o.jsx)(n.a,{href:"https://spring.io/blog/2025/02/14/spring-ai-1-0-0-m6-released",children:"M6 milestone"}),"."]}),(0,o.jsx)(n.p,{children:"Please be aware that future versions of the AI SDK may increase the Spring AI version."})]}),"\n",(0,o.jsx)(n.h2,{id:"orchestration-chat-completion",children:"Orchestration Chat Completion"}),"\n",(0,o.jsx)(n.p,{children:"The Orchestration client is integrated in Spring AI classes:"}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:'ChatModel client = new OrchestrationChatModel();\nOrchestrationModuleConfig config = new OrchestrationModuleConfig().withLlmConfig(GPT_35_TURBO);\nOrchestrationChatOptions opts = new OrchestrationChatOptions(config);\n\nPrompt prompt = new Prompt("What is the capital of France?", opts);\nChatResponse response = client.call(prompt);\n'})}),"\n",(0,o.jsxs)(n.p,{children:["Please find ",(0,o.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/SpringAiOrchestrationService.java",children:"an example in our Spring Boot application"}),"."]}),"\n",(0,o.jsx)(n.h2,{id:"orchestration-masking",children:"Orchestration Masking"}),"\n",(0,o.jsx)(n.p,{children:"Configure Orchestration modules withing Spring AI:"}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:"ChatModel client = new OrchestrationChatModel();\nOrchestrationModuleConfig config = new OrchestrationModuleConfig().withLlmConfig(GPT_35_TURBO);\n\nval masking =\n    DpiMasking.anonymization()\n        .withEntities(DPIEntities.EMAIL, DPIEntities.ADDRESS, DPIEntities.LOCATION);\n\nval opts = new OrchestrationChatOptions(config.withMaskingConfig(masking));\nval prompt =\n    new Prompt(\n        \"Please write 'Hello World!' to me via email. My email address is foo.bar@baz.ai\",\n        opts);\n\nChatResponse response = client.call(prompt);\n"})}),"\n",(0,o.jsxs)(n.p,{children:["Please\nfind ",(0,o.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/SpringAiOrchestrationService.java",children:"an example in our Spring Boot application"}),"."]}),"\n",(0,o.jsx)(n.h2,{id:"stream-chat-completion",children:"Stream chat completion"}),"\n",(0,o.jsx)(n.p,{children:"It's possible to pass a stream of chat completion delta elements, e.g. from the application backend\nto the frontend in real-time."}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:'ChatModel client = new OrchestrationChatModel();\nOrchestrationModuleConfig config = new OrchestrationModuleConfig().withLlmConfig(GPT_35_TURBO);\nOrchestrationChatOptions opts = new OrchestrationChatOptions(config);\n\nPrompt prompt =\n    new Prompt(\n        "Can you give me the first 100 numbers of the Fibonacci sequence?", opts);\nFlux<ChatResponse> flux = client.stream(prompt);\n\n// also possible to keep only the chat completion text\nFlux<String> responseFlux =\n    flux.map(chatResponse -> chatResponse.getResult().getOutput().getContent());\n'})}),"\n",(0,o.jsx)(n.p,{children:(0,o.jsxs)(n.em,{children:["Note: A Spring endpoint can return ",(0,o.jsx)(n.code,{children:"Flux"})," instead of ",(0,o.jsx)(n.code,{children:"ResponseEntity"}),"."]})}),"\n",(0,o.jsxs)(n.p,{children:["Please find ",(0,o.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/SpringAiOrchestrationService.java",children:"an example in our Spring Boot application"}),"."]}),"\n",(0,o.jsx)(n.h2,{id:"tool-calling",children:"Tool Calling"}),"\n",(0,o.jsx)(n.p,{children:"First define a function that will be called by the LLM:"}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:'class WeatherMethod {\n  enum Unit {C,F}\n  record Request(String location, Unit unit) {}\n  record Response(double temp, Unit unit) {}\n\n  @Tool(description = "Get the weather in location")\n  Response getCurrentWeather(@ToolParam Request request) {\n    int temperature = request.location.hashCode() % 30;\n    return new Response(temperature, request.unit);\n  }\n}\n'})}),"\n",(0,o.jsx)(n.p,{children:"Then add your tool to the options:"}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-java",children:'ChatModel client = new OrchestrationChatModel();\nOrchestrationModuleConfig config = new OrchestrationModuleConfig().withLlmConfig(GPT_35_TURBO);\nOrchestrationChatOptions opts = new OrchestrationChatOptions(config);\n\noptions.setToolCallbacks(List.of(ToolCallbacks.from(new WeatherMethod())));\n\noptions.setInternalToolExecutionEnabled(false);// tool execution is not yet available in orchestration\n\nPrompt prompt = new Prompt("What is the weather in Potsdam and in Toulouse?", options);\n\nChatResponse response = client.call(prompt);\n'})}),"\n",(0,o.jsxs)(n.p,{children:["Please find ",(0,o.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/SpringAiOrchestrationService.java",children:"an example in our Spring Boot application"}),"."]})]})}function h(e={}){const{wrapper:n}={...(0,a.R)(),...e.components};return n?(0,o.jsx)(n,{...e,children:(0,o.jsx)(p,{...e})}):p(e)}},8453:(e,n,t)=>{t.d(n,{R:()=>s,x:()=>r});var i=t(6540);const o={},a=i.createContext(o);function s(e){const n=i.useContext(a);return i.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function r(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(o):e.components||o:s(e.components),i.createElement(a.Provider,{value:n},e.children)}}}]);