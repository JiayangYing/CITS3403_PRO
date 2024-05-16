$(() => {
    if(show_reset_pass_modal){
        $('#forgotPasswordModal').modal('show');
    }
    // Forget Password Function
    document.getElementById('forgotPasswordBtn').addEventListener('click', function() {
        $('#forgotPasswordModal').modal('show');
    });
});