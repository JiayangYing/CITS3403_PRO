$(() => {
    const lightSwitch = document.getElementById("toggleDarkTheme");
    const toggleSpan = lightSwitch.querySelector("i");
    const textSpan = lightSwitch.querySelector("span");
    const weatherSpan = document.querySelector("#weather_mode");
    const body = document.querySelector("body");
    const isDarkMode = body.classList.contains(darkModeClass);
    if (isDarkMode) {
        body.classList.add(darkModeClass);
        weatherSpan.classList.replace("fa-sun", "fa-moon");
        textSpan.textContent = textSpan.dataset.light;
    } else {
        body.classList.remove(darkModeClass);
        weatherSpan.classList.replace("fa-moon", "fa-sun");
        textSpan.textContent = textSpan.dataset.dark;
    }
    
    const modeToggle = () => {
        const body = document.querySelector("body");
        const isDarkMode = body.classList.contains(darkModeClass);
        if (isDarkMode) {
            body.classList.remove(darkModeClass);
            localStorage.setItem(darkModeClass, false);
            toggleSpan.classList.replace("fa-sun", "fa-moon");
            textSpan.textContent = textSpan.dataset.dark;
        } else {
            body.classList.add(darkModeClass);
            localStorage.setItem(darkModeClass, true);
            toggleSpan.classList.replace("fa-moon", "fa-sun");
            textSpan.textContent = textSpan.dataset.light;
        }

        weatherSpan.style.removeProperty("animation");
        setTimeout(function () {
            weatherSpan.style.animation = "curvedpath 1.75s linear 1";
        }, 100);
        setTimeout(function () {
            if (weatherSpan.classList.contains("fa-sun")) {
                weatherSpan.classList.replace("fa-sun", "fa-moon");
            } else {
                weatherSpan.classList.replace("fa-moon", "fa-sun");
            }
        }, 750);
    };

    lightSwitch.addEventListener("click", () => {
        modeToggle();
    });
});