$(() => {
    $('.carousel-indicators button').first().addClass('active')
    $('.carousel-inner img').first().parent().addClass('active')
    
    $('#ContactSellerBtn').on('click', function(){
        $modal = $(`#ContactSellerModal`)
        $modal.modal("show");
    });

    $('#ContactSellerModal .row input').prop("disabled", true);
    $('#ContactSellerModal .row input').addClass('input-as-label');
    
    $('#ContactSellerModal').find('#modifyDetails').on('click', function(){
        if($(this).is(':checked')){
            $('#ContactSellerModal .row input').prop("disabled", false);
            $('#ContactSellerModal .row input').removeClass('input-as-label');
        }else{
            $('#ContactSellerModal .row input').prop("disabled", true);
            $('#ContactSellerModal .row input').addClass('input-as-label');
        }
    })

    $('#quantity').on('change', function(){
        var selectedQty = $(this).val()
        const $estPrice = $('#EstimatedProductPrice')
        if(selectedQty){
            $estPrice.text(`AUD ${$('#ProductPrice').text() * selectedQty}`)
        }else{
            $estPrice.text('-')
        }
    })
});