$(() => {
  $('#gridViewBtn').on('click', function() {
    updateUrlParameter('view', 'grid');
  });

  $('#listViewBtn').on('click', function() {
    updateUrlParameter('view', 'list');
  });

  $(".display-card").click(function(){
      var productId = $(this).data('id');
      window.open(`/product/${productId}`, '_blank');
  });

  $("a[data-id].list-group-item").click(function(){
      var productId = $(this).data('id');
      window.open(`/product/${productId}`, '_blank');
  });

  $('#productFilterDropdownBar .dropdown-menu').on('click', function(e) {
    if($(this).hasClass('dropdown-menu')) {
      e.stopPropagation();
    }
  });

  $.each($('#productFilterBar .form-check'), function(idx, formCheck){
    var id = $(formCheck).find('input').attr('id');
    var idNew = `${id}-${idx}`
    $(formCheck).find('input').attr('id', `${idNew}`);
    $(formCheck).find('label').attr('for', `${idNew}`);
  })

  SetPaginationActive('#CategoriesPageNavBar')
})