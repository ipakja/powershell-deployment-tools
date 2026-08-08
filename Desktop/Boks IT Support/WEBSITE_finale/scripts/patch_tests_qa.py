# -*- coding: utf-8 -*-
"""Update tests after QA fixes (FR market, Cirih HR, about dedupe)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST = ROOT / "scripts" / "test_build_site.py"


def main() -> None:
    text = TEST.read_text(encoding="utf-8")
    reps = [
        (
            'B_LANGUAGES = ("de", "en", "it", "sr", "bs", "hr")',
            'B_LANGUAGES = ("de", "en", "fr", "it", "sr", "bs", "hr")',
        ),
        (
            '"city": "Zürich",\n            "meta": "Dva odvojena područja usluga",',
            '"city": "Cirih",\n            "meta": "Dva odvojena područja usluga",',
        ),
        (
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
            (
                '    titles = {\n'
                '        "de": "Unterlagen-Check",\n'
                '        "en": "Document check",\n'
                '        "fr": "Contrôle de documents",\n'
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
                '        "it": "Il partner contrattuale rimango io",\n'
                '        "sr": "Ugovorna strana ostajem ja",\n'
                '        "bs": "Ugovorna strana ostajem ja",\n'
                '        "hr": "Ugovorna strana ostajem ja",\n'
                "    }"
            ),
            (
                "    markers = {\n"
                '        "de": "Vertragspartner bleibe ich",\n'
                '        "en": "I remain the contractual counterparty",\n'
                '        "fr": "Je reste la partie contractuelle",\n'
                '        "it": "Il partner contrattuale rimango io",\n'
                '        "sr": "Ugovorna strana ostajem ja",\n'
                '        "bs": "Ugovorna strana ostajem ja",\n'
                '        "hr": "Ugovorna strana ostajem ja",\n'
                "    }"
            ),
        ),
        (
            '            or "prior agreement" in market\n'
            '            or "previo accordo" in market\n'
            '            or "prethodni dogovor" in market\n',
            (
                '            or "prior agreement" in market\n'
                '            or "accord préalable" in market\n'
                '            or "previo accordo" in market\n'
                '            or "prethodni dogovor" in market\n'
            ),
        ),
        (
            (
                '        "market": {"de-CH", "en", "it-CH", "sr-Latn", "bs", "hr", "x-default"},\n'
            ),
            (
                '        "market": {"de-CH", "en", "fr-CH", "it-CH", "sr-Latn", "bs", "hr", "x-default"},\n'
            ),
        ),
    ]
    for old, new in reps:
        if old not in text:
            if new in text:
                continue
            raise SystemExit(f"missing snippet:\n{old[:140]}")
        text = text.replace(old, new, 1)

    # Add focused regression tests if missing
    if "test_about_has_no_duplicate_specialist_sentence" not in text:
        text += '''


def test_about_has_no_duplicate_specialist_sentence() -> None:
    """About pages must not repeat the external-specialist clause."""
    for code in LANGUAGES:
        text = page(f"{code}/about")
        assert text.count("vorheriger Absprache") <= 1
        assert text.count("prior agreement") <= 1
        assert text.count("prethodni dogovor") <= 1
        assert "Externe Fachpersonen beziehe ich nur nach vorheriger Absprache ein" not in text or text.count("Externe Fachpersonen") == 1


def test_legal_activity_requires_written_mandate_and_localized_entity() -> None:
    """Imprint activity must qualify representation; entity type is localized."""
    de = page("de/legal")
    assert "schriftlichen Mandats" in de
    assert "Einzelfirma" in de
    sr = page("sr/legal")
    assert "pisanog mandata" in sr
    assert "samostalna delatnost" in sr
    hr = page("hr/legal")
    assert "Cirih" in hr
    assert "samostalna djelatnost" in hr
    fr_market = page("fr/marche")
    assert "Contrôle de documents" in fr_market
    assert 'hreflang="fr-CH"' in fr_market
'''

    TEST.write_text(text, encoding="utf-8")
    print("tests updated")


if __name__ == "__main__":
    main()
