export default {
  docsJsSidebar: [
    'overview',
    'getting-started',
    'connecting-to-ai-core',
    {
      type: 'category',
      label: 'Orchestration',
      items: ['orchestration/chat-completion', 'orchestration/embedding']
    },
    {
      type: 'category',
      label: 'Foundation Models',
      link: {
        type: 'doc',
        id: 'foundation-models/foundation-models'
      },
      items: [
        {
          type: 'category',
          label: 'OpenAI',
          items: [
            'foundation-models/openai/chat-completion',
            'foundation-models/openai/embedding',
            'foundation-models/openai/batch'
          ]
        }
      ]
    },
    {
      type: 'category',
      label: 'OpenAI',
      link: {
        type: 'doc',
        id: 'openai/openai'
      },
      items: ['openai/realtime']
    },
    {
      type: 'category',
      label: 'LangChain',
      link: {
        type: 'doc',
        id: 'langchain/langchain'
      },
      items: ['langchain/orchestration', 'langchain/openai']
    },
    {
      type: 'category',
      label: 'AI Core Services',
      items: [
        'ai-core/ai-api',
        'ai-core/document-grounding',
        'ai-core/prompt-registry'
      ]
    },
    {
      type: 'category',
      label: 'Tabular AI',
      items: ['tabular-ai/rpt', 'tabular-ai/context-registry']
    },
    {
      type: 'category',
      label: 'Tutorials',
      items: [
        'tutorials/getting-started-agents',
        'tutorials/scoped-prompt-registry-templates',
        'tutorials/llm-batch-api',
        {
          type: 'link',
          label: 'TechEd: Build Your Own AI Agent',
          href: 'https://github.com/SAP-samples/teched2025-AI160'
        }
      ]
    },
    {
      type: 'link',
      label: 'API Reference',
      href: `pathname:///api/v2/index.html`
    },
    'error-handling',
    'release-notes',
    'release-policy',
    'upgrade-guide',
    'frequently-asked-questions',
    {
      type: 'link',
      label: 'npm',
      href: 'https://www.npmjs.com/org/sap-ai-sdk'
    }
  ]
};
