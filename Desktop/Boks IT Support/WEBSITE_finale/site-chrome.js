/**
 * BIT – Header-Controls (Sprache, Mobile) – nur Dark Mode
 */
(function () {
    "use strict";

    var LANG_PAIRS = [
        { de: "index.html", en: "index_en.html" },
        { de: "services.html", en: "services-en.html" },
        { de: "it-matrix.html", en: "it-matrix-en.html" },
        { de: "kontakt.html", en: "kontakt-en.html" },
        { de: "legal.html", en: "legal-en.html" },
    ];

    function currentFile() {
        var path = window.location.pathname || "";
        var parts = path.split("/");
        return parts[parts.length - 1] || "index.html";
    }

    function isEnglishPage() {
        return document.documentElement.lang === "en" || /-en\.html$/i.test(currentFile()) || currentFile() === "index_en.html";
    }

    function forceDarkMode() {
        document.documentElement.setAttribute("data-theme", "dark");
        if (document.body) {
            document.body.setAttribute("data-theme", "dark");
        }
        document.documentElement.style.colorScheme = "dark";
    }

    function removeThemeControls() {
        document
            .querySelectorAll(".theme-switch-group, #themeToggle, .theme-toggle-btn, .dark-mode-toggle")
            .forEach(function (el) {
                el.remove();
            });
    }

    function createLangSep() {
        var sep = document.createElement("span");
        sep.className = "lang-sep";
        sep.setAttribute("aria-hidden", "true");
        sep.textContent = "|";
        return sep;
    }

    function normalizeLangSwitches() {
        document.querySelectorAll(".lang-switch, .language-switch").forEach(function (container) {
            container.classList.add("lang-switch");

            var links = container.querySelectorAll("a");
            if (links.length < 2) {
                return;
            }

            links.forEach(function (link) {
                link.classList.add("lang-link");
            });

            if (!container.querySelector(".lang-sep")) {
                links[0].insertAdjacentElement("afterend", createLangSep());
            }
        });
    }

    function buildLangSwitch() {
        var file = currentFile();
        var pair = null;
        LANG_PAIRS.forEach(function (p) {
            if (p.de === file || p.en === file) {
                pair = p;
            }
        });
        if (!pair) {
            return null;
        }

        var en = isEnglishPage();
        var wrap = document.createElement("div");
        wrap.className = "lang-switch";
        wrap.setAttribute("role", "group");
        wrap.setAttribute("aria-label", en ? "Choose language" : "Sprache wählen");

        var deLink = document.createElement("a");
        deLink.href = pair.de;
        deLink.className = "lang-link" + (!en ? " active" : "");
        deLink.setAttribute("lang", "de");
        if (!en) {
            deLink.setAttribute("aria-current", "page");
        }
        deLink.textContent = "DE";

        var enLink = document.createElement("a");
        enLink.href = pair.en;
        enLink.className = "lang-link" + (en ? " active" : "");
        enLink.setAttribute("lang", "en");
        if (en) {
            enLink.setAttribute("aria-current", "page");
        }
        enLink.textContent = "EN";

        wrap.appendChild(deLink);
        wrap.appendChild(createLangSep());
        wrap.appendChild(enLink);
        return wrap;
    }

    function getHeaderRow() {
        return (
            document.querySelector("header .header-inner") ||
            document.querySelector(".header .header-content") ||
            document.querySelector("header")
        );
    }

    function placeHeaderControls(controls) {
        if (!controls) {
            return;
        }

        var headerRow = getHeaderRow();
        var headerNav = document.querySelector(".header-nav");

        if (headerRow && headerNav && headerNav.parentElement === headerRow) {
            controls.classList.remove("header-controls--floating");

            var mobileToggle =
                headerRow.querySelector("#mobileMenuToggle") ||
                headerRow.querySelector("#bitMobileMenuToggle") ||
                headerRow.querySelector(".mobile-menu-toggle");

            if (mobileToggle) {
                headerRow.insertBefore(controls, mobileToggle);
            } else {
                headerRow.appendChild(controls);
            }
            return;
        }

        if (headerNav && !headerRow) {
            controls.classList.remove("header-controls--floating");
            if (!headerNav.contains(controls)) {
                headerNav.appendChild(controls);
            }
            return;
        }

        if (!headerRow) {
            controls.classList.add("header-controls--floating");
            if (!document.body.contains(controls)) {
                document.body.appendChild(controls);
            }
            return;
        }

        controls.classList.remove("header-controls--floating");

        var legacyToggle =
            headerRow.querySelector("#mobileMenuToggle") ||
            headerRow.querySelector("#bitMobileMenuToggle") ||
            headerRow.querySelector(".mobile-menu-toggle");

        if (legacyToggle) {
            headerRow.insertBefore(controls, legacyToggle);
        } else {
            headerRow.appendChild(controls);
        }
    }

    function ensureHeaderControls() {
        var controls = document.querySelector(".header-controls");
        if (!controls) {
            controls = document.createElement("div");
            controls.className = "header-controls";

            var existingLang =
                document.querySelector(".header-controls .lang-switch") ||
                document.querySelector(".header-nav .lang-switch") ||
                document.querySelector(".lang-switch") ||
                document.querySelector(".language-switch");

            if (existingLang) {
                var parent = existingLang.parentElement;
                if (parent && parent.classList.contains("header-nav")) {
                    controls = document.createElement("div");
                    controls.className = "header-controls";
                    parent.appendChild(controls);
                } else if (parent) {
                    parent.insertBefore(controls, existingLang);
                } else {
                    document.body.appendChild(controls);
                    controls.classList.add("header-controls--floating");
                }
                controls.appendChild(existingLang);
            } else {
                var built = buildLangSwitch();
                if (built) {
                    document.body.appendChild(controls);
                    controls.classList.add("header-controls--floating");
                    controls.appendChild(built);
                } else {
                    controls.classList.add("header-controls--floating");
                    document.body.appendChild(controls);
                }
            }
        }

        removeThemeControls();

        placeHeaderControls(controls);
        return controls;
    }

    function initMobileNav() {
        if (document.getElementById("mobileMenuToggle") || document.getElementById("bitMobileMenuToggle")) {
            return;
        }

        var navLinks =
            document.querySelector(".header-nav .nav-links") ||
            document.querySelector(".nav .nav-links") ||
            document.querySelector(".header-content .nav-links");
        if (!navLinks) {
            return;
        }

        var headerRow =
            document.querySelector("header .header-inner") ||
            document.querySelector(".header .header-content") ||
            document.querySelector("header");
        if (!headerRow) {
            return;
        }

        var en = isEnglishPage();

        var toggle = document.createElement("button");
        toggle.type = "button";
        toggle.className = "bit-mobile-menu-toggle";
        toggle.id = "bitMobileMenuToggle";
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-controls", "bitMobileNav");
        toggle.setAttribute("aria-label", en ? "Open menu" : "Menü öffnen");
        toggle.innerHTML = "<span></span><span></span><span></span>";

        var drawer = document.createElement("nav");
        drawer.className = "bit-mobile-nav";
        drawer.id = "bitMobileNav";
        drawer.setAttribute("aria-label", en ? "Mobile navigation" : "Mobile Navigation");
        drawer.hidden = true;

        var list = document.createElement("ul");
        list.className = "bit-mobile-nav-links";
        navLinks.querySelectorAll("a").forEach(function (link) {
            var li = document.createElement("li");
            var clone = link.cloneNode(true);
            li.appendChild(clone);
            list.appendChild(li);
        });
        drawer.appendChild(list);

        var controls = headerRow.querySelector(".header-controls");
        if (controls) {
            headerRow.insertBefore(toggle, controls);
        } else {
            headerRow.appendChild(toggle);
        }
        document.body.appendChild(drawer);

        function closeMenu() {
            toggle.classList.remove("is-open");
            drawer.classList.remove("is-open");
            drawer.hidden = true;
            toggle.setAttribute("aria-expanded", "false");
            toggle.setAttribute("aria-label", en ? "Open menu" : "Menü öffnen");
            document.body.style.overflow = "";
        }

        function openMenu() {
            toggle.classList.add("is-open");
            drawer.classList.add("is-open");
            drawer.hidden = false;
            toggle.setAttribute("aria-expanded", "true");
            toggle.setAttribute("aria-label", en ? "Close menu" : "Menü schließen");
            document.body.style.overflow = "hidden";
        }

        toggle.addEventListener("click", function () {
            if (drawer.classList.contains("is-open")) {
                closeMenu();
            } else {
                openMenu();
            }
        });

        list.querySelectorAll("a").forEach(function (link) {
            link.addEventListener("click", closeMenu);
        });

        document.addEventListener("click", function (event) {
            if (
                drawer.classList.contains("is-open") &&
                !drawer.contains(event.target) &&
                !toggle.contains(event.target)
            ) {
                closeMenu();
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closeMenu();
            }
        });
    }

    function groupHeaderToolbar() {
        var headerRow = getHeaderRow();
        if (!headerRow || headerRow.querySelector(".header-toolbar")) {
            return;
        }

        var toolbar = document.createElement("div");
        toolbar.className = "header-toolbar";

        var items = headerRow.querySelectorAll(
            ".header-controls, #bitMobileMenuToggle, #mobileMenuToggle, .mobile-menu-toggle"
        );
        if (!items.length) {
            return;
        }

        items[0].parentNode.insertBefore(toolbar, items[0]);
        items.forEach(function (item) {
            toolbar.appendChild(item);
        });
    }

    function initLegacyMobileMenu() {
        var toggle = document.getElementById("mobileMenuToggle");
        var drawer = document.getElementById("mobileNav");
        if (!toggle || !drawer || toggle.dataset.bitBound) {
            return;
        }
        toggle.dataset.bitBound = "1";

        function closeMenu() {
            toggle.classList.remove("active");
            drawer.classList.remove("active");
            drawer.hidden = true;
            toggle.setAttribute("aria-expanded", "false");
            document.body.style.overflow = "";
        }

        function openMenu() {
            toggle.classList.add("active");
            drawer.classList.add("active");
            drawer.hidden = false;
            toggle.setAttribute("aria-expanded", "true");
            document.body.style.overflow = "hidden";
        }

        toggle.addEventListener("click", function () {
            if (drawer.classList.contains("active")) {
                closeMenu();
            } else {
                openMenu();
            }
        });

        drawer.querySelectorAll("a").forEach(function (link) {
            link.addEventListener("click", closeMenu);
        });

        document.addEventListener("click", function (event) {
            if (
                drawer.classList.contains("active") &&
                !drawer.contains(event.target) &&
                !toggle.contains(event.target)
            ) {
                closeMenu();
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closeMenu();
            }
        });
    }

    function init() {
        forceDarkMode();
        removeThemeControls();
        ensureHeaderControls();
        normalizeLangSwitches();
        initMobileNav();
        initLegacyMobileMenu();
        placeHeaderControls(document.querySelector(".header-controls"));
        groupHeaderToolbar();
        forceDarkMode();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
