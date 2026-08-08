const STORAGE_KEY = "bit-language";
const DISMISSED_KEY = "bit-language-suggestion-dismissed";
const SUPPORTED = new Set(["de", "en", "fr", "sr", "bs", "hr"]);

/** Save an explicit language choice without forcing future redirects. */
export function setLanguage(language, storage = window.localStorage) {
    if (SUPPORTED.has(language)) {
        storage.setItem(STORAGE_KEY, language);
    }
}

/** Return the best supported browser language, if available. */
export function getSuggestedLanguage(navigatorObject = window.navigator) {
    const requested = navigatorObject.languages || [navigatorObject.language];

    for (const locale of requested) {
        const language = String(locale || "").toLowerCase().split("-")[0];
        if (SUPPORTED.has(language)) {
            return language;
        }
    }
    return null;
}

/** Suggest a browser language once; never redirect automatically. */
export function initLanguagePreference(root = document) {
    const current = root.body?.dataset.currentLanguage;
    const navigation = root.querySelector("[data-language-nav]");
    if (!current || !navigation) {
        return;
    }

    navigation.querySelectorAll("a[href]").forEach((link) => {
        const language = new URL(link.href).pathname.split("/").filter(Boolean)[0];
        link.addEventListener("click", () => setLanguage(language));
    });

    const saved = window.localStorage.getItem(STORAGE_KEY);
    const suggested = saved || getSuggestedLanguage();
    if (
        window.sessionStorage.getItem(DISMISSED_KEY) ||
        !suggested ||
        suggested === current ||
        !SUPPORTED.has(suggested)
    ) {
        return;
    }

    const prompt = root.body.dataset.languagePrompt;
    const switchLabel = root.body.dataset.languageSwitch;
    const dismissLabel = root.body.dataset.languageDismiss;
    if (!prompt || !switchLabel || !dismissLabel) {
        return;
    }

    const banner = root.createElement("aside");
    banner.className = "language-suggestion";
    banner.setAttribute("aria-label", prompt);

    const text = root.createElement("p");
    text.textContent = prompt;

    const link = root.createElement("a");
    link.className = "button button-secondary";
    link.href = `/${suggested}/`;
    link.textContent = `${switchLabel}: ${suggested.toUpperCase()}`;
    link.addEventListener("click", () => setLanguage(suggested));

    const dismiss = root.createElement("button");
    dismiss.type = "button";
    dismiss.textContent = dismissLabel;
    dismiss.addEventListener("click", () => {
        window.sessionStorage.setItem(DISMISSED_KEY, "1");
        banner.remove();
    });

    banner.append(text, link, dismiss);
    root.body.appendChild(banner);
}
