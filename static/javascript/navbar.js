document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.getElementById("menu-button");
    const menu = document.querySelector(".menu");

    menuButton.addEventListener("click", function () {
        menu.classList.toggle("open");
        menuButton.classList.toggle("active");
    });
});