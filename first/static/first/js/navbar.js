document.addEventListener("DOMContentLoaded", function () {
    const sections = document.querySelectorAll("section");
    const navLinks = document.querySelectorAll(".nav-link");

    window.addEventListener("scroll", () => {

        let current = "";

        sections.forEach(section => {

            const sectionTop = section.offsetTop - 150;

            if (window.scrollY >= sectionTop) {
                current = section.getAttribute("id")
            }

        });

        navLinks.forEach(link => {

            link.classList.remove("font-bold");

            if (link.getAttribute("href") === "#" + current) {

                link.classList.add("font-bold")
            }

        });
    });

});