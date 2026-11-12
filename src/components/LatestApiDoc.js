import React, { useEffect } from 'react';
import { useLocation } from '@docusaurus/router';
import BrowserOnly from '@docusaurus/BrowserOnly';

function RedirectToLatestVersion({ path }) {
  useEffect(() => {
    window.location.href = path;
  }, [path]);

  return null;
}

export default function LatestApiDoc({ latestBaseUrl, versions }) {
  const explicitLatestBaseUrl = [
    ...latestBaseUrl.split('/').slice(0, -1),
    versions[0]
  ].join('/');
  const loc = useLocation();
  const newPath = loc.pathname.replace(latestBaseUrl, explicitLatestBaseUrl);
  return (
    <BrowserOnly>
      {() => <RedirectToLatestVersion path={newPath} />}
    </BrowserOnly>
  );
}
