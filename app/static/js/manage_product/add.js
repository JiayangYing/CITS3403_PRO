var addProductForm = $("#addProductForm")

$(() => {
    addProductForm.find(".custom-file-input").on("change", function () {
        const currentInput = window.$(this);
        const fileName = window.$(this).val().split("\\").pop();
        const assetName = currentInput.siblings(".custom-file-label").attr("for");
        var file = this.files[0];
        if (file) {
            const uploadImg = new FileReader();
            uploadImg.onload = function (displayImg) {
                var base64 = displayImg.target.result;
                var image = new Image();
                image.src = base64;
                image.onload = function () {
                    currentInput.siblings(".custom-file-label").addClass("selected").html(fileName);
                    currentInput.parents().siblings(".custom-file-preview").attr("src", base64);
                    $(`#${assetName}`).val(base64);
                };
            }
            uploadImg.readAsDataURL(this.files[0]);
        }
    });
});

