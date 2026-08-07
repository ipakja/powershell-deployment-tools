/** Initialize the responsive navigation drawer. */
export function initMobileNav(root = document) {
    const toggle = root.querySelector("[data-menu-toggle]");
    const navigation = root.querySelector("[data-main-nav]");

    if (!toggle || !navigation) {
        return;
    }

    const close = () => {
        navigation.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
    };

    toggle.addEventListener("click", () => {
        const isOpen = navigation.classList.toggle("is-open");
        toggle.setAttribute("aria-expanded", String(isOpen));
    });

    navigation.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", close);
    });

    root.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            close();
        }
    });
}
