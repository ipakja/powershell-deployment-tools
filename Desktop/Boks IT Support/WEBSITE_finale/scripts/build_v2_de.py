"""Build Zustand-A site for active languages (DE + EN)."""
from __future__ import annotations

import html
import json
from pathlib import Path
from string import Template
from typing import Any
from urllib.parse import quote
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
SITE_CONFIG = ROOT / "config" / "site.json"
BASE_TEMPLATE = ROOT / "templates" / "v2" / "base.html"
V2_FILES = {"de": ROOT / "config" / "de_v2.json", "en": ROOT / "config" / "en_v2.json"}

# Shared page keys → per-language path (for hreflang + language switch)
PAGE_PATHS: dict[str, dict[str, str]] = {
    "home": {"de": "/de/", "en": "/en/"},
    "services": {"de": "/de/leistungen/", "en": "/en/services/"},
    "examples": {"de": "/de/beispiele/", "en": "/en/examples/"},
    "process": {"de": "/de/so-funktioniert-es/", "en": "/en/how-it-works/"},
    "audience": {"de": "/de/fuer-unternehmen/", "en": "/en/for-businesses/"},
    "about": {"de": "/de/ueber-bit/", "en": "/en/about-bit/"},
    "faq": {"de": "/de/faq/", "en": "/en/faq/"},
    "inquiry": {"de": "/de/anfrage/", "en": "/en/inquiry/"},
    "market-access": {"de": "/de/market-access/", "en": "/en/market-access/"},
    "legal": {"de": "/de/legal/", "en": "/en/legal/"},
    "svc-users-access": {
        "de": "/de/leistungen/benutzer-und-zugaenge/",
        "en": "/en/services/users-and-access/",
    },
    "svc-m365-workplace": {
        "de": "/de/leistungen/microsoft-365-arbeitsplatz/",
        "en": "/en/services/microsoft-365-workplace/",
    },
    "svc-basischeck": {
        "de": "/de/leistungen/it-basischeck/",
        "en": "/en/services/it-basics-check/",
    },
}

SERVICE_PAIR = {
    "benutzer-und-zugaenge": "svc-users-access",
    "users-and-access": "svc-users-access",
    "microsoft-365-arbeitsplatz": "svc-m365-workplace",
    "microsoft-365-workplace": "svc-m365-workplace",
    "it-basischeck": "svc-basischeck",
    "it-basics-check": "svc-basischeck",
}

SERVICE_ICONS = {
    "users": (
        '<svg class="service-icon-svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<path fill="currentColor" d="M12 12a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm0 2c-4.42 0-8 2.24-8 5v1h16v-1c0-2.76-3.58-5-8-5Z"/>'
        "</svg>"
    ),
    "m365": (
        '<svg class="service-icon-svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<path fill="currentColor" d="M4 5.5 11 4v16l-7-1.5V5.5Zm8-.7 8 1.2v12.4l-8 1.2V4.8Z"/>'
        "</svg>"
    ),
    "security": (
        '<svg class="service-icon-svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<path fill="currentColor" d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5l-8-3Zm0 4a3 3 0 0 1 3 3v1h1v7H8v-7h1V9a3 3 0 0 1 3-3Zm0 2a1 1 0 0 0-1 1v1h2V9a1 1 0 0 0-1-1Z"/>'
        "</svg>"
    ),
    "contact": (
        '<svg class="service-icon-svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<path fill="currentColor" d="M12 3a7 7 0 0 0-7 7v2.2L3 15v2h18v-2l-2-2.8V10a7 7 0 0 0-7-7Zm-2 16h4a2 2 0 0 1-4 0Z"/>'
        "</svg>"
    ),
}


def escape(value: object) -> str:
    """Escape text for HTML body/attributes."""
    return html.escape(str(value), quote=True)


def protected_email_anchor(email: str, *, visible_label: str = "E-Mail") -> str:
    """mailto href keeps the real address; visible text is filled by contact-links.js."""
    user, _, domain = str(email).partition("@")
    return (
        f'<a href="mailto:{escape(email)}" data-contact="email">'
        f'<span data-email-user="{escape(user)}" data-email-domain="{escape(domain)}">'
        f"{escape(visible_label)}</span></a>"
    )


def direct_message_urls(v2: dict[str, Any], contact: dict[str, str]) -> tuple[str, str]:
    """Build WhatsApp and mailto URLs with the pre-filled inquiry template."""
    direct = v2["direct_path"]
    subject = str(direct["subject"])
    body = "\n".join(str(line) for line in direct["body_lines"])
    message = f"{subject}\n\n{body}"
    wa_base = str(contact["whatsapp_url"]).rstrip("/")
    wa_url = f"{wa_base}?text={quote(message, safe='')}"
    mailto_url = (
        f"mailto:{contact['email']}"
        f"?subject={quote(subject, safe='')}"
        f"&body={quote(body, safe='')}"
    )
    return wa_url, mailto_url


def footer_channels_html(site: dict[str, Any], language: str) -> str:
    """Phone, harvest-protected email, WhatsApp — no Viber."""
    contact = site["contact"]
    email_label = "Email" if language == "en" else "E-Mail"
    return (
        f"                    {protected_email_anchor(contact['email'], visible_label=email_label)}\n"
        f'                    <a href="{escape(contact["phone_href"])}">'
        f'{escape(contact["phone_display"])}</a>\n'
        f'                    <a data-contact="whatsapp" href="{escape(contact["whatsapp_url"])}">'
        f"WhatsApp</a>\n"
    )


def json_ld_script(payload: dict[str, Any]) -> str:
    """Embed a JSON-LD script tag (escaped for HTML safety)."""
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    safe = raw.replace("<", "\\u003c")
    return f'    <script type="application/ld+json">{safe}</script>\n'


def professional_service_json_ld(site: dict[str, Any]) -> str:
    """ProfessionalService schema for home (no fake hours/ratings)."""
    contact = site["contact"]
    address = site["address"]
    payload = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "BIT – Boks IT Support",
        "url": site["base_url"] + "/",
        "email": contact["email"],
        "telephone": contact["phone_display"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": address["street"],
            "postalCode": address["postal_code"],
            "addressLocality": address["city"],
            "addressCountry": address["country_code"],
        },
        "areaServed": {"@type": "City", "name": "Zürich"},
        "serviceType": [
            "User and access administration",
            "Microsoft 365 and workplace support",
            "IT basics check",
        ],
    }
    return json_ld_script(payload)


