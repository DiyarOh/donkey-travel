document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.getElementById("menu-button");
    const menu = document.querySelector(".menu");
    const aboutUsLink = document.getElementById("about-us-link");
  
    menuButton.addEventListener("click", function () {
      menu.classList.toggle("open");
      menuButton.classList.toggle("active");
    });
  
    aboutUsLink.addEventListener("click", function (e) {
      e.preventDefault();
  
      const currentPage = window.location.pathname;
      const targetId = aboutUsLink.getAttribute("data-scroll");
      const targetElement = document.getElementById(targetId);
  
      if (currentPage === "/" && targetElement) {
        // Only close the menu if the current page is the index page
        if (menu.classList.contains("open")) {
          menu.classList.remove("open");
          menuButton.classList.remove("active");
        }
  
        const offset = targetElement.offsetTop;
        window.scroll({
          top: offset,
          behavior: "smooth",
        });
      } else {
        // Handle navigation to the index page if not on the index
        window.location.href = "/#about-us";
      }
  
      e.stopPropagation();
    });
  });