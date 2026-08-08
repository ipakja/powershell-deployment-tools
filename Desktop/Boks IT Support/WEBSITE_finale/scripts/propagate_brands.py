# -*- coding: utf-8 -*-
"""Propagate gateway brands to match Hospitality + Market masters."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GATEWAY = {
    "de": {
        "meta_title": "BIT – IT & Hospitality und Market Access Switzerland",
        "meta_description": (
            "Zwei getrennte Leistungsbereiche: IT & Hospitality für Schweizer Betriebe "
            "sowie BIT Market Access Switzerland für internationale Anbieter."
        ),
        "hospitality_title": "IT & Hospitality",
        "market_title": "BIT Market Access Switzerland",
    },
    "en": {
        "meta_title": "BIT – IT & Hospitality and Market Access Switzerland",
        "meta_description": (
            "Two separate service areas: IT & Hospitality for Swiss businesses and "
            "BIT Market Access Switzerland for international providers."
        ),
        "hospitality_title": "IT & Hospitality",
        "market_title": "BIT Market Access Switzerland",
    },
    "fr": {
        "meta_title": "BIT – IT & Hospitality et Market Access Switzerland",
        "meta_description": (
            "Deux domaines distincts : IT & Hospitality pour les entreprises suisses "
            "et BIT Market Access Switzerland pour les prestataires internationaux."
        ),
        "hospitality_title": "IT & Hospitality",
        "market_title": "BIT Market Access Switzerland",
    },
    "it": {
        "meta_title": "BIT – IT & Hospitality e Market Access Switzerland",
        "meta_description": (
            "Due ambiti distinti: IT & Hospitality per imprese svizzere e "
            "BIT Market Access Switzerland per fornitori internazionali."
        ),
        "hospitality_title": "IT & Hospitality",
        "market_title": "BIT Market Access Switzerland",
    },
    "sr": {
        "meta_title": "BIT – IT i ugostiteljstvo i Market Access Switzerland",
        "meta_description": (
            "Dve odvojene oblasti usluga: IT i ugostiteljstvo za švajcarske firme "
            "i BIT Market Access Switzerland za međunarodne ponuđače."
        ),
        "hospitality_title": "IT i ugostiteljstvo",
        "market_title": "BIT Market Access Switzerland",
    },
    "bs": {
        "meta_title": "BIT – IT i ugostiteljstvo i Market Access Switzerland",
        "meta_description": (
            "Dvije odvojene oblasti usluga: IT i ugostiteljstvo za švicarske firme "
            "i BIT Market Access Switzerland za međunarodne ponuđače."
        ),
        "hospitality_title": "IT i ugostiteljstvo",
        "market_title": "BIT Market Access Switzerland",
    },
    "hr": {
        "meta_title": "BIT – IT i ugostiteljstvo i Market Access Switzerland",
        "meta_description": (
            "Dva odvojena područja usluga: IT i ugostiteljstvo za švicarske tvrtke "
            "i BIT Market Access Switzerland za međunarodne ponuđače."
        ),
        "hospitality_title": "IT i ugostiteljstvo",
        "market_title": "BIT Market Access Switzerland",
    },
}


def main() -> None:
    path = ROOT / "config" / "path_content.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for code, payload in GATEWAY.items():
        data["gateway"][code].update(payload)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    site_path = ROOT / "config" / "site.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    site["brand"] = "BIT – IT & Hospitality · Market Access Switzerland"
    site_path.write_text(json.dumps(site, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Gateway brands + schema alternateName aligned.")


if __name__ == "__main__":
    main()
