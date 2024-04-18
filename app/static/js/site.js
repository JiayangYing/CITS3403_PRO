$(() => {
    const lightSwitch = document.getElementById("toggleDarkTheme");
    const toggleSpan = lightSwitch.querySelector("i");
    const textSpan = lightSwitch.querySelector("span");

    const modeToggle = () => {
        const weatherSpan = document.querySelector("#weather_mode");
        const body = document.querySelector("body");

        if (body.classList.contains("dark_mode")) {
            body.classList.remove("dark_mode");
            localStorage.setItem("dark_mode", false);
            toggleSpan.classList.replace("fa-sun", "fa-moon");
            textSpan.textContent = textSpan.dataset.dark;
        } else {
            body.classList.add("dark_mode");
            localStorage.setItem("dark_mode", true);
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