function getSdgImageDirs(isDarkMode) {
    const onSuccess = (response) => {
        const $sdgImgContainer = $("#sdgImages");
        $sdgImgContainer.empty();

        window.$.each(response.sdg_images, function (idx, imgDir) {
            $sdgImgContainer.append(`<img src="/static/img/sdg/${imgDir}" alt="SDG-${idx} Image" width="200" height="200">`);
        });
        // if (response.errorCode !== ErrorCodeNoError) {
        //     GenerateDangerAlertDiv("Failed!", response.message);
        // } else {
        //     const $sdgImgContainer = $("#sdgImages");
        //     $sdgImgContainer.empty();
    
        //     window.$.each(response, function (idx, imgDir) {
        //         $sdgImgContainer.append(`<img src="{{ url_for('static', filename='img/' + ${imgDir}) }}" alt="SDG ${idx} Image">`);
        //     });
        // }
    }

    CallPost("/sdg_img_dirs", { isDarkMode : isDarkMode }, onSuccess, OnAjaxError);
}