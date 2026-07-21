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
import { readFileSync, readdirSync } from 'fs';
import { join, relative, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const repoRoot = join(__dirname, '..');
const docsDir = join(repoRoot, 'docs-js');
const nm = join(repoRoot, 'node_modules');

const sdkPackages = [
  'openai',
  'orchestration',
  'foundation-models',
  'core',
  'ai-api'
];

import ts from 'typescript';

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
    zod: [`${nm}/zod/index.d.ts`]
  }
};

function findMdxFiles(dir) {
  return readdirSync(dir, { recursive: true, withFileTypes: true })
    .filter(
      e => e.isFile() && (e.name.endsWith('.mdx') || e.name.endsWith('.md'))
    )
    .map(e => join(e.parentPath ?? e.path, e.name));
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

function reportError(filePath, line, message) {
  console.error(
    `\n✗ ${relative(process.cwd(), filePath)} (block starting at line ${line})`
  );
  console.error(`  ${message}`);
}

const twoslasher = createTwoslasher({
  compilerOptions,
  extraFiles: { 'package.json': '{"type":"module"}' }
});

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
  }
}

const passed = totalBlocks - failed;
console.log(
  `\nChecked ${totalBlocks} twoslash block(s): ${passed} passed, ${failed} failed.`
);

if (failed > 0) process.exit(1);
