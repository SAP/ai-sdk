import React from 'react';
import OriginalElement from '@theme-original/CodeBlock/Content/Element';

// When Shiki processes a code block the <code> element has no className and
// its children are already highlighted spans. Docusaurus would re-wrap it in
// <Container><code class="codeBlockLines">...</code></Container>, which puts
// a floated <code> element above twoslash popup <span>s and intercepts
// pointer events. Pass Shiki children straight through — the parent <pre
// class="shiki ..."> (rendered by our MDXComponents/Pre swizzle) provides the
// container, Prism-style padding, and scroll behaviour.
export default function CodeBlockElement({ children, className }) {
  if (!className) {
    return <>{children}</>;
  }
  return <OriginalElement className={className}>{children}</OriginalElement>;
}
