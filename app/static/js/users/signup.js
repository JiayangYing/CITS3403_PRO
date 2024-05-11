$(() => {
    
    if ($("#customCheck").is(":checked")) {
        $("#shopNameGroup").show();
    } else {
        $("#shopNameGroup").hide();
    }
    $("#customCheck").on("change", function() {
        // if checked, show name group, otherwise hide it
        if (this.checked) {
            $("#shopNameGroup").show()
        } else {
            $("#shopNameGroup").hide()
        }
    });
});