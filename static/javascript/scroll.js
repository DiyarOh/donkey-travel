document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll("a[data-scroll]");

    links.forEach((link) => {
      link.addEventListener("click", function (e) {
        e.preventDefault();

        const targetId = this.getAttribute("data-scroll");
        const target = document.getElementById(targetId);

        if (target) {
          const offsetTop = target.getBoundingClientRect().top;
          const scrollOptions = {
            behavior: "smooth",
          };

          window.scrollTo({
            top: window.scrollY + offsetTop,
            ...scrollOptions,
          });
        }
      });
    });
  });