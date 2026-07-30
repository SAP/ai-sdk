export default {
  docsPythonSidebar: [
    'overview',
    {
      type: 'category',
      label: 'Examples',
      items: [
        'examples/gen-ai-hub',
        'examples/streaming',
        'examples/prompt-registry',
        'examples/orchestration-service',
        'examples/orchestration-service2',
        'examples/document-grounding',
        'examples/document-grounding2',
        'examples/async-examples',
        'examples/evaluations',
        'examples/batch-service',
        'examples/metering',
        'examples/ai-vs-ai'
      ]
    },
    {
      type: 'category',
      label: 'API Reference',
      collapsed: false,
      items: [
        {
          type: 'link',
          label: 'SAP Cloud SDK for AI (Python) - generative',
          href: 'pathname:///api-python/_api_doc/gen/gen_ai_hub.html'
        },
        {
          type: 'link',
          label: 'SAP AI Core SDK',
          href: 'pathname:///api-python/_api_doc/core/ai_core_sdk.html'
        },
        {
          type: 'link',
          label: 'AI API Client SDK',
          href: 'pathname:///api-python/_api_doc/base/ai_api_client_sdk.html'
        }
      ]
    }
  ]
};
