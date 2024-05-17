const onErrorAjaxDefault = (xhr) => {
    GenerateDangerAlertDiv("Failed!", xhr.responseText);
};

var onErrorOrderTable = (xhr) => {
    GenerateDangerAlertDiv("Failed!", xhr.responseText);
};

var onSuccessOrderTable = (response) => {
    if (response.success) {
        GenerateSuccessAlertDiv("Success!", response.message);
        location.reload();
    } else {
        GenerateDangerAlertDiv("Failed!", response.message);
    }
}

function cancelOrder(orderId, productName) {
    if (!confirm(`Are you sure you want to CANCEL your order for ${productName}?`))
        return;
    CallPost(`/cancel_order/${orderId}`, {}, onSuccessOrderTable, onErrorOrderTable);
}

$(() => {
    SetPaginationActive('#OrderPageNavBar')
});