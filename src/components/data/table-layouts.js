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
      },
      {
        Header: 'Notes',
        accessor: 'java.note'
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
      },
      {
        Header: 'Notes',
        accessor: 'js.note'
      }
    ]
  }
];
