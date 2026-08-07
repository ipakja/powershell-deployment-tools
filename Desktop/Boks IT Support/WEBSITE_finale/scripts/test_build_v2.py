"""Acceptance tests for Zustand-A DE+EN build."""
from __future__ import annotations

import re

import build_site


def setup_module() -> None:
    """Build once for acceptance checks."""
    build_site.build()


def read(path: str) -> str:
    """Read generated HTML."""
    target = build_site.ROOT / path
    if target.is_dir():
        target = target / "index.html"
    return target.read_text(encoding="utf-8")


def test_impressum_is_sole_proprietorship_with_address() -> None:
    legal = read("de/legal/index.html")
    assert "wird derzeit geklärt" not in legal
    assert "Stefan Bogdanovic" in legal
    assert "Einzelunternehmen" in legal
    assert "Schaffhauserstrasse 457" in legal
    assert "8052" in legal
    assert "admin@boksitsupport.ch" in legal
    assert "+41 78 263 27 01" in legal
    assert "Inhaltlich verantwortlich" in legal
    assert "kein Kontaktformular" not in legal
    assert "FormSubmit" not in legal
    assert "Resend" in legal
    assert "Bedarfsabklärung" in legal
    assert "höchstens zwölf Monate" in legal
    assert "/api/inquiry" not in legal
    assert "KV-Speicher" not in legal
    assert "Sobald das Formular freigeschaltet" not in legal
    assert "<!-- BESTÄTIGUNG ERFORDERLICH: Aufbewahrungsdauer Anfragen -->" not in legal
    assert "INQUIRY_LOG" not in legal
    assert "INQUIRY_NOTIFY_EMAIL" not in legal
    assert "Stand: August 2026" in legal
    assert "IT-Support" in legal or "IT-Koordination" in legal
    assert "Market Development" not in legal
    assert 'class="main-nav"' in legal
    assert 'href="/de/beispiele/"' in legal
    assert "Beispiele" in legal
    menu = re.search(r'<nav class="language-nav".*?</nav>', legal, re.S).group(0)
    assert ">DE<" in menu and ">EN<" in menu
    assert ">FR<" not in menu and ">SR<" not in menu
    en = read("en/legal/index.html")
    assert "currently being clarified" not in en
    assert "sole proprietorship" in en
    assert "Schaffhauserstrasse 457" in en
    assert "no contact form" not in en.lower()
    assert "FormSubmit" not in en
    assert "Resend" in en
    assert "twelve months" in en
    assert "/api/inquiry" not in en
    assert "KV storage" not in en
    assert "Once the form is enabled" not in en
    assert "INQUIRY_LOG" not in en
    assert "INQUIRY_NOTIFY_EMAIL" not in en
    assert "Last updated: August 2026" in en
    assert "needs assessment" in en.lower()
    assert 'href="/en/examples/"' in en
    assert "Examples" in en
    en_menu = re.search(r'<nav class="language-nav".*?</nav>', en, re.S).group(0)
    assert 'href="/de/legal/"' in en_menu and 'href="/en/legal/"' in en_menu
    assert ">FR<" not in en_menu


