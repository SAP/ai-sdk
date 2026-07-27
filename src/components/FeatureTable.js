import React from 'react';
import ReactMarkdown from 'react-markdown';
import emoji from 'remark-emoji';
import gfm from 'remark-gfm';
import { features } from './data/features.js';
import { mainFeatureTableLayout } from './data/table-layouts.js';
import Table from './Table.js';

/**
 * Generates a main feature-table in SDK overview.
 * Data (features.js) and Columns layout (table-layouts.js) come from the `data` folder.
 *
 */
export default function FeatureTable() {
  const data = React.useMemo(() => features, []);
  const columns = React.useMemo(() => mainFeatureTableLayout, []);

  return (
    <>
      <b>
        🚧 Work in Progress: Documentation Portal 🚧
        <br />
      </b>
      <br />
      <br />
      <ReactMarkdown remarkPlugins={[gfm, emoji]}>
        **Legend:** :white_check_mark: - Generally Available, :x: - Not
        Available, :wrench: - WIP/limited support, :date: - Planned, :warning: -
        Deprecated
      </ReactMarkdown>
      <Table columns={columns} data={data} />
    </>
  );
}
