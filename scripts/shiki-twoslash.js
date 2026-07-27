import rehypeShiki from '@shikijs/rehype';
import { transformerTwoslash } from '@shikijs/twoslash';
import { compilerOptions } from './compiler-options.js';

export const rehypeShikiTwoslash = [
  rehypeShiki,
  {
    defaultColor: false,
    themes: {
      light: 'github-light',
      dark: 'github-dark'
    },
    transformers: [
      transformerTwoslash({
        explicitTrigger: true,
        twoslashOptions: {
          compilerOptions,
          extraFiles: { 'package.json': '{"type":"module"}' }
        }
      }),
      {
        name: 'store-raw-code',
        pre(node) {
          node.properties['data-raw-code'] = this.source;
        }
      }
    ]
  }
];
