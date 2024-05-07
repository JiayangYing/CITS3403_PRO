document.addEventListener("DOMContentLoaded", function() {
    // Handle Deactivate Account Button Click
    document.getElementById('deactivateAccountBtn').addEventListener('click', function() {
        // Show confirmation modal
        $('#confirmDeactivateModal').modal('show');
    });

    // Handle Confirm Deactivate Button Click
    document.getElementById('confirmDeactivateBtn').addEventListener('click', function() {
        // Get password entered by user
        var password = document.getElementById('deactivatePassword').value;
        // Validate password (you can add your own validation logic here)
        if (password === '') {
            // Show error message or handle validation failure
            alert('Please enter your password.');
            return;
        }
        // You can perform additional validation here if needed
        // If validation succeeds, you can delete the account or perform other actions
        // For now, let's show a confirmation alert
        alert('Account deactivated successfully.');
        // Close the modal
        $('#confirmDeactivateModal').modal('hide');
    })
});

document.addEventListener("DOMContentLoaded", function() {
    // Handle Become a Seller Checkbox Change
    document.getElementById('gridCheck').addEventListener('change', function() {
        var sellerForm = document.getElementById('sellerForm');
        if (this.checked) {
            // Show seller form
            sellerForm.classList.add('show');
        } else {
            // Hide seller form
            sellerForm.classList.remove('show');
        }
    });

    // Handle Confirm Seller Button Click
    document.getElementById('confirmSelletBtn').addEventListener('click', function(e) {
        e.preventDefault(); // Prevent form submission

        // Get password entered by user
        var password = document.getElementById('sellerPassword').value;
        // Get agreement checkbox value
        var agreementChecked = document.getElementById('sellerAgreement').checked;

        // Validate password and agreement (you can add your own validation logic here)
        if (password === '' & !agreementChecked) {
            alert('Please enter your password and agree to the terms and conditions.');
            return;
        }
        if (password === '') {
            // Show error message or handle validation failure
            alert('Please enter your password.');
            return;
        }
        if (!agreementChecked) {
            // Show error message or handle validation failure
            alert('Please agree to the terms and conditions.');
            return;
        }

        // If validation succeeds, you can perform further actions here
        // For now, let's show a confirmation alert
        alert('You have successfully become a seller!');
        // Optionally, you can submit the form or perform other actions here
        window.location.reload();
    });
});

