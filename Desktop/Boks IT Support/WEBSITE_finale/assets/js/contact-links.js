/** Apply safe external-link behavior to direct messenger CTAs. */
export function initContactLinks(root = document) {
    root.querySelectorAll('[data-contact="whatsapp"]').forEach((link) => {
        link.setAttribute("target", "_blank");
        link.setAttribute("rel", "noopener noreferrer");
    });

    root.querySelectorAll('[data-contact="viber"]').forEach((link) => {
        link.setAttribute("rel", "noopener");
    });
}
