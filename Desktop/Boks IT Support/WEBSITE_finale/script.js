/* ==================== BIT MASTER SCRIPT v3 ==================== */
/* SOLID refactor: single-responsibility controllers */

(function () {
    "use strict";

    class ThemeController {
        constructor(root, toggleId, storageKey) {
            this.root = root;
            this.toggle = document.getElementById(toggleId);
            this.icon = this.toggle ? this.toggle.querySelector(".theme-toggle-icon") : null;
            this.storageKey = storageKey;
        }

        init() {
            if (!this.toggle) {
                return;
            }

            const savedTheme = localStorage.getItem(this.storageKey);
            const initialTheme = savedTheme || this.root.getAttribute("data-theme") || "dark";
            this.applyTheme(initialTheme);

            this.toggle.addEventListener("click", () => {
                const current = this.root.getAttribute("data-theme") || "dark";
                this.applyTheme(current === "dark" ? "light" : "dark");
            });
        }

        applyTheme(theme) {
            this.root.setAttribute("data-theme", theme);
            localStorage.setItem(this.storageKey, theme);
            if (this.icon) {
                this.icon.textContent = theme === "light" ? "☀" : "☾";
            }
        }
    }

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

    class TileObserverController {
        init() {
            const tiles = document.querySelectorAll(".tile");
            const sections = document.querySelectorAll(".content-section");
            if (tiles.length === 0 || sections.length === 0) {
                return;
            }

            const observer = new IntersectionObserver(
                (entries) => {
                    entries.forEach((entry) => {
                        if (!entry.isIntersecting) {
                            return;
                        }

                        const sectionId = entry.target.id;
                        tiles.forEach((tile) => {
                            tile.classList.remove("is-active");
                            tile.removeAttribute("aria-current");
                        });

                        const tile = document.querySelector(`.tile[href="#${sectionId}"]`);
                        if (tile) {
                            tile.classList.add("is-active");
                            tile.setAttribute("aria-current", "true");
                        }
                    });
                },
                {
                    threshold: 0.4,
                    rootMargin: "-72px 0px -50% 0px",
                }
            );

            sections.forEach((section) => {
                if (section.id) {
                    observer.observe(section);
                }
            });

            if (window.location.hash) {
                const target = document.getElementById(window.location.hash.substring(1));
                if (target) {
                    setTimeout(() => {
                        target.scrollIntoView({ behavior: "smooth", block: "start" });
                    }, 300);
                }
            }
        }
    }

    class ReadinessController {
        init() {
            const form = document.getElementById("readinessForm");
            const result = document.getElementById("readinessResult");
            const resultScore = document.getElementById("resultScore");
            const resultDiagnosis = document.getElementById("resultDiagnosis");

            if (!form || !result || !resultScore || !resultDiagnosis) {
                return;
            }

            form.addEventListener("submit", (event) => {
                event.preventDefault();

                const q1 = document.querySelector('input[name="q1"]:checked')?.value;
                const q2 = document.querySelector('input[name="q2"]:checked')?.value;
                const q3 = document.querySelector('input[name="q3"]:checked')?.value;

                let score = 0;
                if (q1 === "yes") score += 34;
                if (q2 === "yes") score += 34;
                if (q3 === "yes") score += 34;

                let diagnosis = "Starke Basis.";
                if (score <= 49) {
                    diagnosis = "Hohe System-Lücke.";
                } else if (score <= 79) {
                    diagnosis = "Solide Basis mit Schwachstellen.";
                }

                resultScore.textContent = `${score}/100`;
                resultDiagnosis.textContent = diagnosis;
                result.classList.add("active");

                setTimeout(() => {
                    result.scrollIntoView({
                        behavior: "smooth",
                        block: "nearest",
                    });
                }, 100);
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
        new ThemeController(document.documentElement, "themeToggle", "bit-theme"),
        new SmoothScrollController(),
        new TileObserverController(),
        new ReadinessController(),
        new FaqController(),
        new HeaderShadowController(),
    ]);

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", () => app.init());
    } else {
        app.init();
    }
})();
