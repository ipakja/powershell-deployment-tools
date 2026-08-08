# -*- coding: utf-8 -*-
"""Apply prioritized QA fixes from Stefan's full language review."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def dedupe_about(text: str) -> str:
    """Remove accidental duplicate specialist sentences, keep one clean close."""
    patterns = [
        (
            r"(beziehe externe Fachpersonen nur nach Absprache ein\.)\s*"
            r"Externe Fachpersonen beziehe ich nur nach vorheriger Absprache ein\.",
            r"\1",
        ),
        (
            r"(involve external specialists only by agreement\.)\s*"
            r"I involve external specialists only after prior agreement\.",
            r"\1",
        ),
        (
            r"(ne fais intervenir des spécialistes externes qu’après accord\.)\s*"
            r".*",
            None,
        ),
        (
            r"(uključujem spoljne stručnjake samo uz dogovor\.)\s*"
            r"Spoljne stručnjake uključujem samo uz prethodni dogovor\.",
            r"\1",
        ),
        (
            r"(uključujem vanjske stručnjake samo uz dogovor\.)\s*"
            r"Vanjske stručnjake uključujem samo uz prethodni dogovor\.",
            r"\1",
        ),
        (
            r"(coinvolgo specialisti esterni solo previo accordo\.)\s*"
            r"Coinvolgo specialisti esterni solo previo accordo\.",
            r"\1",
        ),
    ]
    out = text
    for pattern, repl in patterns:
        if repl is None:
            continue
        out = re.sub(pattern, repl, out, flags=re.I)
    # Ensure closing contractual line once
    closers = {
        "de": " Vertragspartner bleibe ich.",
        "en": " I remain the contractual counterparty.",
        "fr": " Je reste la partie contractuelle.",
        "it": " Il partner contrattuale rimango io.",
        "sr": " Ugovorna strana ostajem ja.",
        "bs": " Ugovorna strana ostajem ja.",
        "hr": " Ugovorna strana ostajem ja.",
    }
    return out, closers


def main() -> None:
    site_path = ROOT / "config" / "site.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if "fr" not in site["paths"]["market"]["languages"]:
        langs = site["paths"]["market"]["languages"]
        # insert after en for Swiss order
        if "en" in langs:
            langs.insert(langs.index("en") + 1, "fr")
        else:
            langs.append("fr")
        site["paths"]["market"]["languages"] = langs
    site["paths"]["market"]["slugs"]["fr"] = "marche"
    site_path.write_text(
        json.dumps(site, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    pc_path = ROOT / "config" / "path_content.json"
    pc = json.loads(pc_path.read_text(encoding="utf-8"))

    # 1) Deduplicate about texts
    about_clean = {
        "de": (
            "Ich unterstütze kleine und mittlere Betriebe bei klar abgegrenzten IT- und "
            "Digitalaufgaben. Für den Schweizer B2B-Markt führe ich strukturierte "
            "Pilotmandate durch. Ich prüfe zuerst Ausgangslage, Abhängigkeiten und Grenzen "
            "und dokumentiere die vereinbarten Ergebnisse. Wenn ein Auftrag zusätzliches "
            "Fachwissen verlangt, benenne ich das vor Beginn und beziehe externe "
            "Fachpersonen nur nach Absprache ein. Vertragspartner bleibe ich."
        ),
        "en": (
            "I support small and medium-sized businesses with clearly scoped IT and digital "
            "tasks. For the Swiss B2B market, I conduct structured pilot mandates. I first "
            "assess the starting point, dependencies and limits, then document the agreed "
            "results. If an engagement requires additional expertise, I state this before "
            "work starts and involve external specialists only by agreement. I remain the "
            "contractual counterparty."
        ),
        "fr": (
            "J’accompagne les petites et moyennes entreprises pour des tâches informatiques "
            "et numériques clairement délimitées. Pour le marché B2B suisse, je mène des "
            "mandats pilotes structurés. J’examine d’abord la situation, les dépendances et "
            "les limites, puis je documente les résultats convenus. Si une mission exige une "
            "expertise supplémentaire, je l’indique avant le début et ne fais intervenir des "
            "spécialistes externes qu’après accord. Je reste la partie contractuelle."
        ),
        "it": (
            "Supporto piccole e medie imprese in compiti IT e digitali chiaramente "
            "delimitati. Per il mercato B2B svizzero conduco mandati pilota strutturati. "
            "Prima verifico situazione di partenza, dipendenze e limiti, poi documento i "
            "risultati concordati. Se un incarico richiede competenze aggiuntive, lo indico "
            "prima dell'inizio e coinvolgo specialisti esterni solo previo accordo. Il "
            "partner contrattuale rimango io."
        ),
        "sr": (
            "Podržavam mala i srednja preduzeća u jasno ograničenim IT i digitalnim "
            "zadacima. Za švajcarsko B2B tržište vodim strukturisane pilot-mandate. Prvo "
            "proveravam početnu situaciju, zavisnosti i granice, a zatim dokumentujem "
            "dogovorene rezultate. Ako mandat zahteva dodatno stručno znanje, to navodim "
            "pre početka i uključujem spoljne stručnjake samo uz dogovor. Ugovorna strana "
            "ostajem ja."
        ),
        "bs": (
            "Podržavam mala i srednja preduzeća u jasno ograničenim IT i digitalnim "
            "zadacima. Za švicarsko B2B tržište vodim strukturirane pilot-mandate. Prvo "
            "provjeravam početnu situaciju, zavisnosti i granice, a zatim dokumentujem "
            "dogovorene rezultate. Ako mandat zahtijeva dodatno stručno znanje, to navodim "
            "prije početka i uključujem vanjske stručnjake samo uz dogovor. Ugovorna strana "
            "ostajem ja."
        ),
        "hr": (
            "Podržavam mala i srednja poduzeća u jasno ograničenim IT i digitalnim "
            "zadacima. Za švicarsko B2B tržište vodim strukturirane pilot-mandate. Najprije "
            "provjeravam početno stanje, ovisnosti i granice, a zatim dokumentiram "
            "dogovorene rezultate. Ako mandat zahtijeva dodatno stručno znanje, to navodim "
            "prije početka i uključujem vanjske stručnjake samo uz dogovor. Ugovorna strana "
            "ostajem ja."
        ),
    }
    for code, text in about_clean.items():
        pc[code]["common"]["about_text"] = text

    # 5) HR city Cirih for consistency with SR/BS on this site
    for key in ("meta_title", "meta_description", "eyebrow", "pricing"):
        pass
    # fix HR hospitality city references and gateway uses locale city

    # Revenue meta wording (soft restriction in snippet)
    revenue_meta = {
        "de": (
            "Abgegrenzte IT-, Hospitality- und Revenue-Datenprüfung für KMU, Hotels und "
            "Gastronomie in Zürich."
        ),
        "en": (
            "Scoped IT, hospitality and revenue-data review for SMEs, hotels and "
            "restaurants in Zurich."
        ),
        "fr": (
            "Support informatique, hospitality et contrôle délimité des données de revenue "
            "pour PME, hôtels et restaurants à Zurich."
        ),
        "it": (
            "Supporto IT, hospitality e verifica delimitata dei dati di revenue per PMI, "
            "hotel e ristoranti a Zurigo."
        ),
        "sr": (
            "Ograničena IT i ugostiteljska podrška te provera revenue-podataka za mala i "
            "srednja preduzeća, hotele i restorane u Cirihu."
        ),
        "bs": (
            "Ograničena IT i ugostiteljska podrška te provjera revenue-podataka za mala i "
            "srednja preduzeća, hotele i restorane u Cirihu."
        ),
        "hr": (
            "Ograničena IT i ugostiteljska podrška te provjera revenue-podataka za mala i "
            "srednja poduzeća, hotele i restorane u Cirihu."
        ),
    }
    revenue_lead = {
        "de": (
            "Ich unterstütze KMU, Hotels und Gastronomiebetriebe bei konkreten Störungen, "
            "Systemfragen, digitalen Arbeitsabläufen und abgegrenzter Revenue-Datenprüfung."
        ),
        "en": (
            "I support SMEs, hotels and restaurants with specific incidents, system "
            "questions, digital workflows and scoped revenue-data review."
        ),
        "fr": (
            "J’accompagne PME, hôtels et restaurants pour des incidents précis, des "
            "questions système, des processus numériques et un contrôle délimité des "
            "données de revenue."
        ),
        "it": (
            "Supporto PMI, hotel e ristoranti con incidenti concreti, domande di sistema, "
            "flussi digitali e verifica delimitata dei dati di revenue."
        ),
        "sr": (
            "Podržavam mala i srednja preduzeća, hotele i restorane kod konkretnih smetnji, "
            "sistemskih pitanja, digitalnih tokova rada i ograničene provere "
            "revenue-podataka."
        ),
        "bs": (
            "Podržavam mala i srednja preduzeća, hotele i restorane kod konkretnih smetnji, "
            "sistemskih pitanja, digitalnih tokova rada i ograničene provjere "
            "revenue-podataka."
        ),
        "hr": (
            "Podržavam mala i srednja poduzeća, hotele i restorane kod konkretnih smetnji, "
            "sistemskih pitanja, digitalnih tijekova rada i ograničene provjere "
            "revenue-podataka."
        ),
    }
    for code in revenue_meta:
        pc[code]["hospitality"]["meta_description"] = revenue_meta[code]
        pc[code]["hospitality"]["lead"] = revenue_lead[code]
        # keep body item wording with "anhand gelieferter Daten"
        if code == "hr":
            pc[code]["hospitality"]["meta_title"] = (
                "Digitalne usluge i ugostiteljstvo Cirih | BIT"
            )
            pc[code]["hospitality"]["eyebrow"] = (
                "Digitalne usluge i ugostiteljstvo · Cirih"
            )
            # pricing travel line
            pc[code]["hospitality"]["pricing"] = [
                item.replace("Züricha", "Ciriha").replace("Zürich", "Cirih")
                for item in pc[code]["hospitality"]["pricing"]
            ]

    # 2) French market page
    pc["fr"]["market"] = {
        "meta_title": "Pilote suisse pour le développement de marché B2B | BIT",
        "meta_description": (
            "Six semaines de validation structurée du marché pour une offre B2B "
            "clairement définie en Suisse."
        ),
        "eyebrow": "Développement du marché suisse",
        "title": "Du contrôle de documents au pilote marché suisse.",
        "lead": (
            "J’examine avec vous si et comment une offre clairement définie peut être "
            "positionnée et testée auprès d’entreprises suisses sélectionnées."
        ),
        "nav": ["Contrôle de documents", "Prix", "Limites"],
        "document_title": "Contrôle de documents",
        "document_text": (
            "Votre offre, profil de capacité ou texte d’entreprise en allemand "
            "commercial suisse. {small_job} par document, 5 jours ouvrables, un cycle "
            "de corrections."
        ),
        "pilot_eyebrow": "Deuxième étape",
        "pilot_title": "Le pilote de six semaines",
        "pilot_intro": (
            "Le pilote est un mandat de validation délimité avec des résultats "
            "documentés."
        ),
        "deliverables": [
            (
                "Entretien de démarrage et délimitation écrite de l’offre, du segment "
                "cible et des hypothèses"
            ),
            (
                "Examen du positionnement, de l’argumentaire de valeur, de la logique "
                "tarifaire et des documents existants"
            ),
            "Liste motivée d’entreprises cibles et d’interlocuteurs adaptés",
            (
                "Premier contact convenu au nom de BIT ; représentation uniquement avec "
                "mandat écrit explicite"
            ),
            "Documentation hebdomadaire des activités, réponses et questions ouvertes",
            (
                "Rapport final avec observations et une recommandation sobre pour la "
                "suite"
            ),
        ],
        "pricing": [
            "Contrôle de documents : {small_job} par document",
            "Prix fixe du pilote : {pilot}",
            "Paiement du pilote : 50 % à la commande, 50 % après le rapport final",
        ],
        "optional_title": "Optionnel après le pilote",
        "optional": (
            "Un mandat suivant n’est convenu qu’avec un intérêt mutuel, un périmètre "
            "écrit et une rémunération séparée. Je fais intervenir des spécialistes "
            "externes uniquement après accord préalable. Je reste la partie "
            "contractuelle."
        ),
        "exclusions": [
            (
                "Aucun engagement de clients, de chiffre d’affaires, de contrats ou de "
                "succès commercial"
            ),
            "Aucun conseil juridique, fiscal, douanier ou de certification",
            (
                "Aucun pouvoir de représentation, de conclusion de contrats ou "
                "d’encaissement sans mandat écrit explicite"
            ),
            (
                "Frais de déplacement, traductions ou prestations de tiers non inclus "
                "dans le prix fixe"
            ),
        ],
        "honesty": (
            "Le pilote n’utilise aucune preuve de succès inventée et ne crée pas de "
            "demande de marché. Il fournit une base documentée pour décider ; un "
            "résultat négatif motivé est aussi un résultat utile."
        ),
    }

    pc_path.write_text(
        json.dumps(pc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # 3+4 legal activity + entity type localization
    legal_updates = {
        "de": {
            "activity": (
                "Schweizer Marktentwicklung und Vertretung auf Grundlage eines "
                "schriftlichen Mandats sowie IT-Support und digitale Unterstützung für "
                "KMU und Hospitality."
            ),
            "entity_type": "Einzelfirma",
            "city": "Zürich",
        },
        "en": {
            "activity": (
                "Swiss market development and representation on the basis of a written "
                "mandate, as well as IT support and digital assistance for SMEs and "
                "hospitality."
            ),
            "entity_type": "sole proprietorship (Einzelfirma under Swiss law)",
            "city": "Zurich",
        },
        "fr": {
            "activity": (
                "Développement du marché suisse et représentation sur la base d’un "
                "mandat écrit, ainsi que support IT et assistance numérique pour les "
                "PME et l’hospitality."
            ),
            "entity_type": "entreprise individuelle (Einzelfirma selon le droit suisse)",
            "city": "Zurich",
        },
        "it": {
            "activity": (
                "Sviluppo del mercato svizzero e rappresentanza sulla base di un mandato "
                "scritto, nonché supporto IT e assistenza digitale per PMI e hospitality."
            ),
            "entity_type": "ditta individuale (Einzelfirma secondo il diritto svizzero)",
            "city": "Zurigo",
        },
        "sr": {
            "activity": (
                "Razvoj švajcarskog tržišta i zastupanje na osnovu pisanog mandata, kao i "
                "IT podrška i digitalna pomoć za mala i srednja preduzeća i ugostiteljstvo."
            ),
            "entity_type": "samostalna delatnost (Einzelfirma po švajcarskom pravu)",
            "city": "Cirih",
        },
        "bs": {
            "activity": (
                "Razvoj švicarskog tržišta i zastupanje na osnovu pisanog mandata, kao i "
                "IT podrška i digitalna pomoć za mala i srednja preduzeća i ugostiteljstvo."
            ),
            "entity_type": "samostalna djelatnost (Einzelfirma po švicarskom pravu)",
            "city": "Cirih",
        },
        "hr": {
            "activity": (
                "Razvoj švicarskog tržišta i zastupanje na temelju pisanog mandata, kao i "
                "IT podrška i digitalna pomoć za mala i srednja poduzeća i ugostiteljstvo."
            ),
            "entity_type": "samostalna djelatnost (Einzelfirma po švicarskom pravu)",
            "city": "Cirih",
        },
    }
    for code, updates in legal_updates.items():
        path = ROOT / "locales" / f"{code}.json"
        loc = json.loads(path.read_text(encoding="utf-8"))
        loc["legal_page"]["activity"] = updates["activity"]
        loc["legal_page"]["entity_type"] = updates["entity_type"]
        loc["legal_page"]["city"] = updates["city"]
        # about lead for it had bare Einzelfirma
        if code == "it":
            pc2 = json.loads(pc_path.read_text(encoding="utf-8"))
            pc2["it"]["common"]["about_lead"] = (
                "Sono Stefan Bogdanovic e gestisco BIT come ditta individuale "
                "(Einzelfirma) a Zurigo."
            )
            pc_path.write_text(
                json.dumps(pc2, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        if code == "hr":
            loc["footer"]["location"] = "Cirih, Švicarska"
        path.write_text(
            json.dumps(loc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    # 6) www -> apex redirect for Cloudflare Pages
    redirects = ROOT / "_redirects"
    current = redirects.read_text(encoding="utf-8")
    host_rules = (
        "\n# Force non-www on Cloudflare Pages\n"
        "https://www.boksitsupport.ch/* https://boksitsupport.ch/:splat 301\n"
        "http://www.boksitsupport.ch/* https://boksitsupport.ch/:splat 301\n"
    )
    if "www.boksitsupport.ch" not in current:
        redirects.write_text(current.rstrip() + "\n" + host_rules, encoding="utf-8")

    print("QA fixes applied")
    print("market langs", site["paths"]["market"]["languages"])
    print("market slugs", site["paths"]["market"]["slugs"])


if __name__ == "__main__":
    main()
