import React from 'react';
import OriginalPre from '@theme-original/MDXComponents/Pre';
import { useThemeConfig } from '@docusaurus/theme-common';
import {
  CodeBlockContextProvider,
  createCodeBlockMetadata
} from '@docusaurus/theme-common/internal';
import Container from '@theme/CodeBlock/Container';
import Buttons from '@theme/CodeBlock/Buttons';
// Reaches into compiled output — not a public API, check on major Docusaurus upgrades
import styles from '@docusaurus/theme-classic/lib/theme/CodeBlock/Layout/styles.module.css';

function ShikiPreWithButtons({ code, ...preProps }) {
  const { prism } = useThemeConfig();
  // Strips prism magic comments from code to be copied
  const metadata = createCodeBlockMetadata({
    code,
    magicComments: prism.magicComments
  });

  return (
    <CodeBlockContextProvider
      metadata={metadata}
      // Required by CodeBlockContextProvider; isEnabled/isCodeScrollable=false hides the word-wrap button.
      wordWrap={{ isEnabled: false, isCodeScrollable: false }}
    >
      <Container as="div" className={styles.codeBlockContent}>
        <pre {...preProps} />
        <Buttons />
      </Container>
    </CodeBlockContextProvider>
  );
}

export default function Pre(props) {
  if (props.className?.includes('shiki')) {
    const { 'data-raw-code': code = '', ...preProps } = props;
    return <ShikiPreWithButtons code={code} {...preProps} />;
  }
  return <OriginalPre {...props} />;
}
