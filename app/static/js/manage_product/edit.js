$(() => {
  jsonPath = JSON.parse(images.replace(/&#39;/g, '"'));
  $.each(jsonPath["paths"], function (idx, path) {
    addPreviewFile(path, idx);
  });
  $;
  document
    .getElementById("imageInput")
    .addEventListener("change", handleFileSelect);
});

function addPreviewFile(imgSrc, i) {
  var preview = document.getElementById("imagePreview");
  var checked = i == $("#main_idx").val() - 1 ? "checked" : "";
  const containerHTML = `
        <div class="form-check image-container">
            <label for="checkbox-img${i}">
                <img src="${imgSrc}" class="custom-file-preview ms-4">
            </label>
            <input type="checkbox" id="checkbox-img-${i}" data-id="${
    i + 1
  }" name="checkbox-img" class="main-image-checkbox" ${checked}>
        </div>
    `;
  preview.innerHTML += containerHTML;

  $(".form-check input:checkbox").on("change", function (e) {
    $(".form-check input:checkbox").prop("checked", false);
    $(this).prop("checked", true);
    const dataId = parseInt($(this).data("id"));
    console.log(dataId);
    $("#main_idx").val(dataId);
  });
}

function handleFileSelect(event) {
  const files = event.target.files;
  var preview = document.getElementById("imagePreview");

  // Clear any existing content in the preview container
  preview.innerHTML = "";

  const n = files.length >= 6 ? 6 : files.length;
  for (let i = 0; i < n; i++) {
    const file = files[i];
    if (!file.type.match("image.*")) {
      continue;
    }

    const reader = new FileReader();
    reader.onload = function (event) {
      const containerHTML = `
                <div class="form-check image-container">
                    <label for="checkbox-img${i}">
                        <img src="${
                          event.target.result
                        }" class="custom-file-preview ms-4">
                    </label>
                    <input type="checkbox" id="checkbox-img-${i}" data-id="${
        i + 1
      }" name="checkbox-img" class="main-image-checkbox">
                </div>
            `;
      preview.innerHTML += containerHTML;

      $(".form-check input:checkbox").on("change", function (e) {
        $(".form-check input:checkbox").prop("checked", false);
        $(this).prop("checked", true);
        const dataId = parseInt($(this).data("id"));
        $("#main_idx").val(dataId);
      });
    };
    reader.readAsDataURL(file);
  }
}
