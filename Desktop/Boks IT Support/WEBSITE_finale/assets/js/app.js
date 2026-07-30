import { initContactLinks } from "./contact-links.js";
import { initLanguagePreference } from "./language-preference.js";
import { initMobileNav } from "./mobile-nav.js";

/** Initialize the shared site chrome. */
export function initChrome(root = document) {
    initMobileNav(root);
    initContactLinks(root);
    initLanguagePreference(root);
}

initChrome();
