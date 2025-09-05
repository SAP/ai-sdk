const { ProvidePlugin } = require('webpack');

// We have to polyfill some Node APIs because Docusaurus migrated to Webpack 5
// This is mainly required because of remark related modules which don't load otherwise
// Also process is required for local runs
class ESMPolyfillWrapper {
  apply(compiler) {
    compiler.options.plugins.push(
      new ProvidePlugin({
        process: 'process/browser.js'
      })
    );
  }
}

/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
  title: 'SAP Cloud SDK for AI',
  tagline: 'The one-stop shop for integrating AI into SAP Cloud applications.',
  url: 'https://sap.github.io/',
  baseUrl: '/ai-sdk/',
  onBrokenLinks: 'ignore',
  onBrokenMarkdownLinks: 'throw',
  favicon: 'img/AI-SDK-Logo.svg',
  organizationName: 'SAP',
  projectName: 'ai-sdk',
  trailingSlash: false,
  themes: ['@saucelabs/theme-github-codeblock'],
  themeConfig: {
    colorMode: {
      respectPrefersColorScheme: true,
      disableSwitch: true
    },
    prism: {
      additionalLanguages: ['powershell', 'java', 'groovy'],
      theme: require('prism-react-renderer').themes.github,
      darkTheme: require('prism-react-renderer').themes.dracula
    },
    algolia: {
      apiKey: '441c57554e5a0ca9338cc9f047fb10c8',
      indexName: 'sap_cloud-sdk-ai',
      appId: 'E4A268JVO0',
      algoliaOptions: {} // Optional, if provided by Algolia
    },
    navbar: {
      title: 'SAP Cloud SDK for AI',
      logo: {
        alt: 'SAP Cloud SDK for AI',
        src: 'img/AI-SDK-Logo.svg',
        srcDark: 'img/AI-SDK-Logo.svg'
      },
      items: [
        {
          label: 'Overview',
          type: 'doc',
          docId: 'overview-cloud-sdk-for-ai',
          position: 'left'
        },
        {
          label: '☕ Java',
          to: 'docs/java/overview-cloud-sdk-for-ai-java',
          position: 'left',
          docsPluginId: 'docs-java',
          activeBasePath: 'docs/java',
          sdkSwitch: true
        },
        {
          label: '🚀 JavaScript',
          to: 'docs/js/overview-cloud-sdk-for-ai-js',
          position: 'left',
          docsPluginId: 'docs-js',
          activeBasePath: 'docs/js',
          sdkSwitch: true
        },
        {
          type: 'docsVersionDropdown',
          position: 'right',
          docsPluginId: 'docs-js'
        },
        {
          type: 'docsVersionDropdown',
          position: 'right',
          docsPluginId: 'docs-java'
        }
      ]
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'SAP Cloud SDK for AI Java',
          items: [
            {
              label: 'Tutorials',
              href: 'https://developers.sap.com/group.sap-ai-core-generative.html'
            },
            {
              label: 'Maven',
              href: 'https://central.sonatype.com/search?smo=true&namespace=com.sap.ai.sdk'
            },
            {
              label: 'GitHub',
              href: 'https://github.com/SAP/ai-sdk-java'
            },
            {
              label: 'Sample Code',
              href: 'https://github.com/SAP/ai-sdk-java/tree/main/sample-code/spring-app'
            },
            {
              label: 'Support',
              to: 'docs/overview/get-support'
            }
          ]
        },
        {
          title: 'SAP Cloud SDK for AI JavaScript',
          items: [
            {
              label: 'Tutorials',
              href: 'https://developers.sap.com/group.sap-ai-core-generative.html'
            },
            {
              label: 'npm',
              href: 'https://www.npmjs.com/org/sap-ai-sdk'
            },
            {
              label: 'GitHub',
              href: 'https://github.com/SAP/ai-sdk-js'
            },
            {
              label: 'Sample Code',
              href: 'https://github.com/SAP/ai-sdk-js/tree/main/sample-code'
            },
            {
              label: 'Support',
              to: 'docs/overview/get-support'
            }
          ]
        },
        {
          title: 'SAP Cloud SDK for AI Python',
          items: [
            {
              label: 'Tutorials',
              href: 'https://developers.sap.com/group.sap-ai-core-generative.html'
            },
            {
              label: 'PyPI',
              href: 'https://pypi.org/project/generative-ai-hub-sdk/'
            }
          ]
        },
        {
          title: 'Additional Resources',
          items: [
            {
              label: 'SAP Cloud SDK (Java) - GitHub',
              href: 'https://github.com/SAP/cloud-sdk-java'
            },
            {
              label: 'SAP Cloud SDK (JavaScript) - GitHub',
              href: 'https://github.com/SAP/cloud-sdk-js'
            },
            {
              label: 'SAP Cloud SDK Documentation',
              href: 'https://sap.github.io/cloud-sdk/'
            }
          ]
        }
      ],
      copyright: `Copyright © ${new Date().getFullYear()} SAP SE or an SAP affiliate company. All rights reserved.`
    },
    codeblock: {
      showGithubLink: true,
      githubLinkLabel: 'View on GitHub',
      showRunmeLink: false
    }
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebarsDocsCommon.js'),
          editUrl: 'https://github.com/SAP/ai-sdk/edit/main',
          routeBasePath: 'docs/overview',
          path: 'docs'
        },
        theme: {
          customCss: [require.resolve('./src/css/custom.css')]
        },
        sitemap: {
          changefreq: 'weekly',
          priority: 0.5,
          ignorePatterns: ['/ai-sdk/api/**', '/ai-sdk/components/**']
        }
      }
    ]
  ],
  customFields: {},
  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'docs-java',
        path: 'docs-java',
        editUrl: 'https://github.com/SAP/ai-sdk/edit/main',
        routeBasePath: 'docs/java',
        sidebarPath: require.resolve('./sidebarsDocsJava.js'),
        lastVersion: 'current',
        versions: {
          current: {
            label: 'v1',
            badge: false
          }
        }
      }
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'docs-js',
        path: 'docs-js',
        editUrl: 'https://github.com/SAP/ai-sdk/edit/main',
        routeBasePath: 'docs/js',
        sidebarPath: require.resolve('./sidebarsDocsJs.js'),
        lastVersion: 'v1',
        versions: {
          current: {
            label: 'v2',
            banner: 'unreleased',
            badge: true
          },
          v1: {
            label: 'v1',
            badge: false
          }
        }
      }
    ],
    [
      '@docusaurus/plugin-sitemap',
      {
        id: 'sitemap-js',
        filename: 'sitemap-js.xml',
        changefreq: 'weekly',
        priority: 0.5,
        ignorePatterns: ['**/docs/java/**']
      }
    ],
    [
      '@docusaurus/plugin-sitemap',
      {
        id: 'sitemap-java',
        filename: 'sitemap-java.xml',
        changefreq: 'weekly',
        priority: 0.5,
        ignorePatterns: ['**/docs/js/**']
      }
    ],
    [
      '@docusaurus/plugin-client-redirects',
      {
        redirects: [
          // Java
          {
            from: '/docs/java/guides/ai-core-deployment',
            to: '/docs/java/ai-core/ai-core-deployment'
          },
          {
            from: '/docs/java/guides/document-grounding',
            to: '/docs/java/ai-core/document-grounding'
          },
          {
            from: '/docs/java/guides/openai-chat-completion',
            to: '/docs/java/foundation-models/openai/chat-completion'
          },
          {
            from: '/docs/java/guides/orchestration-chat-completion',
            to: '/docs/java/orchestration/chat-completion'
          },
          {
            from: '/docs/java/guides/spring-ai-integration',
            to: '/docs/java/spring-ai/orchestration'
          },
          {
            from: '/docs/java/guides/connecting-to-ai-core',
            to: '/docs/java/connecting-to-ai-core'
          },
          // JavaScript
          {
            from: '/docs/js/guides/ai-api',
            to: '/docs/js/ai-core/ai-api'
          },
          {
            from: '/docs/js/guides/document-grounding',
            to: '/docs/js/ai-core/document-grounding'
          },
          {
            from: '/docs/js/guides/prompt-registry',
            to: '/docs/js/ai-core/prompt-registry'
          },
          {
            from: '/docs/js/guides/openai-chat-completion',
            to: '/docs/js/foundation-models/openai/chat-completion'
          },
          {
            from: '/docs/js/guides/openai-chat-embedding',
            to: '/docs/js/foundation-models/openai/embedding'
          },
          {
            from: '/docs/js/guides/orchestration-chat-completion',
            to: '/docs/js/orchestration/chat-completion'
          },
          {
            from: '/docs/js/guides/langchain',
            to: '/docs/js/langchain'
          },
          {
            from: '/docs/js/guides/connecting-to-ai-core',
            to: '/docs/js/connecting-to-ai-core'
          }
        ]
      }
    ],
    function nodeWebpackPolyfillPlugin(context, options) {
      return {
        name: 'nodeWebpackPolyfill',
        configureWebpack(config, isServer) {
          return {
            plugins: [new ESMPolyfillWrapper()]
          };
        }
      };
    }
  ],
  i18n: {
    defaultLocale: 'en',
    locales: ['en']
  }
};
