document.addEventListener("DOMContentLoaded", function () {

    const sections = document.querySelectorAll("section[id]");
    const navLinks = document.querySelectorAll(".nav-link");

    function activateLink() {

        let scrollY = window.scrollY;

        sections.forEach(section => {

            const sectionTop = section.offsetTop - 150;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute("id");

            if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {

                navLinks.forEach(link => {
                    link.classList.remove("text-blue-500", "font-bold");

                    if (link.getAttribute("href").includes("#" + sectionId)) {
                        link.classList.add("text-blue-500", "font-bold");
                    }
                });

            }

        });
    }

    window.addEventListener("scroll", activateLink);
});