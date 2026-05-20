const { createRequire } = require('module');
const require2 = createRequire(require.resolve('rehype-twoslash'));
module.exports = require('rehype-twoslash').default ?? require('rehype-twoslash');
