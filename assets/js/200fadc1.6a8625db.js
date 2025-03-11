"use strict";(self.webpackChunksap_ai_sdk_documentation=self.webpackChunksap_ai_sdk_documentation||[]).push([[996],{726:(e,n,i)=>{i.r(n),i.d(n,{assets:()=>o,contentTitle:()=>r,default:()=>h,frontMatter:()=>a,metadata:()=>t,toc:()=>c});const t=JSON.parse('{"id":"release-notes/release-notes-0-to-14","title":"release-notes-0-to-14","description":"1.3.0 - February 13, 2025","source":"@site/docs-java/release-notes/release-notes-0-to-14.mdx","sourceDirName":"release-notes","slug":"/release-notes/release-notes-0-to-14","permalink":"/docs/java/release-notes/release-notes-0-to-14","draft":false,"unlisted":false,"editUrl":"https://github.com/SAP/ai-sdk/edit/main/docs-java/release-notes/release-notes-0-to-14.mdx","tags":[],"version":"current","frontMatter":{}}');var s=i(4848),l=i(8453);const a={},r=void 0,o={},c=[{value:"1.3.0 - February 13, 2025",id:"130---february-13-2025",level:2},{value:"\ud83d\udd27 Compatibility Notes",id:"-compatibility-notes",level:3},{value:"\u2728 New Functionality",id:"-new-functionality",level:3},{value:"1.2.0 - January 30, 2025",id:"120---january-30-2025",level:2},{value:"\ud83d\udd27 Compatibility Notes",id:"-compatibility-notes-1",level:3},{value:"\u2728 New Functionality",id:"-new-functionality-1",level:3},{value:"\ud83d\udcc8 Improvements",id:"-improvements",level:3},{value:"1.1.0 - January 07, 2025",id:"110---january-07-2025",level:2},{value:"\ud83d\udd27 Compatibility Notes",id:"-compatibility-notes-2",level:3},{value:"\u2728 New Functionality",id:"-new-functionality-2",level:3},{value:"\ud83d\udcc8 Improvements",id:"-improvements-1",level:3},{value:"1.0.0 - December 03, 2024",id:"100---december-03-2024",level:2},{value:"\u2728 New Functionality",id:"-new-functionality-3",level:3}];function d(e){const n={a:"a",admonition:"admonition",code:"code",h2:"h2",h3:"h3",li:"li",p:"p",ul:"ul",...(0,l.R)(),...e.components};return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(n.h2,{id:"130---february-13-2025",children:"1.3.0 - February 13, 2025"}),"\n",(0,s.jsx)(n.p,{children:(0,s.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.3.0",children:"All Release Changes"})}),"\n",(0,s.jsx)(n.h3,{id:"-compatibility-notes",children:"\ud83d\udd27 Compatibility Notes"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.code,{children:"Message.content()"})," returns a ",(0,s.jsx)(n.code,{children:"ContentItem"})," now instead of a ",(0,s.jsx)(n.code,{children:"String"}),". Use ",(0,s.jsx)(n.code,{children:"((TextItem) Message.content().items().get(0)).text()"})," if the corresponding ",(0,s.jsx)(n.code,{children:"ContentItem"})," is a ",(0,s.jsx)(n.code,{children:"TextItem"})," and the string representation is needed."]}),"\n"]}),"\n",(0,s.jsx)(n.h3,{id:"-new-functionality",children:"\u2728 New Functionality"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsx)(n.li,{children:"Upgrade to release 2502a of AI Core."}),"\n",(0,s.jsxs)(n.li,{children:["Orchestration:","\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:[(0,s.jsxs)(n.a,{href:"guides/orchestration-chat-completion#chat-completion-filter",children:["Add ",(0,s.jsx)(n.code,{children:"LlamaGuardFilter"})]}),"."]}),"\n",(0,s.jsx)(n.li,{children:(0,s.jsx)(n.a,{href:"guides/orchestration-chat-completion#add-images-and-multiple-text-inputs-to-a-message",children:"Convenient methods to create messages containing images and multiple text inputs"})}),"\n",(0,s.jsx)(n.li,{children:(0,s.jsx)(n.a,{href:"guides/orchestration-chat-completion#set-a-response-format",children:"Enable setting the response format"})}),"\n"]}),"\n"]}),"\n"]}),"\n",(0,s.jsx)(n.h2,{id:"120---january-30-2025",children:"1.2.0 - January 30, 2025"}),"\n",(0,s.jsx)(n.p,{children:(0,s.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.2.0",children:"All Release Changes"})}),"\n",(0,s.jsx)(n.h3,{id:"-compatibility-notes-1",children:"\ud83d\udd27 Compatibility Notes"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.code,{children:"SingleChatMessage"}),", as well as new ",(0,s.jsx)(n.code,{children:"MultiChatMessage"}),", are now subtypes of new interface ",(0,s.jsx)(n.code,{children:"ChatMessage"}),".\nMost variables or methods previously typed as ",(0,s.jsx)(n.code,{children:"ChatMessage"})," in ",(0,s.jsx)(n.code,{children:"model"})," package are now typed as ",(0,s.jsx)(n.code,{children:"SingleChatMessage"}),"."]}),"\n",(0,s.jsxs)(n.li,{children:["Add missing ",(0,s.jsx)(n.code,{children:"@Beta"})," annotations to all ",(0,s.jsx)(n.code,{children:"com.sap.ai.sdk.core.client"})," and ",(0,s.jsx)(n.code,{children:"com.sap.ai.sdk.core.model"})," classes."]}),"\n"]}),"\n",(0,s.jsx)(n.h3,{id:"-new-functionality-1",children:"\u2728 New Functionality"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:["New Orchestration features:","\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsx)(n.li,{children:(0,s.jsx)(n.a,{href:"guides/spring-ai-integration",children:"Spring AI integration"})}),"\n",(0,s.jsx)(n.li,{children:(0,s.jsx)(n.a,{href:"guides/orchestration-chat-completion#grounding",children:"Add Grounding configuration convenience"})}),"\n",(0,s.jsxs)(n.li,{children:["Images are now supported as input in newly introduced ",(0,s.jsx)(n.code,{children:"MultiChatMessage"}),"."]}),"\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.code,{children:"MultiChatMessage"})," also allows for multiple content items (text or image) in one object."]}),"\n",(0,s.jsxs)(n.li,{children:["Grounding input can be masked with ",(0,s.jsx)(n.code,{children:"DPIConfig"}),"."]}),"\n",(0,s.jsx)(n.li,{children:"LLama Guard can now be used for content filtering."}),"\n",(0,s.jsx)(n.li,{children:"Support for tool calling and response format"}),"\n",(0,s.jsx)(n.li,{children:"Updated the list for supported models (e.g., added amazon nova models)."}),"\n"]}),"\n"]}),"\n"]}),"\n",(0,s.jsx)(n.h3,{id:"-improvements",children:"\ud83d\udcc8 Improvements"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsx)(n.li,{children:"Update Orchestration client to version 0.48.2 (2501a)"}),"\n"]}),"\n",(0,s.jsx)(n.h2,{id:"110---january-07-2025",children:"1.1.0 - January 07, 2025"}),"\n",(0,s.jsx)(n.p,{children:(0,s.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.1.0",children:"All Release Changes"})}),"\n",(0,s.jsx)(n.h3,{id:"-compatibility-notes-2",children:"\ud83d\udd27 Compatibility Notes"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:["Changed return type of ",(0,s.jsx)(n.code,{children:"List<Double> getEmbedding()"})," from experimental API ",(0,s.jsx)(n.code,{children:"OpenAiEmbeddingData"})," to ",(0,s.jsx)(n.code,{children:"float[]"})," to match recent Spring AI change."]}),"\n"]}),"\n",(0,s.jsx)(n.h3,{id:"-new-functionality-2",children:"\u2728 New Functionality"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:["Added ",(0,s.jsx)(n.code,{children:"streamChatCompletion()"})," and ",(0,s.jsx)(n.code,{children:"streamChatCompletionDeltas()"})," to the ",(0,s.jsx)(n.code,{children:"OrchestrationClient"}),"."]}),"\n"]}),"\n",(0,s.jsx)(n.h3,{id:"-improvements-1",children:"\ud83d\udcc8 Improvements"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsx)(n.li,{children:"Update AI Core client to 2.37.0"}),"\n"]}),"\n",(0,s.jsx)(n.h2,{id:"100---december-03-2024",children:"1.0.0 - December 03, 2024"}),"\n",(0,s.jsx)(n.p,{children:(0,s.jsx)(n.a,{href:"https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F1.0.0",children:"All Release Changes"})}),"\n",(0,s.jsx)(n.h3,{id:"-new-functionality-3",children:"\u2728 New Functionality"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:["Introduce AI Core client to consume the ",(0,s.jsx)(n.a,{href:"https://api.sap.com/api/AI_CORE_API/overview",children:"AI Core Rest APIs"}),".\nHere are a few features:","\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsx)(n.li,{children:"Artifact management: register and organize datasets and model artifacts."}),"\n",(0,s.jsx)(n.li,{children:"Configuration management: set up configurations for various models and use cases."}),"\n",(0,s.jsx)(n.li,{children:"Deployment management: deploy AI models and manage their lifecycle within SAP AI Core."}),"\n"]}),"\n"]}),"\n",(0,s.jsxs)(n.li,{children:["Introduce Orchestration client for consuming the following features of the orchestration service:","\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsx)(n.li,{children:"Harmonized LLM access via orchestration"}),"\n",(0,s.jsx)(n.li,{children:"Prompt templates"}),"\n",(0,s.jsx)(n.li,{children:"Content filtering"}),"\n",(0,s.jsx)(n.li,{children:"Masking"}),"\n"]}),"\n"]}),"\n",(0,s.jsxs)(n.li,{children:["Introduce the OpenAI client to consume the following features:","\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:["Chat completion and streaming chat completion","\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsx)(n.li,{children:"Text"}),"\n",(0,s.jsx)(n.li,{children:"Images"}),"\n",(0,s.jsx)(n.li,{children:"Tools"}),"\n"]}),"\n"]}),"\n",(0,s.jsx)(n.li,{children:"Generate embeddings for input text."}),"\n"]}),"\n"]}),"\n"]}),"\n",(0,s.jsx)(n.admonition,{type:"warning",children:(0,s.jsxs)(n.p,{children:["All classes under any of the ",(0,s.jsx)(n.code,{children:"...model"})," packages are generated from an OpenAPI specification and marked as ",(0,s.jsx)(n.code,{children:"@Beta"}),".\nThis means that these model classes are not guaranteed to be stable and may change with future releases.\nThey are safe to use, but may require updates even in minor releases."]})})]})}function h(e={}){const{wrapper:n}={...(0,l.R)(),...e.components};return n?(0,s.jsx)(n,{...e,children:(0,s.jsx)(d,{...e})}):d(e)}},8453:(e,n,i)=>{i.d(n,{R:()=>a,x:()=>r});var t=i(6540);const s={},l=t.createContext(s);function a(e){const n=t.useContext(l);return t.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function r(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(s):e.components||s:a(e.components),t.createElement(l.Provider,{value:n},e.children)}}}]);