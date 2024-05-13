$(() => {
    if(show_deavtivate_modal){
        $('#confirmDeactivateModal').modal('show');
    }
    // Handle Deactivate Account Button Click
    document.getElementById('deactivateAccountBtn').addEventListener('click', function() {
        // Show confirmation modal
        $('#confirmDeactivateModal').modal('show');
    });
    
    // Handle Become a Seller Checkbox Change
    document.getElementById('gridCheck').addEventListener('change', function() {
        var sellerForm = document.getElementById('sellerForm');
        if (sellerForm.classList.contains('show')) {
            sellerForm.classList.remove('show');
        } else {
            sellerForm.classList.add('show');
        }
    });
});
