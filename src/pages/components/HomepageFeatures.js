import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: <>SAP Cloud SDK for AI (Java)</>,
    link: 'docs/java/getting-started',
    Svg: () => <span style={{ fontSize: '200px' }}>☕️</span>,
    badge: (
      <>
        <a href="https://central.sonatype.com/search?smo=true&namespace=com.sap.ai.sdk">
          <img
            alt="Maven Central Version"
            src="https://img.shields.io/maven-central/v/com.sap.ai.sdk/core?color=dark-green"
          />
        </a>
        &nbsp;&nbsp;
        <a href="https://central.sonatype.com/search?smo=true&namespace=com.sap.ai.sdk">
          <img
            alt="Maven Central License"
            src="https://img.shields.io/npm/l/%40sap-ai-sdk%2Fai-api?color=dark-green"
          />
        </a>
      </>
    ),
    description: (
      <div data-nosnippet>
        <a href="docs/java/getting-started">Get Started</a>
      </div>
    )
  },
  {
    title: <>SAP Cloud SDK for AI (JavaScript)</>,
    link: 'docs/js/getting-started',
    Svg: () => <span style={{ fontSize: '200px' }}>🚀</span>,
    badge: (
      <>
        <a href="https://www.npmjs.com/org/sap-ai-sdk">
          <img
            alt="npm Version"
            src="https://img.shields.io/npm/v/%40sap-ai-sdk%2Fai-api?color=dark-green"
          />
        </a>
        &nbsp;&nbsp;
        <a href="https://www.npmjs.com/org/sap-ai-sdk">
          <img
            alt="npm License"
            src="https://img.shields.io/npm/l/%40sap-ai-sdk%2Fai-api?color=dark-green"
          />
        </a>
      </>
    ),
    description: (
      <div data-nosnippet>
        <a href="docs/js/getting-started">Get Started</a>
      </div>
    )
  },
  {
    title: <>SAP Cloud SDK for AI (Python)</>,
    link: 'https://help.sap.com/doc/generative-ai-hub-sdk/CLOUD/en-US/index.html',
    Svg: () => <span style={{ fontSize: '200px' }}>🐍</span>,
    badge: (
      <>
        <a href="https://pypi.org/project/sap-ai-sdk-gen/">
          <img
            alt="PyPI Version"
            src="https://img.shields.io/pypi/v/sap-ai-sdk-gen?color=dark-green"
          />
        </a>
        &nbsp;&nbsp;
        <a href="https://pypi.org/project/generative-ai-hub-sdk/">
          <img
            alt="PyPI License"
            src="https://img.shields.io/pypi/l/sap-ai-sdk-gen?color=dark-green"
          />
        </a>
      </>
    ),
    description: (
      <div data-nosnippet>
        <a href="https://help.sap.com/doc/generative-ai-hub-sdk/CLOUD/en-US/index.html">
          Get Started
        </a>
      </div>
    )
  }
];

function Feature({ Svg, link, badge, title, description }) {
  return (
    <div className={clsx('col')}>
      <div
        className="text--center"
        style={{ height: '300px', overflow: 'hidden' }}
      >
        <a href={link} style={{ textDecoration: 'none' }}>
          <Svg alt={title} />
        </a>
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        {badge || ''}
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
