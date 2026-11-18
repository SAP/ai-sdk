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
import { readFile, glob } from 'node:fs/promises';
import { join, dirname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import ts from 'typescript';

const require = createRequire(import.meta.url);
// TS7 ships lib declarations in a separate @typescript/old package; resolve it
// at runtime so TSVFS can locate individual lib.*.d.ts files.
let tsLibDirectory;
try {
  tsLibDirectory = dirname(
    require.resolve('@typescript/old/lib/typescript.js')
  );
} catch {
  // Pre-TS7: lib files live alongside typescript.js
  tsLibDirectory = undefined;
}

const __dirname = dirname(fileURLToPath(import.meta.url));
const repoRoot = join(__dirname, '..');
const docsDir = join(repoRoot, 'docs-js');
const configPath = join(docsDir, 'twoslash-config.json');

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
  const text = Array.isArray(message)
    ? message
        .map(e => `Line ${(e.line ?? 0) + 1}: TS${e.code} ${e.text}`)
        .join('\n  ')
    : message;
  console.error(
    `\n✗ ${relative(process.cwd(), filePath)} (block starting at line ${line})`
  );
  console.error(`  ${text}`);
}

async function main() {
  const config = ts.readConfigFile(configPath, ts.sys.readFile).config;
  const { include = [], exclude = [], files: explicitFiles = [] } = config;
  const { options } = ts.parseJsonConfigFileContent(config, ts.sys, docsDir);

  const included = await Array.fromAsync(
    glob(include, { cwd: docsDir, exclude })
  );

  const files = [...included, ...explicitFiles].map(f => join(docsDir, f));

  if (!files.length) {
    console.error('No files matched the file patterns in twoslash-config.json');
    process.exit(1);
  }

  const twoslasher = createTwoslasher({
    vfsRoot: repoRoot,
    compilerOptions: options,
    extraFiles: { 'package.json': '{"type":"module"}' },
    ...(tsLibDirectory ? { tsLibDirectory } : {})
  });

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
            reportError(filePath, line, result.errors);
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
