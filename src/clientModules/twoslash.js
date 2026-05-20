import { computePosition, shift } from '@floating-ui/dom';

function show(target) {
  const id = target.dataset.popoverTarget;
  const popover = document.getElementById(id);
  if (!popover) return;
  popover.showPopover();
  computePosition(target, popover, {
    placement: 'bottom-start',
    middleware: [shift({ padding: 5 })]
  }).then(({ x, y }) => {
    Object.assign(popover.style, { left: `${x}px`, top: `${y}px` });
  });
}

export function onRouteDidUpdate() {
  for (const target of document.querySelectorAll(
    '.rehype-twoslash-popover-target'
  )) {
    let timer;
    target.addEventListener('click', () => show(target));
    target.addEventListener('mouseenter', () => {
      timer = setTimeout(() => show(target), 300);
    });
    target.addEventListener('mouseleave', () => clearTimeout(timer));
    if (target.classList.contains('rehype-twoslash-autoshow')) show(target);
  }
}
