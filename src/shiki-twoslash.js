import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import rehypeShiki from '@shikijs/rehype';
import { transformerTwoslash } from '@shikijs/twoslash';
import ts from 'typescript';

const nm = join(dirname(fileURLToPath(import.meta.url)), '..', 'node_modules');

const sdkPackages = [
  'openai',
  'orchestration',
  'foundation-models',
  'core',
  'ai-api',
  'document-grounding',
  'langchain',
  'llm-batch',
  'rpt',
  'prompt-registry'
];

const compilerOptions = {
  target: ts.ScriptTarget.ES2022,
  module: ts.ModuleKind.NodeNext,
  moduleResolution: ts.ModuleResolutionKind.NodeNext,
  strict: true,
  paths: {
    ...Object.fromEntries(
      sdkPackages.map(p => [
        `@sap-ai-sdk/${p}`,
        [`${nm}/@sap-ai-sdk/${p}/dist/index.d.ts`]
      ])
    ),
    openai: [`${nm}/openai/index.d.ts`],
    'openai/*': [`${nm}/openai/*.d.ts`],
    zod: [`${nm}/zod/index.d.ts`],
    langchain: [`${nm}/langchain/dist/index.d.ts`],
    '@langchain/core': [`${nm}/@langchain/core/dist/index.d.ts`],
    '@langchain/core/*': [`${nm}/@langchain/core/dist/*.d.ts`],
    '@langchain/langgraph': [`${nm}/@langchain/langgraph/dist/index.d.ts`],
    '@sap-cloud-sdk/resilience': [
      `${nm}/@sap-cloud-sdk/resilience/dist/index.d.ts`
    ],
    '@sap-cloud-sdk/http-client': [
      `${nm}/@sap-cloud-sdk/http-client/dist/index.d.ts`
    ]
  }
};

export const rehypeShikiTwoslash = [
  rehypeShiki,
  {
    defaultColor: false,
    themes: {
      light: 'github-light',
      dark: 'github-dark'
    },
    transformers: [
      transformerTwoslash({
        explicitTrigger: true,
        twoslashOptions: {
          compilerOptions,
          extraFiles: { 'package.json': '{"type":"module"}' }
        }
      }),
      {
        name: 'store-raw-code',
        pre(node) {
          node.properties['data-raw-code'] = this.source;
        }
      }
    ]
  }
];
