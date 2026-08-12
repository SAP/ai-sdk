export const mainFeatureTableLayout = [
  {
    header: 'Feature',
    id: 'feature',
    columns: [
      {
        id: 'feature-name',
        header: 'Name',
        accessorKey: 'name'
      }
    ]
  },
  {
    header: '☕️ Java',
    id: 'java',
    columns: [
      {
        id: 'java-status',
        header: 'Status',
        accessorKey: 'java.status'
      },
      {
        id: 'java-docs',
        header: 'Docs',
        accessorKey: 'java.docsLink'
      }
    ]
  },
  {
    header: '🚀 JavaScript',
    id: 'javascript',
    columns: [
      {
        id: 'js-status',
        header: 'Status',
        accessorKey: 'js.status'
      },
      {
        id: 'js-docs',
        header: 'Docs',
        accessorKey: 'js.docsLink'
      }
    ]
  },
  {
    header: '🐍 Python',
    id: 'python',
    columns: [
      {
        id: 'python-status',
        header: 'Status',
        accessorKey: 'python.status'
      },
      {
        id: 'python-docs',
        header: 'Docs',
        accessorKey: 'python.docsLink'
      }
    ]
  }
];
