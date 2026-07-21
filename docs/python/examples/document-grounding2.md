# Document Grounding — Vector, Retrieval and Pipelines

This page demonstrates the Vector API, Retrieval API, and extended Pipelines API.

## Client Initialization[​](#client-initialization "Direct link to Client Initialization")

```
from gen_ai_hub.proxy import get_proxy_client

from gen_ai_hub.document_grounding.client import PipelineAPIClient, VectorAPIClient, RetrievalAPIClient



proxy_client = get_proxy_client(proxy_version='gen-ai-hub')



pipelines = PipelineAPIClient(proxy_client)

vector = VectorAPIClient(proxy_client)

retrieval = RetrievalAPIClient(proxy_client)
```

## Pipelines API[​](#pipelines-api "Direct link to Pipelines API")

### List and Search Pipelines[​](#list-and-search-pipelines "Direct link to List and Search Pipelines")

```
from gen_ai_hub.document_grounding.models.pipeline import SearchPipelineRequest, SearchPipelineData



pipelines_list = pipelines.get_pipelines(top=10)



search_req = SearchPipelineRequest(data=SearchPipelineData(search='<SEARCH_QUERY>'))

search_res = pipelines.search_pipelines(search_req)
```

### Pipeline Status and Manual Trigger[​](#pipeline-status-and-manual-trigger "Direct link to Pipeline Status and Manual Trigger")

```
from gen_ai_hub.document_grounding.models.pipeline import ManualPipelineTrigger



pipeline_id = '<PIPELINE_ID>'



status = pipelines.get_pipeline_status(pipeline_id)



trigger_req = ManualPipelineTrigger()

trigger_res = pipelines.trigger_pipeline(pipeline_id, trigger_req)
```

### Executions and Documents[​](#executions-and-documents "Direct link to Executions and Documents")

```
execs = pipelines.get_pipeline_executions(pipeline_id, top=20)



execution_id = '<EXECUTION_ID>'

execution = pipelines.get_pipeline_execution_by_id(pipeline_id, execution_id)



docs = pipelines.get_execution_documents(pipeline_id, execution_id, top=50)



document_id = '<DOCUMENT_ID>'

doc = pipelines.get_execution_document_by_id(pipeline_id, execution_id, document_id)



pipeline_docs = pipelines.get_pipeline_documents(pipeline_id, top=50)

pipeline_doc = pipelines.get_pipeline_document_by_id(pipeline_id, document_id)
```

## Vector API[​](#vector-api "Direct link to Vector API")

### List Collections[​](#list-collections "Direct link to List Collections")

```
collections = vector.get_collections(top=50)
```

### Create a Collection[​](#create-a-collection "Direct link to Create a Collection")

```
from gen_ai_hub.document_grounding.models.vector import CollectionCreateRequest, EmbeddingConfig



create_req = CollectionCreateRequest(

    title='My SDK Demo Collection',

    embeddingConfig=EmbeddingConfig(modelName='text-embedding-3-large'),

    metadata=[],

)

create_res = vector.create_collection(create_req)
```

### Add, Update and Delete Documents[​](#add-update-and-delete-documents "Direct link to Add, Update and Delete Documents")

```
from gen_ai_hub.document_grounding.models.vector import (

    DocumentsCreateRequest, DocumentsUpdateRequest,

    TextOnlyBaseChunk, BaseDocument, VectorKeyValueListPair

)



collection_id = '<COLLECTION_ID>'



doc = BaseDocument(

    chunks=[TextOnlyBaseChunk(content='Hello from SDK Vector API', metadata=[])],

    metadata=[VectorKeyValueListPair(key='source', value=['notebook'])],

)



created = vector.create_documents(collection_id, DocumentsCreateRequest(documents=[doc]))

documents = vector.get_documents(collection_id, top=20)

document_id = documents.resources[0].id



vector.delete_document(collection_id, document_id)
```

### Text Search[​](#text-search "Direct link to Text Search")

```
from gen_ai_hub.document_grounding.models.vector import (

    TextSearchRequest, VectorSearchFilter, VectorSearchConfiguration

)



search_req = TextSearchRequest(

    query='Hello',

    filters=[

        VectorSearchFilter(

            id='f1',

            collectionIds=[collection_id],

            configuration=VectorSearchConfiguration(maxChunkCount=5, maxDocumentCount=3),

            documentMetadata=[],

            chunkMetadata=[],

            collectionMetadata=[],

        )

    ],

)

search_res = vector.search(search_req)
```

## Retrieval API[​](#retrieval-api "Direct link to Retrieval API")

### List Repositories[​](#list-repositories "Direct link to List Repositories")

```
repos = retrieval.get_data_repositories(top=50)



repo_id = '<DATA_REPOSITORY_ID>'

repo = retrieval.get_data_repository_by_id(repo_id)
```

### Retrieval Search[​](#retrieval-search "Direct link to Retrieval Search")

```
from gen_ai_hub.document_grounding.models.retrieval import (

    RetrievalSearchInput, RetrievalSearchFilter, RetrievalSearchConfiguration

)



retrieval_req = RetrievalSearchInput(

    query='How to configure Document Grounding?',

    filters=[

        RetrievalSearchFilter(

            id='r1',

            dataRepositoryType='help.sap.com',

            searchConfiguration=RetrievalSearchConfiguration(maxChunkCount=5, maxDocumentCount=3),

            dataRepositories=[],

        )

    ],

)

retrieval_res = retrieval.search(retrieval_req)
```
