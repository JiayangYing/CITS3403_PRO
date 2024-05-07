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

    var url = new URL(window.location.href);
    pageNum = url.searchParams.get('page')
    $('#ProductPageNavBar a').each(function(i, a){
      $a = $(a)
      if(`${$a.text()}` === pageNum){
        $a.parent().addClass('active')
        return false
      }
    })
});