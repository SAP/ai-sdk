import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import ts from 'typescript';

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), '..');

export const compilerOptions = {
  target: ts.ScriptTarget.ES2022,
  module: ts.ModuleKind.NodeNext,
  moduleResolution: ts.ModuleResolutionKind.NodeNext,
  strict: true,
  baseUrl: repoRoot,
  paths: {
    ...Object.fromEntries(
      [
        '@langchain/core',
        '@langchain/langgraph',
        '@sap-ai-sdk/openai',
        '@sap-ai-sdk/orchestration',
        '@sap-ai-sdk/foundation-models',
        '@sap-ai-sdk/core',
        '@sap-ai-sdk/ai-api',
        '@sap-ai-sdk/document-grounding',
        '@sap-ai-sdk/langchain',
        '@sap-ai-sdk/llm-batch',
        '@sap-ai-sdk/rpt',
        '@sap-ai-sdk/prompt-registry',
        '@sap-cloud-sdk/resilience',
        '@sap-cloud-sdk/http-client',
        'langchain'
      ].map(p => [p, [`node_modules/${p}/dist/index.d.ts`]])
    ),
    // openai and zod publish types at the root, not under dist/
    openai: ['node_modules/openai/index.d.ts'],
    'openai/*': ['node_modules/openai/*.d.ts'],
    zod: ['node_modules/zod/index.d.ts'],
    '@langchain/core/*': ['node_modules/@langchain/core/dist/*.d.ts']
  }
};
