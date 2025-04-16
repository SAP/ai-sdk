"use strict";(self.webpackChunksap_ai_sdk_documentation=self.webpackChunksap_ai_sdk_documentation||[]).push([[2473],{8453:(e,n,i)=>{i.d(n,{R:()=>d,x:()=>a});var s=i(6540);const t={},o=s.createContext(t);function d(e){const n=s.useContext(o);return s.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function a(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(t):e.components||t:d(e.components),s.createElement(o.Provider,{value:n},e.children)}},9529:(e,n,i)=>{i.r(n),i.d(n,{assets:()=>r,contentTitle:()=>a,default:()=>p,frontMatter:()=>d,metadata:()=>s,toc:()=>l});const s=JSON.parse('{"id":"foundation-models/openai/embedding","title":"Embedding","description":"How to use the SAP AI SDK for Java to perform embedding tasks using OpenAI models deployed on SAP AI Core.","source":"@site/docs-java/foundation-models/openai/embedding.mdx","sourceDirName":"foundation-models/openai","slug":"/foundation-models/openai/embedding","permalink":"/ai-sdk/docs/java/foundation-models/openai/embedding","draft":false,"unlisted":false,"editUrl":"https://github.com/SAP/ai-sdk/edit/main/docs-java/foundation-models/openai/embedding.mdx","tags":[],"version":"current","frontMatter":{"id":"embedding","title":"Embedding","hide_title":false,"hide_table_of_contents":false,"description":"How to use the SAP AI SDK for Java to perform embedding tasks using OpenAI models deployed on SAP AI Core.","keywords":["sap","cloud","sdk","ai"]},"sidebar":"docsJavaSidebar","previous":{"title":"Chat Completion","permalink":"/ai-sdk/docs/java/foundation-models/openai/chat-completion"},"next":{"title":"Orchestration Integration","permalink":"/ai-sdk/docs/java/spring-ai/orchestration"}}');var t=i(4848),o=i(8453);const d={id:"embedding",title:"Embedding",hide_title:!1,hide_table_of_contents:!1,description:"How to use the SAP AI SDK for Java to perform embedding tasks using OpenAI models deployed on SAP AI Core.",keywords:["sap","cloud","sdk","ai"]},a=void 0,r={},l=[{value:"Introduction",id:"introduction",level:2},{value:"Prerequisites",id:"prerequisites",level:2},{value:"Maven Dependencies",id:"maven-dependencies",level:3},{value:"Usage",id:"usage",level:2},{value:"Embedding",id:"embedding",level:2}];function c(e){const n={a:"a",admonition:"admonition",code:"code",h2:"h2",h3:"h3",li:"li",p:"p",pre:"pre",strong:"strong",ul:"ul",...(0,o.R)(),...e.components},{Details:i}=n;return i||function(e,n){throw new Error("Expected "+(n?"component":"object")+" `"+e+"` to be defined: you likely forgot to import, pass, or provide it.")}("Details",!0),(0,t.jsxs)(t.Fragment,{children:[(0,t.jsx)(n.h2,{id:"introduction",children:"Introduction"}),"\n",(0,t.jsx)(n.p,{children:"This guide demonstrates how to use the SAP AI SDK for Java to perform embedding tasks using OpenAI models deployed on SAP AI Core."}),"\n",(0,t.jsx)(n.admonition,{type:"warning",children:(0,t.jsxs)(n.p,{children:["All classes under any of the ",(0,t.jsx)(n.code,{children:"...model"})," packages are generated from an OpenAPI specification.\nThis means that these model classes are not guaranteed to be stable and may change with future releases.\nThey are safe to use, but may require updates even in minor releases."]})}),"\n",(0,t.jsxs)(i,{children:[(0,t.jsx)("summary",{children:"New User Interface (v1.4.0)"}),(0,t.jsxs)(n.p,{children:["We're excited to introduce a new user interface for OpenAI embedding calls starting with ",(0,t.jsx)(n.strong,{children:"version 1.4.0"}),". This update is designed to improve the SAP AI SDK by:"]}),(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsxs)(n.li,{children:[(0,t.jsx)(n.strong,{children:"Decoupling Layers:"})," Separating the convenience layer from the model classes to deliver a more stable and maintainable experience."]}),"\n",(0,t.jsxs)(n.li,{children:[(0,t.jsx)(n.strong,{children:"Staying Current:"})," Making it easier for the SAP AI SDK to adapt to the latest changes in the OpenAI API specification."]}),"\n",(0,t.jsxs)(n.li,{children:[(0,t.jsx)(n.strong,{children:"Consistent Design:"})," Aligning with the Orchestrator convenience API for a smoother transition and easier adoption."]}),"\n"]}),(0,t.jsx)(n.p,{children:(0,t.jsx)(n.strong,{children:"Please Note:"})}),(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsx)(n.li,{children:"The new interface is gradually being rolled out across the SAP AI SDK."}),"\n",(0,t.jsx)(n.li,{children:"We welcome your feedback to help us refine this interface."}),"\n",(0,t.jsx)(n.li,{children:"The existing interface (v1.0.0) is deprecated but available."}),"\n"]})]}),"\n",(0,t.jsx)(n.h2,{id:"prerequisites",children:"Prerequisites"}),"\n",(0,t.jsxs)(n.p,{children:["Before using the AI Core module, ensure that you have met all the general requirements outlined in the ",(0,t.jsx)(n.a,{href:"../../overview-cloud-sdk-for-ai-java#general-requirements",children:"overview"}),".\nAdditionally, include the necessary Maven dependency in your project."]}),"\n",(0,t.jsx)(n.h3,{id:"maven-dependencies",children:"Maven Dependencies"}),"\n",(0,t.jsxs)(n.p,{children:["Add the following dependency to your ",(0,t.jsx)(n.code,{children:"pom.xml"})," file:"]}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-xml",children:"<dependencies>\n    <dependency>\n        <groupId>com.sap.ai.sdk.foundationmodels</groupId>\n        <artifactId>openai</artifactId>\n        <version>${ai-sdk.version}</version>\n    </dependency>\n</dependencies>\n"})}),"\n",(0,t.jsxs)(n.p,{children:["See ",(0,t.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/pom.xml",children:"an example pom in our Spring Boot application"})]}),"\n",(0,t.jsx)(n.h2,{id:"usage",children:"Usage"}),"\n",(0,t.jsx)(n.p,{children:"In addition to the prerequisites above, we assume you have already set up the following to carry out the examples in this guide:"}),"\n",(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsxs)(n.li,{children:["\n",(0,t.jsx)(n.p,{children:(0,t.jsx)(n.strong,{children:"A Deployed OpenAI Model in SAP AI Core"})}),"\n",(0,t.jsxs)(n.ul,{children:["\n",(0,t.jsxs)(n.li,{children:["\n",(0,t.jsxs)(n.p,{children:["Refer\nto ",(0,t.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-deployment-for-generative-ai-model-in-sap-ai-core",children:"How to deploy a model to AI Core"}),"\nfor setup instructions."]}),"\n"]}),"\n",(0,t.jsxs)(n.li,{children:["\n",(0,t.jsxs)(n.p,{children:["In case the model is deployed in a custom resource group, refer to ",(0,t.jsx)(n.a,{href:"chat-completion#using-a-custom-resource-group",children:"this section"}),"."]}),"\n"]}),"\n",(0,t.jsxs)(n.li,{children:["\n",(0,t.jsxs)(i,{children:[(0,t.jsxs)("summary",{children:["Example deployed model from the AI Core ",(0,t.jsx)("code",{children:"/deployments"})," endpoint"]}),(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-json",children:'{\n  "id": "d123456abcdefg",\n  "deploymentUrl": "https://api.ai.region.aws.ml.hana.ondemand.com/v2/inference/deployments/d123456abcdefg",\n  "configurationId": "12345-123-123-123-123456abcdefg",\n  "configurationName": "gpt-4o-mini",\n  "scenarioId": "foundation-models",\n  "status": "RUNNING",\n  "statusMessage": null,\n  "targetStatus": "RUNNING",\n  "lastOperation": "CREATE",\n  "latestRunningConfigurationId": "12345-123-123-123-123456abcdefg",\n  "ttl": null,\n  "details": {\n    "scaling": {\n      "backendDetails": {}\n    },\n    "resources": {\n      "backendDetails": {\n        "model": {\n          "name": "gpt-4o-mini",\n          "version": "latest"\n        }\n      }\n    }\n  },\n  "createdAt": "2024-07-03T12:44:22Z",\n  "modifiedAt": "2024-07-16T12:44:19Z",\n  "submissionTime": "2024-07-03T12:44:51Z",\n  "startTime": "2024-07-03T12:45:56Z",\n  "completionTime": null\n}\n'})})]}),"\n"]}),"\n"]}),"\n"]}),"\n"]}),"\n",(0,t.jsx)(n.h2,{id:"embedding",children:"Embedding"}),"\n",(0,t.jsx)(n.p,{children:(0,t.jsx)(n.strong,{children:"Since v1.4.0"})}),"\n",(0,t.jsx)(n.p,{children:"Get the embeddings of a text input in list of float values:"}),"\n",(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var request = new OpenAiEmbeddingRequest(List.of("Hello World"));\n\nOpenAiEmbeddingResponse response = OpenAiClient.forModel(TEXT_EMBEDDING_3_SMALL).embedding(request);\nfloat[] embedding = embedding.getEmbeddings().get(0);\n'})}),"\n",(0,t.jsxs)(i,{children:[(0,t.jsx)("summary",{children:(0,t.jsx)("b",{children:"Since v1.0.0"})}),(0,t.jsx)(n.pre,{children:(0,t.jsx)(n.code,{className:"language-java",children:'var request = new OpenAiEmbeddingParameters().setInput("Hello World");\n\nOpenAiEmbeddingOutput embedding = OpenAiClient.forModel(TEXT_EMBEDDING_3_SMALL).embedding(request);\n\nfloat[] embedding = embedding.getData().get(0).getEmbedding();\n'})}),(0,t.jsxs)(n.p,{children:["See ",(0,t.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app/src/main/java/com/sap/ai/sdk/app/services/OpenAiService.java",children:"an example in our Spring Boot application"})]})]})]})}function p(e={}){const{wrapper:n}={...(0,o.R)(),...e.components};return n?(0,t.jsx)(n,{...e,children:(0,t.jsx)(c,{...e})}):c(e)}}}]);