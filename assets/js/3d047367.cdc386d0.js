"use strict";(self.webpackChunksap_ai_sdk_documentation=self.webpackChunksap_ai_sdk_documentation||[]).push([[69],{4611:(e,n,i)=>{i.r(n),i.d(n,{assets:()=>a,contentTitle:()=>c,default:()=>h,frontMatter:()=>r,metadata:()=>t,toc:()=>l});const t=JSON.parse('{"id":"guides/connecting-to-ai-core","title":"Connecting to AI Core","description":"How to connect to AI Core in BTP using a wide variety of credentials.","source":"@site/docs-java/guides/connecting-to-ai-core.mdx","sourceDirName":"guides","slug":"/guides/connecting-to-ai-core","permalink":"/ai-sdk/docs/java/guides/connecting-to-ai-core","draft":false,"unlisted":false,"editUrl":"https://github.com/SAP/ai-sdk/edit/main/docs-java/guides/connecting-to-ai-core.mdx","tags":[],"version":"current","frontMatter":{"id":"connecting-to-ai-core","title":"Connecting to AI Core","hide_title":false,"hide_table_of_contents":false,"description":"How to connect to AI Core in BTP using a wide variety of credentials.","keywords":["sap","cloud","sdk","ai"]},"sidebar":"docsJavaSidebar","previous":{"title":"Getting Started","permalink":"/ai-sdk/docs/java/getting-started"},"next":{"title":"AI Core Deployment","permalink":"/ai-sdk/docs/java/guides/ai-core-deployment"}}');var s=i(4848),o=i(8453);const r={id:"connecting-to-ai-core",title:"Connecting to AI Core",hide_title:!1,hide_table_of_contents:!1,description:"How to connect to AI Core in BTP using a wide variety of credentials.",keywords:["sap","cloud","sdk","ai"]},c=void 0,a={},l=[{value:"Table of Contents",id:"table-of-contents",level:2},{value:"Using a Service Binding",id:"using-a-service-binding",level:2},{value:"Providing a Service Binding Locally",id:"providing-a-service-binding-locally",level:3},{value:"Using CAP Hybrid Testing",id:"using-cap-hybrid-testing",level:4},{value:"Using the <code>AICORE_SERVICE_KEY</code> Environment Variable",id:"using-the-aicore_service_key-environment-variable",level:4},{value:"Using a Destination from the BTP Destination Service",id:"using-a-destination-from-the-btp-destination-service",level:2},{value:"Creating a Custom Destination",id:"creating-a-custom-destination",level:2}];function d(e){const n={a:"a",admonition:"admonition",blockquote:"blockquote",code:"code",h2:"h2",h3:"h3",h4:"h4",li:"li",ol:"ol",p:"p",pre:"pre",strong:"strong",ul:"ul",...(0,o.R)(),...e.components},{Details:i}=n;return i||function(e,n){throw new Error("Expected "+(n?"component":"object")+" `"+e+"` to be defined: you likely forgot to import, pass, or provide it.")}("Details",!0),(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(n.h2,{id:"table-of-contents",children:"Table of Contents"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.a,{href:"#using-a-service-binding",children:"Using a Service Binding"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsx)(n.li,{children:(0,s.jsx)(n.a,{href:"#providing-a-service-binding-locally",children:"Providing a Service Binding Locally"})}),"\n",(0,s.jsx)(n.li,{children:(0,s.jsxs)(n.a,{href:"#using-the-aicore_service_key-environment-variable",children:["Using the ",(0,s.jsx)(n.code,{children:"AICORE_SERVICE_KEY"})," Environment Variable"]})}),"\n"]}),"\n"]}),"\n",(0,s.jsx)(n.li,{children:(0,s.jsx)(n.a,{href:"#using-a-destination-from-the-btp-destination-service",children:"Using a Destination from the BTP Destination Service"})}),"\n",(0,s.jsx)(n.li,{children:(0,s.jsx)(n.a,{href:"#creating-a-custom-destination",children:"Creating a Custom Destination"})}),"\n"]}),"\n",(0,s.jsxs)(n.p,{children:["The AI SDK uses the ",(0,s.jsxs)(n.a,{href:"https://sap.github.io/cloud-sdk/docs/java/features/connectivity/destination-service",children:[(0,s.jsx)(n.code,{children:"Destination"})," concept of the SAP Cloud SDK"]})," to connect to AI Core.\nThis allows for a seamless integration in BTP and offers a wide variety of managing the credentials for the connection."]}),"\n",(0,s.jsx)(n.h2,{id:"using-a-service-binding",children:"Using a Service Binding"}),"\n",(0,s.jsxs)(n.p,{children:["By default, the AI SDK will look for an ",(0,s.jsx)(n.code,{children:"aicore"})," service binding in the environment of the application."]}),"\n",(0,s.jsxs)(n.p,{children:["When running on SAP BTP, ",(0,s.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-service-instance",children:"create an instance of the AI Core service"})," and bind it to your application.\nThe AI SDK will automatically detect the service binding and use it to connect to AI Core."]}),"\n",(0,s.jsx)(n.p,{children:"If no service binding could be found (and no other destination has been given), the AI SDK will throw an exception:"}),"\n",(0,s.jsxs)(n.blockquote,{children:["\n",(0,s.jsx)(n.p,{children:"Could not find any matching service bindings for service identifier 'aicore'"}),"\n"]}),"\n",(0,s.jsx)(n.p,{children:"To run your code outside SAP BTP (e.g. locally), you will have to provide the credentials manually."}),"\n",(0,s.jsx)(n.h3,{id:"providing-a-service-binding-locally",children:"Providing a Service Binding Locally"}),"\n",(0,s.jsx)(n.p,{children:"For local development, you can provide the service credentials locally in various ways."}),"\n",(0,s.jsx)(n.h4,{id:"using-cap-hybrid-testing",children:"Using CAP Hybrid Testing"}),"\n",(0,s.jsxs)(n.p,{children:["When developing a ",(0,s.jsx)(n.a,{href:"https://cap.cloud.sap/docs/",children:"CAP application"}),", you can use the ",(0,s.jsx)(n.a,{href:"https://cap.cloud.sap/docs/advanced/hybrid-testing#services-on-cloud-foundry",children:"hybrid testing"})," approach.\nAssuming your AI Core service instance is called ",(0,s.jsx)(n.code,{children:"aicore"}),", the following command runs a Maven command with the credentials of the service instance:"]}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:"cds bind --to aicore --exec mvn spring-boot:run\n"})}),"\n",(0,s.jsxs)(n.h4,{id:"using-the-aicore_service_key-environment-variable",children:["Using the ",(0,s.jsx)(n.code,{children:"AICORE_SERVICE_KEY"})," Environment Variable"]}),"\n",(0,s.jsxs)(n.p,{children:["You can also provide the service credentials in the ",(0,s.jsx)(n.code,{children:"AICORE_SERVICE_KEY"})," environment variable.\nFirst, ",(0,s.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-service-key",children:"create a service key for your AI Core service instance"}),".\nCopy the resulting JSON object."]}),"\n",(0,s.jsxs)(n.p,{children:["Then set the environment variable ",(0,s.jsx)(n.code,{children:"AICORE_SERVICE_KEY"})," to be defined for however you want to run your code.\nHow exactly to set this depends on how you run your code (e.g. via IDE, command line etc.) and potentially on your operating system."]}),"\n",(0,s.jsx)(n.p,{children:"Here are three examples of how this can be done:"}),"\n",(0,s.jsxs)(n.ol,{children:["\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsxs)(i,{children:[(0,s.jsxs)("summary",{children:["Using a ",(0,s.jsx)(n.code,{children:".env"})," file"]}),(0,s.jsxs)(n.p,{children:["Create a ",(0,s.jsx)(n.code,{children:".env"})," file in the ",(0,s.jsx)(n.strong,{children:"working directory"})," from which you run your code.\nAdd the following line:"]}),(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-txt",children:'AICORE_SERVICE_KEY={ "clientid": "...", "clientsecret": "...", "url": "...", "serviceurls": { "AI_API_URL": "..." } }\n'})}),(0,s.jsx)(n.admonition,{type:"info",children:(0,s.jsxs)(n.p,{children:["The value of ",(0,s.jsx)(n.code,{children:"AICORE_SERVICE_KEY"})," must be a single line, so remove any line breaks from the service key JSON."]})})]}),"\n"]}),"\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsxs)(i,{children:[(0,s.jsx)("summary",{children:"Using the command line on Mac OS"}),(0,s.jsx)(n.p,{children:"Run your code with the following command:"}),(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-bash",children:'export AICORE_SERVICE_KEY=\'{ "clientid": "...", "clientsecret": "...", "url": "...", "serviceurls": { "AI_API_URL": "..." } }\'\nmvn ...\n'})})]}),"\n"]}),"\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsxs)(i,{children:[(0,s.jsx)("summary",{children:"Using PowerShell on Windows"}),(0,s.jsx)(n.p,{children:"Run your code with the following command:"}),(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-shell",children:'$env:AICORE_SERVICE_KEY=\'{ "clientid": "...", "clientsecret": "...", "url": "...", "serviceurls": { "AI_API_URL": "..." } }\'\nmvn ...\n'})})]}),"\n"]}),"\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsxs)(i,{children:[(0,s.jsx)("summary",{children:"Using an IntelliJ run configuration"}),(0,s.jsxs)(n.p,{children:["In IntelliJ, go to ",(0,s.jsx)(n.code,{children:"Run"})," > ",(0,s.jsx)(n.code,{children:"Edit Configurations..."})," > ",(0,s.jsx)(n.code,{children:"Environment variables"}),".\nAdd a new environment variable with the name ",(0,s.jsx)(n.code,{children:"AICORE_SERVICE_KEY"})," and paste the service key as value."]}),(0,s.jsxs)(n.p,{children:["For more information, see the ",(0,s.jsx)(n.a,{href:"https://www.jetbrains.com/help/idea/run-debug-configuration-application.html#configure-environment-variables",children:"official IntelliJ documentation"}),"."]})]}),"\n"]}),"\n"]}),"\n",(0,s.jsx)(n.h2,{id:"using-a-destination-from-the-btp-destination-service",children:"Using a Destination from the BTP Destination Service"}),"\n",(0,s.jsx)(n.p,{children:"You can define a destination in the BTP Destination Service and use that to connect to AI Core."}),"\n",(0,s.jsxs)(i,{children:[(0,s.jsx)("summary",{children:"How to create a Destination in the SAP BTP Cockpit"}),(0,s.jsxs)(n.ol,{children:["\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsxs)(n.p,{children:[(0,s.jsx)(n.a,{href:"https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/create-service-key",children:"Create a service key for your AI Core service instance"}),"."]}),"\n"]}),"\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsx)(n.p,{children:"Create a new Destination in the SAP BTP Cockpit with the following properties:"}),"\n"]}),"\n"]}),(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsxs)(n.p,{children:[(0,s.jsx)(n.strong,{children:"Name"}),": ",(0,s.jsx)(n.code,{children:"my-aicore"})]}),"\n"]}),"\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsxs)(n.p,{children:[(0,s.jsx)(n.strong,{children:"Type"}),": ",(0,s.jsx)(n.code,{children:"HTTP"})]}),"\n"]}),"\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsxs)(n.p,{children:[(0,s.jsx)(n.strong,{children:"URL"}),": ",(0,s.jsx)(n.code,{children:"[serviceurls.AI_API_URL]"})]}),"\n"]}),"\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsxs)(n.p,{children:[(0,s.jsx)(n.strong,{children:"Proxy Type"}),": ",(0,s.jsx)(n.code,{children:"Internet"})]}),"\n"]}),"\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsxs)(n.p,{children:[(0,s.jsx)(n.strong,{children:"Authentication"}),": ",(0,s.jsx)(n.code,{children:"OAuth2ClientCredentials"})]}),"\n"]}),"\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsxs)(n.p,{children:[(0,s.jsx)(n.strong,{children:"Client ID"}),": ",(0,s.jsx)(n.code,{children:"[clientid]"})]}),"\n"]}),"\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsxs)(n.p,{children:[(0,s.jsx)(n.strong,{children:"Client Secret"}),": ",(0,s.jsx)(n.code,{children:"[clientsecret]"})]}),"\n"]}),"\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsxs)(n.p,{children:[(0,s.jsx)(n.strong,{children:"Token Service URL Type"}),": ",(0,s.jsx)(n.code,{children:"Dedicated"})]}),"\n"]}),"\n",(0,s.jsxs)(n.li,{children:["\n",(0,s.jsxs)(n.p,{children:[(0,s.jsx)(n.strong,{children:"Token Service URL"}),": ",(0,s.jsx)(n.code,{children:"[url]/oauth/token"})]}),"\n",(0,s.jsxs)(n.p,{children:["Fill in the values for URL, client ID, client secret, and token service URL from the service key JSON.\nMake sure to add ",(0,s.jsx)(n.code,{children:"/oauth/token"})," in the token service URL."]}),"\n"]}),"\n"]})]}),"\n",(0,s.jsx)(n.p,{children:"To use the destination, ensure you have created an instance of the BTP Destination Service and bound it to your application."}),"\n",(0,s.jsx)(n.admonition,{type:"tip",children:(0,s.jsxs)(n.p,{children:["If you are using CAP, you can again use Hybrid Testing to bind the destination service to your application when running ",(0,s.jsx)(n.strong,{children:"locally"}),"."]})}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-java",children:'Destination destination = DestinationAccessor.getDestination("my-aicore").asHttp();\nAiCoreService aiCoreService = new AiCoreService().withBaseDestination(destination);\n'})}),"\n",(0,s.jsxs)(n.p,{children:["Now you can use the ",(0,s.jsx)(n.code,{children:"AiCoreService"})," as follows:"]}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-java",children:'// To create an OpenAiClient:\nvar openAiDestination = aiCoreService.getInferenceDestination().forModel(OpenAiModel.TEXT_EMBEDDING_3_LARGE);\nvar client = OpenAiClient.withCustomDestination(openAiDestination);\n\n// To create an OrchestrationClient:\nvar orchestrationDestination = aiCoreService.getInferenceDestination().forScenario("orchestration");\nvar client = new OrchestrationClient(orchestrationDestination);\n\n// To create any of the com.sap.ai.sdk.core.client.* classes (e.g. DeploymentApi):\nnew DeploymentApi(aiCoreService);\n'})}),"\n",(0,s.jsx)(n.admonition,{type:"info",children:(0,s.jsxs)(n.p,{children:["The ",(0,s.jsx)(n.code,{children:"destination"})," obtained from BTP destination service will expire once the contained OAuth2 token expires.\nPlease run the above code for each request to ensure the destination is up-to-date.\nDestinations are cached by default, so this does not come with a performance penalty.\nTo learn more, see the ",(0,s.jsx)(n.a,{href:"https://sap.github.io/cloud-sdk/docs/java/features/connectivity/destination-service",children:"SAP Cloud SDK documentation"}),"."]})}),"\n",(0,s.jsx)(n.h2,{id:"creating-a-custom-destination",children:"Creating a Custom Destination"}),"\n",(0,s.jsx)(n.p,{children:"If the above options are not suitable for your use case (e.g. because you are obtaining the credentials in a completely different way), you can also use a custom-built destination:"}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-java",children:'var destination = OAuth2DestinationBuilder\n    .forTargetUrl("https://<ai-api-url>")\n    .withTokenEndpoint("https://<xsuaa-url>/oauth/token")\n    .withClient(new ClientCertificate("<cert>", "<key>", "<clientid>"), OnBehalfOf.TECHNICAL_USER_PROVIDER)\n    .build();\n\nAiCoreService aiCoreService = new AiCoreService().withBaseDestination(destination);\n'})}),"\n",(0,s.jsx)(n.p,{children:"The above example assumes you are using a client certificate for authentication and have stored the relevant credentials somewhere.\nYou are free to use X509 certificates (also via the Zero Trust Identity Service) or a client secret."}),"\n",(0,s.jsxs)(n.p,{children:["For more details, refer to the ",(0,s.jsx)(n.a,{href:"https://sap.github.io/cloud-sdk/docs/java/features/connectivity/destination-service",children:"SAP Cloud SDK documentation"}),"."]})]})}function h(e={}){const{wrapper:n}={...(0,o.R)(),...e.components};return n?(0,s.jsx)(n,{...e,children:(0,s.jsx)(d,{...e})}):d(e)}},8453:(e,n,i)=>{i.d(n,{R:()=>r,x:()=>c});var t=i(6540);const s={},o=t.createContext(s);function r(e){const n=t.useContext(o);return t.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function c(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(s):e.components||s:r(e.components),t.createElement(o.Provider,{value:n},e.children)}}}]);