$(document).ready(function() {
    $('#gridViewBtn').on('click', function() {
      $('#productGrid').removeClass('d-none');
      $('#productList').addClass('d-none');
    });
  
    $('#listViewBtn').on('click', function() {
      $('#productList').removeClass('d-none');
      $('#productGrid').addClass('d-none');
    });
});