# Generative AI Custom Evaluation

This page showcases how to use the Evaluations SDK to benchmark LLMs, evaluate orchestration configurations, or prompts.

## Setup[​](#setup "Direct link to Setup")

```
from gen_ai_hub.evaluations import EvaluationClient

from dotenv import load_dotenv

import os



load_dotenv(override=True)



client = EvaluationClient(

    base_url=os.getenv("AICORE_BASE_URL"),

    auth_url=os.getenv("AICORE_AUTH_URL"),

    client_id=os.getenv("AICORE_CLIENT_ID"),

    client_secret=os.getenv("AICORE_CLIENT_SECRET"),

    resource_group=os.getenv("AICORE_RESOURCE_GROUP"),

    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),

    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),

    orchestration_url=os.getenv("ORCHESTRATION_URL")

)



# Alternative initialization from environment

# client = EvaluationClient.from_env()
```

## One-Time Setup: Create Secrets[​](#one-time-setup-create-secrets "Direct link to One-Time Setup: Create Secrets")

```
import json



AWS_S3_ENDPOINT = "s3-eu-central-1.amazonaws.com"



default_secret_creds = {

    "data": {}, "type": "S3", "pathPrefix": "sdkOutputFiles",

    "endpoint": AWS_S3_ENDPOINT, "bucket": os.getenv("AWS_BUCKET_ID"),

    "region": os.getenv("AWS_REGION"), "usehttps": "1",

}

input_secret_creds = {

    "data": {}, "name": "sdk-data", "type": "S3", "pathPrefix": "sdk_input_files/data",

    "endpoint": AWS_S3_ENDPOINT, "bucket": os.getenv("AWS_BUCKET_ID"),

    "region": os.getenv("AWS_REGION"), "usehttps": "1",

}



response = client.setup(

    default_secret_body=default_secret_creds,

    input_secret_body=input_secret_creds,

    replace_existing=True

)

print(json.dumps(response, indent=4, ensure_ascii=False))
```

## List Available Models and Metrics[​](#list-available-models-and-metrics "Direct link to List Available Models and Metrics")

```
models_list = client.list_available_models()

print([m["model"] for m in models_list])



metrics_list = client.get_system_supported_metrics()

print([m["name"] for m in metrics_list])
```

## Define Evaluation Config[​](#define-evaluation-config "Direct link to Define Evaluation Config")

```
from gen_ai_hub.prompt_registry import PromptTemplateSpec, PromptTemplate

from gen_ai_hub.orchestration.models.template_ref import TemplateRef

from gen_ai_hub.evaluations import Dataset, MetricConfig, MetricRef, EvaluationConfig

from gen_ai_hub.orchestration.models.llm import LLM



evaluation_config_list = [

    EvaluationConfig(

        llm=LLM(name="gpt-4o", version="latest"),

        template=PromptTemplateSpec(

            template=[PromptTemplate(

                role="user",

                content="Provide a concise and informative response to the following consumer health question: {{?question}}"

            )]

        ),

        template_variable_mapping={"question": "topic"},

        dataset_config=Dataset("eval-data/testdata/medicalqna_dataset.csv"),

        metrics=[

            MetricConfig(

                reference=MetricRef(id="3ea07c1f-5b10-4b12-bf46-6d429faf8010"),

                variable_mapping={"reference": "ground_truth"},

            ),

        ],

    ),

    EvaluationConfig(

        orchestration_registry_reference="fa938934-ca94-4f8d-b59d-76c4570f0394",

        template_variable_mapping={"question": "topic"},

        dataset_config=Dataset("eval-data/testdata/medicalqna_dataset.csv"),

        metrics=[

            MetricConfig(

                reference=MetricRef(id="3ea07c1f-5b10-4b12-bf46-6d429faf8010"),

                variable_mapping={"reference": "ground_truth"},

            ),

            MetricConfig(reference=MetricRef(name="Content Filter on Input")),

        ],

    ),

    EvaluationConfig(

        llm=LLM(name="gpt-5", version="latest"),

        template=TemplateRef(id="73282020-9141-46af-981f-c4816dd01d33"),

        template_variable_mapping={"question": "topic"},

        dataset_config=Dataset("eval-data/testdata/medicalqna_dataset.csv"),

        metrics=[

            MetricConfig(reference=MetricRef(name="Pointwise Instruction Following")),

        ],

    ),

]
```

## Run Evaluation[​](#run-evaluation "Direct link to Run Evaluation")

```
evaluation_runs = client.evaluate(evaluation_config_list)



for current_run in evaluation_runs:

    print(f"id: {current_run.id}, status: {current_run.status}")
```

## Wait for Completion[​](#wait-for-completion "Direct link to Wait for Completion")

```
for current_run in evaluation_runs:

    print("Waiting for run:", current_run.id)

    current_run.wait_for_completion(timeout=3600)
```

## Debugging[​](#debugging "Direct link to Debugging")

```
import json



debug_info = current_run.get_debug_info()

print("Debug info:", debug_info)



debug_logs = current_run.get_debug_logs()

print("Logs:", json.dumps(debug_logs, indent=4, default=str))
```

## View Results[​](#view-results "Direct link to View Results")

### Aggregate Results[​](#aggregate-results "Direct link to Aggregate Results")

```
run1_data = evaluation_runs[0].results()

run2_data = evaluation_runs[1].results().aggregations()

print(run1_data)
```

### Completion Responses[​](#completion-responses "Direct link to Completion Responses")

```
data = evaluation_runs[0].results().completions()

print(data.head())
```

### Metric Evaluation[​](#metric-evaluation "Direct link to Metric Evaluation")

```
data = evaluation_runs[0].results().metrics()

print(data.head())
```
