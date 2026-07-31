import { visit } from 'unist-util-visit';

const isCutDirective = (s, l) =>
  new RegExp(`^\\s*\\/\\/\\s*---cut${s}---\\s*$`).test(l);
const twoslashNotationRe = /^\s*\/\/\s*(@(?!ts-)[\w]+|\^\?|\^\||\^\^\^)\s*$/;

// notations with visual effects that warrant a warning when stripped
const warnNotations = new Set([
  '@errors',
  '@showEmit',
  '@showEmittedFile',
  '@filename',
  '^?',
  '^|',
  '^^^'
]);

function stripUnsupported(lines, fileInfo, warn) {
  return lines.filter((l, i) => {
    const match = twoslashNotationRe.exec(l);
    if (warnNotations.has(match?.[1]))
      warn(
        `remark-strip-twoslash-cuts: unsupported twoslash notation "${match[1]}" at ${fileInfo} line ${i + 1} — stripped`
      );
    return !match;
  });
}

function cutBefore(lines) {
  const idx = lines.findLastIndex(l => isCutDirective('(-before)?', l));
  return idx === -1 ? lines : lines.slice(idx + 1);
}

function cutAfter(lines) {
  const idx = lines.findIndex(l => isCutDirective('-after', l));
  return idx === -1 ? lines : lines.slice(0, idx);
}

function cutBlock(lines, startIdx, fileInfo) {
  const relativeEndIdx = lines
    .slice(startIdx + 1)
    .findIndex(l => isCutDirective('-end', l));
  if (relativeEndIdx === -1) {
    throw new Error(
      `remark-strip-twoslash-cuts: ---cut-start--- has no matching ---cut-end--- (${fileInfo})`
    );
  }
  const endIdx = startIdx + 1 + relativeEndIdx;
  return [...lines.slice(0, startIdx), ...lines.slice(endIdx + 1)];
}

function cutBlocks(lines, fileInfo) {
  const starts = lines.flatMap((l, i) =>
    isCutDirective('-start', l) ? [i] : []
  );
  const cutLines = starts.reduceRight(
    (acc, startIdx) => cutBlock(acc, startIdx, fileInfo),
    lines
  );
  if (cutLines.some(l => isCutDirective('-end', l))) {
    throw new Error(
      `remark-strip-twoslash-cuts: ---cut-end--- has no matching ---cut-start--- (${fileInfo})`
    );
  }
  return cutLines;
}

/**
 * Remark plugin that strips twoslash cut directives from fenced code blocks
 * so they don't appear in the rendered output.
 * https://twoslash.netlify.app/refs/notations#cutting-a-code-sample
 *
 */
export default function stripTwoslashCutDirectives() {
  return (tree, file) => {
    visit(tree, 'code', node => {
      if (!node.meta?.includes('twoslash')) return;
      const fileInfo = `${file.path ?? 'unknown'}:${node.position?.start.line ?? '?'}`;
      const warn = msg => file.message(msg);
      let lines = node.value.split('\n');
      lines = stripUnsupported(lines, fileInfo, warn);
      lines = cutBefore(lines);
      lines = cutAfter(lines);
      lines = cutBlocks(lines, fileInfo);
      node.value = lines.join('\n');
    });
  };
}
