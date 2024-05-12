$(() => {
    // Forget Password Function
    document.getElementById('forgotPasswordBtn').addEventListener('click', function() {
        $('#forgotPasswordModal').modal('show');
    });

    document.getElementById('confirmForgotPasswordBtn').addEventListener('click', function() {
        var emailInput = document.getElementById('forgotPasswordEmail');
        if (!emailInput.checkValidity()) {
            alert('Please enter a valid email address.');
            return;
        }
        var email = emailInput.value;
        alert('Password reset instructions sent to ' + email);
        $('#forgotPasswordModal').modal('hide');
    });
});