def test_homepage_zurich_pilot_concerns_and_footer() -> None:
    de = read("de/index.html")
    en = read("en/index.html")
    assert "IT-Support für kleine Unternehmen ohne eigene IT" in de
    assert "IT-Koordination für Zürich und remote in der Schweiz" in de
    assert "Zürich und remote in der Schweiz" in de
    assert "Wer dahintersteht" in de
    assert "Stefan Bogdanovic, Zürich" in de
    assert "IT-Anliegen prüfen lassen" in de
    assert "begrenzten Einführungsbetriebs" in de
    assert 'href="/de/anfrage/?area=users-access"' in de
    assert 'href="/de/leistungen/benutzer-und-zugaenge/">Ein ehemaliger' not in de
    assert 'href="/de/anfrage/?area=users-access">Ein ehemaliger Mitarbeiter hat noch aktive Konten<' in de
    assert 'href="/de/market-access/">Market Access<' not in de
    assert "Market Access (Archiv)" not in de
    hero = re.search(r'<section class="hero">.*?</section>', de, re.S).group(0)
    eyebrow = re.search(r'class="eyebrow">(.*?)</p>', hero).group(1)
    h1 = re.search(r"<h1>(.*?)</h1>", hero).group(1)
    assert eyebrow != h1
    assert hero.index("hero-actions") < hero.index("pilot-banner")
    assert "IT support for small businesses without in-house IT" in en
    assert "IT coordination for Zurich and remote across Switzerland" in en
    assert "Zurich and remote across Switzerland" in en
    assert 'href="/en/inquiry/?area=users-access"' in en
    assert 'href="/en/services/users-and-access/">A former employee' not in en
    assert 'href="/en/inquiry/?area=users-access">A former employee still has active accounts<' in en
    assert 'href="/en/market-access/">Market Access<' not in en
    assert "Market Access (archive)" not in en
    assert "inquiry" in read("de/anfrage/index.html")
    assert 'value="users-access"' in read("de/anfrage/index.html")
    assert 'id="inquiry-form"' in read("de/anfrage/index.html")
    assert 'data-inquiry-offline="true"' not in read("de/anfrage/index.html")
    cta_de = re.search(r'id="cta".*?</section>', de, re.S).group(0)
    assert cta_de.count("Rückmeldung in der Regel innerhalb von zwei Arbeitstagen") == 1
    assert de.count("IT-Basischeck ab CHF 190") == 1
    cta_en = re.search(r'id="cta".*?</section>', en, re.S).group(0)
    assert cta_en.count("Reply usually within two working days") == 1
    assert en.count("IT basics check from CHF 190") == 1

def test_english_home_and_language_switch() -> None:
    en = read("en/index.html")
    assert "IT support for small businesses without in-house IT" in en
    assert "Have your IT need reviewed" in en
    assert "Describe a pilot need" not in en
    assert "IT support" in en
    assert "gateway-card" not in en
    assert "Market Access Switzerland" not in en
    assert "Zwei getrennte" not in en
    assert 'hreflang="de-CH"' in en and 'hreflang="en"' in en
    menu = re.search(r'<nav class="language-nav".*?</nav>', en, re.S).group(0)
    assert 'href="/de/"' in menu and 'href="/en/"' in menu
    assert ">FR<" not in menu
    de = read("de/index.html")
    assert 'href="/en/"' in de
    assert "IT-Anliegen prüfen lassen" in de
    assert "Pilotbedarf schildern" not in de
    assert "Anliegen unverbindlich schildern" not in de
    assert "gateway-card" not in de
    assert "Zwei getrennte" not in de
    root = (build_site.ROOT / "index.html").read_text(encoding="utf-8")
    assert "gateway-card" not in root
    assert "Zwei getrennte" not in root
    assert 'url=/de/' in root or 'href="/de/"' in root
    assert "Market Access Switzerland" not in root


def test_language_switch_stays_on_page_type() -> None:
    de_services = read("de/leistungen/index.html")
    menu = re.search(r'<nav class="language-nav".*?</nav>', de_services, re.S).group(0)
    assert 'href="/en/services/"' in menu
    en_inquiry = read("en/inquiry/index.html")
    menu = re.search(r'<nav class="language-nav".*?</nav>', en_inquiry, re.S).group(0)
    assert 'href="/de/anfrage/"' in menu


