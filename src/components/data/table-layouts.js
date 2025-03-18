export const mainFeatureTableLayout = [
  {
    Header: 'Feature',
    columns: [
      {
        Header: 'Name',
        accessor: 'name'
      }
    ]
  },
  {
    Header: '☕️ Java',
    columns: [
      {
        Header: 'Status',
        accessor: 'java.status'
      },
      {
        Header: 'Docs',
        accessor: 'java.docsLink'
      }
    ]
  },
  {
    Header: '🚀 JavaScript',
    columns: [
      {
        Header: 'Status',
        accessor: 'js.status'
      },
      {
        Header: 'Docs',
        accessor: 'js.docsLink'
      }
    ]
  }
];