def faq_page_json_ld(v2: dict[str, Any], site: dict[str, Any], path: str) -> str:
    """FAQPage schema from existing FAQ items."""
    entities = [
        {
            "@type": "Question",
            "name": item["q"],
            "acceptedAnswer": {"@type": "Answer", "text": item["a"]},
        }
        for item in v2["faq"]["items"]
    ]
    payload = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities,
        "url": site["base_url"] + path,
    }
    return json_ld_script(payload)


def load_site() -> dict[str, Any]:
    """Load site config."""
    return json.loads(SITE_CONFIG.read_text(encoding="utf-8"))


def load_v2(language: str) -> dict[str, Any]:
    """Load Zustand-A content for one language."""
    return json.loads(V2_FILES[language].read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    """Write UTF-8 HTML without Windows newlines."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def active_languages(site: dict[str, Any]) -> list[str]:
    """Return active public languages (default DE+EN)."""
    return list(site.get("active_languages") or ["de", "en"])


def hreflang_for(code: str) -> str:
    """Map language code to hreflang value."""
    return {"de": "de-CH", "en": "en"}.get(code, code)


def alternate_links(page_key: str, site: dict[str, Any]) -> str:
    """Render DE/EN alternate links for one logical page."""
    paths = PAGE_PATHS[page_key]
    langs = active_languages(site)
    lines = []
    for code in langs:
        href = f'{site["base_url"]}{paths[code]}'
        lines.append(
            f'    <link rel="alternate" hreflang="{hreflang_for(code)}" href="{escape(href)}">'
        )
    default = paths.get("de") or paths[langs[0]]
    lines.append(
        f'    <link rel="alternate" hreflang="x-default" '
        f'href="{escape(site["base_url"] + default)}">'
    )
    return "\n".join(lines)


def language_switcher(page_key: str, current: str, site: dict[str, Any]) -> str:
    """Language menu that stays on the equivalent page."""
    paths = PAGE_PATHS[page_key]
    links = []
    for code in active_languages(site):
        current_attr = ' aria-current="page"' if code == current else ""
        links.append(
            f'                <a href="{escape(paths[code])}"{current_attr}>'
            f"{code.upper()}</a>"
        )
    return "\n".join(links)


def nav_html(v2: dict[str, Any], current_path: str) -> str:
    """Render main navigation with current page marker."""
    links = []
    for item in v2["nav"]:
        current_attr = ' aria-current="page"' if item["href"] == current_path else ""
        links.append(
            f'                <a href="{escape(item["href"])}"{current_attr}>'
            f'{escape(item["label"])}</a>'
        )
    return "\n".join(links)


def section(title: str, body: str, *, intro: str = "", section_id: str = "") -> str:
    """Wrap a content block in the standard section shell."""
    id_attr = f' id="{escape(section_id)}"' if section_id else ""
    intro_html = f'<p class="section-intro">{escape(intro)}</p>' if intro else ""
    return (
        f'        <section class="section"{id_attr}>\n'
        f'            <div class="container">\n'
        f"                <h2>{escape(title)}</h2>\n"
        f"{intro_html}"
        f"{body}"
        f"            </div>\n"
        f"        </section>\n"
    )


def process_list_html(steps: list[Any]) -> str:
    """Numbered process steps with a single source of truth (span, not ol markers)."""
    items = "\n".join(
        f"                    <li><span>{i}</span><span class=\"process-text\">{escape(step)}</span></li>"
        for i, step in enumerate(steps, start=1)
    )
    return f'                <ul class="process-list">\n{items}\n                </ul>\n'


def ul(items: list[Any], class_name: str = "plain-list") -> str:
    """Render a plain unordered list (strings or {text, href} objects)."""
    lis = []
    for item in items:
        if isinstance(item, dict):
            text = escape(item["text"])
            href = item.get("href")
            if href:
                lis.append(
                    f'                    <li><a href="{escape(href)}">{text}</a></li>'
                )
            else:
                lis.append(f"                    <li>{text}</li>")
        else:
            lis.append(f"                    <li>{escape(item)}</li>")
    return (
        f'                <ul class="{class_name}">\n'
        + "\n".join(lis)
        + "\n                </ul>\n"
    )


def cards(
    items: list[dict[str, str]],
    *,
    link_prefix: str | None = None,
) -> str:
    """Render service or concern cards."""
    blocks = ['                <div class="card-grid">']
    for item in items:
        title = escape(item["title"])
        text = escape(item.get("text", ""))
        if link_prefix and item.get("slug"):
            href = f"{link_prefix}{item['slug']}/"
            blocks.append(
                f'                    <a class="info-card info-card-link" href="{escape(href)}">'
                f"<h3>{title}</h3><p>{text}</p></a>"
            )
        else:
            blocks.append(
                f'                    <article class="info-card"><h3>{title}</h3>'
                f"<p>{text}</p></article>"
            )
    blocks.append("                </div>\n")
    return "\n".join(blocks) + "\n"


def service_cards(v2: dict[str, Any]) -> str:
    """Render service cards with benefit line, icon and secondary CTA."""
    ui = v2["ui"]
    path_prefix = v2["services"]["path"]
    view_label = escape(ui["view_service"])
    blocks = ['                <div class="card-grid service-card-grid">']
    for item in v2["services"]["cards"]:
        href = f"{path_prefix}{item['slug']}/"
        icon = SERVICE_ICONS.get(item.get("icon", ""), SERVICE_ICONS["users"])
        benefit = item.get("benefit") or ""
        benefit_html = (
            f'                        <p class="service-benefit">{escape(benefit)}</p>\n'
            if benefit
            else ""
        )
        price = item.get("price_label") or ""
        price_html = (
            f'                        <p class="services-price-hint">{escape(price)}</p>\n'
            if price
            else ""
        )
        blocks.append(
            '                    <article class="info-card service-card">\n'
            f'                        <span class="service-icon" data-icon="{escape(item.get("icon", ""))}">'
            f"{icon}</span>\n"
            f"                        <h3>{escape(item['title'])}</h3>\n"
            f"{benefit_html}"
            f"                        <p>{escape(item['text'])}</p>\n"
            f"{price_html}"
            f'                        <a class="service-card-cta" href="{escape(href)}">{view_label}</a>\n'
            "                    </article>"
        )
    blocks.append("                </div>\n")
    return "\n".join(blocks) + "\n"

def services_section_body(v2: dict[str, Any], *, include_price_panel: bool = False) -> str:
    """Shared services body: cards, scope note, vendor note, guideline price, CTA."""
    ui = v2["ui"]
    services = v2["services"]
    parts = [
        service_cards(v2),
        f'                <p class="services-scope-note">{escape(services["scope_note"])}</p>\n',
    ]
    vendor_note = services.get("vendor_note") or ""
    if vendor_note:
        parts.append(
            f'                <p class="services-vendor-note">{escape(vendor_note)}</p>\n'
        )
    parts.append(
        f'                <p class="services-price-hint">{escape(ui["from_small_job"])}</p>\n'
    )
    if include_price_panel:
        prices = v2["prices"]
        parts.append(
            '                <div class="price-panel">\n'
            f'                    <p class="eyebrow">{escape(ui["guidelines_title"])}</p>\n'
            f"                    <p>{escape(v2['price_note'])}</p>\n"
            '                    <ul class="plain-list">\n'
            f"                        <li>{escape(ui['hourly_line'].format(**prices))}</li>\n"
            f"                        <li>{escape(ui['small_job_line'].format(**prices))}</li>\n"
            f"                        <li>{escape(ui['travel_line'].format(**prices))}</li>\n"
            "                    </ul>\n"
            "                </div>\n"
        )
    parts.append(
        '                <div class="hero-actions services-section-actions">\n'
        f'                    <a class="button button-primary" href="{escape(v2["cta_primary_href"])}">'
        f'{escape(v2["cta_primary"])}</a>\n'
        "                </div>\n"
    )
    return "".join(parts)

def cta_block(
    v2: dict[str, Any],
    *,
    include_whatsapp: bool = False,
    site: dict[str, Any] | None = None,
) -> str:
    """Closing CTA: primary form link; optional WhatsApp secondary (home)."""
    closing = v2["closing"]
    response = closing.get("response_expectation") or ""
    response_html = (
        f'                <p class="response-expectation">{escape(response)}</p>\n'
        if response
        else ""
    )
    whatsapp_html = ""
    if include_whatsapp:
        contact = (site or load_site())["contact"]
        wa_url, _ = direct_message_urls(v2, contact)
        label = closing.get("whatsapp_label") or v2.get("direct_path", {}).get(
            "whatsapp_label", "WhatsApp"
        )
        whatsapp_html = (
            f'                    <a class="button button-whatsapp" data-contact="whatsapp" '
            f'href="{escape(wa_url)}">{escape(label)}</a>\n'
        )
    return section(
        closing["title"],
        (
            f'                <p class="section-intro">{escape(closing["text"])}</p>\n'
            f'                <p class="muted">{escape(closing["note"])}</p>\n'
            f"{response_html}"
            f'                <div class="hero-actions">\n'
            f'                    <a class="button button-primary" href="{escape(v2["cta_primary_href"])}">'
            f'{escape(v2["cta_primary"])}</a>\n'
            f"{whatsapp_html}"
            f"                </div>\n"
        ),
        section_id="cta",
    )

def render_page(
    *,
    v2: dict[str, Any],
    site: dict[str, Any],
    path: str,
    page_key: str,
    meta_title: str,
    meta_description: str,
    main: str,
    page_id: str,
    extra_head: str = "",
    extra_scripts: str = "",
) -> str:
    """Fill the shared v2 base template."""
    language = v2["language"]
    canonical = f'{site["base_url"]}{path}'
    footer_note = (
        v2["footer_channels_note"]
        if v2.get("inquiry", {}).get("live", False)
        else v2.get("footer_channels_note_offline", v2["footer_channels_note"])
    )
    return Template(BASE_TEMPLATE.read_text(encoding="utf-8")).substitute(
        html_lang=escape(v2["html_lang"]),
        og_locale=escape(v2["og_locale"]),
        language=escape(language),
        meta_title=escape(meta_title),
        meta_description=escape(meta_description),
        canonical=escape(canonical),
        alternate_links=alternate_links(page_key, site),
        page_id=escape(page_id),
        skip=escape(v2["skip"]),
        nav_aria=escape(v2["nav_aria"]),
        menu_label=escape(v2["menu_label"]),
        languages_label=escape(v2["languages_label"]),
        nav_links=nav_html(v2, path),
        language_links=language_switcher(page_key, language, site),
        main=main,
        footer_note=escape(footer_note),
        footer_channels=footer_channels_html(site, language),
        inquiry_href=escape(v2["cta_primary_href"]),
        inquiry_label=escape(v2["inquiry_label"]),
        legal_label=escape(v2["legal_label"]),
        extra_head=extra_head,
        extra_scripts=extra_scripts,
    )


def home_main(v2: dict[str, Any]) -> str:
    """Homepage sections for the live DE/EN IT site."""
    home = v2["home"]
    trust_block = home.get("trust_block") or {}
    trust_html = ""
    if trust_block.get("title") and trust_block.get("text"):
        trust_html = section(
            trust_block["title"],
            f'                <p>{escape(trust_block["text"])}</p>\n',
        )
    subline = home.get("cta_subline") or ""
    subline_html = (
        f'                <p class="hero-subline">{escape(subline)}</p>\n' if subline else ""
    )
    outcome = home.get("outcome") or ""
    outcome_html = (
        f'                <p class="hero-outcome">{escape(outcome)}</p>\n' if outcome else ""
    )
    teaser = home.get("examples_teaser") or {}
    teaser_html = ""
    if teaser.get("title"):
        teaser_html = section(
            teaser["title"],
            (
                f'                <p>{escape(teaser.get("text", ""))}</p>\n'
                f'                <div class="hero-actions">\n'
                f'                    <a class="button button-secondary" href="{escape(teaser.get("href", "#"))}">'
                f'{escape(teaser.get("cta", ""))}</a>\n'
                "                </div>\n"
            ),
        )
    partner = home.get("partner") or {}
    partner_html = ""
    if partner.get("title") and partner.get("text"):
        partner_html = section(
            partner["title"],
            f'                <p>{escape(partner["text"])}</p>\n',
            section_id="vertragspartner",
        )
    return "".join(
        [
            (
                '        <section class="hero">\n'
                '            <div class="container">\n'
                f'                <p class="eyebrow">{escape(home["eyebrow"])}</p>\n'
                f"                <h1>{escape(home['h1'])}</h1>\n"
                f'                <p class="hero-lead">{escape(home["lead"])}</p>\n'
                f'                <p class="trust-line">{escape(home["trust"])}</p>\n'
                f"{outcome_html}"
                '                <div class="hero-actions">\n'
                f'                    <a class="button button-primary" href="{escape(v2["cta_primary_href"])}">'
                f'{escape(v2["cta_primary"])}</a>\n'
                f'                    <a class="button button-secondary" href="{escape(v2["cta_secondary_href"])}">'
                f'{escape(v2["cta_secondary"])}</a>\n'
                "                </div>\n"
                f"{subline_html}"
                f'                <p class="pilot-banner">{escape(home["pilot_banner"])}</p>\n'
                "            </div>\n"
                "        </section>\n"
            ),
            section(v2["concerns"]["title"], ul(v2["concerns"]["items"])),
            section(v2["problem"]["title"], cards(v2["problem"]["items"])),
            section(
                v2["services"]["title"],
                services_section_body(v2),
                intro=v2["services"]["intro"],
            ),
            partner_html,
            section(
                v2["limits"]["title"],
                ul(v2["limits"]["items"]),
                intro=v2["limits"]["lead"],
            ),
            section(
                v2["process"]["title"],
                process_list_html(v2["process"]["steps"]),
            ),
            teaser_html,
            trust_html,
            cta_block(v2, include_whatsapp=True),
        ]
    )

def leistungen_main(v2: dict[str, Any]) -> str:
    """Services overview."""
    ui = v2["ui"]
    areas_label = ui.get("three_areas") or ui.get("four_areas") or ""
    return (
        '        <section class="hero"><div class="container">\n'
        f'            <p class="eyebrow">{escape(ui["services_eyebrow"])}</p>\n'
        f"            <h1>{escape(v2['services']['title'])}</h1>\n"
        f'            <p class="hero-lead">{escape(v2["services"]["intro"])}</p>\n'
        "        </div></section>\n"
        + section(
            areas_label,
            services_section_body(v2, include_price_panel=True),
        )
        + section(
            v2["limits"]["title"],
            ul(v2["limits"]["items"]),
            intro=v2["limits"]["lead"],
        )
        + cta_block(v2)
    )

def leistung_detail_main(v2: dict[str, Any], card: dict[str, str]) -> str:
    """Single service detail page with outcomes, steps, boundaries and CTA."""
    ui = v2["ui"]
    detail = card.get("detail") or {}
    area = card.get("area") or ""
    cta_href = v2["cta_primary_href"]
    if area:
        sep = "&" if "?" in cta_href else "?"
        cta_href = f"{cta_href}{sep}area={area}"
    parts = [
        '        <section class="hero"><div class="container">\n'
        f'            <p class="eyebrow"><a href="{escape(v2["services"]["path"])}">'
        f'{escape(ui["back_to_services"])}</a></p>\n'
        f"            <h1>{escape(card['title'])}</h1>\n"
    ]
    if card.get("benefit"):
        parts.append(f'            <p class="service-benefit">{escape(card["benefit"])}</p>\n')
    parts.append(f'            <p class="hero-lead">{escape(card["text"])}</p>\n')
    if card.get("price_label"):
        parts.append(
            f'            <p class="services-price-hint">{escape(card["price_label"])}</p>\n'
        )
    parts.append(
        '            <div class="hero-actions">\n'
        f'                <a class="button button-primary" href="{escape(cta_href)}">'
        f'{escape(v2["cta_primary"])}</a>\n'
        "            </div>\n"
        "        </div></section>\n"
    )
    if detail.get("intro"):
        parts.append(
            section(
                card.get("benefit") or card["title"],
                f'                <p>{escape(detail["intro"])}</p>\n',
            )
        )
    if detail.get("situations"):
        parts.append(
            section(ui.get("situations_title", "Situations"), ul(detail["situations"]))
        )
    if detail.get("steps"):
        parts.append(
            section(ui.get("steps_title", "Steps"), process_list_html(detail["steps"]))
        )
    if detail.get("required_info"):
        parts.append(
            section(
                ui.get("required_info_title", "Required info"),
                ul(detail["required_info"]),
            )
        )
    if detail.get("boundaries"):
        parts.append(
            section(
                ui.get("boundaries_title", "Boundaries"),
                f'                <p>{escape(detail["boundaries"])}</p>\n',
            )
        )
    if detail.get("closing"):
        parts.append(
            f'        <section class="section"><div class="container">\n'
            f'                <p>{escape(detail["closing"])}</p>\n'
            f'                <div class="hero-actions">\n'
            f'                    <a class="button button-primary" href="{escape(cta_href)}">'
            f'{escape(v2["cta_primary"])}</a>\n'
            f"                </div>\n"
            f"        </div></section>\n"
        )
    # Internal links to examples, FAQ, process, other services
    other = [
        c
        for c in v2["services"]["cards"]
        if c.get("slug") and c["slug"] != card.get("slug")
    ]
    link_items = []
    for c in other:
        link_items.append(
            {
                "text": c["title"],
                "href": f"{v2['services']['path']}{c['slug']}/",
            }
        )
    link_items.append(
        {
            "text": v2.get("examples_page", {}).get("title", "Examples"),
            "href": PAGE_PATHS["examples"][v2["language"]],
        }
    )
    link_items.append(
        {
            "text": v2["process"]["title"],
            "href": PAGE_PATHS["process"][v2["language"]],
        }
    )
    link_items.append({"text": "FAQ", "href": PAGE_PATHS["faq"][v2["language"]]})
    parts.append(section(ui.get("view_service", "Related"), ul(link_items)))
    parts.append(cta_block(v2))
    return "".join(parts)

def examples_main(v2: dict[str, Any]) -> str:
    """Musterfälle / sample cases page (labelled samples only)."""
    page = v2["examples_page"]
    ui = v2["ui"]
    note = (page.get("note") or "").strip()
    note_html = (
        f'            <p class="form-notice">{escape(note)}</p>\n' if note else ""
    )
    blocks = [
        '        <section class="hero"><div class="container">\n'
        f'            <p class="eyebrow">{escape(ui.get("examples_eyebrow", ""))}</p>\n'
        f"            <h1>{escape(page['title'])}</h1>\n"
        f'            <p class="hero-lead">{escape(page["lead"])}</p>\n'
        f"{note_html}"
        "        </div></section>\n"
    ]
    for case in page["cases"]:
        if v2["language"] == "en":
            labels = {
                "situation": "Starting point",
                "required": "Required details",
                "steps": "Process",
                "approvals": "Required approvals",
                "result": "Outcome",
            }
        else:
            labels = {
                "situation": "Ausgangslage",
                "required": "Benötigte Angaben",
                "steps": "Ablauf",
                "approvals": "Freigaben",
                "result": "Ergebnis",
            }
        body = (
            f'                <h3>{escape(labels["situation"])}</h3>\n'
            f'                <p>{escape(case["situation"])}</p>\n'
            f'                <h3>{escape(labels["required"])}</h3>\n'
            + ul(case["required"])
            + f'                <h3>{escape(labels["steps"])}</h3>\n'
            + process_list_html(case["steps"])
            + f'                <h3>{escape(labels["approvals"])}</h3>\n'
            + f'                <p>{escape(case["approvals"])}</p>\n'
            + f'                <h3>{escape(labels["result"])}</h3>\n'
            + f'                <p>{escape(case["result"])}</p>\n'
        )
        blocks.append(section(case["title"], body))
    report = page["report"]
    report_body = f'                <p class="section-intro">{escape(report["intro"])}</p>\n'
    for sec in report["sections"]:
        report_body += (
            f"                <h3>{escape(sec['title'])}</h3>\n"
            f"                <p>{escape(sec['text'])}</p>\n"
        )
    blocks.append(
        section(
            report["title"],
            report_body,
            section_id="report",
        )
    )
    blocks.append(cta_block(v2))
    return "".join(blocks)

def process_main(v2: dict[str, Any]) -> str:
    """Process page."""
    ui = v2["ui"]
    steps = v2["process"]["steps"]
    return (
        '        <section class="hero"><div class="container">\n'
        f'            <p class="eyebrow">{escape(ui["process_eyebrow"])}</p>\n'
        f"            <h1>{escape(v2['process']['title'])}</h1>\n"
        f'            <p class="hero-lead">{escape(ui["process_lead"])}</p>\n'
        "        </div></section>\n"
        + section(
            ui["five_steps"],
            process_list_html(steps),
        )
        + cta_block(v2)
    )


def audience_main(v2: dict[str, Any]) -> str:
    """Audience page: what → for whom → when it fits → boundaries."""
    a = v2["audience"]
    ui = v2["ui"]
    nofit_body = ul(a["nofit"])
    note = a.get("nofit_note") or ""
    if note:
        nofit_body += f'                <p class="muted audience-nofit-note">{escape(note)}</p>\n'
    return (
        '        <section class="hero"><div class="container">\n'
        f'            <p class="eyebrow">{escape(ui["audience_eyebrow"])}</p>\n'
        f"            <h1>{escape(a['title'])}</h1>\n"
        f'            <p class="hero-lead">{escape(a["lead"])}</p>\n'
        "        </div></section>\n"
        + section(a["services_title"], ul(a["services"]))
        + section(a["fit_title"], ul(a["fit"]))
        + section(a["nofit_title"], nofit_body)
        + section(
            v2["role"]["title"],
            (
                f'                <p>{escape(v2["role"]["owns"])}</p>\n'
                f'                <p>{escape(v2["role"]["tech"])}</p>\n'
                f'                <p>{escape(v2["role"]["contract"])}</p>\n'
            ),
        )
        + section(
            v2["examples"]["title"],
            cards(v2["examples"]["items"]),
            intro=v2["examples"]["note"],
        )
        + cta_block(v2)
    )


def about_main(v2: dict[str, Any]) -> str:
    """About BIT page with published SIZ credentials when provided."""
    about = v2["about"]
    paragraphs = "\n".join(f"                <p>{escape(p)}</p>" for p in about["body"])
    credentials = about.get("credentials") or []
    cred_html = ""
    if credentials:
        items = "\n".join(
            f"                    <li>{escape(item)}</li>" for item in credentials
        )
        cred_html = (
            '                <ul class="plain-list about-credentials">\n'
            f"{items}\n"
            "                </ul>\n"
        )
    return (
        '        <section class="section"><div class="container about-layout">\n'
        '            <img class="about-photo" src="/ICH.png" alt="Stefan Bogdanovic" width="430">\n'
        '            <div class="about-copy">\n'
        f'                <p class="eyebrow">{escape(about["title"])}</p>\n'
        f"                <h1>{escape(about['lead'])}</h1>\n"
        f"{paragraphs}\n"
        f"{cred_html}"
        f'                <p class="pilot-banner">{escape(about["pilot"])}</p>\n'
        f'                <a class="button button-primary" href="{escape(v2["cta_primary_href"])}">'
        f'{escape(v2["cta_primary"])}</a>\n'
        "            </div>\n"
        "        </div></section>\n"
    )


def faq_main(v2: dict[str, Any]) -> str:
    """FAQ list."""
    ui = v2["ui"]
    items = []
    for entry in v2["faq"]["items"]:
        items.append(
            "                <details class=\"faq-item\">\n"
            f"                    <summary>{escape(entry['q'])}</summary>\n"
            f"                    <p>{escape(entry['a'])}</p>\n"
            "                </details>"
        )
    return (
        '        <section class="hero"><div class="container">\n'
        f'            <p class="eyebrow">{escape(ui["faq_eyebrow"])}</p>\n'
        f"            <h1>{escape(v2['faq']['title'])}</h1>\n"
        "        </div></section>\n"
        + section(ui["answers"], "\n".join(items) + "\n")
        + cta_block(v2)
    )


def inquiry_main(v2: dict[str, Any], site: dict[str, Any] | None = None) -> str:
    """Inquiry page: WhatsApp/mailto direct path above the existing form."""
    site = site or load_site()
    contact = site["contact"]
    iq = v2["inquiry"]
    f = v2["form"]
    lang = v2["language"]
    direct = v2["direct_path"]
    wa_url, _ = direct_message_urls(v2, contact)
    email_label = "Email" if lang == "en" else "E-Mail"
    email_user, _, email_domain = str(contact["email"]).partition("@")
    subject_enc = quote(str(direct["subject"]), safe="")
    body_enc = quote("\n".join(str(line) for line in direct["body_lines"]), safe="")
    offline = ""
    form_disabled = ""
    submit_disabled = ""
    if not iq.get("live", False):
        offline = (
            f'            <p class="pilot-banner" role="status">{escape(iq["offline_banner"])} '
            f"{protected_email_anchor(contact['email'], visible_label=email_label)}</p>\n"
        )
        form_disabled = ' aria-disabled="true" data-inquiry-offline="true"'
        submit_disabled = ' disabled="disabled" aria-disabled="true"'
    response = iq.get("response_expectation") or ""
    response_html = (
        f'            <p class="response-expectation">{escape(response)}</p>\n'
        if response
        else ""
    )
    optional_heading = f.get("optional_heading") or (
        "Additional details (optional)" if lang == "en" else "Weitere Angaben (optional)"
    )
    contact_line = (
        f'                <p class="inquiry-direct-contact">'
        f'<a href="{escape(contact["phone_href"])}">{escape(contact["phone_display"])}</a>'
        f" · {protected_email_anchor(contact['email'], visible_label=email_label)}"
        f' · <a data-contact="whatsapp" href="{escape(contact["whatsapp_url"])}">WhatsApp</a>'
        f"</p>\n"
    )
    return (
        '        <section class="hero"><div class="container">\n'
        f'            <p class="eyebrow">{escape(v2["ui"]["inquiry_eyebrow"])}</p>\n'
        f"            <h1>{escape(iq['title'])}</h1>\n"
        f'            <p class="hero-lead">{escape(iq["lead"])}</p>\n'
        f"{offline}"
        f'            <p class="form-notice">{escape(iq["notice"])}</p>\n'
        f"{response_html}"
        f'            <p class="form-security">{escape(iq["security"])}</p>\n'
        "        </div></section>\n"
        '        <section class="section"><div class="container">\n'
        '            <div class="inquiry-direct">\n'
        f'                <p class="inquiry-direct-intro">{escape(direct["intro"])}</p>\n'
        '                <div class="hero-actions">\n'
        f'                    <a class="button button-whatsapp" data-contact="whatsapp" '
        f'href="{escape(wa_url)}">{escape(direct["whatsapp_label"])}</a>\n'
        f'                    <a class="button button-secondary" href="#" role="button" '
        f"data-direct-mailto "
        f'data-email-user="{escape(email_user)}" '
        f'data-email-domain="{escape(email_domain)}" '
        f'data-mailto-subject-enc="{escape(subject_enc)}" '
        f'data-mailto-body-enc="{escape(body_enc)}">'
        f'{escape(direct["email_label"])}</a>\n'
        "                </div>\n"
        f"{contact_line}"
        "            </div>\n"
        f'            <h2 class="inquiry-form-alt-heading">{escape(direct["form_heading"])}</h2>\n'
        f'            <form class="inquiry-form" id="inquiry-form" novalidate{form_disabled} '
        f'data-success="{escape(iq["success"])}" data-error="{escape(iq["error"])}">\n'
        f'                <input type="hidden" name="language" value="{escape(lang)}">\n'
        '                <div class="form-grid">\n'
        f'                    <label>{escape(f["company"])}<input name="company" required maxlength="200" autocomplete="organization"></label>\n'
        f'                    <label>{escape(f["first_name"])}<input name="first_name" required maxlength="100" autocomplete="given-name"></label>\n'
        f'                    <label>{escape(f["last_name"])}<input name="last_name" required maxlength="100" autocomplete="family-name"></label>\n'
        f'                    <label>{escape(f["email"])}<input name="email" type="email" required maxlength="200" autocomplete="email"></label>\n'
        f'                    <label>{escape(f["employees"])}\n'
        '                        <select name="employees" required>\n'
        f'                            <option value="">{escape(f["choose"])}</option>\n'
        '                            <option>1–4</option><option>5–10</option><option>11–25</option>\n'
        '                            <option>26–50</option><option>51+</option>\n'
        "                        </select>\n"
        "                    </label>\n"
        f'                    <label>{escape(f["area"])}\n'
        '                        <select name="area" required>\n'
        f'                            <option value="">{escape(f["choose"])}</option>\n'
        f'                            <option value="users-access">{escape(f["onboarding"])}</option>\n'
        f'                            <option value="m365-workplace">{escape(f["offboarding"])}</option>\n'
        f'                            <option value="basischeck">{escape(f["workplace"])}</option>\n'
        f'                            <option value="several">{escape(f["several"])}</option>\n'
        f'                            <option value="unclear">{escape(f["still_unclear"])}</option>\n'
        "                        </select>\n"
        "                    </label>\n"
        "                </div>\n"
        f'                <label class="form-full">{escape(f["description"])}\n'
        f'                    <textarea name="description" required maxlength="4000" rows="6" '
        f'placeholder="{escape(f["desc_placeholder"])}"></textarea>\n'
        "                </label>\n"
        f'                <p class="form-optional-heading">{escape(optional_heading)}</p>\n'
        '                <div class="form-grid">\n'
        f'                    <label>{escape(f["phone"])}<input name="phone" type="tel" maxlength="40" autocomplete="tel"></label>\n'
        f'                    <label>{escape(f["location"])}<input name="location" maxlength="120"></label>\n'
        f'                    <label>{escape(f["industry"])}<input name="industry" maxlength="120"></label>\n'
        f'                    <label>{escape(f["workstations"])}\n'
        '                        <select name="workstations">\n'
        f'                            <option value="">{escape(f["choose"])}</option>\n'
        '                            <option>1–5</option><option>6–15</option><option>16–40</option>\n'
        '                            <option>41+</option>\n'
        "                        </select>\n"
        "                    </label>\n"
        f'                    <label>{escape(f["m365"])}\n'
        '                        <select name="m365">\n'
        f'                            <option value="">{escape(f["choose"])}</option>\n'
        f'                            <option>{escape(f["yes"])}</option>'
        f'<option>{escape(f["no"])}</option><option>{escape(f["unclear"])}</option>\n'
        "                        </select>\n"
        "                    </label>\n"
        f'                    <label>{escape(f["internal_it"])}\n'
        '                        <select name="internal_it">\n'
        f'                            <option value="">{escape(f["choose"])}</option>\n'
        f'                            <option>{escape(f["yes"])}</option>'
        f'<option>{escape(f["no"])}</option><option>{escape(f["partial"])}</option>\n'
        "                        </select>\n"
        "                    </label>\n"
        f'                    <label>{escape(f["external_it"])}\n'
        '                        <select name="external_it">\n'
        f'                            <option value="">{escape(f["choose"])}</option>\n'
        f'                            <option>{escape(f["yes"])}</option>'
        f'<option>{escape(f["no"])}</option>\n'
        "                        </select>\n"
        "                    </label>\n"
        f'                    <label>{escape(f["start"])}\n'
        '                        <select name="start">\n'
        f'                            <option value="">{escape(f["choose"])}</option>\n'
        f'                            <option>{escape(f["immediate"])}</option>'
        f'<option>{escape(f["within_2_weeks"])}</option>\n'
        f'                            <option>{escape(f["within_1_month"])}</option>'
        f'<option>{escape(f["later"])}</option>\n'
        "                        </select>\n"
        "                    </label>\n"
        "                </div>\n"
        '                <label class="form-check">\n'
        '                    <input name="privacy" type="checkbox" required>\n'
        f"                    <span>{escape(iq['privacy_label'])} "
        f'(<a href="/{lang}/legal/">{escape(v2["legal_label"])}</a>)</span>\n'
        "                </label>\n"
        '                <input type="text" name="website" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true">\n'
        f'                <button class="button button-primary" type="submit"{submit_disabled}>'
        f'{escape(iq["submit"])}</button>\n'
        '                <p class="form-status" id="inquiry-status" role="status" aria-live="polite"></p>\n'
        "            </form>\n"
        "        </div></section>\n"
        + cta_block(v2)
    )

def market_access_main(v2: dict[str, Any]) -> str:
    """Market Access notice: IT focus; former market offer not continued."""
    archive = v2["market_access_archive"]
    lang = v2["language"]
    return (
        '        <section class="hero"><div class="container">\n'
        f"            <h1>{escape(archive['title'])}</h1>\n"
        f'            <p class="hero-lead">{escape(archive["lead"])}</p>\n'
        '            <div class="hero-actions">\n'
        f'                <a class="button button-primary" href="/{lang}/">'
        f'{escape(archive["cta"])}</a>\n'
        "            </div>\n"
        "        </div></section>\n"
    )


def write_sitemap(site: dict[str, Any], routes: list[str]) -> None:
    """Sitemap for active languages only."""
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ElementTree.register_namespace("", namespace)
    urlset = ElementTree.Element(f"{{{namespace}}}urlset")
    for route in sorted(set(routes)):
        entry = ElementTree.SubElement(urlset, f"{{{namespace}}}url")
        ElementTree.SubElement(entry, f"{{{namespace}}}loc").text = site["base_url"] + route
        ElementTree.SubElement(entry, f"{{{namespace}}}lastmod").text = "2026-08-07"
    tree = ElementTree.ElementTree(urlset)
    ElementTree.indent(tree, space="  ")
    tree.write(ROOT / "sitemap.xml", encoding="utf-8", xml_declaration=True)


def write_redirects() -> None:
    """Root + market → current home; hospitality → services; EN stays live."""
    lines = [
        "# Active: DE + EN. Root always → /de/. FR/IT/SR/BS/HR temporarily 302 → /de/",
        "/ /de/ 301",
        "/index.html /de/ 301",
        "",
        "# Former Market Access URLs → current home (no archive page)",
        "/de/market-access /de/ 301",
        "/de/market-access/ /de/ 301",
        "/en/market-access /en/ 301",
        "/en/market-access/ /en/ 301",
        "/de/markt /de/ 301",
        "/de/markt/ /de/ 301",
        "/en/market /en/ 301",
        "/en/market/ /en/ 301",
        "/fr/marche /de/ 301",
        "/fr/marche/ /de/ 301",
        "/it/mercato /de/ 301",
        "/it/mercato/ /de/ 301",
        "/sr/trziste /de/ 301",
        "/sr/trziste/ /de/ 301",
        "/bs/trziste /de/ 301",
        "/bs/trziste/ /de/ 301",
        "/hr/trziste /de/ 301",
        "/hr/trziste/ /de/ 301",
        "",
        "# Hospitality → services (all former locale folders)",
        "/de/hospitality /de/leistungen/ 301",
        "/de/hospitality/ /de/leistungen/ 301",
        "/en/hospitality /en/services/ 301",
        "/en/hospitality/ /en/services/ 301",
        "/fr/hospitality /de/leistungen/ 301",
        "/fr/hospitality/ /de/leistungen/ 301",
        "/it/hospitality /de/leistungen/ 301",
        "/it/hospitality/ /de/leistungen/ 301",
        "/sr/hospitality /de/leistungen/ 301",
        "/sr/hospitality/ /de/leistungen/ 301",
        "/bs/hospitality /de/leistungen/ 301",
        "/bs/hospitality/ /de/leistungen/ 301",
        "/hr/hospitality /de/leistungen/ 301",
        "/hr/hospitality/ /de/leistungen/ 301",
        "",
        "# Inactive locales → DE (after specific hospitality/market rules)",
        "/fr /de/ 302",
        "/fr/ /de/ 302",
        "/fr/* /de/ 302",
        "/it /de/ 302",
        "/it/ /de/ 302",
        "/it/* /de/ 302",
        "/sr /de/ 302",
        "/sr/ /de/ 302",
        "/sr/* /de/ 302",
        "/bs /de/ 302",
        "/bs/ /de/ 302",
        "/bs/* /de/ 302",
        "/hr /de/ 302",
        "/hr/ /de/ 302",
        "/hr/* /de/ 302",
        "",
        "# Legacy service detail slugs → new Leistung pages",
        "/de/leistungen/onboarding /de/leistungen/benutzer-und-zugaenge/ 301",
        "/de/leistungen/onboarding/ /de/leistungen/benutzer-und-zugaenge/ 301",
        "/de/leistungen/offboarding /de/leistungen/benutzer-und-zugaenge/ 301",
        "/de/leistungen/offboarding/ /de/leistungen/benutzer-und-zugaenge/ 301",
        "/de/leistungen/arbeitsplatz-anfragen /de/leistungen/microsoft-365-arbeitsplatz/ 301",
        "/de/leistungen/arbeitsplatz-anfragen/ /de/leistungen/microsoft-365-arbeitsplatz/ 301",
        "/de/leistungen/anbieterkoordination /de/leistungen/ 301",
        "/de/leistungen/anbieterkoordination/ /de/leistungen/ 301",
        "/de/leistungen/ansprechpartner /de/leistungen/ 301",
        "/de/leistungen/ansprechpartner/ /de/leistungen/ 301",
        "/de/leistungen/zugang-sicherheit /de/leistungen/it-basischeck/ 301",
        "/de/leistungen/zugang-sicherheit/ /de/leistungen/it-basischeck/ 301",
        "/en/services/onboarding /en/services/users-and-access/ 301",
        "/en/services/onboarding/ /en/services/users-and-access/ 301",
        "/en/services/offboarding /en/services/users-and-access/ 301",
        "/en/services/offboarding/ /en/services/users-and-access/ 301",
        "/en/services/workplace-requests /en/services/microsoft-365-workplace/ 301",
        "/en/services/workplace-requests/ /en/services/microsoft-365-workplace/ 301",
        "/en/services/vendor-coordination /en/services/ 301",
        "/en/services/vendor-coordination/ /en/services/ 301",
        "/en/services/single-point-of-contact /en/services/ 301",
        "/en/services/single-point-of-contact/ /en/services/ 301",
        "/en/services/access-security-basics /en/services/it-basics-check/ 301",
        "/en/services/access-security-basics/ /en/services/it-basics-check/ 301",
        "",
        "# Legacy German routes",
        "/services /de/leistungen/ 301",
        "/services.html /de/leistungen/ 301",
        "/packages /de/leistungen/ 301",
        "/packages.html /de/leistungen/ 301",
        "/it-matrix /de/leistungen/ 301",
        "/it-matrix.html /de/leistungen/ 301",
        "/kontakt /de/anfrage/ 301",
        "/kontakt.html /de/anfrage/ 301",
        "/rechtliches /de/legal/ 301",
        "/legal /de/legal/ 301",
        "/legal.html /de/legal/ 301",
        "/about /de/ueber-bit/ 301",
        "/about.html /de/ueber-bit/ 301",
        "/de/about /de/ueber-bit/ 301",
        "/de/about/ /de/ueber-bit/ 301",
        "/en/about /en/about-bit/ 301",
        "/en/about/ /en/about-bit/ 301",
        "",
        "# Legacy English entry points → EN (not DE)",
        "/index_en /en/ 302",
        "/index_en.html /en/ 302",
        "/index-en.html /en/ 302",
        "/en.html /en/ 302",
        "/services-en /en/services/ 302",
        "/services-en.html /en/services/ 302",
        "/packages-en /en/services/ 302",
        "/packages-en.html /en/services/ 302",
        "/it-matrix-en /en/services/ 302",
        "/it-matrix-en.html /en/services/ 302",
        "/kontakt-en /en/inquiry/ 302",
        "/kontakt-en.html /en/inquiry/ 302",
        "/legal-en /en/legal/ 302",
        "/legal-en.html /en/legal/ 302",
        "",
        "# Force non-www on Cloudflare Pages",
        "https://www.boksitsupport.ch/* https://boksitsupport.ch/:splat 301",
        "http://www.boksitsupport.ch/* https://boksitsupport.ch/:splat 301",
        "",
    ]
    write_text(ROOT / "_redirects", "\n".join(lines) + "\n")


def write_headers() -> None:
    """Security + anti-stale HTML cache headers for Cloudflare Pages."""
    content = """\
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=(), payment=(), usb=()
  Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; font-src 'self'; form-action 'self'
  Cache-Control: no-cache, no-store, must-revalidate
  CDN-Cache-Control: no-store

/assets/*
  Cache-Control: public, max-age=86400, must-revalidate
  CDN-Cache-Control: public, max-age=86400

/assets/js/inquiry-form.js
  Cache-Control: no-cache, must-revalidate
  CDN-Cache-Control: no-store
"""
    write_text(ROOT / "_headers", content)


def build_language(language: str, site: dict[str, Any], routes: list[str]) -> None:
    """Generate all Zustand-A pages for one language."""
    v2 = load_v2(language)

    def emit(rel: str, html_doc: str, *, in_sitemap: bool = True) -> None:
        clean = rel.strip("/")
        write_text(ROOT / clean / "index.html", html_doc)
        if in_sitemap:
            routes.append(f"/{clean}/")

    pages = [
        ("home", PAGE_PATHS["home"][language], v2["home"]["meta_title"], v2["home"]["meta_description"], home_main(v2), "home"),
        (
            "services",
            PAGE_PATHS["services"][language],
            v2["services"]["title"] + " | BIT",
            v2["home"]["meta_description"],
            leistungen_main(v2),
            "services",
        ),
        (
            "examples",
            PAGE_PATHS["examples"][language],
            v2["examples_page"]["meta_title"],
            v2["examples_page"]["meta_description"],
            examples_main(v2),
            "examples",
        ),
        (
            "process",
            PAGE_PATHS["process"][language],
            v2["process"]["title"] + " | BIT",
            v2["process"]["title"],
            process_main(v2),
            "process",
        ),
        (
            "audience",
            PAGE_PATHS["audience"][language],
            v2["audience"]["title"] + " | BIT",
            v2["audience"]["title"],
            audience_main(v2),
            "audience",
        ),
        (
            "about",
            PAGE_PATHS["about"][language],
            v2["about"]["meta_title"],
            v2["about"]["meta_description"],
            about_main(v2),
            "about",
        ),
        (
            "faq",
            PAGE_PATHS["faq"][language],
            v2["faq"]["meta_title"],
            v2["faq"]["meta_description"],
            faq_main(v2),
            "faq",
        ),
        (
            "inquiry",
            PAGE_PATHS["inquiry"][language],
            v2["inquiry"]["meta_title"],
            v2["inquiry"]["meta_description"],
            inquiry_main(v2, site),
            "inquiry",
        ),
    ]

    for page_key, path, title, desc, main, page_id in pages:
        extra_scripts = ""
        extra_head = ""
        if page_id == "inquiry":
            extra_scripts = (
                '    <script type="module" src="/assets/js/inquiry-form.js?v=10"></script>\n'
            )
        if page_id in {"home", "services", "about", "process", "examples", "audience"}:
            extra_head = professional_service_json_ld(site)
        if page_id == "faq":
            extra_head = faq_page_json_ld(v2, site, path) + professional_service_json_ld(site)
        if page_id in {c["slug"] for c in v2["services"]["cards"]}:
            extra_head = professional_service_json_ld(site)
        emit(
            path,
            render_page(
                v2=v2,
                site=site,
                path=path,
                page_key=page_key,
                meta_title=title,
                meta_description=desc,
                main=main,
                page_id=page_id,
                extra_head=extra_head,
                extra_scripts=extra_scripts,
            ),
        )

    for card in v2["services"]["cards"]:
        page_key = SERVICE_PAIR[card["slug"]]
        path = PAGE_PATHS[page_key][language]
        emit(
            path,
            render_page(
                v2=v2,
                site=site,
                path=path,
                page_key=page_key,
                meta_title=f"{card['title']} | BIT",
                meta_description=card["text"][:155],
                main=leistung_detail_main(v2, card),
                page_id=card["slug"],
                extra_head=professional_service_json_ld(site),
            ),
        )


ROOT_REDIRECT_HTML = """<!DOCTYPE html>
<html lang="de-CH">
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0;url=/de/">
    <link rel="canonical" href="https://boksitsupport.ch/de/">
    <title>BIT – Weiterleitung</title>
</head>
<body>
    <p><a href="/de/">Weiter zur deutschen Startseite</a></p>
</body>
</html>
"""


def build_v2() -> list[str]:
    """Generate DE+EN Zustand-A pages, sitemap and redirects."""
    site = load_site()
    routes: list[str] = []
    for language in active_languages(site):
        build_language(language, site, routes)

    # Root must never ship dual-gateway or full home HTML; middleware/_redirects 301 → /de/.
    write_text(ROOT / "index.html", ROOT_REDIRECT_HTML)

    # Include legal pages in sitemap (built by legacy renderer)
    for language in active_languages(site):
        routes.append(f"/{language}/legal/")

    write_sitemap(site, routes)
    write_redirects()
    write_headers()
    return routes


if __name__ == "__main__":
    built = build_v2()
    print(f"Built {len(built)} v2 routes")