def test_sitemap_includes_de_and_en_not_fr() -> None:
    sitemap = (build_site.ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert "https://boksitsupport.ch/de/" in sitemap
    assert "https://boksitsupport.ch/en/" in sitemap
    assert "https://boksitsupport.ch/en/inquiry/" in sitemap
    assert "/fr/" not in sitemap
    assert "market-access" not in sitemap


def test_market_access_redirects_to_home_no_html() -> None:
    """Old market URLs 301 to current home; no crawlable archive HTML."""
    assert not (build_site.ROOT / "de" / "market-access").exists()
    assert not (build_site.ROOT / "en" / "market-access").exists()
    home_de = read("de/index.html")
    home_en = read("en/index.html")
    legal_de = read("de/legal/index.html")
    assert 'href="/de/market-access/"' not in home_de
    assert 'href="/en/market-access/"' not in home_en
    assert 'href="/de/market-access/"' not in legal_de
    redirects = (build_site.ROOT / "_redirects").read_text(encoding="utf-8")
    assert "/de/market-access/ /de/ 301" in redirects
    assert "/en/market-access/ /en/ 301" in redirects
    assert "/de/markt/ /de/ 301" in redirects
    assert "/en/market/ /en/ 301" in redirects
    assert "/ /de/ 301" in redirects
    assert "/index.html /de/ 301" in redirects
    mw = (build_site.ROOT / "functions" / "_middleware.js").read_text(encoding="utf-8")
    assert "market-access" in mw
    assert 'pathname === "/"' in mw
    assert "https://boksitsupport.ch/de/" in mw


def test_redirects_keep_en_live_and_fr_302_via_middleware() -> None:
    redirects = (build_site.ROOT / "_redirects").read_text(encoding="utf-8")
    assert "/en/market/ /en/ 301" in redirects
    assert "/index_en.html /en/ 302" in redirects
    mw = (build_site.ROOT / "functions" / "_middleware.js").read_text(encoding="utf-8")
    assert "fr|it|sr|bs|hr" in mw
    assert "en|" not in mw or "^(fr|" in mw


def test_prices_richtwerte_no_pilot_on_it_pages() -> None:
    for path in ("de/leistungen/index.html", "en/services/index.html"):
        text = read(path)
        assert "CHF 120" in text and "CHF 190" in text
        assert "4&#x27;900" not in text and "4'900" not in text


def test_no_travel_flat_rate_remote_policy_on_it_pages() -> None:
    """IT price surfaces use remote-first wording, not CHF 35 travel."""
    de_remote = (
        "Die meisten Anfragen werden remote bearbeitet. Ist ein Termin vor Ort "
        "erforderlich, wird er vorab vereinbart und im Angebot separat ausgewiesen "
        "– im Raum Zürich."
    )
    en_remote = (
        "Most requests are handled remotely. If an on-site appointment is required, "
        "it is agreed in advance and listed separately in the quote — Zurich area."
    )
    for path in (
        "de/leistungen/index.html",
        "de/faq/index.html",
        "en/services/index.html",
        "en/faq/index.html",
    ):
        text = read(path)
        assert "CHF 35" not in text
        assert "Anfahrt innerhalb Zürichs" not in text
        assert "Travel within Zurich" not in text
    assert de_remote in read("de/leistungen/index.html")
    assert de_remote in read("de/faq/index.html")
    assert en_remote in read("en/services/index.html")
    assert en_remote in read("en/faq/index.html")


def test_footer_offline_and_inquiry_gated() -> None:
    """When inquiry.live is true: form enabled; footer uses live channel note."""
    home = read("de/index.html")
    assert "Anfrageformular" in home
    assert "Direktweg" in home or "WhatsApp" in home
    inquiry = read("de/anfrage/index.html")
    assert 'data-inquiry-offline="true"' not in inquiry
    assert 'disabled="disabled"' not in inquiry
    assert 'type="submit"' in inquiry
    assert "inquiry-form.js?v=10" in inquiry
    en_inquiry = read("en/inquiry/index.html")
    assert 'data-inquiry-offline="true"' not in en_inquiry
    assert "Form delivery is being set up" not in en_inquiry


def test_inquiry_offline_markup_when_gated() -> None:
    """Build helper still emits HTML disabled when live is false (regression)."""
    import copy

    import build_v2_de

    cfg = copy.deepcopy(build_v2_de.load_v2("de"))
    cfg["inquiry"]["live"] = False
    html = build_v2_de.inquiry_main(cfg)
    assert 'data-inquiry-offline="true"' in html
    assert 'disabled="disabled"' in html
    assert 'aria-disabled="true"' in html


def test_inquiry_direct_path_whatsapp_and_mailto() -> None:
    """Anfrage/inquiry: dual-path buttons above form; home closing has WhatsApp secondary."""
    de = read("de/anfrage/index.html")
    en = read("en/inquiry/index.html")
    assert "https://wa.me/41782632701?text=" in de
    assert 'data-direct-mailto' in de
    assert 'data-mailto-subject-enc=' in de
    assert 'data-mailto-body-enc=' in de
    assert "Per WhatsApp schildern" in de
    assert "Per E-Mail schildern" in de
    assert "Oder über das Formular" in de
    assert "Am schnellsten geht es so" in de
    assert 'class="inquiry-direct"' in de
    assert 'id="inquiry-form"' in de
    assert de.index("inquiry-direct") < de.index('id="inquiry-form"')
    assert "Rückmeldung in der Regel innerhalb von zwei Arbeitstagen." in de
    assert "Pilotbedarf" not in de
    assert "Viber" not in de
    assert "Market Access (Archiv)" not in de
    assert "Market Access" not in de
    assert 'data-contact="email"' in de
    assert 'data-email-user="admin"' in de
    assert 'data-email-domain="boksitsupport.ch"' in de
    # Visible footer/contact text must not hardcode the full address as link text
    assert re.search(
        r'data-contact="email"[^>]*>\s*<span[^>]*>E-Mail</span>',
        de,
    )

    assert "https://wa.me/41782632701?text=" in en
    assert 'data-direct-mailto' in en
    assert 'data-mailto-subject-enc=' in en
    assert "Describe via WhatsApp" in en
    assert "Describe via email" in en
    assert "Or use the form" in en
    assert "The quickest way is this" in en
    assert "Reply usually within two working days." in en
    assert "Pilotbedarf" not in en
    assert "Viber" not in en
    assert "Market Access (Archiv)" not in en
    assert "Market Access" not in en

    home_de = read("de/index.html")
    home_en = read("en/index.html")
    cta_de = re.search(r'<section class="section" id="cta">.*?</section>', home_de, re.S)
    cta_en = re.search(r'<section class="section" id="cta">.*?</section>', home_en, re.S)
    assert cta_de and "button-primary" in cta_de.group(0)
    assert "button-whatsapp" in cta_de.group(0)
    assert "https://wa.me/41782632701?text=" in cta_de.group(0)
    assert "Per WhatsApp schildern" in cta_de.group(0)
    assert cta_en and "button-whatsapp" in cta_en.group(0)
    assert "Describe via WhatsApp" in cta_en.group(0)
    assert "universal.css?v=15" in de
    assert (build_site.ROOT / "docs" / "INQUIRY_DIRECT.md").is_file()


def test_siz_credentials_published() -> None:
    about = read("de/ueber-bit/index.html")
    en_about = read("en/about-bit/index.html")
    assert "<!-- BESTÄTIGUNG ERFORDERLICH" not in about
    assert "ICT Professional SIZ" in about
    assert "Systems &amp; Network" in about
    assert "ICT Power-User SIZ" in about
    assert "ICT Professional SIZ" in en_about
    assert "ICT Power-User SIZ" in en_about
    home = read("de/index.html")
    assert "Ansprechpartner" in home
    assert "schriftlichem Rahmen" in home or "schriftlicher Rahmen" in home
    assert "nachvollziehbarem Abschluss" in home or "nachvollziehbarer Abschluss" in home


def test_services_rewrite_structure_and_slugs() -> None:
    """New Leistungssektion: statement heading, scope under cards, new slugs."""
    de_home = read("de/index.html")
    de_svc = read("de/leistungen/index.html")
    en_home = read("en/index.html")
    en_svc = read("en/services/index.html")

    assert "Drei klare Einstiege" in de_home
    assert "Drei klare Einstiege" in de_svc
    assert "Three clear entry points" in en_home
    assert "Three clear entry points" in en_svc

    for text in (de_home, de_svc):
        assert "5–50 Mitarbeitenden" in text
        assert "CHF 190" in text
        assert "Leistung ansehen" in text
        assert "benutzer-und-zugaenge" in text
        assert "microsoft-365-arbeitsplatz" in text
        assert "it-basischeck" in text
        assert "Mitarbeiter-Onboarding" not in text

    assert "Anbieterkoordination ist kein eigener" in de_home or "Anbieterkoordination ist kein eigener" in de_svc

    for text in (en_home, en_svc):
        assert "Zurich" in text
        assert "CHF 190" in text
        assert "View service" in text
        assert "users-and-access" in text
        assert "microsoft-365-workplace" in text
        assert "it-basics-check" in text

    # Scope limitation is under cards (body), not the section intro / hero lead alone
    for path in ("de/leistungen/index.html", "en/services/index.html"):
        html = read(path)
        assert "services-scope-note" in html
        hero = re.search(r'<section class="hero">.*?</section>', html, re.S).group(0)
        assert "Nicht jedes Problem ist automatisch enthalten" not in hero
        assert "Not every issue is automatically included" not in hero

    assert "Fachperson" in read("de/leistungen/it-basischeck/index.html") or "Absprache" in read(
        "de/leistungen/it-basischeck/index.html"
    )
    assert "specialist" in read("en/services/it-basics-check/index.html") or "agreement" in read(
        "en/services/it-basics-check/index.html"
    )


def test_legacy_hospitality_and_market_html_removed() -> None:
    """Old dual-path HTML must not exist in deploy output (redirects only)."""
    banned_dirs = [
        "de/hospitality",
        "de/markt",
        "de/market-access",
        "en/hospitality",
        "en/market",
        "en/market-access",
        "fr/hospitality",
        "fr/marche",
        "it/hospitality",
        "it/mercato",
        "sr/hospitality",
        "sr/trziste",
        "bs/hospitality",
        "bs/trziste",
        "hr/hospitality",
        "hr/trziste",
        "de/about",
        "en/about",
    ]
    for rel in banned_dirs:
        path = build_site.ROOT / rel
        assert not path.exists(), f"stale crawlable path still present: {rel}"
    # Safety: no CHF 4'900 pilot copy anywhere under lang market/hospitality names
    for html_file in build_site.ROOT.rglob("index.html"):
        rel = str(html_file.relative_to(build_site.ROOT)).replace("\\", "/")
        if any(
            seg in rel
            for seg in (
                "hospitality",
                "markt",
                "/market/",
                "market-access",
                "marche",
                "mercato",
                "trziste",
            )
        ):
            raise AssertionError(f"unexpected legacy path file: {rel}")
        text = html_file.read_text(encoding="utf-8")
        assert "4&#x27;900" not in text and "4'900" not in text
        assert "gateway-card" not in text
        assert "Zwei getrennte" not in text


def test_hospitality_redirects_all_langs() -> None:
    redirects = (build_site.ROOT / "_redirects").read_text(encoding="utf-8")
    assert "/de/hospitality/ /de/leistungen/ 301" in redirects
    assert "/en/hospitality/ /en/services/ 301" in redirects
    assert "/fr/hospitality/ /de/leistungen/ 301" in redirects
    mw = (build_site.ROOT / "functions" / "_middleware.js").read_text(encoding="utf-8")
    assert "legacyPathRedirect" in mw
    assert "hospitality" in mw


def test_legacy_service_slug_redirects() -> None:
    redirects = (build_site.ROOT / "_redirects").read_text(encoding="utf-8")
    assert (
        "/de/leistungen/onboarding/ /de/leistungen/benutzer-und-zugaenge/ 301" in redirects
    )
    assert (
        "/de/leistungen/offboarding/ /de/leistungen/benutzer-und-zugaenge/ 301" in redirects
    )
    assert (
        "/de/leistungen/arbeitsplatz-anfragen/ /de/leistungen/microsoft-365-arbeitsplatz/ 301"
        in redirects
    )
    assert (
        "/de/leistungen/anbieterkoordination/ /de/leistungen/ 301"
        in redirects
    )
    assert "/en/services/onboarding/ /en/services/users-and-access/ 301" in redirects
    assert "/en/services/offboarding/ /en/services/users-and-access/ 301" in redirects
    assert (
        "/en/services/workplace-requests/ /en/services/microsoft-365-workplace/ 301"
        in redirects
    )
    assert (
        "/en/services/vendor-coordination/ /en/services/ 301"
        in redirects
    )


def test_examples_pages_and_nav() -> None:
    de = read("de/beispiele/index.html")
    en = read("en/examples/index.html")
    assert "Muster: Austritt" in de
    assert "Muster: Neuer Mitarbeiter" in de
    assert "Musterbericht" in de
    assert "Sample:" in en
    assert "IT-Anliegen prüfen lassen" in de
    home = read("de/index.html")
    assert 'href="/de/beispiele/"' in home
    assert "application/ld+json" in home
    assert "ProfessionalService" in home
    faq = read("de/faq/index.html")
    assert "FAQPage" in faq
    inquiry = read("de/anfrage/index.html")
    assert "zwei Arbeitstagen" in inquiry
    assert "Rückmeldung in der Regel innerhalb von zwei Arbeitstagen" in inquiry
    assert 'data-success="Danke. Ihre Angaben sind eingegangen. Rückmeldung in der Regel innerhalb von zwei Arbeitstagen."' in inquiry
    assert 'name="workstations"' in inquiry
    m = re.search(r'<select name="workstations"[^>]*>', inquiry)
    assert m and "required" not in m.group(0)
    legal = read("de/legal/index.html")
    assert "FormSubmit" not in legal
    assert "dauerhaft" not in legal
    assert "INQUIRY_LOG" not in legal
    assert "Viber" not in legal
    assert "/api/inquiry" not in legal
    assert "höchstens zwölf Monate" in legal
    assert 'href="/de/beispiele/"' in legal
    assert "Beispiele" in legal
    assert legal.count("Schaffhauserstrasse 457") == 1
    assert 'id="legal-address"' not in legal
    assert 'id="legal-contact"' not in legal
    en_legal = read("en/legal/index.html")
    assert "FormSubmit" not in en_legal
    assert "Viber" not in en_legal
    assert "/api/inquiry" not in en_legal
    assert "twelve months" in en_legal
    assert 'href="/en/examples/"' in en_legal
    assert "Examples" in en_legal


def test_footer_has_no_viber() -> None:
    for path in (
        "de/index.html",
        "en/index.html",
        "de/legal/index.html",
        "en/legal/index.html",
        "de/anfrage/index.html",
    ):
        text = read(path)
        assert "Viber" not in text
        assert "viber://" not in text
        assert 'data-contact="whatsapp"' in text


def test_inactive_locales_have_no_static_html() -> None:
    for lang in ("fr", "it", "sr", "bs", "hr"):
        assert not (build_site.ROOT / lang).exists(), f"inactive locale tree still present: {lang}"
    redirects = (build_site.ROOT / "_redirects").read_text(encoding="utf-8")
    assert "/fr/ /de/ 302" in redirects
    assert "/it/ /de/ 302" in redirects
    assert "/sr/ /de/ 302" in redirects
    headers = (build_site.ROOT / "_headers").read_text(encoding="utf-8")
    assert "Content-Security-Policy:" in headers
    assert "CDN-Cache-Control: no-store" in headers
    assert "X-Content-Type-Options: nosniff" in headers
    assert "Permissions-Policy:" in headers


def test_single_cta_string() -> None:
    for path in (
        "de/index.html",
        "de/leistungen/index.html",
        "de/anfrage/index.html",
        "en/index.html",
    ):
        text = read(path)
        assert "Pilotbedarf" not in text
        assert "Anliegen unverbindlich schildern" not in text
        assert "Describe a pilot need" not in text
    assert "IT-Anliegen prüfen lassen" in read("de/index.html")
    assert "Have your IT need reviewed" in read("en/index.html")


def test_anfrage_title_h1_footer_and_response_expectation() -> None:
    """Anfrage page: CTA-aligned H1, response sentence, clean footer."""
    de = read("de/anfrage/index.html")
    en = read("en/inquiry/index.html")
    assert "<title>IT-Anliegen prüfen lassen | BIT</title>" in de
    assert "<h1>IT-Anliegen prüfen lassen</h1>" in de
    assert "Pilotbedarf" not in de
    assert "Viber" not in de
    assert "Market Access" not in de
    assert "Market Access (Archiv)" not in de
    assert "Rückmeldung in der Regel innerhalb von zwei Arbeitstagen." in de
    assert 'class="response-expectation"' in de
    assert "<title>Have your IT need reviewed | BIT</title>" in en
    assert "<h1>Have your IT need reviewed</h1>" in en
    assert "Reply usually within two working days." in en
    assert "Viber" not in en
    assert "Market Access" not in en
    assert "Market Access (Archiv)" not in en
    assert (build_site.ROOT / "functions" / "api" / "inquiries.js").is_file()
    assert (build_site.ROOT / "docs" / "INQUIRY_NOTIFY.md").is_file()
    assert (build_site.ROOT / "scripts" / "list_inquiries.ps1").is_file()
    assert (build_site.ROOT / "functions" / "api" / "inquiry-notify-test.js").is_file()


def test_phase2_markers_partner_examples_process_list() -> None:
    """Phase 2+3: no internal markers, partner section, third example, single numbering."""
    visitor_paths = [
        "de/index.html",
        "en/index.html",
        "de/beispiele/index.html",
        "en/examples/index.html",
        "de/faq/index.html",
        "en/faq/index.html",
        "de/leistungen/index.html",
        "en/services/index.html",
        "de/so-funktioniert-es/index.html",
        "en/how-it-works/index.html",
        "de/ueber-bit/index.html",
        "en/about-bit/index.html",
        "de/anfrage/index.html",
        "en/inquiry/index.html",
        "de/legal/index.html",
        "en/legal/index.html",
    ]
    for path in visitor_paths:
        text = read(path)
        assert "Zustand A" not in text
        assert "State A" not in text
        assert "Zustand B" not in text
        assert "MVP" not in text
        assert "Phase 1" not in text
        assert "Phase 2" not in text
        assert "Alles-inklusive" not in text
        assert "all-inclusive" not in text.lower()
        assert "Viber" not in text
        assert "FormSubmit" not in text

    home = read("de/index.html")
    assert "Ein Vertragspartner, ein Ansprechpartner" in home
    assert 'id="vertragspartner"' in home
    assert home.index('id="vertragspartner"') < home.index("<h2>Klar abgegrenzt</h2>")
    assert "bei Spezialthemen wird die technische Umsetzung" not in home
    hero = re.search(r'<section class="hero">.*?</section>', home, re.S).group(0)
    assert "Spezialthemen" not in hero

    en_home = read("en/index.html")
    assert "One contractual partner, one contact person" in en_home
    assert "for specialist topics, technical execution is coordinated" not in en_home.lower()

    about = read("de/ueber-bit/index.html")
    assert "Vertragspartner bleibe ich" in about
    legal = read("de/legal/index.html")
    assert "Vertragspartner bleibe ich" in legal

    examples = read("de/beispiele/index.html")
    assert "So kann ein Auftrag bei BIT ablaufen" in examples
    assert "illustrative Musterfälle" in examples
    assert "Muster: Outlook funktioniert an einem Arbeitsplatz nicht" in examples
    assert "besonders schützenswerte Personendaten" in examples
    assert "Offene Punkte und Risiken" in examples
    assert "Freigegebene Änderungen innerhalb des vereinbarten Leistungsumfangs" in examples
    assert "Freigegebene Konten, Rechte und Lizenzen" in examples
    assert "Zustand A" not in examples
    assert 'class="form-notice"' not in examples

    en_ex = read("en/examples/index.html")
    assert "How an engagement with BIT can run" in en_ex
    assert "Sample: Outlook does not work at a workstation" in en_ex
    assert "specially protected personal data" in en_ex
    assert "Open points and risks" in en_ex

    # Process list: ul + span numbering only (no double ol markers in source)
    for path in (
        "de/index.html",
        "de/beispiele/index.html",
        "de/so-funktioniert-es/index.html",
        "en/index.html",
        "en/examples/index.html",
        "en/how-it-works/index.html",
    ):
        html = read(path)
        assert '<ul class="process-list">' in html
        assert '<ol class="process-list">' not in html
        # text extraction must not yield "1 1" from adjacent duplicate markers
        for m in re.finditer(
            r'<li><span>(\d+)</span><span class="process-text">', html
        ):
            assert m.group(1).isdigit()
        assert not re.search(
            r'<span>(\d+)</span>\s*<span>\1</span>', html
        ), f"double number markers in {path}"

    faq = read("de/faq/index.html")
    assert "Können alle IT-Probleme übernommen werden?" in faq
    assert "klar abgegrenzte Benutzer-, Zugangs- und Arbeitsplatzaufgaben" in faq
    assert "Durch das Absenden entsteht noch kein Auftrag" in read("de/index.html")

    users = read("de/leistungen/benutzer-und-zugaenge/index.html")
    words = re.findall(r"[A-Za-zÄÖÜäöü]{2,}", users)
    assert len(words) >= 280
    assert 'area=users-access' in users
    assert "ProfessionalService" in users

    assert (build_site.ROOT / "docs" / "PHASE2_PLAN.md").is_file()
    assert (build_site.ROOT / "functions" / "api" / "inquiry-notify-test.js").is_file()
    notify = (build_site.ROOT / "docs" / "INQUIRY_NOTIFY.md").read_text(encoding="utf-8")
    assert "/api/inquiry-notify-test" in notify
    assert "TELEGRAM_BOT_TOKEN" in notify

