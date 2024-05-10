$(() => { 
    document.getElementById('imageInput').addEventListener('change', handleFileSelect); 
});

function handleFileSelect(event) { 
    const files = event.target.files; 
    const preview = document.getElementById('imagePreview'); 

    // Clear any existing content in the preview container
    preview.innerHTML = '';

    const n = files.length>=6 ? 6 : files.length
    for (let i = 0; i < n; i++) { 
        const file = files[i]; 
        if (!file.type.match('image.*')) { 
            continue; 
        }

        const reader = new FileReader(); 
        reader.onload = function(event) { 
            const containerHTML = `
                <div class="form-check image-container">
                    <label for="checkbox-img${i}">
                        <img src="${event.target.result}" class="custom-file-preview ms-4">
                    </label>
                    <input type="checkbox" id="checkbox-img${i}" name="checkbox-img" class="main-image-checkbox">
                </div>
            `;
            preview.innerHTML += containerHTML;

            $(".form-check input:checkbox").on('change', function(e){
                $(".form-check input:checkbox").prop('checked', false)
                $(this).prop('checked', true)
            });
    
        }; 
        reader.readAsDataURL(file); 
    }
}