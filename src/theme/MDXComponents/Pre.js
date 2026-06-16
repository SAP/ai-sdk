import React from 'react';

/**
 * `@shikijs/rehype` emits `<pre class="shiki">…</pre>` at build time and
 * we want that wrapper preserved. Other code blocks (e.g. `​```js reference`
 * blocks intercepted by `@saucelabs/theme-github-codeblock`) need to reach
 * `@theme/CodeBlock` via our `MDXComponents/Code` so the saucelabs swizzle
 * can fetch GitHub source at runtime — for those, we unwrap the way the
 * default Docusaurus `Pre` does so the wrapping `<pre>` is provided by
 * `@theme/CodeBlock` instead.
 *
 * Heuristic: if the inner `<code>` has React-element children, Shiki ran;
 * keep the `<pre>` wrapper. Otherwise unwrap and let `Code` decide.
 */
function isShikiPre(children) {
  for (const child of React.Children.toArray(children)) {
    if (!React.isValidElement(child)) continue;
    const grand = child.props?.children;
    if (React.Children.toArray(grand).some(g => React.isValidElement(g))) {
      return true;
    }
  }
  return false;
}

export default function MDXPre(props) {
  return isShikiPre(props.children) ? (
    <pre {...props} />
  ) : (
    <>{props.children}</>
  );
}
