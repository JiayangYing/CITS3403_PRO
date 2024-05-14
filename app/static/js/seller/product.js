var clickedProductId = 0;

const onErrorAjaxDefault = (xhr) => {
    GenerateDangerAlertDiv("Failed!", xhr.responseText);
};

const onErrorOrderTable = (xhr) => {
    GenerateDangerAlertDiv("Failed!", xhr.responseText, '#productOrder_AlertModalDiv');
};

const onSuccessOrderTable = (response) => {
    if (response.error !== 'Success') {
        GenerateSuccessAlertDiv("Success!", response.message);
        loadOrders(clickedProductId);
    } else {
        GenerateDangerAlertDiv("Failed!", xhr.responseText, '#productOrder_AlertModalDiv');
    }
}

function approveOrder(orderId, lastName) {
    if (!confirm(`Are you sure you want to APPROVE order from ${lastName}?`))
        return;
    CallPost("/Order/Approve", { orderId: orderId }, onSuccessOrderTable, onErrorOrderTable);
}

function rejectOrder(orderId, lastName) {
    if (!confirm(`Are you sure you want to APPROVE order from ${lastName}?`))
        return;
    CallPost("/Order/Reject", { orderId: orderId }, onSuccessOrderTable, onErrorOrderTable);
}

function loadOrders(productId, productTitle = null) {
    clickedProductId = productId
    if(productTitle)
        $("#popup-product-name").text(productTitle);
    const onSuccess = (response) => {
        $table = $("#product-order-table")
        $table.find("tbody").empty();
        
        $.each(response.orders, function(index, order) {
            var row = `<tr class = ${order.status}>
                        <td>${index + 1}</td>
                        <td>${order.first_name}</td>
                        <td>${order.last_name}</td>
                        <td>${order.email}</td>
                        <td>${order.contact_no}</td>
                        <td>${order.created_on}</td>
                        <td>${order.qty}</td>
                        <td>${order.status}</td>
                        <td>
                            <button class="btn btn-success btn-sm ml-0" title="Approve" onclick="approveOrder(${order.id}, ${order.last_name})"><span><i class="fa-solid fa-check"></i> Approve</span></button>
                            <button class="btn btn-danger btn-sm ml-0" title="Reject" onclick="rejectOrder(${order.id}, ${order.last_name})"><span><i class="fa-solid fa-xmark"></i> Reject</span></button>
                        </td>
                    </tr>`;
                    $table.find("tbody").append(row);
        });
        $("#productOrderModal").modal('show');
    };
    CallPost(`/get_orders/${productId}`, {}, onSuccess, onErrorAjaxDefault);
}

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