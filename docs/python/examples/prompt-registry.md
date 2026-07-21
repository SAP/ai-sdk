# Prompt Registry

The Prompt Registry API allows you to create, manage, and retrieve prompt and orchestration config templates for use in SAP AI Core when working with Generative AI Hub models.

See [SAP Help](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/prompt-registry?locale=en-US) for the difference between **imperative** and **declarative** prompt templates.

## Prompt Template Management[​](#prompt-template-management "Direct link to Prompt Template Management")

### Initialize Client[​](#initialize-client "Direct link to Initialize Client")

```
from gen_ai_hub.proxy import get_proxy_client

from gen_ai_hub.prompt_registry import PromptTemplateClient



proxy_client = get_proxy_client(proxy_version="gen-ai-hub")

prompt_registry_client = PromptTemplateClient(proxy_client=proxy_client)
```

### Create a Prompt Template[​](#create-a-prompt-template "Direct link to Create a Prompt Template")

```
from gen_ai_hub.prompt_registry import PromptTemplateSpec, PromptTemplate



prompt_template_spec = PromptTemplateSpec(

    template=[PromptTemplate(role='system', content='You are a helpful assistant.')]

)



template_id = prompt_registry_client.create_prompt_template(

    scenario='MyScenario',

    name='prompt_template_name',

    version='1.0.0',

    prompt_template_spec=prompt_template_spec

).id



print(f"Created Prompt Template with ID: {template_id}")
```

### Retrieve a Prompt Template[​](#retrieve-a-prompt-template "Direct link to Retrieve a Prompt Template")

```
response = prompt_registry_client.get_prompt_template_by_id(template_id)

print(response.spec.template)
```

### Modify a Prompt Template[​](#modify-a-prompt-template "Direct link to Modify a Prompt Template")

```
prompt_template_spec = PromptTemplateSpec(

    template=[PromptTemplate(role='system', content='You are a helpful assistant for {{ ?topic }}.')]

)

response = prompt_registry_client.create_prompt_template(

    scenario='MyScenario',

    name='prompt_template_name',

    version='1.0.0',

    prompt_template_spec=prompt_template_spec

)

input_template_id = response.id

print(response.message)
```

### Prompt Template History[​](#prompt-template-history "Direct link to Prompt Template History")

```
response = prompt_registry_client.get_prompt_template_history(

    scenario='MyScenario', name='prompt_template_name', version='1.0.0'

)

print(response.json())
```

### Fill a Prompt Template[​](#fill-a-prompt-template "Direct link to Fill a Prompt Template")

```
response = prompt_registry_client.fill_prompt_template_by_id(

    template_id=input_template_id, input_params={"topic": "chemistry"}

)

print(response.parsed_prompt)
```

## Orchestration Config Management[​](#orchestration-config-management "Direct link to Orchestration Config Management")

### Initialize Client[​](#initialize-client-1 "Direct link to Initialize Client")

```
from gen_ai_hub.proxy import get_proxy_client

from gen_ai_hub.prompt_registry import OrchestrationConfigClient



proxy_client = get_proxy_client(proxy_version="gen-ai-hub")

prompt_registry_client = OrchestrationConfigClient(proxy_client=proxy_client)
```

### Create an Orchestration Config[​](#create-an-orchestration-config "Direct link to Create an Orchestration Config")

```
from gen_ai_hub.orchestration_v2 import (

    OrchestrationConfig, ModuleConfig, LLMModelDetails, UserMessage, Template, PromptTemplatingModuleConfig

)



config_spec = OrchestrationConfig(

    modules=ModuleConfig(

        prompt_templating=PromptTemplatingModuleConfig(

            prompt=Template(template=[UserMessage(content="Hello, World!")]),

            model=LLMModelDetails(name="gpt-4o-mini")

        )

    )

)



template_id = prompt_registry_client.create_orchestration_config(

    scenario='MyScenario',

    name='prompt_template_name',

    version='1.0.0',

    spec=config_spec

).id



print(f"Created Orchestration Config Template with ID: {template_id}")
```

### Retrieve an Orchestration Config[​](#retrieve-an-orchestration-config "Direct link to Retrieve an Orchestration Config")

```
response = prompt_registry_client.get_orchestration_config_by_id(template_id)

print(response.spec)
```

By scenario, name, and version:

```
response = prompt_registry_client.get_orchestration_configs(

    scenario='MyScenario', name='prompt_template_name', version='1.0.0'

)

print(response.resources)
```

### Export an Orchestration Config[​](#export-an-orchestration-config "Direct link to Export an Orchestration Config")

```
response = prompt_registry_client.export_orchestration_config(config_id=template_id)

print(response)
```
