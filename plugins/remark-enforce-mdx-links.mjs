import { extname } from 'node:path';
import { visit } from 'unist-util-visit';

const skipPrefixes = [
  'http://',
  'https://',
  '/',
  '#',
  'mailto:',
  'pathname://'
];

/** @returns {import('unified').Plugin} */
export default function remarkEnforceMdxLinks() {
  return (tree, file) => {
    const violations = [];

    visit(tree, 'link', node => {
      // remove anchor
      const url = node.url?.split('#')?.[0];

      if (
        !url ||
        // external url
        skipPrefixes.some(p => node.url?.startsWith(p)) ||
        // file link
        extname(url)
      ) {
        return;
      }

      // slug-based link
      violations.push({ url: node.url, line: node.position?.start?.line });
    });

    if (violations.length) {
      const list = violations
        .map(v => `  line ${v.line}: [${v.url}]`)
        .join('\n');
      file.fail(
        `Relative doc links must use .mdx file paths, not slugs.\n${list}\n`
      );
    }
  };
}
