module.exports = {
  env: {
    browser: true,
    es6: true
  },
  extends: ['plugin:react/recommended', 'prettier'],
  settings: {
    react: {
      version: 'detect'
    }
  },
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly'
  },
  parserOptions: {
    ecmaFeatures: {
      jsx: true
    },
    ecmaVersion: 11,
    sourceType: 'module'
  },
  plugins: ['react', 'prettier'],
  rules: {
    'react/prop-types': 'off'
  },
  ignorePatterns: ['build/**', 'node_modules/**', 'static/**']
};
