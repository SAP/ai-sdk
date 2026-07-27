module.exports = {
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
      items: [
        {
          type: 'link',
          label: 'gen_ai_hub',
          href: 'pathname:///api-python/gen_ai_hub.html'
        },
        {
          type: 'link',
          label: 'gen_ai_hub.batch_service',
          href: 'pathname:///api-python/gen_ai_hub.batch_service.html'
        },
        {
          type: 'link',
          label: 'gen_ai_hub.document_grounding',
          href: 'pathname:///api-python/gen_ai_hub.document_grounding.html'
        },
        {
          type: 'link',
          label: 'gen_ai_hub.evaluations',
          href: 'pathname:///api-python/gen_ai_hub.evaluations.html'
        },
        {
          type: 'link',
          label: 'gen_ai_hub.orchestration',
          href: 'pathname:///api-python/gen_ai_hub.orchestration.html'
        },
        {
          type: 'link',
          label: 'gen_ai_hub.orchestration_v2',
          href: 'pathname:///api-python/gen_ai_hub.orchestration_v2.html'
        },
        {
          type: 'link',
          label: 'gen_ai_hub.prompt_registry',
          href: 'pathname:///api-python/gen_ai_hub.prompt_registry.html'
        },
        {
          type: 'link',
          label: 'gen_ai_hub.proxy',
          href: 'pathname:///api-python/gen_ai_hub.proxy.html'
        }
      ]
    }
  ]
};
