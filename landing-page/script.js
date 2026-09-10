document.addEventListener("DOMContentLoaded", function () {
    var container = document.querySelector(".popup-container");
    var popupButtons = document.querySelectorAll(".open-popup");
    var closeButton = document.querySelector(".popup-close");
    var form = document.querySelector(".popup-form");

    popupButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            container.style.display = "flex";
        });
    });

    container.addEventListener("click", function (event) {
        if (event.target === container) {
            container.style.display = "none";
        }
    });

    closeButton.addEventListener("click", function () {
        container.style.display = "none";
    });

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        container.style.display = "none";
        form.reset();
    });
});