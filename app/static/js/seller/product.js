var clickedProductId = 0;
var currentPage = 1;

const onErrorAjaxDefault = (xhr) => {
    GenerateDangerAlertDiv("Failed!", xhr.responseText);
};

var onErrorOrderTable = (xhr) => {
    divId = $('#productOrderModal.show').length ? '#productOrder_AlertModalDiv' : ''
    GenerateDangerAlertDiv("Failed!", xhr.responseText, divId);
};

var onSuccessOrderTable = (response) => {
    divId = $('#productOrderModal.show').length ? '#productOrder_AlertModalDiv' : ''
    if (response.success) {
        GenerateSuccessAlertDiv("Success!", response.message, divId);
        loadOrders(clickedProductId);
    } else {
        GenerateDangerAlertDiv("Failed!", response.message, divId);
    }
}

function approveOrder(orderId, lastName) {
    if (!confirm(`Are you sure you want to APPROVE order from ${lastName}?`))
        return;
    CallPost(`/approve_order/${orderId}`, {}, onSuccessOrderTable, onErrorOrderTable);
}

function rejectOrder(orderId, lastName) {
    if (!confirm(`Are you sure you want to REJECT order from ${lastName}?`))
        return;
    CallPost(`/reject_order/${orderId}`, {}, onSuccessOrderTable, onErrorOrderTable);
}

function loadOrders(productId = clickedProductId, productName = null, page = currentPage) {
    clickedProductId = productId
    currentPage = page
    if(productName)
        $("#popup-product-name").text(productName);
    const onSuccess = (response) => {
        $table = $("#product-order-table")
        $table.find("tbody").empty();
        
        $.each(response.orders, function(index, order) {
            var btn = `
                <button class="btn btn-success btn-sm ml-0" title="Approve" onclick="approveOrder(${order.id}, '${order.last_name}')"><span><i class="fa-solid fa-check"></i> Approve</span></button>
                <button class="btn btn-danger btn-sm ml-0" title="Reject" onclick="rejectOrder(${order.id}, '${order.last_name}')"><span><i class="fa-solid fa-xmark"></i> Reject</span></button>
            `
            var row = `
                <tr data-status=${order.status}>
                    <td>${index + 1}</td>
                    <td>${order.first_name}</td>
                    <td>${order.last_name}</td>
                    <td>${order.email}</td>
                    <td>${order.contact_no}</td>
                    <td>${order.created_on}</td>
                    <td>${order.qty}</td>
                    <td>${order.status}</td>
                    <td>
                        ${order.status == 'Pending' ? btn : ''}
                    </td>
                </tr>`;
            $table.find("tbody").append(row);
        });

        $('#OrderPageNavBar').parents('div.row').first().remove()
        var pagesHTML = ``
        $.each(response.pages, function(index, p) {
            active = page==p ? 'active' : ''
            pagesHTML += `
                <li class="page-item ${active}">
                    <a class="page-link" onclick="loadOrders(${productId}, '${productName}', ${p})">${p}</a>
                </li>`;
        });
        prevHTML = `
            <li class="page-item ${response.pages.includes(page-1) ? '' : 'disabled'}">
                <a class="page-link" onclick="loadOrders(${productId}, '${productName}', ${page-1})">Previous</a>
            </li>`
        nextHTML = `
            <li class="page-item ${response.pages.includes(page+1) ? '' : 'disabled'}">
                <a class="page-link" onclick="loadOrders(${productId}, '${productName}', ${page+1})">Next</a>
            </li>`

        $table.parents('div.modal-body').first().append(
            `
            <div class="row">
                <div class="col-12">
                    <div class="mt-2 mr-2 d-flex justify-content-end">
                        <nav aria-label="OrderPageNav">
                            <ul id="OrderPageNavBar" class="pagination">
                                ${prevHTML}
                                ${pagesHTML}
                                ${nextHTML}
                            </ul>
                        </nav>
                    </div>
                </div>
            </div>
            `
        )
        $("#productOrderModal").modal('show');
    };
    CallPost(`/get_orders/${productId}`, { page : currentPage }, onSuccess, onErrorAjaxDefault);
}

function switchIsActive(productId) {
    
    const onSuccessActivation = (response) => {
        if (response.success) {
            GenerateSuccessAlertDiv("Success!", response.message);
        } else {
            GenerateDangerAlertDiv("Failed!", response.message);
            current_checked = $(`#isActive_${productId}`).prop('checked')
            $(`#isActive_${productId}`).prop('checked', !current_checked )
        }
    }
    CallPost(`/product_activation/${productId}`, {}, onSuccessActivation, onErrorAjaxDefault);
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

    SetPaginationActive('#ProductPageNavBar')
});