/* ==================== BIT MASTER SCRIPT v3 ==================== */
/* Active controllers for the start pages only */

(function () {
    "use strict";

    class SmoothScrollController {
        init() {
            document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
                anchor.addEventListener("click", (event) => {
                    const href = anchor.getAttribute("href");
                    if (!href || href === "#") {
                        return;
                    }

                    const target = document.querySelector(href);
                    if (!target) {
                        return;
                    }

                    event.preventDefault();
                    target.scrollIntoView({
                        behavior: "smooth",
                        block: "start",
                    });

                    if (history.pushState) {
                        history.pushState(null, "", href);
                    }
                });
            });
        }
    }

    class FaqController {
        init() {
            const questions = document.querySelectorAll(".faq-question");
            if (questions.length === 0) {
                return;
            }

            questions.forEach((question) => {
                question.addEventListener("click", () => {
                    const isExpanded = question.getAttribute("aria-expanded") === "true";
                    const currentItem = question.closest(".faq-item");

                    questions.forEach((q) => {
                        q.setAttribute("aria-expanded", "false");
                        const item = q.closest(".faq-item");
                        if (item) {
                            item.removeAttribute("open");
                        }
                    });

                    if (!isExpanded && currentItem) {
                        question.setAttribute("aria-expanded", "true");
                        currentItem.setAttribute("open", "");
                    }
                });
            });
        }
    }

    class HeaderShadowController {
        init() {
            const header = document.querySelector("header");
            if (!header) {
                return;
            }

            window.addEventListener("scroll", () => {
                header.style.boxShadow =
                    window.scrollY > 50 ? "0 2px 8px rgba(0, 0, 0, 0.3)" : "none";
            });
        }
    }

    class App {
        constructor(controllers) {
            this.controllers = controllers;
        }

        init() {
            this.controllers.forEach((controller) => controller.init());
            if (typeof console !== "undefined") {
                console.log("BIT: Seite geladen.");
            }
        }
    }

    const app = new App([
        new SmoothScrollController(),
        new FaqController(),
        new HeaderShadowController(),
    ]);

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", () => app.init());
    } else {
        app.init();
    }
})();
