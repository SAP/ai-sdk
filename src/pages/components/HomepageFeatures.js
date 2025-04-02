import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: <>SAP Cloud SDK for AI Java</>,
    link: 'docs/java/getting-started',
    Svg: () => <span style={{ fontSize: '200px' }}>☕️</span>,
    badge: (
      <a href="https://central.sonatype.com/search?smo=true&namespace=com.sap.ai.sdk">
        <img
          alt="Maven Central Version"
          src="https://img.shields.io/maven-central/v/com.sap.ai.sdk/core?color=dark-green"
        />
      </a>
    ),
    description: (
      <div data-nosnippet>
        <b>
          🚧 Work in Progress: Documentation Portal 🚧
          <br />
          We are actively working on the documentation portal. Expect frequent
          updates and changes.
        </b>
        <br />
        <a href="docs/java/getting-started">
          Get started with the SAP Cloud SDK for AI for Java.
        </a>
      </div>
    )
  },
  {
    title: <>SAP Cloud SDK for AI JavaScript</>,
    link: 'docs/js/getting-started',
    Svg: () => <span style={{ fontSize: '200px' }}>🚀</span>,
    badge: (
      <img
        alt="NPM Version"
        src="https://img.shields.io/npm/v/%40sap-ai-sdk%2Fai-api?color=dark-green"
      />
    ),
    description: (
      <div data-nosnippet>
        <b>
          🚧 Work in Progress: Documentation Portal 🚧
          <br />
          We are actively working on the documentation portal. Expect frequent
          updates and changes.
        </b>
        <br />
        <a href="docs/js/getting-started">
          Get started with the SAP Cloud SDK for AI for JavaScript
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
