module.exports = {
  docsJavaSidebar: [
    'overview-cloud-sdk-for-ai-java',
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
      label: 'Spring AI',
      items: ['spring-ai/orchestration', 'spring-ai/openai']
    },
    {
      type: 'category',
      label: 'AI Core Services',
      items: [
        'ai-core/ai-core-deployment',
        'ai-core/document-grounding',
        'ai-core/prompt-registry'
      ]
    },
        {
          type: 'category',
          label: 'Tutorials',
          items: [
            'tutorials/agentic-workflows'
          ]
        },
    'release-notes',
    'frequently-asked-questions',
    {
      type: 'link',
      label: 'Maven Central',
      href: 'https://central.sonatype.com/search?q=g:com.sap.cloud.sdk*&smo=true'
    }
  ]
};
