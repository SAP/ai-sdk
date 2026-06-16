import React from 'react';
import CodeBlock from '@theme/CodeBlock';
import CodeInline from '@theme/CodeInline';

/**
 * `@shikijs/rehype` already converts most fenced code blocks to fully-
 * rendered `<pre><code>...spans...</code></pre>` HTML at build time. The
 * default Docusaurus `MDXComponents/Code` would route blocks through
 * `@theme/CodeBlock` (Prism-based) and re-tokenize, losing Shiki's spans
 * and twoslash markup.
 *
 * However, some blocks are deliberately *not* highlighted by Shiki — most
 * notably `​```js reference …` blocks handled by
 * `@saucelabs/theme-github-codeblock`, which fetches code from GitHub at
 * runtime. Those need to flow through `@theme/CodeBlock` so the saucelabs
 * swizzle can intercept them.
 *
 * Heuristic: if `children` is a single string (or array of strings),
 * Shiki didn't run on this block, so we hand it to `@theme/CodeBlock`.
 * If it's already React elements (Shiki's `<span>` tree), we passthrough
 * to a plain `<code>`.
 *
 * Inline code (no newline) always uses the themed `CodeInline` —
 * see https://github.com/facebook/docusaurus/pull/9704.
 */
function shouldBeInline(props) {
  return (
    typeof props.children !== 'undefined' &&
    React.Children.toArray(props.children).every(
      el => typeof el === 'string' && !el.includes('\n')
    )
  );
}

function isShikiOutput(children) {
  // Shiki produces an element tree (top-level `<span class="line">`s).
  // Raw fenced code without Shiki has string children.
  return React.Children.toArray(children).some(el => React.isValidElement(el));
}

function PassthroughCodeBlock(props) {
  return <code {...props} />;
}

export default function MDXCode(props) {
  if (shouldBeInline(props)) {
    return <CodeInline {...props} />;
  }
  return isShikiOutput(props.children) ? (
    <PassthroughCodeBlock {...props} />
  ) : (
    <CodeBlock {...props} />
  );
}
