function on_submit_set_enable(){
    if(!$('#modifyDetails').prop('checked')){
        $('#modifyDetails').trigger('click');
    }
}

$(() => {
    if(show_contact_seller_modal){
        $('#ContactSellerModal').modal('show');
    }

    if($('#quantity').val()){
        setTimeout(() => {
            $('#quantity').trigger('change')
        }, 100);
    }

    $('.carousel-indicators button').first().addClass('active')
    $('.carousel-inner img').first().parent().addClass('active')
    
    $('#ContactSellerBtn').on('click', function(){
        $modal = $(`#ContactSellerModal`)
        $modal.modal("show");
    });

    var $disabledInput = $('#ContactSellerModal .row input')
    $disabledInput.prop("disabled", true);
    $disabledInput.addClass('input-as-label');
    
    $disabledInput.on('touchstart', function(){
        if(!$(this).val() && $(this).prop('disabled')){
            $('#modifyDetails').trigger('click');
        }
    })

    $('#ContactSellerModal').find('#modifyDetails').on('click', function(){
        if($(this).is(':checked')){
            $disabledInput.prop("disabled", false);
            $disabledInput.removeClass('input-as-label');
        }else{
            $disabledInput.prop("disabled", true);
            $disabledInput.addClass('input-as-label');
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