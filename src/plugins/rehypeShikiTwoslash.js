/**
 * Rehype plugin that runs `@shikijs/rehype` with the `@shikijs/twoslash`
 * transformer plus a small custom transformer that adds a copy button to
 * every code block. Replaces both Prism (default Docusaurus highlighter)
 * and `starry-night` (the highlighter bundled with `rehype-twoslash`) so
 * all code blocks share one consistent theme.
 *
 * `@shikijs/rehype` and `@shikijs/twoslash` are ESM-only, so this CommonJS
 * wrapper loads them via dynamic `import()` and returns an async unified
 * transformer. The dynamic import resolves once and is cached for
 * subsequent calls.
 *
 * `​```js reference` blocks (handled by `@saucelabs/theme-github-codeblock`
 * to inline code from GitHub at runtime) are intentionally skipped here:
 * Shiki would otherwise pre-render the literal URL as syntax-highlighted
 * JavaScript and the saucelabs theme would never get a chance to fetch
 * the real source. We hide those blocks from `@shikijs/rehype` by
 * temporarily stripping their `language-*` class, then put it back
 * afterwards so Docusaurus's default `CodeBlock` still sees the language.
 */

let pluginPromise;

/**
 * Shiki transformer that adds a copy-to-clipboard button next to each code
 * block, and replaces `github-light`'s pure-white background with a softer
 * GitHub-style gray so blocks stand out from page content. The raw source
 * is embedded as a `data-code` attribute on the button so a small client
 * module can copy it without parsing the DOM.
 *
 * The wrapping is done in the `root` hook so it runs after
 * `@shikijs/twoslash` has finished adding its popover siblings — the
 * resulting structure is:
 *
 *   <div class="code-block">
 *     <button class="code-block-copy-button" data-code="…">⧉</button>
 *     <pre class="shiki …">…</pre>
 *     …twoslash popover divs…
 *   </div>
 */
function transformerCodeBlockChrome() {
  const lightBg = '#f6f8fa';

  return {
    name: 'code-block-chrome',
    pre(node) {
      // Shiki emits `--shiki-light-bg: #fff` inline. Override to a softer
      // GitHub-style gray that stands out from the page background.
      const style = node.properties?.style;
      if (typeof style === 'string') {
        node.properties.style = style.replace(
          /--shiki-light-bg:\s*[^;]+;?/,
          `--shiki-light-bg: ${lightBg};`
        );
      }
    },
    root(root) {
      const source = this.source;
      const button = {
        type: 'element',
        tagName: 'button',
        properties: {
          className: ['code-block-copy-button'],
          type: 'button',
          'aria-label': 'Copy code to clipboard',
          'data-code': source
        },
        children: [
          {
            type: 'element',
            tagName: 'span',
            properties: {
              className: ['code-block-copy-icon'],
              'aria-hidden': 'true'
            },
            // Icon glyphs come from CSS `::before`/`::after` so we can
            // cross-fade between copy and copied states without layout shift.
            children: []
          }
        ]
      };

      const wrapper = {
        type: 'element',
        tagName: 'div',
        properties: { className: ['code-block'] },
        children: [button, ...root.children]
      };

      return { ...root, children: [wrapper] };
    }
  };
}

async function loadPlugin() {
  const [{ default: rehypeShiki }, { transformerTwoslash }] = await Promise.all(
    [import('@shikijs/rehype'), import('@shikijs/twoslash')]
  );

  // Match Docusaurus's existing Prism choices: github (light) + dracula (dark).
  // Shiki bundles both under the same names.
  return rehypeShiki({
    themes: {
      light: 'github-light',
      dark: 'dracula'
    },
    defaultColor: false,
    transformers: [
      transformerTwoslash({
        explicitTrigger: true, // only run on ```ts twoslash blocks
        renderer: undefined // use the default rich-html renderer
      }),
      transformerCodeBlockChrome()
    ]
  });
}

/**
 * Walk a HAST tree and yield every `<code>` element that lives directly
 * inside a `<pre>` (i.e. fenced code blocks, not inline code).
 */
function* iterateFencedCode(node) {
  if (!node || typeof node !== 'object') return;
  if (
    node.type === 'element' &&
    node.tagName === 'pre' &&
    Array.isArray(node.children)
  ) {
    const head = node.children[0];
    if (head?.type === 'element' && head.tagName === 'code') {
      yield head;
    }
  }
  if (Array.isArray(node.children)) {
    for (const child of node.children) yield* iterateFencedCode(child);
  }
}

/**
 * Pull the meta string off a `<code>` node. Different MDX/markdown chains
 * stash it in different places — both are checked for safety.
 */
function getMeta(code) {
  return code.data?.meta ?? code.properties?.metastring ?? '';
}

/**
 * `​```js reference …` blocks should be left alone for the saucelabs
 * `@theme/CodeBlock` swizzle to fetch from GitHub at runtime. We hide them
 * from `@shikijs/rehype` by stripping their `language-*` class on the way
 * in (Shiki bails when no language is resolved) and restoring it on the
 * way out so Docusaurus's downstream `CodeBlock` still sees the language.
 */
function maskReferenceBlocks(tree) {
  /** @type {Array<{code: any, languageClass: string}>} */
  const masked = [];
  for (const code of iterateFencedCode(tree)) {
    const meta = getMeta(code);
    if (!/\breference\b/.test(meta)) continue;
    const classes = code.properties?.className;
    const list = Array.isArray(classes) ? classes : classes ? [classes] : [];
    const languageClass = list.find(
      c => typeof c === 'string' && c.startsWith('language-')
    );
    if (!languageClass) continue;
    code.properties.className = list.filter(c => c !== languageClass);
    masked.push({ code, languageClass });
  }
  return masked;
}

function unmaskReferenceBlocks(masked) {
  for (const { code, languageClass } of masked) {
    const list = code.properties?.className;
    code.properties.className = Array.isArray(list)
      ? [...list, languageClass]
      : [languageClass];
  }
}

module.exports = function rehypeShikiTwoslash() {
  return async function transformer(tree, file) {
    if (!pluginPromise) {
      pluginPromise = loadPlugin();
    }
    const plugin = await pluginPromise;
    const masked = maskReferenceBlocks(tree);
    try {
      return await plugin(tree, file);
    } finally {
      unmaskReferenceBlocks(masked);
    }
  };
};
