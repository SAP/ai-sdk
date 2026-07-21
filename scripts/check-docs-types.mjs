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
import { readFileSync, readdirSync, statSync } from 'fs';
import { join, relative } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const repoRoot = join(__dirname, '..');
const docsDir = join(repoRoot, 'docs-js');
const nm = join(repoRoot, 'node_modules');

const compilerOptions = {
  target: 99 /* ES2022 */,
  module: 99 /* ESNext */,
  moduleResolution: 100 /* Bundler */,
  strict: true,
  paths: {
    '@sap-ai-sdk/openai': [`${nm}/@sap-ai-sdk/openai/dist/index.d.ts`],
    '@sap-ai-sdk/orchestration': [`${nm}/@sap-ai-sdk/orchestration/dist/index.d.ts`],
    '@sap-ai-sdk/foundation-models': [`${nm}/@sap-ai-sdk/foundation-models/dist/index.d.ts`],
    '@sap-ai-sdk/core': [`${nm}/@sap-ai-sdk/core/dist/index.d.ts`],
    '@sap-ai-sdk/ai-api': [`${nm}/@sap-ai-sdk/ai-api/dist/index.d.ts`],
    'openai': [`${nm}/openai/index.d.ts`],
    'openai/*': [`${nm}/openai/*.d.ts`],
    'zod': [`${nm}/zod/index.d.ts`],
  },
};

function findMdxFiles(dir) {
  const results = [];
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) {
      results.push(...findMdxFiles(full));
    } else if (entry.endsWith('.mdx') || entry.endsWith('.md')) {
      results.push(full);
    }
  }
  return results;
}

function extractTwoslashBlocks(content, filePath) {
  const blocks = [];
  // Match ```ts twoslash or ```typescript twoslash fenced code blocks
  const fence = /^```(?:ts|typescript)\s+twoslash\s*\n([\s\S]*?)^```/gm;
  let match;
  while ((match = fence.exec(content)) !== null) {
    const lineNumber = content.slice(0, match.index).split('\n').length;
    blocks.push({ code: match[1], line: lineNumber, filePath });
  }
  return blocks;
}

const twoslasher = createTwoslasher({ compilerOptions });

const files = findMdxFiles(docsDir);
let totalBlocks = 0;
let failed = 0;

for (const file of files) {
  const content = readFileSync(file, 'utf8');
  const blocks = extractTwoslashBlocks(content, file);
  if (blocks.length === 0) continue;

  for (const { code, line, filePath } of blocks) {
    totalBlocks++;
    try {
      const result = twoslasher(code, 'ts');
      if (result.errors.length > 0) {
        failed++;
        const rel = relative(process.cwd(), filePath);
        console.error(`\n✗ ${rel} (block starting at line ${line})`);
        for (const err of result.errors) {
          console.error(`  Line ${(err.line ?? 0) + 1}: TS${err.code} ${err.text}`);
        }
      }
    } catch (e) {
      failed++;
      const rel = relative(process.cwd(), filePath);
      console.error(`\n✗ ${rel} (block starting at line ${line})`);
      console.error(`  ${e.message}`);
    }
  }
}

const passed = totalBlocks - failed;
console.log(`\nChecked ${totalBlocks} twoslash block(s): ${passed} passed, ${failed} failed.`);

if (failed > 0) process.exit(1);
