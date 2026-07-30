"""Build the localized two-path static website."""
from __future__ import annotations

import html
import json
from pathlib import Path
from string import Template
from typing import Any, Iterable
from xml.etree import ElementTree

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
        links = []
        for code in languages:
            href = (
                self.route(path_key, code)
                if path_key
                else f"/{code}/{suffix}"
            )
            current_attr = ' aria-current="page"' if code == current else ""
            links.append(
                f'                <a href="{href}"{current_attr}>'
                f'{escape(self.language_map[code]["label"])}</a>'
            )
        return "\n".join(links)

    def alternate_links(self, path_key: str | None, suffix: str = "") -> str:
        """Render only existing localized alternates."""
        if path_key:
            languages = self.config["paths"][path_key]["languages"]
            route = lambda code: self.route(path_key, code)
        else:
            languages = list(registered_languages(self.config))
            route = lambda code: f"/{code}/{suffix}"
        links = [
            f'    <link rel="alternate" hreflang="{self.language_map[code]["hreflang"]}" '
            f'href="{self.config["base_url"]}{route(code)}">'
            for code in languages
        ]
        default = "de" if "de" in languages else languages[0]
        links.append(
            f'    <link rel="alternate" hreflang="x-default" '
            f'href="{self.config["base_url"]}{route(default)}">'
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
            primary = entry + pilot
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
            "whatsapp_label": escape(common["whatsapp"]),
            "viber_label": escape(common["viber"]),
            "email_label": escape(common["email"]),
            "whatsapp_url": escape(self.config["contact"]["whatsapp_url"]),
            "viber_url": escape(self.config["contact"]["viber_url"]),
            "email": escape(self.config["contact"]["email"]),
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
            about_text=escape(common["about_text"]),
            about_independent=escape(common["about_independent"]),
            image_alt=escape(common["image_alt"]), back=escape(common["back"]),
            location=escape(locale["footer"]["location"]),
            legal_label=escape(common["legal"]),
        )

    def render_legal(self, language: str) -> str:
        """Render shared legal/privacy page with factual Swiss details."""
        locale = self.locales[language]
        legal = locale["legal_page"]
        common = self.content[language]["common"]
        address = self.config["address"]
        contact = self.config["contact"]
        privacy = f'{legal["privacy"]} {legal["privacy_messaging"]}'
        context = {
            "html_lang": escape(locale["lang"]), "language": language,
            "canonical": f'{self.config["base_url"]}/{language}/legal/',
            "alternate_links": self.alternate_links(None, "legal/"),
            "language_links": self.language_links(
                language, list(registered_languages(self.config)), suffix="legal/"
            ),
            "nav_languages": escape(common["languages"]),
            "legal_title": escape(legal["title"]), "legal_eyebrow": escape(legal["eyebrow"]),
            "legal_lead": escape(legal["lead"]), "legal_meta_description": escape(legal["lead"]),
            "legal_back": escape(common["back"]),
            "legal_provider_title": escape(legal["provider_title"]),
            "legal_provider_name": (
                f'{escape(self.personal_name(language))} · '
                f'BIT – Boks IT Support · {escape(legal["entity_type"])}'
            ),
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
            "liability": escape(legal["liability"].replace("Garantie", "Zusicherung").replace("guarantee", "assurance")),
            "copyright_title": escape(legal["copyright_title"]),
            "copyright": escape(legal["copyright"]),
            "privacy_title": escape(legal["privacy_title"]), "privacy": escape(privacy),
            "jurisdiction_title": escape(legal["jurisdiction_title"]),
            "jurisdiction": escape(legal["jurisdiction"]),
            "legal_updated": escape(legal["updated"]),
            "phone_href": escape(contact["phone_href"]),
            "phone_display": escape(contact["phone_display"]),
            "email": escape(contact["email"]),
            "footer_location": escape(locale["footer"]["location"]),
            "footer_legal": escape(common["legal"]), "footer_privacy": escape(legal["privacy_title"]),
        }
        return self.templates.get("legal.html").substitute(context)


def write_sitemap(config: dict[str, Any]) -> None:
    """Generate a sitemap containing only real output routes."""
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ElementTree.register_namespace("", namespace)
    urlset = ElementTree.Element(f"{{{namespace}}}urlset")
    routes = ["/"]
    routes.extend(f"/{code}/" for code in registered_languages(config))
    for path_data in config["paths"].values():
        routes.extend(
            f'/{code}/{path_data["slugs"][code]}/'
            for code in path_data["languages"]
        )
    for code in registered_languages(config):
        routes.extend((f"/{code}/about/", f"/{code}/legal/"))
    for route in routes:
        entry = ElementTree.SubElement(urlset, f"{{{namespace}}}url")
        ElementTree.SubElement(entry, f"{{{namespace}}}loc").text = (
            config["base_url"] + route
        )
        ElementTree.SubElement(entry, f"{{{namespace}}}lastmod").text = "2026-07-30"
    tree = ElementTree.ElementTree(urlset)
    ElementTree.indent(tree, space="  ")
    tree.write(ROOT / "sitemap.xml", encoding="utf-8", xml_declaration=True)


def build() -> None:
    """Build all localized routes."""
    config = load_config()
    locales = load_locales(config)
    renderer = SiteRenderer(config, locales, TemplateRepository())
    write_text(ROOT / "index.html", renderer.render_gateway("de", root=True))
    for language in registered_languages(config):
        write_text(ROOT / language / "index.html", renderer.render_gateway(language))
        write_text(
            ROOT / language / "about" / "index.html", renderer.render_about(language)
        )
        write_text(
            ROOT / language / "legal" / "index.html", renderer.render_legal(language)
        )
    for path_key, path_data in config["paths"].items():
        for language in path_data["languages"]:
            slug = path_data["slugs"][language]
            write_text(
                ROOT / language / slug / "index.html",
                renderer.render_service(path_key, language),
            )
    write_sitemap(config)


if __name__ == "__main__":
    build()
