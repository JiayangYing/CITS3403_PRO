const sdgIdxs = [13,14,15]

function getSdgImageDirs(isDarkMode) {
    const onSuccess = (response) => {
        const $sdgImgContainer = $("#sdgImages");
        $sdgImgContainer.empty();
        window.$.each(response.sdg_images, function (idx, imgDir) {
            idx += 1
            var imgClass = '' 
            var imgStyle = ''
            var isSetModal = false
            if (sdgIdxs.indexOf(idx) !== -1){
                imgClass = 'fa-beat-fade'
                imgStyle = '--fa-beat-fade-opacity: 0.5; --fa-beat-fade-scale: 0.9;'
                isSetModal = true
            }
            var img = $("<img>").attr({
                src: `/static/img/sdg/${imgDir}`,
                alt: `SDG_${idx}`,
                width: 200,
                height: 200
              }).addClass(imgClass).attr("style", imgStyle);
            $sdgImgContainer.append(img);

            if(isSetModal){
                $(img).on('click', function(){
                    $modal = $(`#${this.alt}Modal`)
                    $modal.modal("show");
                });
            }
        });
    }

    CallPost("/sdg_img_dirs", { isDarkMode : isDarkMode }, onSuccess, OnAjaxError);
}

$(() => {
    const body = document.querySelector("body");
    getSdgImageDirs(body.classList.contains(darkModeClass));

    var $lightSwitch = $("#toggleDarkTheme");
    $lightSwitch.on("click", function() {
        setTimeout(() => {
            getSdgImageDirs(body.classList.contains(darkModeClass));
        }, 100);
    });
});