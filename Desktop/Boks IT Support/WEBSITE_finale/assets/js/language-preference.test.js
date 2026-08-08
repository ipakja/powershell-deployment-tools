import { describe, expect, it } from "vitest";

import { getSuggestedLanguage, setLanguage } from "./language-preference.js";


describe("language preference", () => {
    it("selects the first supported browser language", () => {
        expect(
            getSuggestedLanguage({ languages: ["it-CH", "fr-CH", "de-CH"] }),
        ).toBe("fr");
    });

    it("returns null when no browser language is supported", () => {
        expect(getSuggestedLanguage({ languages: ["it-CH", "es"] })).toBeNull();
    });

    it("persists only supported explicit choices", () => {
        const values = new Map();
        const storage = {
            setItem: (key, value) => values.set(key, value),
        };

        setLanguage("sr", storage);
        setLanguage("it", storage);

        expect(values.get("bit-language")).toBe("sr");
    });
});
