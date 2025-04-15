module.exports = {
  docsJsSidebar: [
    'overview-cloud-sdk-for-ai-js',
    'getting-started',
    'connecting-to-ai-core',
    {
      type: 'category',
      label: 'Orchestration',
      items: ['orchestration/chat-completion']
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
    'error-handling',
    {
      type: 'link',
      label: 'npm',
      href: 'https://www.npmjs.com/org/sap-ai-sdk'
    }
  ]
};
