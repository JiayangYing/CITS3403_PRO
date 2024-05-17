const sdgIdxs = [8, 10, 12, 13];

function getSdgImageDirs(isDarkMode) {
    const onSuccess = (response) => {
        const $sdgImgContainer = $("#sdgImages");
        $sdgImgContainer.empty();
        let imgCount = 0;

        response.sdg_images.forEach((imgDir, idx) => {
            if (imgCount % 5 === 0) {
                $sdgImgContainer.append($("<div>").addClass('row'));
            }
            imgCount++;

            let imgClass = ''; 
            let imgStyle = '';
            if (sdgIdxs.includes(imgCount)) {
                imgClass = 'fa-beat-fade';
                imgStyle = '--fa-beat-fade-opacity: 0.5; --fa-beat-fade-scale: 0.9;';
            }

            let img = $("<img>").attr({
                src: `/static/img/sdg/${imgDir}`,
                alt: `SDG_${imgCount}`,
                width: 200,
                height: 200
            }).addClass(imgClass).attr("style", imgStyle);

            let $row = $sdgImgContainer.find('.row').last();
            $row.append(`<div class='col p-0'>${img.prop('outerHTML')}</div>`);

            if (idx === response.sdg_images.length - 1) {
                let emptyCols = 5 - $row.children('.col').length;
                for (let i = 0; i < emptyCols; i++) {
                    $row.append(`<div class='col p-0'></div>`);
                }
            }
        });

        $sdgImgContainer.on('click', 'img', function() {
            let imgIndex = parseInt(this.alt.replace("SDG_", ""));
            if (sdgIdxs.includes(imgIndex)) {
                $(`#${this.alt}Modal`).modal("show");
            }
        });
    }

    CallPost("/sdg_img_dirs", { isDarkMode: isDarkMode }, onSuccess, OnAjaxError);
}

$(() => {
    const body = document.querySelector("body");
    getSdgImageDirs(body.classList.contains(darkModeClass));

    $("#toggleDarkTheme").on("click", function() {
        setTimeout(() => {
            getSdgImageDirs(body.classList.contains(darkModeClass));
        }, 100);
    });
    
    $(".category-body .category[data-id]").click(function(){
        var url = $(this).data("id");
        window.location.href = url;
    });
});
