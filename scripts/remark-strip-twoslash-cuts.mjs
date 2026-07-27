import { visit } from 'unist-util-visit';

const cut = /^\s*\/\/\s*---cut---\s*$/;
const cutBefore = /^\s*\/\/\s*---cut-before---\s*$/;
const cutStart = /^\s*\/\/\s*---cut-start---\s*$/;
const cutEnd = /^\s*\/\/\s*---cut-end---\s*$/;
const cutAfter = /^\s*\/\/\s*---cut-after---\s*$/;

/**
 * Remark plugin that strips twoslash cut directives from fenced code blocks
 * so they don't appear in the rendered output.
 * https://twoslash.netlify.app/refs/notations#cutting-a-code-sample
 *
 */
export default function remarkStripTwoslashCuts() {
  return tree => {
    visit(tree, 'code', node => {
      let lines = node.value.split('\n');

      const cutIdx = lines.findLastIndex(l => cut.test(l) || cutBefore.test(l));
      const cutAfterIdx = lines.findIndex(l => cutAfter.test(l));

      lines = lines.slice(
        cutIdx + 1,
        cutAfterIdx === -1 ? undefined : cutAfterIdx
      );

      let startIdx;
      while ((startIdx = lines.findIndex(l => cutStart.test(l))) !== -1) {
        const endIdx = lines.findIndex(
          (l, i) => i > startIdx && cutEnd.test(l)
        );
        lines = [...lines.slice(0, startIdx), ...lines.slice(endIdx + 1)];
      }

      node.value = lines.join('\n');
    });
  };
}
