# -*- coding: utf-8 -*-
"""Align legal form wording, about practice, contact labels, redirects."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ENTITY = {
    "de": "Rechtsform beziehungsweise selbstständiger Status wird derzeit geklärt",
    "en": "Legal form / self-employed status is currently being clarified",
    "fr": "La forme juridique / le statut d’indépendant est actuellement en cours de clarification",
    "it": "La forma giuridica / lo status di indipendente è attualmente in chiarimento",
    "sr": "Pravni oblik, odnosno status samostalne delatnosti, trenutno se razjašnjava",
    "bs": "Pravni oblik, odnosno status samostalne djelatnosti, trenutno se razjašnjava",
    "hr": "Pravni oblik, odnosno status samostalne djelatnosti, trenutačno se razjašnjava",
}

PHONE = {
    "de": "Anrufen",
    "en": "Call",
    "fr": "Appeler",
    "it": "Chiama",
    "sr": "Pozovi",
    "bs": "Nazovi",
    "hr": "Nazovi",
}

ABOUT_PRACTICE = {
    "de": (
        "Ich kenne operative Abläufe zwischen Rezeption, Reservierungen, Abrechnung und "
        "Hotelsystemen aus der Schweizer Praxis. Ergänzend unterstütze ich kleine Teams "
        "bei Microsoft 365, Geräten und Benutzerzugängen. Von Zürich aus arbeite ich auf "
        "Deutsch, Englisch sowie Serbisch, Bosnisch und Kroatisch und verbinde Schweizer "
        "Betriebsrealität mit dem südosteuropäischen Markt."
    ),
    "en": (
        "I know operational workflows between reception, reservations, billing and hotel "
        "systems from Swiss practice. I also support small teams with Microsoft 365, "
        "devices and user access. From Zurich I work in German, English and Serbian, "
        "Bosnian and Croatian, connecting Swiss operating reality with the South-East "
        "European market."
    ),
    "fr": (
        "Je connais les processus opérationnels entre réception, réservations, facturation "
        "et systèmes hôteliers issus de la pratique suisse. J’accompagne aussi de petites "
        "équipes pour Microsoft 365, appareils et accès utilisateurs. Depuis Zurich, je "
        "travaille en allemand, anglais ainsi qu’en serbe, bosniaque et croate, et je "
        "relie la réalité opérationnelle suisse au marché d’Europe du Sud-Est."
    ),
    "it": (
        "Conosco i flussi operativi tra reception, prenotazioni, fatturazione e sistemi "
        "alberghieri dalla pratica svizzera. Supporto anche piccoli team con Microsoft 365, "
        "dispositivi e accessi utente. Da Zurigo lavoro in tedesco, inglese nonché serbo, "
        "bosniaco e croato, collegando la realtà operativa svizzera al mercato "
        "dell’Europa sud-orientale."
    ),
    "sr": (
        "Poznajem operativne tokove između recepcije, rezervacija, obračuna i hotelskih "
        "sistema iz švajcarske prakse. Pored toga pomažem malim timovima oko Microsoft 365, "
        "uređaja i korisničkih pristupa. Iz Ciriha radim na nemačkom, engleskom i srpskom, "
        "bosanskom i hrvatskom i povezujem švajcarsku poslovnu realnost sa "
        "jugoistočnoevropskim tržištem."
    ),
    "bs": (
        "Poznajem operativne tokove između recepcije, rezervacija, obračuna i hotelskih "
        "sistema iz švicarske prakse. Pored toga pomažem malim timovima oko Microsoft 365, "
        "uređaja i korisničkih pristupa. Iz Ciriha radim na njemačkom, engleskom i srpskom, "
        "bosanskom i hrvatskom i povezujem švicarsku poslovnu realnost sa "
        "jugoistočnoevropskim tržištem."
    ),
    "hr": (
        "Poznajem operativne tokove između recepcije, rezervacija, obračuna i hotelskih "
        "sustava iz švicarske prakse. Osim toga pomažem malim timovima oko Microsoft 365, "
        "uređaja i korisničkih pristupa. Iz Ciriha radim na njemačkom, engleskom te srpskom, "
        "bosanskom i hrvatskom i povezujem švicarsku poslovnu stvarnost s "
        "jugoistočnoeuropskim tržištem."
    ),
}


def main() -> None:
    pc_path = ROOT / "config" / "path_content.json"
    pc = json.loads(pc_path.read_text(encoding="utf-8"))
    for code, text in ABOUT_PRACTICE.items():
        pc[code]["common"]["about_practice"] = text
        pc[code]["common"]["phone"] = PHONE[code]
    # Soften mini-scope phrasing in BS/HR special-task steps if present.
    for code, old, new in [
        (
            "bs",
            "uz poseban mini-obim",
            "uz zasebno, pismeno dogovoren dodatni obim",
        ),
        (
            "hr",
            "uz poseban mini-opseg",
            "uz zasebno, pisano dogovoren dodatni opseg",
        ),
        (
            "de",
            "separaten Mini-Umfang",
            "separat vereinbarten Zusatzauftrag",
        ),
    ]:
        for step in pc[code]["hospitality"]["process"]["steps"]:
            step["text"] = step["text"].replace(old, new)
    pc_path.write_text(json.dumps(pc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for code, entity in ENTITY.items():
        loc_path = ROOT / "locales" / f"{code}.json"
        locale = json.loads(loc_path.read_text(encoding="utf-8"))
        locale["legal_page"]["entity_type"] = entity
        loc_path.write_text(
            json.dumps(locale, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    redirects = """# Canonical multilingual structure
/index.html /de/ 301
/index_en /en/ 301
/index_en.html /en/ 301
/index-en.html /en/ 301
/en.html /en/ 301

# Legacy German routes
/services /de/hospitality/ 301
/services.html /de/hospitality/ 301
/packages /de/hospitality/ 301
/packages.html /de/hospitality/ 301
/it-matrix /de/hospitality/ 301
/it-matrix.html /de/hospitality/ 301
/kontakt /de/hospitality/#contact 301
/kontakt.html /de/hospitality/#contact 301
/rechtliches /de/legal/ 301
/legal /de/legal/ 301
/legal.html /de/legal/ 301

# Legacy English routes
/services-en /en/hospitality/ 301
/services-en.html /en/hospitality/ 301
/packages-en /en/hospitality/ 301
/packages-en.html /en/hospitality/ 301
/it-matrix-en /en/hospitality/ 301
/it-matrix-en.html /en/hospitality/ 301
/kontakt-en /en/hospitality/#contact 301
/kontakt-en.html /en/hospitality/#contact 301
/legal-en /en/legal/ 301
/legal-en.html /en/legal/ 301

# Force non-www on Cloudflare Pages
https://www.boksitsupport.ch/* https://boksitsupport.ch/:splat 301
http://www.boksitsupport.ch/* https://boksitsupport.ch/:splat 301
"""
    (ROOT / "_redirects").write_text(redirects, encoding="utf-8")
    print("Content + redirects updated.")


if __name__ == "__main__":
    main()
