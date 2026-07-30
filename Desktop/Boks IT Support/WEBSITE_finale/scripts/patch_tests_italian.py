# -*- coding: utf-8 -*-
"""Patch acceptance tests for Italian language support."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST = ROOT / "scripts" / "test_build_site.py"


def main() -> None:
    text = TEST.read_text(encoding="utf-8")
    replacements = [
        (
            'LANGUAGES = ("de", "en", "fr", "sr", "bs", "hr")',
            'LANGUAGES = ("de", "en", "fr", "it", "sr", "bs", "hr")',
        ),
        (
            'A_LANGUAGES = ("de", "en", "fr", "sr", "bs", "hr")',
            'A_LANGUAGES = ("de", "en", "fr", "it", "sr", "bs", "hr")',
        ),
        (
            'B_LANGUAGES = ("de", "en", "sr", "bs", "hr")',
            'B_LANGUAGES = ("de", "en", "it", "sr", "bs", "hr")',
        ),
        (
            (
                '    assert "it" not in config["paths"]["hospitality"]["languages"]\n'
                '    assert "it" not in config["paths"]["market"]["languages"]\n'
            ),
            (
                '    assert "it" in config["paths"]["hospitality"]["languages"]\n'
                '    assert "it" in config["paths"]["market"]["languages"]\n'
                '    assert config["paths"]["market"]["slugs"]["it"] == "mercato"\n'
            ),
        ),
        (
            (
                '    titles = {\n'
                '        "de": "Unterlagen-Check",\n'
                '        "en": "Document check",\n'
                '        "sr": "Provera dokumentacije",\n'
                '        "bs": "Provjera dokumentacije",\n'
                '        "hr": "Provjera dokumentacije",\n'
                "    }"
            ),
            (
                '    titles = {\n'
                '        "de": "Unterlagen-Check",\n'
                '        "en": "Document check",\n'
                '        "it": "Controllo documenti",\n'
                '        "sr": "Provera dokumentacije",\n'
                '        "bs": "Provjera dokumentacije",\n'
                '        "hr": "Provjera dokumentacije",\n'
                "    }"
            ),
        ),
        (
            (
                "    markers = {\n"
                '        "de": "Vertragspartner bleibe ich",\n'
                '        "en": "I remain the contractual counterparty",\n'
                '        "sr": "Ugovorna strana ostajem ja",\n'
                '        "bs": "Ugovorna strana ostajem ja",\n'
                '        "hr": "Ugovorna strana ostajem ja",\n'
                "    }"
            ),
            (
                "    markers = {\n"
                '        "de": "Vertragspartner bleibe ich",\n'
                '        "en": "I remain the contractual counterparty",\n'
                '        "it": "Il partner contrattuale rimango io",\n'
                '        "sr": "Ugovorna strana ostajem ja",\n'
                '        "bs": "Ugovorna strana ostajem ja",\n'
                '        "hr": "Ugovorna strana ostajem ja",\n'
                "    }"
            ),
        ),
        (
            (
                '            or "Je reste la partie contractuelle" in hospitality\n'
                '            or "Ugovorna strana ostajem ja" in hospitality\n'
            ),
            (
                '            or "Je reste la partie contractuelle" in hospitality\n'
                '            or "Il partner contrattuale rimango io" in hospitality\n'
                '            or "Ugovorna strana ostajem ja" in hospitality\n'
            ),
        ),
        (
            (
                "    for code, marker in {\n"
                '        "de": "Vertragspartner bleibe ich",\n'
                '        "en": "I remain the contractual counterparty",\n'
                '        "fr": "Je reste la partie contractuelle",\n'
                '        "sr": "Ugovorna strana ostajem ja",\n'
                '        "bs": "Ugovorna strana ostajem ja",\n'
                '        "hr": "Ugovorna strana ostajem ja",\n'
                "    }.items():"
            ),
            (
                "    for code, marker in {\n"
                '        "de": "Vertragspartner bleibe ich",\n'
                '        "en": "I remain the contractual counterparty",\n'
                '        "fr": "Je reste la partie contractuelle",\n'
                '        "it": "Il partner contrattuale rimango io",\n'
                '        "sr": "Ugovorna strana ostajem ja",\n'
                '        "bs": "Ugovorna strana ostajem ja",\n'
                '        "hr": "Ugovorna strana ostajem ja",\n'
                "    }.items():"
            ),
        ),
        (
            '"fr": "Ma façon de procéder",\n',
            '"fr": "Ma façon de procéder",\n        "it": "Come procedo",\n',
        ),
        (
            '"fr": r"\\b(nous|notre|nos)\\b",\n',
            (
                '"fr": r"\\b(nous|notre|nos)\\b",\n'
                '        "it": r"\\b(noi|nostro|nostra|nostri|nostre)\\b",\n'
            ),
        ),
        (
            (
                '        "hospitality": {"de-CH", "en", "fr-CH", "sr-Latn", "bs", "hr", "x-default"},\n'
                '        "market": {"de-CH", "en", "sr-Latn", "bs", "hr", "x-default"},\n'
                "    }\n"
                '    shared = {"de-CH", "en", "fr-CH", "sr-Latn", "bs", "hr", "x-default"}'
            ),
            (
                '        "hospitality": {"de-CH", "en", "fr-CH", "it-CH", "sr-Latn", "bs", "hr", "x-default"},\n'
                '        "market": {"de-CH", "en", "it-CH", "sr-Latn", "bs", "hr", "x-default"},\n'
                "    }\n"
                '    shared = {"de-CH", "en", "fr-CH", "it-CH", "sr-Latn", "bs", "hr", "x-default"}'
            ),
        ),
        (
            '"fr": "métadonnées",\n',
            '"fr": "métadonnées",\n        "it": "metadati",\n',
        ),
        (
            '            or "prior agreement" in market\n'
            '            or "prethodni dogovor" in market\n',
            (
                '            or "prior agreement" in market\n'
                '            or "previo accordo" in market\n'
                '            or "prethodni dogovor" in market\n'
            ),
        ),
        (
            "six-week|sechs wochen|",
            "six-week|sechs wochen|sei settimane|",
        ),
        (
            "written mandate|schriftlichem mandat|",
            "written mandate|schriftlichem mandat|mandato scritto|",
        ),
    ]
    for old, new in replacements:
        if old not in text:
            if new.strip() in text:
                continue
            raise SystemExit(f"Missing expected snippet:\n{old[:120]}")
        text = text.replace(old, new, 1)

    TEST.write_text(text, encoding="utf-8")
    site = json.loads((ROOT / "config" / "site.json").read_text(encoding="utf-8"))
    codes = [item["code"] for item in site["languages"]]
    if "it" not in codes:
        raise SystemExit("Italian missing from site.json")
    print("tests updated; languages", codes)


if __name__ == "__main__":
    main()
