export const mainFeatureTableLayout = [
  {
    Header: 'Feature',
    id: 'feature',
    columns: [
      {
        id: 'feature-name',
        Header: 'Name',
        accessorKey: 'name'
      }
    ]
  },
  {
    Header: '☕️ Java',
    id: 'java',
    columns: [
      {
        id: 'java-status',
        Header: 'Status',
        accessorKey: 'java.status'
      },
      {
        id: 'java-docs',
        Header: 'Docs',
        accessorKey: 'java.docsLink'
      }
    ]
  },
  {
    Header: '🚀 JavaScript',
    id: 'javascript',
    columns: [
      {
        id: 'js-status',
        Header: 'Status',
        accessorKey: 'js.status'
      },
      {
        id: 'js-docs',
        Header: 'Docs',
        accessorKey: 'js.docsLink'
      }
    ]
  },
  {
    Header: '🐍 Python',
    id: 'python',
    columns: [
      {
        id: 'python-status',
        Header: 'Status',
        accessorKey: 'python.status'
      },
      {
        id: 'python-docs',
        Header: 'Docs',
        accessorKey: 'python.docsLink'
      }
    ]
  }
];
