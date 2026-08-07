/** Apply safe external-link behavior, reveal harvest-protected emails, open direct mailto. */
export function initContactLinks(root = document) {
    root.querySelectorAll('[data-contact="whatsapp"]').forEach((link) => {
        link.setAttribute("target", "_blank");
        link.setAttribute("rel", "noopener noreferrer");
    });

    root.querySelectorAll('[data-contact="viber"]').forEach((link) => {
        link.setAttribute("rel", "noopener");
    });

    root.querySelectorAll('[data-contact="email"]').forEach((link) => {
        const span = link.querySelector("[data-email-user][data-email-domain]");
        if (!span) {
            return;
        }
        const user = span.getAttribute("data-email-user") || "";
        const domain = span.getAttribute("data-email-domain") || "";
        if (user && domain) {
            span.textContent = `${user}@${domain}`;
        }
    });

    root.querySelectorAll("[data-direct-mailto]").forEach((link) => {
        link.addEventListener("click", (event) => {
            event.preventDefault();
            const user = link.getAttribute("data-email-user") || "";
            const domain = link.getAttribute("data-email-domain") || "";
            const subjectEnc = link.getAttribute("data-mailto-subject-enc") || "";
            const bodyEnc = link.getAttribute("data-mailto-body-enc") || "";
            if (!user || !domain) {
                return;
            }
            window.location.href =
                `mailto:${user}@${domain}?subject=${subjectEnc}&body=${bodyEnc}`;
        });
    });
}
