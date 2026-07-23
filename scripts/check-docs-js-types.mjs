#!/usr/bin/env node
/**
 * Type-checks TypeScript code blocks in .mdx documentation files using twoslash.
 *
 * Code blocks tagged with "ts twoslash" are extracted and run through the TypeScript
 * compiler. Any type errors cause the script to exit with code 1.
 *
 * Use the // ---cut--- directive to hide setup lines (imports, boilerplate) from the
 * rendered output while still including them for type-checking.
 */
import { createTwoslasher } from 'twoslash';
import { readFile, readdir } from 'fs/promises';
import { join, relative, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const repoRoot = join(__dirname, '..');
const docsDir = join(repoRoot, 'docs-js');
const nm = join(repoRoot, 'node_modules');

import ts from 'typescript';

const compilerOptions = {
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

async function findMdxFiles(dir) {
  return (await readdir(dir, { recursive: true, withFileTypes: true }))
    .filter(
      e => e.isFile() && (e.name.endsWith('.mdx') || e.name.endsWith('.md'))
    )
    .map(e => join(e.parentPath, e.name));
}

function extractTwoslashBlocks(content, filePath) {
  // Match ```ts twoslash or ```typescript twoslash fenced code blocks
  const fence = /^```(?:ts|typescript)\s+twoslash\s*\n([\s\S]*?)^```/gm;
  return [...content.matchAll(fence)].map(match => ({
    code: match[1],
    line: content.slice(0, match.index).split('\n').length,
    filePath
  }));
}

function reportError(filePath, line, message) {
  console.error(
    `\n✗ ${relative(process.cwd(), filePath)} (block starting at line ${line})`
  );
  console.error(`  ${message}`);
}

async function main() {
  const twoslasher = createTwoslasher({
    compilerOptions,
    extraFiles: { 'package.json': '{"type":"module"}' }
  });

  const files = await findMdxFiles(docsDir);

  const results = await Promise.all(
    files.map(async file => {
      const content = await readFile(file, 'utf8');
      const blocks = extractTwoslashBlocks(content, file);
      let failed = 0;
      blocks.forEach(({ code, line, filePath }) => {
        try {
          const result = twoslasher(code, 'ts');
          if (result.errors.length) {
            failed++;
            reportError(
              filePath,
              line,
              result.errors
                .map(e => `Line ${(e.line ?? 0) + 1}: TS${e.code} ${e.text}`)
                .join('\n  ')
            );
          }
        } catch (e) {
          failed++;
          reportError(filePath, line, e.message);
        }
      });
      return { total: blocks.length, failed };
    })
  );

  const totalBlocks = results.reduce((sum, r) => sum + r.total, 0);
  const failed = results.reduce((sum, r) => sum + r.failed, 0);

  const passed = totalBlocks - failed;
  console.log(
    `\nChecked ${totalBlocks} twoslash block(s): ${passed} passed, ${failed} failed.`
  );

  if (failed > 0) process.exit(1);
}

await main();
