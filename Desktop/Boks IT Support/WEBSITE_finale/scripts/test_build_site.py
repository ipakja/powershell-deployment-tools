"""Acceptance tests for the two-path static build."""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

import build_site

LANGUAGES = ("de", "en", "fr", "it", "sr", "bs", "hr")
A_LANGUAGES = ("de", "en", "fr", "it", "sr", "bs", "hr")
B_LANGUAGES = ("de", "en", "fr", "it", "sr", "bs", "hr")


class LinkParser(HTMLParser):
    """Collect links from built HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


def setup_module() -> None:
    """Build output once for acceptance checks."""
    build_site.build()


def page(path: str) -> str:
    """Read one generated route."""
    return (build_site.ROOT / path / "index.html").read_text(encoding="utf-8")


def test_routes_prices_and_contact_are_centralized() -> None:
    config = build_site.load_config()
    assert config["prices"] == {
        "hourly": "CHF 120",
        "small_job": "CHF 190",
        "zurich_travel": "CHF 35",
        "pilot": "CHF 4'900",
        "pilot_payment": "50/50",
    }
    assert config["contact"]["phone_href"] == "tel:+41782632701"
    assert "41782632701" in config["contact"]["whatsapp_url"]
    assert "41782632701" in config["contact"]["viber_url"]
    assert "it" in config["paths"]["hospitality"]["languages"]
    assert "it" in config["paths"]["market"]["languages"]
    assert config["paths"]["market"]["slugs"]["it"] == "mercato"


def test_root_is_gateway_without_contact_or_hero_extras() -> None:
    root = (build_site.ROOT / "index.html").read_text(encoding="utf-8")
    assert root.count('class="gateway-card"') == 2
    assert "/de/hospitality/" in root and "/de/markt/" in root
    assert "BIT — Stefan Bogdanovic, Zürich" in root
    assert 'href="/de/legal/"' in root
    assert "Impressum" in root
    assert "Zwei getrennte Leistungsbereiche" in root
    assert not re.search(r"(wa\.me|viber:|mailto:|tel:|floating-contact|trust-line)", root)
    assert "<form" not in root.lower()


def test_south_slavic_gateways_are_fully_localized() -> None:
    german_markers = (
        "Zwei getrennte",
        "Bitte wählen",
        "für Schweizer Hotels",
        "für internationale Anbieter",
        "Leistungsbereiche",
    )
    expected = {
        "sr": {
            "title": "Dve odvojene oblasti usluga.",
            "subtitle": "Izaberite onu koja vam odgovara.",
            "city": "Cirih",
            "meta": "Dve odvojene oblasti usluga",
        },
        "bs": {
            "title": "Dvije odvojene oblasti usluga.",
            "subtitle": "Odaberite onu koja vam odgovara.",
            "city": "Cirih",
            "meta": "Dvije odvojene oblasti usluga",
        },
        "hr": {
            "title": "Dva odvojena područja usluga.",
            "subtitle": "Odaberite ono koje vam odgovara.",
            "city": "Cirih",
            "meta": "Dva odvojena područja usluga",
        },
    }
    for code, values in expected.items():
        text = page(code)
        assert values["title"] in text
        assert values["subtitle"] in text
        assert f"Stefan Bogdanović, {values['city']}" in text
        assert values["meta"] in text
        assert f"/{code}/hospitality/" in text
        assert "gateway-note" not in text
        assert all(marker not in text for marker in german_markers)


def test_south_slavic_pages_use_diacritic_name() -> None:
    for code in ("sr", "bs", "hr"):
        for route in (
            code,
            f"{code}/trziste",
            f"{code}/hospitality",
            f"{code}/about",
            f"{code}/legal",
        ):
            text = page(route)
            assert "Bogdanović" in text
            assert "Bogdanovic" not in text


def test_contractual_counterparty_line_is_present() -> None:
    """Keep the factual first-person responsibility wording, not the old provider phrase."""
    markers = {
        "de": "Vertragspartner bleibe ich",
        "en": "I remain the contractual counterparty",
        "fr": "Je reste la partie contractuelle",
        "it": "Il partner contrattuale rimango io",
        "sr": "Ugovorna strana ostajem ja",
        "bs": "Ugovorna strana ostajem ja",
        "hr": "Ugovorna strana ostajem ja",
    }
    forbidden = "Verantwortung und Qualitätssicherung bleiben bei BIT"
    config = build_site.load_config()
    for code in B_LANGUAGES:
        market = page(f'{code}/{config["paths"]["market"]["slugs"][code]}')
        assert markers[code] in market
        assert forbidden not in market
        assert (
            "vorheriger Absprache" in market
            or "prior agreement" in market
            or "accord préalable" in market
            or "previo accordo" in market
            or "prethodni dogovor" in market
        )
    for code in A_LANGUAGES:
        hospitality = page(f'{code}/{config["paths"]["hospitality"]["slugs"][code]}')
        assert forbidden not in hospitality
        assert (
            "Vertragspartner bleibe ich" in hospitality
            or "I remain the contractual counterparty" in hospitality
            or "Je reste la partie contractuelle" in hospitality
            or "Il partner contrattuale rimango io" in hospitality
            or "Ugovorna strana ostajem ja" in hospitality
        )
    for code, marker in {
        "de": "Vertragspartner bleibe ich",
        "en": "I remain the contractual counterparty",
        "fr": "Je reste la partie contractuelle",
        "it": "Il partner contrattuale rimango io",
        "sr": "Ugovorna strana ostajem ja",
        "bs": "Ugovorna strana ostajem ja",
        "hr": "Ugovorna strana ostajem ja",
    }.items():
        legal = page(f"{code}/legal")
        assert marker in legal
        assert "pripremamo" not in legal
        assert "garantujemo" not in legal
        assert "garantiramo" not in legal
        assert "jamčimo" not in legal


def test_hospitality_south_slavic_terminology() -> None:
    """Serbian ekavica / Bosnian-Croatian ijekavica IT terms stay locale-correct."""
    sr = page("sr/hospitality")
    assert "računar" in sr and "štampač" in sr and "podešavanja" in sr
    assert "Dokumentujem naloge, uloge, ažuriranja i predaju" in sr
    assert "operativnim sistemom" not in sr
    bs = page("bs/hospitality")
    assert "računar" in bs and "štampač" in bs and "postavke" in bs
    hr = page("hr/hospitality")
    assert "računal" in hr and "pisač" in hr and "postavke" in hr
    assert "Dokumentiram račune, uloge, ažuriranja i predaju" in hr
    assert "operacijskim sustavom" not in hr


def test_market_entry_product_precedes_pilot() -> None:
    config = build_site.load_config()
    titles = {
        "de": "Unterlagen-Check",
        "en": "Document check",
        "fr": "Contrôle de documents",
        "it": "Controllo documenti",
        "sr": "Provera dokumentacije",
        "bs": "Provjera dokumentacije",
        "hr": "Provjera dokumentacije",
    }
    for code in B_LANGUAGES:
        text = page(f'{code}/{config["paths"]["market"]["slugs"][code]}')
        offer = re.search(r'id="offer".*?</section>', text, re.S).group(0)
        pilot = re.search(r'id="pilot".*?</section>', text, re.S).group(0)
        assert titles[code] in offer
        assert "CHF 190" in offer
        assert text.index('id="offer"') < text.index('id="pilot"')
        assert "CHF 4&#x27;900" in text
        assert "RAS" not in text


def test_about_and_legal_language_switch_stays_on_page_type() -> None:
    for page_type in ("about", "legal"):
        for code in LANGUAGES:
            text = page(f"{code}/{page_type}")
            menu = re.search(r'<nav class="language-nav".*?</nav>', text, re.S).group(0)
            for target in LANGUAGES:
                assert f'href="/{target}/{page_type}/"' in menu
            assert not re.search(r'href="/[a-z]{2}/"[^>]*>[A-Z]{2}</a>', menu)


def test_gateway_exclusions_heading_is_first_person() -> None:
    text = page("de/hospitality")
    assert "Was ich nicht mache" in text
    assert "Was ich nicht mache" in page("de/markt")


def test_service_routes_have_exact_path_language_menus() -> None:
    config = build_site.load_config()
    for path_key, expected in (("hospitality", A_LANGUAGES), ("market", B_LANGUAGES)):
        for language in expected:
            slug = config["paths"][path_key]["slugs"][language]
            text = page(f"{language}/{slug}")
            menu = re.search(r'<nav class="language-nav".*?</nav>', text, re.S).group(0)
            labels = re.findall(r">([A-Z]{2})</a>", menu)
            assert labels == [code.upper() for code in expected]


def test_paths_never_cross_link() -> None:
    config = build_site.load_config()
    a_routes = {
        f'/{code}/{config["paths"]["hospitality"]["slugs"][code]}/'
        for code in A_LANGUAGES
    }
    b_routes = {
        f'/{code}/{config["paths"]["market"]["slugs"][code]}/'
        for code in B_LANGUAGES
    }
    for code in A_LANGUAGES:
        text = page(f'{code}/{config["paths"]["hospitality"]["slugs"][code]}')
        assert not any(route in text for route in b_routes)
    for code in B_LANGUAGES:
        text = page(f'{code}/{config["paths"]["market"]["slugs"][code]}')
        assert not any(route in text for route in a_routes)


def test_hospitality_has_five_step_workflow_only() -> None:
    """Render the localized workflow on Path A without changing Path B."""
    config = build_site.load_config()
    titles = {
        "de": "So gehe ich vor",
        "en": "How I proceed",
        "fr": "Ma façon de procéder",
        "it": "Come procedo",
        "sr": "Kako postupam",
        "bs": "Kako postupam",
        "hr": "Kako postupam",
    }
    for code in A_LANGUAGES:
        text = page(f'{code}/{config["paths"]["hospitality"]["slugs"][code]}')
        process = re.search(
            r'<section class="section" id="process">(.*?)</section>', text, re.S
        )
        assert process
        assert titles[code] in process.group(1)
        assert process.group(1).count('class="process-step"') == 5
        assert "Revenue" in text or "revenue" in text

    for code in B_LANGUAGES:
        text = page(f'{code}/{config["paths"]["market"]["slugs"][code]}')
        assert 'id="process"' not in text


def test_prices_exclusions_and_pilot_terms_are_visible() -> None:
    config = build_site.load_config()
    for code in A_LANGUAGES:
        text = page(f'{code}/{config["paths"]["hospitality"]["slugs"][code]}')
        assert "CHF 120" in text and "CHF 190" in text and "CHF 35" in text
        assert 'id="limits"' in text
        assert all(
            term not in text.lower()
            for term in (">dns<", "basis-security", "process & project")
        )
        assert "Revenue" in text or "revenue" in text
    for code in B_LANGUAGES:
        text = page(f'{code}/{config["paths"]["market"]["slugs"][code]}')
        assert "CHF 4&#x27;900" in text
        assert re.search(r"50\s*%", text) and 'id="limits"' in text
        assert re.search(
            r"(six-week|sechs wochen|sei settimane|six semaines|šestonedelj|šestosedmi|šestotjed)",
            text,
            re.I,
        )
        assert re.search(
            r"(written mandate|schriftlichem mandat|mandat écrit|mandato scritto|pisani mandat)",
            text,
            re.I,
        )


def test_first_person_and_origin_language_on_marketing_pages() -> None:
    config = build_site.load_config()
    provider_plural = {
        "de": r"\b(wir|uns|unser(?:e|er|em|en|es)?)\b",
        "en": r"\b(we|our|ours|us)\b",
        "fr": r"\b(nous|notre|nos)\b",
        "it": r"\b(noi|nostro|nostra|nostri|nostre)\b",
        "sr": r"\b(mi|naš(?:a|e|i)?)\b",
        "bs": r"\b(mi|naš(?:a|e|i)?)\b",
        "hr": r"\b(mi|naš(?:a|e|i)?)\b",
    }
    origin_terms = (
        r"\b(Balkan|Balkans|Serbia|Southeast Europe|Jugoistočna|Balkan(?:a|u|om)?)\b"
    )
    for path_key, codes in (("hospitality", A_LANGUAGES), ("market", B_LANGUAGES)):
        for code in codes:
            slug = config["paths"][path_key]["slugs"][code]
            text = re.sub(r"<[^>]+>", " ", page(f"{code}/{slug}"))
            assert not re.search(provider_plural[code], text, re.I)
            assert not re.search(origin_terms, text, re.I)


def test_hreflang_and_schema_are_path_specific() -> None:
    config = build_site.load_config()
    expected = {
        "hospitality": {"de-CH", "en", "fr-CH", "it-CH", "sr-Latn", "bs", "hr", "x-default"},
        "market": {"de-CH", "en", "fr-CH", "it-CH", "sr-Latn", "bs", "hr", "x-default"},
    }
    shared = {"de-CH", "en", "fr-CH", "it-CH", "sr-Latn", "bs", "hr", "x-default"}
    for path_key, codes in (("hospitality", A_LANGUAGES), ("market", B_LANGUAGES)):
        for code in codes:
            text = page(f'{code}/{config["paths"][path_key]["slugs"][code]}')
            assert set(re.findall(r'hreflang="([^"]+)"', text)) == expected[path_key]
            schema = json.loads(
                re.search(
                    r'<script type="application/ld\+json">(.*?)</script>', text, re.S
                ).group(1)
            )
            assert schema["@type"] == "ProfessionalService"
            assert schema["alternateName"] == config["brand"]
            assert schema["areaServed"]["name"] == "CH"
            assert schema["founder"]["name"] == build_site.SiteRenderer.personal_name(code)
            assert schema["contactPoint"]
    for code in LANGUAGES:
        about = page(f"{code}/about")
        legal = page(f"{code}/legal")
        assert set(re.findall(r'hreflang="([^"]+)"', about)) == shared
        assert set(re.findall(r'hreflang="([^"]+)"', legal)) == shared
        assert set(re.findall(r'hreflang="([^"]+)"', page(code))) == shared
        about_schema = json.loads(
            re.search(
                r'<script type="application/ld\+json">(.*?)</script>', about, re.S
            ).group(1)
        )
        assert about_schema["@type"] == "ProfessionalService"


def test_legal_and_about_facts() -> None:
    english_blob = (
        "Key points of the terms",
        "WhatsApp and Viber may process",
        "comprehensive legal advice",
    )
    privacy_markers = {
        "de": "Metadaten",
        "en": "metadata",
        "fr": "métadonnées",
        "it": "metadati",
        "sr": "metapodatke",
        "bs": "metapodatke",
        "hr": "metapodatke",
    }
    for code in LANGUAGES:
        legal = page(f"{code}/legal")
        about = page(f"{code}/about")
        assert "Einzelfirma" in legal
        assert "Schaffhauserstrasse 457" in legal
        assert "WhatsApp" in legal and "Viber" in legal
        assert privacy_markers[code].lower() in legal.lower()
        assert "UID" not in legal and "VAT ID" not in legal
        assert "/ICH.png" in about
        if code != "en":
            assert all(blob not in legal for blob in english_blob)


def test_no_forms_web3forms_or_wrong_numbers() -> None:
    for html_file in build_site.ROOT.rglob("index.html"):
        text = html_file.read_text(encoding="utf-8")
        assert "<form" not in text.lower()
        assert "web3forms" not in text.lower()
        for match in re.findall(r"(?:tel:|wa\.me/|number=%2B)(\d+)", text):
            assert match == "41782632701"


def test_all_generated_internal_links_resolve() -> None:
    root = Path(build_site.ROOT)
    for html_file in root.rglob("index.html"):
        if "templates" in html_file.parts:
            continue
        parser = LinkParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for href in parser.links:
            parsed = urlparse(href)
            if not href.startswith("/") or parsed.netloc:
                continue
            route = parsed.path
            target = root / route.lstrip("/")
            if route.endswith("/"):
                target = target / "index.html"
            assert target.exists(), f"{html_file}: unresolved {href}"



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
    assert "Zürich" not in hr
    assert "samostalna djelatnost" in hr
    fr_market = page("fr/marche")
    assert "Contrôle de documents" in fr_market
    assert 'hreflang="fr-CH"' in fr_market


def test_hr_city_spelling_is_cirih_everywhere() -> None:
    """Croatian pages use Cirih consistently, never Zürich."""
    for path in ("hr", "hr/hospitality", "hr/trziste", "hr/about", "hr/legal"):
        text = page(path)
        assert "Cirih" in text
        assert "Zürich" not in text


def test_it_legal_terms_order_and_specialists() -> None:
    """Italian imprint: specialists, then counterparty, then key-points disclaimer."""
    text = page("it/legal")
    assert "Coinvolgo specialisti esterni solo previo accordo" in text
    specialist = text.index("Coinvolgo specialisti esterni solo previo accordo")
    partner = text.index("Il partner contrattuale rimango io")
    disclaimer = text.index("Si tratta di punti essenziali")
    assert specialist < partner < disclaimer


def test_hospitality_meta_uses_revenue_data_wording() -> None:
    """Hospitality meta descriptions align on scoped revenue-data review."""
    markers = {
        "de": "Revenue-Datenprüfung",
        "en": "revenue-data review",
        "fr": "données de revenue",
        "it": "dati di revenue",
        "sr": "revenue-podataka",
        "bs": "revenue-podataka",
        "hr": "revenue-podataka",
    }
    for code, marker in markers.items():
        text = page(f"{code}/hospitality")
        desc = re.search(r'name="description" content="([^"]+)"', text).group(1)
        assert marker in desc
        assert "Revenue-Management-Unterstützung" not in desc
