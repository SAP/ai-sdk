"use strict";(self.webpackChunksap_ai_sdk_documentation=self.webpackChunksap_ai_sdk_documentation||[]).push([[8759],{3383:(e,n,i)=>{i.r(n),i.d(n,{assets:()=>a,contentTitle:()=>c,default:()=>h,frontMatter:()=>r,metadata:()=>t,toc:()=>d});const t=JSON.parse('{"id":"connecting-to-ai-core","title":"Connecting to AI Core","description":"How to connect to AI Core in BTP using a wide variety of credentials.","source":"@site/docs-js/connecting-to-ai-core.mdx","sourceDirName":".","slug":"/connecting-to-ai-core","permalink":"/ai-sdk/docs/js/connecting-to-ai-core","draft":false,"unlisted":false,"editUrl":"https://github.com/SAP/ai-sdk/edit/main/docs-js/connecting-to-ai-core.mdx","tags":[],"version":"current","frontMatter":{"id":"connecting-to-ai-core","title":"Connecting to AI Core","hide_title":false,"hide_table_of_contents":false,"description":"How to connect to AI Core in BTP using a wide variety of credentials.","keywords":["sap","cloud","sdk","ai","btp","ai core"]},"sidebar":"docsJsSidebar","previous":{"title":"Getting Started","permalink":"/ai-sdk/docs/js/getting-started"},"next":{"title":"Chat Completion","permalink":"/ai-sdk/docs/js/orchestration/chat-completion"}}');var s=i(4848),o=i(8453);const r={id:"connecting-to-ai-core",title:"Connecting to AI Core",hide_title:!1,hide_table_of_contents:!1,description:"How to connect to AI Core in BTP using a wide variety of credentials.",keywords:["sap","cloud","sdk","ai","btp","ai core"]},c=void 0,a={},d=[{value:"Using a Service Binding",id:"using-a-service-binding",level:2},{value:"Providing a Service Binding Locally",id:"providing-a-service-binding-locally",level:3},{value:"Using CAP Hybrid Testing",id:"using-cap-hybrid-testing",level:4},{value:"Using the <code>AICORE_SERVICE_KEY</code> Environment Variable",id:"using-the-aicore_service_key-environment-variable",level:4},{value:"Using a Destination",id:"using-a-destination",level:2},{value:"Using the SAP BTP Destination Service",id:"using-the-sap-btp-destination-service",level:3},{value:"Creating a Custom Destination",id:"creating-a-custom-destination",level:3}];function l(e){const n={a:"a",admonition:"admonition",code:"code",h2:"h2",h3:"h3",h4:"h4",li:"li",ol:"ol",p:"p",pre:"pre",strong:"strong",ul:"ul",...(0,o.R)(),...e.components},{Details:i}=n;return i||function(e,n){throw new Error("Expected "+(n?"component":"object")+" `"+e+"` to be defined: you likely forgot to import, pass, or provide it.")}("Details",!0),(0,s.jsxs)(s.Fragment,{children:[(0,s.jsxs)(n.p,{children:["The SAP Cloud SDK for AI uses the ",(0,s.jsx)(n.a,{href:"https://sap.github.io/cloud-sdk/docs/js/features/connectivity/destinations",children:"Destination concept of the SAP Cloud SDK"})," to connect to AI Core.\nThis allows for a seamless integration in SAP BTP and offers a wide variety of managing the credentials for the connection."]}),"\n",(0,s.jsx)(n.h2,{id:"using-a-service-binding",children:"Using a Service Binding"}),"\n",(0,s.jsxs)(n.p,{children:["By default, the SAP Cloud SDK for AI will look for an ",(0,s.jsx)(n.code,{children:"aicore"})," service binding in the environment of the application."]}),"\n",(0,s.jsxs)(n.p,{children:["When running on SAP BTP, ",(0,s.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-service-instance",children:"create an instance of the AI Core service"})," and bind it to your application."]}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:["In Cloud Foundry, it's accessed from the ",(0,s.jsx)(n.code,{children:"VCAP_SERVICES"})," environment variable."]}),"\n",(0,s.jsxs)(n.li,{children:["In Kubernetes / Kyma environments, you have to mount the service binding as a secret instead, for more information refer to ",(0,s.jsx)(n.a,{href:"https://www.npmjs.com/package/@sap/xsenv#usage-in-kubernetes",children:"this documentation"}),"."]}),"\n"]}),"\n",(0,s.jsx)(n.p,{children:"If no service binding is found and no destination is explicitly provided, the SDK throws an exception:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-txt",children:"Could not find service credentials for AI Core. Please check the service binding.\n"})}),"\n",(0,s.jsx)(n.p,{children:"To run the code outside of SAP BTP (e.g., locally), provide the necessary credentials manually."}),"\n",(0,s.jsx)(n.h3,{id:"providing-a-service-binding-locally",children:"Providing a Service Binding Locally"}),"\n",(0,s.jsx)(n.p,{children:"For local development, you can provide the service credentials locally in several ways."}),"\n",(0,s.jsx)(n.h4,{id:"using-cap-hybrid-testing",children:"Using CAP Hybrid Testing"}),"\n",(0,s.jsxs)(n.p,{children:["When developing a ",(0,s.jsx)(n.a,{href:"https://cap.cloud.sap/docs/",children:"CAP application"}),", you can use the ",(0,s.jsx)(n.a,{href:"https://cap.cloud.sap/docs/advanced/hybrid-testing#services-on-cloud-foundry",children:"hybrid testing"})," approach.\nThe following command will bind the credential of your AI Core service instance:"]}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"cds bind -2 AICORE_INSTANCE_NAME\n"})}),"\n",(0,s.jsx)(n.p,{children:"Then run the application with the hybrid profile:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"cds-tsx watch --profile hybrid\n"})}),"\n",(0,s.jsxs)(n.h4,{id:"using-the-aicore_service_key-environment-variable",children:["Using the ",(0,s.jsx)(n.code,{children:"AICORE_SERVICE_KEY"})," Environment Variable"]}),"\n",(0,s.jsxs)(n.p,{children:["You can provide the service credential in the ",(0,s.jsx)(n.code,{children:"AICORE_SERVICE_KEY"})," environment variable.\nSAP Cloud SDK for AI will read it through ",(0,s.jsx)(n.code,{children:"process.env.AICORE_SERVICE_KEY"})," variable."]}),"\n",(0,s.jsxs)(n.p,{children:[(0,s.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-service-key",children:"Create a service key"})," for your AI Core service instance and copy the resulting JSON object."]}),"\n",(0,s.jsxs)(n.p,{children:["Next, set the environment variable ",(0,s.jsx)(n.code,{children:"AICORE_SERVICE_KEY"}),", e.g., by creating a ",(0,s.jsx)(n.code,{children:".env"})," file with the following content:"]}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-txt",children:'AICORE_SERVICE_KEY=\'{\n    "clientid": "...",\n    ...\n}\'\n'})}),"\n",(0,s.jsxs)(n.p,{children:["Load the ",(0,s.jsx)(n.code,{children:".env"})," file by using ",(0,s.jsx)(n.a,{href:"https://www.npmjs.com/package/dotenv",children:"dotenv"})," or running ",(0,s.jsx)(n.code,{children:"node --env-file=.env ..."}),"."]}),"\n",(0,s.jsxs)(n.p,{children:["For NextJS, see ",(0,s.jsx)(n.a,{href:"https://nextjs.org/docs/pages/building-your-application/configuring/environment-variables",children:"this documentation"}),"."]}),"\n",(0,s.jsx)(n.h2,{id:"using-a-destination",children:"Using a Destination"}),"\n",(0,s.jsx)(n.h3,{id:"using-the-sap-btp-destination-service",children:"Using the SAP BTP Destination Service"}),"\n",(0,s.jsx)(n.p,{children:"You can define a destination in the SAP BTP Destination Service and use that to connect to SAP AI Core."}),"\n",(0,s.jsxs)(i,{children:[(0,s.jsx)("summary",{children:"How to create a Destination in the SAP BTP Cockpit"}),(0,s.jsxs)(n.ol,{children:["\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsxs)(n.p,{children:[(0,s.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-service-key",children:"Create a service key for your AI Core service instance"}),"."]}),"\n"]}),"\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsx)(n.p,{children:"Create a new Destination in the SAP BTP Cockpit with the following properties:"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.strong,{children:"Name"}),": ",(0,s.jsx)(n.code,{children:"my-aicore"})]}),"\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.strong,{children:"Type"}),": ",(0,s.jsx)(n.code,{children:"HTTP"})]}),"\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.strong,{children:"URL"}),": ",(0,s.jsx)(n.code,{children:"[serviceurls.AI_API_URL]"})]}),"\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.strong,{children:"Proxy Type"}),": ",(0,s.jsx)(n.code,{children:"Internet"})]}),"\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.strong,{children:"Authentication"}),": ",(0,s.jsx)(n.code,{children:"OAuth2ClientCredentials"})]}),"\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.strong,{children:"Client ID"}),": ",(0,s.jsx)(n.code,{children:"[clientid]"})]}),"\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.strong,{children:"Client Secret"}),": ",(0,s.jsx)(n.code,{children:"[clientsecret]"})]}),"\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.strong,{children:"Token Service URL Type"}),": ",(0,s.jsx)(n.code,{children:"Dedicated"})]}),"\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.strong,{children:"Token Service URL"}),": ",(0,s.jsx)(n.code,{children:"[url]/oauth/token"})]}),"\n"]}),"\n",(0,s.jsxs)(n.p,{children:["Fill in the values for URL, client ID, client secret, and token service URL from the service key JSON.\nMake sure to add ",(0,s.jsx)(n.code,{children:"/oauth/token"})," in the token service URL."]}),"\n"]}),"\n"]})]}),"\n",(0,s.jsx)(n.admonition,{type:"tip",children:(0,s.jsxs)(n.p,{children:["If you are using CAP, you can again use Hybrid Testing to bind the destination service to your application when running ",(0,s.jsx)(n.strong,{children:"locally"}),"."]})}),"\n",(0,s.jsx)(n.p,{children:"Ensure you have created an instance of the SAP BTP Destination Service and bound it to your application."}),"\n",(0,s.jsxs)(n.p,{children:["By default, the fetched destination is cached.\nCheck the ",(0,s.jsx)(n.a,{href:"https://sap.github.io/cloud-sdk/docs/js/features/connectivity/destination-cache#cache-expiration",children:"Cache Expiration"})," section of the SAP Cloud SDK documentation for more details."]}),"\n",(0,s.jsxs)(n.p,{children:["This destination can be used later when initializing a client or calling the ",(0,s.jsx)(n.code,{children:"execute()"})," method."]}),"\n",(0,s.jsx)(n.h3,{id:"creating-a-custom-destination",children:"Creating a Custom Destination"}),"\n",(0,s.jsxs)(n.p,{children:["You can register a destination for AI Core programmatically.\nFor more details, refer to the ",(0,s.jsx)(n.a,{href:"https://sap.github.io/cloud-sdk/docs/js/features/connectivity/destinations#register-destination",children:"Register Destination"})," section of the SAP Cloud SDK documentation."]})]})}function h(e={}){const{wrapper:n}={...(0,o.R)(),...e.components};return n?(0,s.jsx)(n,{...e,children:(0,s.jsx)(l,{...e})}):l(e)}},8453:(e,n,i)=>{i.d(n,{R:()=>r,x:()=>c});var t=i(6540);const s={},o=t.createContext(s);function r(e){const n=t.useContext(o);return t.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function c(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(s):e.components||s:r(e.components),t.createElement(o.Provider,{value:n},e.children)}}}]);