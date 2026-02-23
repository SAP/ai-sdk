// Get the current version label from docusaurus config
const docusaurusConfig = require('./docusaurus.config.js');
const jsDocsPlugin = docusaurusConfig.plugins.find(
  plugin => Array.isArray(plugin) && plugin[1]?.id === 'docs-js'
);
const currentVersionLabel = jsDocsPlugin?.[1]?.versions?.current?.label || 'v2';

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
    'rpt',
    {
      type: 'category',
      label: 'Tutorials',
      items: [
        'tutorials/getting-started-with-agents',
        'tutorials/using-scoped-prompt-registry-templates',
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
      href: `pathname:///api/${currentVersionLabel}/index.html`
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