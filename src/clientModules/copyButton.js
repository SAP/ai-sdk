/**
 * Client module that wires up copy-to-clipboard for buttons emitted by
 * the `transformerCopyButton` Shiki transformer. Each button carries the
 * raw code in its `data-code` attribute. Re-runs on every Docusaurus
 * route change so dynamically loaded pages get listeners too.
 */

const COPIED_CLASS = 'code-block-copy-button--copied';
const RESET_MS = 1500;

async function copy(text) {
  if (navigator.clipboard) {
    return navigator.clipboard.writeText(text);
  }
  // Non-secure-context fallback — same approach Docusaurus uses.
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.setAttribute('readonly', '');
  ta.style.position = 'absolute';
  ta.style.left = '-9999px';
  document.body.appendChild(ta);
  ta.select();
  document.execCommand('copy');
  ta.remove();
}

function onClick(event) {
  const button = event.currentTarget;
  const code = button.dataset.code;
  if (typeof code !== 'string') return;
  copy(code).then(() => {
    button.classList.add(COPIED_CLASS);
    setTimeout(() => button.classList.remove(COPIED_CLASS), RESET_MS);
  });
}

export function onRouteDidUpdate() {
  for (const button of document.querySelectorAll(
    '.code-block-copy-button:not([data-copy-bound])'
  )) {
    button.addEventListener('click', onClick);
    button.dataset.copyBound = 'true';
  }
}
