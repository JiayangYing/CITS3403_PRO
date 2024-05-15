$(() => {
    // Handle avatar selection
    $('.modal-body i').click(function () {
        var avatarClass = $(this).attr('class');
        // Update preview
        $('.avatar-container > i').attr('class', avatarClass + ' fa-4x');
        $('#avatar').val($(this).data('id'))
        // Close modal
        $('#avatarModal').modal('hide');
    });

    $('.avatar-container i').click(function () {
        $('#avatarModal').modal('show');
    });

});
