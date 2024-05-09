$(() => {
    $("#product-table tbody").on("click", "td.dt-control", function () {
        $tr = $(this).parent();
        x=$tr
        if ($tr.hasClass('shown')){
            $tr.removeClass('shown')
            $tr.next("tr").addClass('d-none')
        }else {
            $tr.addClass('shown')
            $tr.next("tr").removeClass('d-none')
        }
    });
});