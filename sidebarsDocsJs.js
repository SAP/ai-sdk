module.exports = {
  docsJsSidebar: [
    'overview-cloud-sdk-for-ai-js',
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
            'foundation-models/openai/embedding'
          ]
        }
      ]
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
      label: 'Tutorials',
      items: [
        'tutorials/getting-started-with-agents',
        'tutorials/using-scoped-prompt-registry-templates-with-headers',
        {
          type: 'link',
          label: 'TechEd: Build Your Own AI Agent',
          href: 'https://github.com/SAP-samples/teched2025-AI160'
        }
      ]
    },
    'error-handling',
    'release-notes',
    'upgrade-guide',
    'frequently-asked-questions',
    {
      type: 'link',
      label: 'npm',
      href: 'https://www.npmjs.com/org/sap-ai-sdk'
    }
  ]
};
