"""Build the localized two-path static website."""
from __future__ import annotations

import html
import json
import shutil
from pathlib import Path
from string import Template
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "site.json"
CONTENT_PATH = ROOT / "config" / "path_content.json"
LOCALES_DIR = ROOT / "locales"
TEMPLATES_DIR = ROOT / "templates"


def escape(value: object) -> str:
    """Escape text inserted into HTML."""
    return html.escape(str(value), quote=True)


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    """Load and validate central routing and commercial configuration."""
    config = json.loads(path.read_text(encoding="utf-8"))
    codes = [item["code"] for item in config["languages"]]
    if len(codes) != len(set(codes)):
        raise ValueError("Language codes must be unique")
    for path_data in config["paths"].values():
        if set(path_data["languages"]) != set(path_data["slugs"]):
            raise ValueError("Every path language requires exactly one slug")
    return config


def load_locale(language: str) -> dict[str, Any]:
    """Load legacy shared legal translations."""
    return json.loads((LOCALES_DIR / f"{language}.json").read_text(encoding="utf-8"))


def load_locales(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Load all registered shared locale data."""
    return {item["code"]: load_locale(item["code"]) for item in config["languages"]}


def load_content(path: Path = CONTENT_PATH) -> dict[str, Any]:
    """Load path-specific content."""
    return json.loads(path.read_text(encoding="utf-8"))


def registered_languages(config: dict[str, Any]) -> Iterable[str]:
    """Return registered language codes."""
    return (item["code"] for item in config["languages"])


def write_text(path: Path, content: str) -> None:
    """Write deterministic UTF-8 output."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


class TemplateRepository:
    """Load static templates."""
    def __init__(self, base_path: Path = TEMPLATES_DIR) -> None:
        self.base_path = base_path
        self._cache: dict[str, Template] = {}

    def get(self, name: str) -> Template:
        """Return one cached template."""
        if name not in self._cache:
            self._cache[name] = Template(
                (self.base_path / name).read_text(encoding="utf-8")
            )
        return self._cache[name]


class SiteRenderer:
    """Render gateway, service, about and legal pages."""
    def __init__(
        self,
        config: dict[str, Any],
        locales: dict[str, dict[str, Any]],
        templates: TemplateRepository,
        content: dict[str, Any] | None = None,
    ) -> None:
        self.config = config
        self.locales = locales
        self.templates = templates
        self.content = content or load_content()
        self.language_map = {item["code"]: item for item in config["languages"]}

    def route(self, path_key: str, language: str) -> str:
        """Return a localized path route."""
        slug = self.config["paths"][path_key]["slugs"][language]
        return f"/{language}/{slug}/"

    @staticmethod
    def personal_name(language: str) -> str:
        """Return the requested personal-name spelling for each locale."""
        return (
            "Stefan Bogdanović"
            if language in {"sr", "bs", "hr"}
            else "Stefan Bogdanovic"
        )

    def language_links(
        self,
        current: str,
        languages: list[str],
        path_key: str | None = None,
        suffix: str = "",
    ) -> str:
        """Render a text-only language menu for the active path."""
        active = self.config.get("active_languages") or ["de", "en"]
        if self.config.get("phase1_de_only"):
            active = ["de"]
        links = []
        for code in active:
            if path_key and code in self.config["paths"][path_key]["slugs"]:
                href = self.route(path_key, code)
            elif suffix == "about/":
                href = f"/{code}/ueber-bit/" if code == "de" else f"/{code}/about-bit/"
            else:
                href = f"/{code}/{suffix}"
            current_attr = ' aria-current="page"' if code == current else ""
            label = self.language_map.get(code, {"label": code.upper()})["label"]
            links.append(
                f'                <a href="{href}"{current_attr}>{escape(label)}</a>'
            )
        return "\n".join(links)

    def alternate_links(self, path_key: str | None, suffix: str = "") -> str:
        """Render alternates for active languages only."""
        active = self.config.get("active_languages") or ["de", "en"]
        if self.config.get("phase1_de_only"):
            active = ["de"]

        def route_for(code: str) -> str:
            if path_key:
                return self.route(path_key, code)
            if suffix == "about/":
                return f"/{code}/ueber-bit/" if code == "de" else f"/{code}/about-bit/"
            return f"/{code}/{suffix}"

        links = [
            f'    <link rel="alternate" hreflang="{self.language_map[code]["hreflang"]}" '
            f'href="{self.config["base_url"]}{route_for(code)}">'
            for code in active
            if code in self.language_map
        ]
        default = "de" if "de" in active else active[0]
        links.append(
            f'    <link rel="alternate" hreflang="x-default" '
            f'href="{self.config["base_url"]}{route_for(default)}">'
        )
        return "\n".join(links)

    def render_gateway(self, language: str = "de", root: bool = False) -> str:
        """Render the neutral one-screen gateway."""
        gateway = self.content["gateway"][language]
        locale = self.locales[language]
        common = self.content[language]["common"]
        hospitality_languages = self.config["paths"]["hospitality"]["languages"]
        market_languages = self.config["paths"]["market"]["languages"]
        hospitality_language = language if language in hospitality_languages else "en"
        market_language = language if language in market_languages else "en"
        city = locale["legal_page"]["city"]
        identity = gateway["identity"].format(city=city)
        context = {
            "html_lang": escape(locale["lang"]),
            "canonical": self.config["base_url"] + ("/" if root else f"/{language}/"),
            "alternate_links": self.alternate_links(None),
            "language": language,
            "meta_title": escape(gateway["meta_title"]),
            "meta_description": escape(gateway["meta_description"]),
            "language_prompt": escape(locale["language_suggestion"]["prompt"]),
            "language_switch": escape(locale["language_suggestion"]["switch"]),
            "language_dismiss": escape(locale["language_suggestion"]["dismiss"]),
            "skip": escape(common["skip"]),
            "identity": escape(identity),
            "title": escape(gateway["title"]),
            "subtitle": escape(gateway["subtitle"]),
            "hospitality_title": escape(gateway["hospitality_title"]),
            "hospitality_text": escape(gateway["hospitality_text"]),
            "hospitality_note": (
                f'<span class="gateway-note">{escape(gateway["hospitality_note"])}</span>'
                if gateway.get("hospitality_note")
                else ""
            ),
            "market_title": escape(gateway["market_title"]),
            "market_text": escape(gateway["market_text"]),
            "hospitality_url": self.route("hospitality", hospitality_language),
            "market_url": self.route("market", market_language),
            "languages_label": escape(common["languages"]),
            "language_links": self.language_links(
                language, list(registered_languages(self.config))
            ),
            "legal_url": f"/{language}/legal/",
            "legal_label": escape(locale["footer"]["legal"]),
        }
        return self.templates.get("gateway.html").substitute(context)

    def structured_data(
        self,
        canonical: str,
        language: str,
        description: str,
        service_types: list[str],
    ) -> str:
        """Render consistent ProfessionalService schema."""
        contact = self.config["contact"]
        address = self.config["address"]
        payload = {
            "@context": "https://schema.org",
            "@type": "ProfessionalService",
            "@id": f"{canonical}#business",
            "name": self.config["site_name"],
            "alternateName": self.config["brand"],
            "url": canonical,
            "description": description,
            "inLanguage": self.locales[language]["lang"],
            "telephone": contact["phone_display"],
            "email": contact["email"],
            "address": {
                "@type": "PostalAddress",
                "streetAddress": address["street"],
                "postalCode": address["postal_code"],
                "addressLocality": self.locales[language]["legal_page"]["city"],
                "addressCountry": "CH",
            },
            "areaServed": {"@type": "Country", "name": "CH"},
            "founder": {
                "@type": "Person",
                "name": self.personal_name(language),
            },
            "contactPoint": [{
                "@type": "ContactPoint",
                "contactType": "customer service",
                "telephone": contact["phone_display"],
                "email": contact["email"],
            }],
            "serviceType": service_types,
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

    @staticmethod
    def list_html(items: list[str], prices: dict[str, str]) -> str:
        """Render a list while substituting centrally configured prices."""
        return "".join(
            f"<li>{escape(item.format(**prices))}</li>" for item in items
        )

    def process_html(self, process: dict[str, Any]) -> str:
        """Render the five-step Path A engagement workflow."""
        steps = "".join(
            self.templates.get("components/process-step.html").substitute(
                number=f"{index:02d}",
                title=escape(step["title"]),
                text=escape(step["text"]),
            )
            for index, step in enumerate(process["steps"], start=1)
        )
        return (
            '<section class="section" id="process"><div class="container">'
            f'<div class="section-heading"><div><h2>{escape(process["title"])}</h2>'
            f'<p class="section-intro">{escape(process["intro"])}</p></div></div>'
            f'<div class="process-grid">{steps}</div></div></section>'
        )

    def sample_html(self, page: dict[str, Any]) -> str:
        """Render anonymised market-pilot sample deliverable format."""
        if "sample_title" not in page:
            return ""
        groups = (
            ("sample_targets_title", "sample_targets"),
            ("sample_criteria_title", "sample_criteria"),
            ("sample_findings_title", "sample_findings"),
            ("sample_report_title", "sample_report"),
        )
        blocks = "".join(
            f'<div class="market-panel"><h3>{escape(page[title_key])}</h3>'
            f'<ul class="market-list">{"".join(f"<li>{escape(item)}</li>" for item in page[list_key])}'
            "</ul></div>"
            for title_key, list_key in groups
        )
        return (
            '<section class="section" id="sample"><div class="container">'
            f'<h2>{escape(page["sample_title"])}</h2>'
            f'<p class="section-intro">{escape(page["sample_note"])}</p>'
            f'<div class="card-grid two-column">{blocks}</div>'
            "</div></section>"
        )

    def service_sections(
        self, path_key: str, page: dict[str, Any], common: dict[str, str]
    ) -> str:
        """Render path-specific offer sections."""
        prices = self.config["prices"]
        if path_key == "hospitality":
            cards = "".join(
                '<article class="card"><h3>'
                + escape(block["title"])
                + "</h3><p>"
                + escape(block["text"])
                + "</p><ul>"
                + self.list_html(block["items"], prices)
                + "</ul></article>"
                for block in page["blocks"]
            )
            primary = (
                '<section class="section" id="offer"><div class="container">'
                f'<div class="card-grid two-column">{cards}</div></div></section>'
            )
            process = self.process_html(page["process"])
        else:
            entry = (
                '<section class="section" id="offer"><div class="container market-layout">'
                f'<div><p class="eyebrow">{escape(page["eyebrow"])}</p>'
                f'<h2>{escape(page["document_title"])}</h2>'
                f'<p>{escape(page["document_text"].format(**prices))}</p></div>'
                "</div></section>"
            )
            pilot = (
                '<section class="section" id="pilot"><div class="container market-layout">'
                f'<div><p class="eyebrow">{escape(page["pilot_eyebrow"])}</p>'
                f'<h2>{escape(page["pilot_title"])}</h2><p>{escape(page["pilot_intro"])}</p></div>'
                f'<div class="market-panel"><ul class="market-list">{self.list_html(page["deliverables"], prices)}</ul></div>'
                "</div></section>"
            )
            sample = self.sample_html(page)
            primary = entry + pilot + sample
            process = ""
        pricing = (
            '<section class="section" id="price"><div class="container market-layout">'
            f'<div><p class="eyebrow">{escape(common["price"])}</p><h2>{escape(common["price"])}</h2></div>'
            f'<div class="market-panel"><ul class="market-list">{self.list_html(page["pricing"], prices)}</ul></div>'
            "</div></section>"
        )
        optional = ""
        if path_key == "market":
            optional = (
                '<section class="section"><div class="container">'
                f'<h2>{escape(page["optional_title"])}</h2><p class="section-intro">{escape(page["optional"])}</p>'
                "</div></section>"
            )
        limits = (
            '<section class="section assurance-section" id="limits"><div class="container market-layout">'
            f'<div><p class="eyebrow">{escape(common["exclusions"])}</p><h2>{escape(common["exclusions"])}</h2>'
            f'<p>{escape(page["honesty"])}</p></div><div class="market-panel">'
            f'<ul class="market-list">{self.list_html(page["exclusions"], prices)}</ul></div>'
            "</div></section>"
        )
        return primary + process + pricing + optional + limits

    def contact_actions_html(self, language: str, path_key: str, common: dict[str, str]) -> str:
        """Order contact CTAs: Swiss hospitality prefers email/phone first."""
        contact = self.config["contact"]
        email = (
            f'<a class="button button-secondary" href="mailto:{escape(contact["email"])}">'
            f'{escape(common["email"])}</a>'
        )
        phone = (
            f'<a class="button button-secondary" href="{escape(contact["phone_href"])}">'
            f'{escape(common.get("phone", contact["phone_display"]))}</a>'
        )
        whatsapp = (
            f'<a class="button button-whatsapp" data-contact="whatsapp" '
            f'href="{escape(contact["whatsapp_url"])}">{escape(common["whatsapp"])}</a>'
        )
        viber = (
            f'<a class="button button-viber" data-contact="viber" '
            f'href="{escape(contact["viber_url"])}">{escape(common["viber"])}</a>'
        )
        swiss_formal = path_key == "hospitality" and language in {"de", "fr", "it"}
        ordered = (
            [email, phone, whatsapp, viber]
            if swiss_formal
            else [whatsapp, viber, email, phone]
        )
        return "\n                        ".join(ordered)

    def render_service(self, path_key: str, language: str) -> str:
        """Render one path-specific service page."""
        page = self.content[language][path_key]
        common = self.content[language]["common"]
        locale = self.locales[language]
        path_data = self.config["paths"][path_key]
        route = self.route(path_key, language)
        canonical = self.config["base_url"] + route
        nav_targets = ("offer", "price", "limits")
        nav_links = "".join(
            f'<a href="#{target}">{escape(label)}</a>'
            for target, label in zip(nav_targets, page["nav"])
        )
        location = locale["footer"]["location"]
        context = {
            "html_lang": escape(locale["lang"]),
            "language": language,
            "path_key": path_key,
            "meta_title": escape(page["meta_title"]),
            "meta_description": escape(page["meta_description"]),
            "canonical": canonical,
            "canonical_path": route,
            "alternate_links": self.alternate_links(path_key),
            "structured_data": self.structured_data(
                canonical,
                language,
                page["meta_description"],
                (
                    [block["title"] for block in page["blocks"]]
                    if path_key == "hospitality"
                    else [page["document_title"], page["pilot_title"]]
                ),
            ),
            "language_prompt": escape(locale["language_suggestion"]["prompt"]),
            "language_switch": escape(locale["language_suggestion"]["switch"]),
            "language_dismiss": escape(locale["language_suggestion"]["dismiss"]),
            "skip": escape(common["skip"]),
            "nav_aria": escape(locale["nav"]["aria"]),
            "nav_links": nav_links,
            "about_label": escape(common["about"]),
            "contact_label": escape(common["contact"]),
            "menu_label": escape(common["menu"]),
            "languages_label": escape(common["languages"]),
            "language_links": self.language_links(
                language, path_data["languages"], path_key
            ),
            "eyebrow": escape(page["eyebrow"]),
            "title": escape(page["title"]),
            "lead": escape(page["lead"]),
            "main_sections": self.service_sections(path_key, page, common),
            "warning": escape(common["warning"]),
            "contact_actions": self.contact_actions_html(language, path_key, common),
            "whatsapp_url": escape(self.config["contact"]["whatsapp_url"]),
            "viber_url": escape(self.config["contact"]["viber_url"]),
            "location": escape(location),
            "legal_label": escape(common["legal"]),
        }
        return self.templates.get("service.html").substitute(context)

    def render_about(self, language: str) -> str:
        """Render one shared localized about page."""
        common = self.content[language]["common"]
        locale = self.locales[language]
        canonical = f'{self.config["base_url"]}/{language}/about/'
        schema = self.structured_data(
            canonical,
            language,
            common["about_lead"],
            [common["about_title"]],
        )
        return self.templates.get("about.html").substitute(
            html_lang=escape(locale["lang"]), language=language,
            canonical=canonical, alternate_links=self.alternate_links(None, "about/"),
            structured_data=schema,
            skip=escape(common["skip"]), languages_label=escape(common["languages"]),
            language_links=self.language_links(
                language, list(registered_languages(self.config)), suffix="about/"
            ),
            about_title=escape(common["about_title"]),
            about_lead=escape(common["about_lead"]),
            about_practice=escape(common["about_practice"]),
            about_text=escape(common["about_text"]),
            about_languages=escape(common["about_languages"]),
            about_independent=escape(common["about_independent"]),
            image_alt=escape(common["image_alt"]), back=escape(common["back"]),
            location=escape(locale["footer"]["location"]),
            legal_label=escape(common["legal"]),
        )

    def _active_language_codes(self) -> list[str]:
        """Public languages for switcher/hreflang (DE+EN)."""
        active = list(self.config.get("active_languages") or ["de", "en"])
        if self.config.get("phase1_de_only"):
            return ["de"]
        return active

    def _privacy_body_html(self, legal: dict[str, Any]) -> str:
        """Render structured privacy section (trusted locale HTML structure)."""
        detail = legal.get("privacy_detail") or {}
        if not detail:
            # Legacy fallback for inactive locales still using flat strings
            parts = [legal.get("privacy", ""), legal.get("privacy_messaging", "")]
            return f"                        <p>{escape(' '.join(p for p in parts if p))}</p>"

        lines: list[str] = [
            f"                        <p>{escape(detail['intro'])}</p>",
            f"                        <h3>{escape(detail['categories_title'])}</h3>",
            "                        <ul>",
        ]
        for item in detail["categories"]:
            lines.append(f"                            <li>{escape(item)}</li>")
        lines.extend(
            [
                "                        </ul>",
                f"                        <h3>{escape(detail['purpose_title'])}</h3>",
                f"                        <p>{escape(detail['purpose'])}</p>",
                f"                        <h3>{escape(detail['basis_title'])}</h3>",
                f"                        <p>{escape(detail['basis'])}</p>",
                f"                        <h3>{escape(detail['retention_title'])}</h3>",
            ]
        )
        confirm = (detail.get("retention_confirm") or "").strip()
        if confirm:
            lines.append(f"                        <!-- {escape(confirm)} -->")
        lines.extend(
            [
                f"                        <p>{escape(detail['retention'])}</p>",
                f"                        <h3>{escape(detail['processors_title'])}</h3>",
                f"                        <p>{escape(detail['processors'])}</p>",
                f"                        <h3>{escape(detail['abroad_title'])}</h3>",
                f"                        <p>{escape(detail['abroad'])}</p>",
                f"                        <h3>{escape(detail['rights_title'])}</h3>",
                f"                        <p>{escape(detail['rights'])}</p>",
                f"                        <h3>{escape(detail['contact_title'])}</h3>",
                f"                        <p>{escape(detail['contact'])}</p>",
                f"                        <p>{escape(detail['no_tracking'])}</p>",
            ]
        )
        return "\n".join(lines)

    def _v2_nav_and_footer(self, language: str) -> dict[str, str]:
        """Reuse Zustand-A nav/footer labels for legal chrome alignment."""
        v2_path = ROOT / "config" / f"{language}_v2.json"
        if not v2_path.exists():
            # Inactive languages: minimal chrome without main nav
            return {
                "nav_links": "",
                "nav_aria": "Navigation",
                "menu_label": "Menu",
                "skip": "Skip",
                "footer_note": "",
                "inquiry_href": f"/{language}/",
                "inquiry_label": "Contact",
                "terms_href": "/de/agb/" if language == "de" else "/en/terms/",
                "terms_label": "AGB" if language == "de" else "Terms",
                "footer_legal": "Legal",
                "footer_city": "Zürich" if language == "de" else "Zurich",
            }
        v2 = json.loads(v2_path.read_text(encoding="utf-8"))
        nav_bits = []
        for item in v2["nav"]:
            nav_bits.append(
                f'                <a href="{escape(item["href"])}">'
                f'{escape(item["label"])}</a>'
            )
        live = v2.get("inquiry", {}).get("live", False)
        footer_note = (
            v2["footer_channels_note"]
            if live
            else v2.get("footer_channels_note_offline", v2["footer_channels_note"])
        )
        return {
            "nav_links": "\n".join(nav_bits),
            "nav_aria": escape(v2["nav_aria"]),
            "menu_label": escape(v2["menu_label"]),
            "skip": escape(v2["skip"]),
            "footer_note": escape(footer_note),
            "inquiry_href": escape(v2["cta_primary_href"]),
            "inquiry_label": escape(v2["inquiry_label"]),
            "terms_href": escape(
                "/de/agb/" if language == "de" else "/en/terms/"
            ),
            "terms_label": escape(v2.get("terms_label") or ("AGB" if language == "de" else "Terms")),
            "footer_legal": escape(v2.get("legal_label") or "Legal"),
            "footer_city": escape("Zürich" if language == "de" else "Zurich"),
        }

    def render_legal(self, language: str) -> str:
        """Render shared legal/privacy page with factual Swiss details."""
        locale = self.locales[language]
        legal = locale["legal_page"]
        common = self.content[language]["common"]
        address = self.config["address"]
        contact = self.config["contact"]
        chrome = self._v2_nav_and_footer(language)
        active = self._active_language_codes()
        context = {
            "html_lang": escape(locale["lang"]),
            "language": language,
            "canonical": f'{self.config["base_url"]}/{language}/legal/',
            "alternate_links": self.alternate_links(None, "legal/"),
            # Legal switcher: active languages only (DE/EN), never FR/SR/BS/HR
            "language_links": self.language_links(
                language, active, suffix="legal/"
            ),
            "nav_languages": escape(common["languages"]),
            "nav_links": chrome["nav_links"],
            "nav_aria": chrome["nav_aria"],
            "menu_label": chrome["menu_label"],
            "skip": chrome["skip"],
            "legal_title": escape(legal["title"]),
            "legal_eyebrow": escape(legal["eyebrow"]),
            "legal_lead": escape(legal["lead"]),
            "legal_meta_description": escape(legal["lead"]),
            "legal_back": escape(legal.get("back") or common["back"]),
            "legal_provider_title": escape(legal["provider_title"]),
            "legal_provider_name": escape(legal["provider_name"]),
            "legal_entity_note": escape(legal["entity_type"]),
            "legal_owner": escape(legal["owner"]),
            "legal_activity_title": escape(legal["activity_title"]),
            "legal_activity": escape(legal["activity"]),
            "legal_address_title": escape(legal["address_title"]),
            "address_street": escape(address["street"]),
            "address_postal_code": escape(address["postal_code"]),
            "address_city": escape(legal["city"]),
            "address_country": escape(legal["country"]),
            "legal_contact_title": escape(legal["contact_title"]),
            "legal_registration_title": escape(legal["terms_title"]),
            "legal_registration": escape(legal["terms"]),
            "liability_title": escape(legal["liability_title"]),
            "liability": escape(
                legal["liability"]
                .replace("Garantie", "Zusicherung")
                .replace("guarantee", "assurance")
            ),
            "copyright_title": escape(legal["copyright_title"]),
            "copyright": escape(legal["copyright"]),
            "privacy_title": escape(legal["privacy_title"]),
            "privacy_body": self._privacy_body_html(legal),
            "jurisdiction_title": escape(legal["jurisdiction_title"]),
            "jurisdiction": escape(legal["jurisdiction"]),
            "legal_updated": escape(legal["updated"]),
            "phone_href": escape(contact["phone_href"]),
            "phone_display": escape(contact["phone_display"]),
            "email": escape(contact["email"]),
            "whatsapp_url": escape(contact["whatsapp_url"]),
            "viber_url": escape(contact["viber_url"]),
            "footer_city": chrome["footer_city"],
            "footer_note": chrome["footer_note"],
            "inquiry_href": chrome["inquiry_href"],
            "inquiry_label": chrome["inquiry_label"],
            "terms_href": chrome["terms_href"],
            "terms_label": chrome["terms_label"],
            "footer_legal": chrome["footer_legal"],
        }
        return self.templates.get("legal.html").substitute(context)


def legacy_path_output_dirs(config: dict[str, Any]) -> list[Path]:
    """Return hospitality/market slug folders that must not ship as crawlable HTML."""
    dirs: list[Path] = []
    for path_data in config["paths"].values():
        for language in path_data["languages"]:
            slug = path_data["slugs"][language]
            dirs.append(ROOT / language / slug)
    return dirs


def remove_legacy_path_pages(config: dict[str, Any]) -> list[str]:
    """
    Delete hospitality/market HTML so Cloudflare Pages serves
    _redirects / middleware 301s instead of stale static bodies.
    Also drop superseded /{lang}/about/ trees (redirected to ueber-bit/about-bit).
    """
    removed: list[str] = []
    targets = list(legacy_path_output_dirs(config))
    for language in registered_languages(config):
        targets.append(ROOT / language / "about")
    # Former Market Access archive pages: serve 301 via middleware/_redirects only
    for language in ("de", "en"):
        targets.append(ROOT / language / "market-access")
    for path in targets:
        if path.exists():
            shutil.rmtree(path)
            removed.append(str(path.relative_to(ROOT)).replace("\\", "/"))
    return removed


def remove_inactive_locale_trees(config: dict[str, Any]) -> list[str]:
    """
    Delete FR/IT/SR/BS/HR trees entirely so no old gateway/legal HTML can be served.
    Redirects come from _redirects + functions/_middleware.js only.
    """
    removed: list[str] = []
    active = set(config.get("active_languages") or ["de", "en"])
    for language in registered_languages(config):
        if language in active:
            continue
        path = ROOT / language
        if path.exists():
            shutil.rmtree(path)
            removed.append(language)
    return removed


def build() -> None:
    """Build legal + Zustand-A (v2); never ship old path or inactive-locale HTML."""
    config = load_config()
    locales = load_locales(config)
    renderer = SiteRenderer(config, locales, TemplateRepository())
    active = list(config.get("active_languages") or ["de", "en"])
    if config.get("phase1_de_only"):
        active = ["de"]

    # Active languages only: legal pages. Inactive locale dirs are purged after v2.
    for language in registered_languages(config):
        if language in active:
            write_text(
                ROOT / language / "legal" / "index.html",
                renderer.render_legal(language),
            )

    # Phase-3: DE+EN Zustand-A, redirects, sitemap — then purge legacy + inactive HTML
    from build_v2_de import build_v2

    build_v2()
    remove_legacy_path_pages(config)
    remove_inactive_locale_trees(config)


if __name__ == "__main__":
    build()
