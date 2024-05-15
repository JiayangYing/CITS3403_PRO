$(() => {
  $('#gridViewBtn').on('click', function() {
    updateUrlParameter('view', 'grid');
  });

  $('#listViewBtn').on('click', function() {
    updateUrlParameter('view', 'list');
  });

  $('#listViewBtn').on('click', function() {
    updateUrlParameter('view', 'list');
  });

  SetPaginationActive('#CategoriesPageNavBar')
});