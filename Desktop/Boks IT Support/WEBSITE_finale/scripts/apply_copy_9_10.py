# -*- coding: utf-8 -*-
"""Apply copy/positioning polish 9/10 to DE/EN configs and legal locales."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict:
    """Load JSON object from path."""
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    """Write JSON with stable formatting."""
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")


def patch_de(de: dict) -> None:
    """Apply German marketing copy updates."""
    de["home"]["why_bit"]["items"] = [
        "Ein zentraler Servicezugang statt mehrerer paralleler Anbieterkontakte",
        "Klarer Leistungsumfang vor dem Start",
        "Dokumentierter Ablauf von Anfrage bis Abschluss",
        "Fachkompetenz nach Bedarf innerhalb des BIT-Service",
        "Passender Leistungsumfang für kleinere Unternehmen ohne interne IT",
        "BIT bleibt Vertragspartner und steuert Qualität und Abrechnung",
    ]
    de["home"]["partner"] = {
        "title": "Sie beauftragen BIT – nicht mehrere Anbieter",
        "text": (
            "Sie beauftragen den definierten Service bei BIT. Wenn Spezialkompetenz erforderlich ist, "
            "koordiniert BIT diese innerhalb des vereinbarten Service und bleibt bis zum dokumentierten "
            "Abschluss Ihr Ansprechpartner. Zusätzliche Kosten werden vorab ausgewiesen und nur nach "
            "Ihrer Freigabe ausgelöst."
        ),
    }

    de["services"]["intro"] = (
        "Drei klar definierte Services für wiederkehrende Benutzer-, Zugangs- und Arbeitsplatzaufgaben. "
        "Remote ist der Normalweg; Termine vor Ort im Raum Zürich werden vorab vereinbart und im Angebot "
        "separat ausgewiesen."
    )
    de["services"]["scope_note"] = "Umfang und Zuständigkeit werden vorab vereinbart."

    c0 = de["services"]["cards"][0]
    c0["what"] = (
        "BIT setzt definierte Benutzer- und Zugangsprozesse strukturiert um und koordiniert die "
        "erforderlichen Freigaben."
    )
    c0["text"] = (
        "BIT setzt definierte Benutzer- und Zugangsprozesse strukturiert um und koordiniert die "
        "erforderlichen Freigaben. Am Ende: Übersicht der bearbeiteten und offenen Punkte."
    )
    c0["detail"]["boundaries"] = (
        "Technische Spezialfälle ausserhalb des vereinbarten Umfangs werden vor Beginn geprüft. "
        "Keine 24/7-Bereitschaft und kein unbegrenzter Leistungsumfang. "
        "BIT ersetzt keine interne IT-Abteilung und übernimmt keine unbegrenzten Pauschalaufträge. "
        "Vor Auftragsannahme prüft BIT die Machbarkeit des angefragten Service."
    )

    c1 = de["services"]["cards"][1]
    c1["what"] = (
        "BIT bearbeitet und koordiniert standardisierte Microsoft-365- und Arbeitsplatzfälle – "
        "etwa Anmeldung, Outlook, Teams und typische Arbeitsplatzblockaden."
    )
    c1["text"] = c1["what"]
    c1["outcome"] = (
        "Am Ende erhalten Sie ein dokumentiertes Ergebnis und eine klare Übersicht offener Punkte."
    )
    c1["detail"]["intro"] = (
        "Wenn Anmeldung, Outlook oder Teams an einem Arbeitsplatz stocken, kostet das sofort Arbeitszeit. "
        "BIT grenzt ein, ob Konto, Gerät oder Dienst betroffen ist, und bearbeitet klar abgegrenzte "
        "Standardfälle. Ergebnis zuerst: weniger Unterbruch und ein fester Ansprechpartner bis zum "
        "dokumentierten Abschluss. Remote ist der Normalweg; Vor-Ort-Termine im Raum Zürich nur nach "
        "Vereinbarung und separat im Angebot."
    )

    de["limits"]["items"] = [
        "keine 24/7-Störungsbereitschaft",
        "keine unbegrenzten Support-Pauschalen",
        "zusätzliche Leistungen nur nach vorheriger Abstimmung und Freigabe",
    ]

    for ex in de["process"]["extras"]:
        if ex["title"] == "Zusatzaufwand":
            ex["text"] = (
                "Zusätzlicher Spezialaufwand wird vorab ausgewiesen und nur nach Ihrer Freigabe ausgeführt."
            )
        if ex["title"] == "Dokumentierter Abschluss":
            ex["text"] = (
                "Am Ende erhalten Sie ein nachvollziehbares Ergebnis mit erledigten Punkten, offenen "
                "Punkten und – falls erforderlich – empfohlenen nächsten Schritten."
            )

    de["audience"]["services"] = [
        "Benutzer-Onboarding und Offboarding",
        "Konten, Rollen und Zugangsänderungen",
        "Microsoft-365- und Arbeitsplatzservices",
        "Koordination spezialisierter Facharbeit bei Bedarf",
        "Dokumentation und Nachverfolgung",
    ]
    de["audience"]["nofit_note"] = (
        "Vor Auftragsannahme prüft BIT die Machbarkeit des angefragten Service. "
        "Zusätzliche Spezialleistungen können bei Bedarf innerhalb des BIT-Service koordiniert werden."
    )
    de["role"]["owns"] = (
        "Aufnahme, Servicekoordination, Qualitätskontrolle, Kommunikation, Dokumentation und Abschluss."
    )
    de["role"]["tech"] = (
        "BIT prüft vor Auftragsannahme die Machbarkeit. Falls Spezialkompetenz erforderlich ist, "
        "wird diese innerhalb des vereinbarten BIT-Service koordiniert. BIT bleibt Ihr zentraler "
        "Ansprechpartner."
    )
    de["examples"] = {
        "title": "Typische Servicefälle",
        "note": "Illustrative Musterabläufe – keine Kundenreferenzen – finden Sie auf der Beispielseite.",
        "cta": "Typische Fälle ansehen",
        "href": "/de/beispiele/",
        "items": [],
    }

    de["about"]["body"] = [
        (
            "Ich kenne operative Abläufe aus Hotel- und Rezeptionsumfeld: Benutzerwechsel, Zugänge, "
            "Übergaben, Verantwortlichkeiten sowie alltägliche Arbeitsplatz- und Systemfragen kleiner Betriebe."
        ),
        (
            "BIT ist ein inhabergeführter Serviceanbieter in Zürich. Als Inhaber verantworte ich Aufnahme, "
            "Koordination, Qualität und dokumentierten Abschluss der beauftragten Services und bleibe von "
            "der Anfrage bis zum Abschluss Ihr zentraler Ansprechpartner."
        ),
        "Arbeitssprachen: Deutsch und Englisch.",
    ]
    de["about"]["credentials_title"] = "Qualifikationen"

    de["faq"]["items"] = [
        {
            "q": "Für welche Unternehmen ist BIT gedacht?",
            "a": (
                "Für kleinere Unternehmen mit ca. 5–50 Mitarbeitenden ohne eigene interne IT, "
                "überwiegend Windows und Microsoft 365 – Zürich und remote in der Schweiz."
            ),
        },
        {
            "q": "Ersetzt BIT eine eigene IT-Abteilung?",
            "a": (
                "BIT ist für kleinere Unternehmen gedacht, die keine eigene interne IT benötigen, aber "
                "für definierte Benutzer-, Zugangs- und Arbeitsplatzservices einen zentralen "
                "Ansprechpartner brauchen."
            ),
        },
        {
            "q": "Können alle IT-Probleme übernommen werden?",
            "a": (
                "Nein. BIT konzentriert sich auf Benutzer-, Zugangs-, Microsoft-365- und standardisierte "
                "Arbeitsplatzservices. Bei komplexeren Spezialthemen prüft BIT vorab, ob diese innerhalb "
                "des Service übernommen oder koordiniert werden können."
            ),
        },
        {
            "q": "Arbeitet BIT nur mit Hotels?",
            "a": (
                "Nein. Hotel und Rezeption sind Teil des operativen Erfahrungshintergrunds. Das Angebot "
                "richtet sich branchenübergreifend an kleinere Schweizer Unternehmen ohne interne IT."
            ),
        },
        {
            "q": "Wer führt technische Änderungen aus?",
            "a": (
                "BIT verantwortet den beauftragten Service und bleibt Ihr Ansprechpartner. Standardisierte "
                "Aufgaben werden innerhalb des BIT-Service umgesetzt. Wenn Spezialkompetenz erforderlich "
                "ist, koordiniert BIT geeignete Facharbeit innerhalb des vereinbarten Auftrags."
            ),
        },
        {
            "q": "Wie werden Zugangsänderungen freigegeben?",
            "a": (
                "Zugangs- und Berechtigungsänderungen erfolgen nur nach Freigabe einer vom Unternehmen "
                "autorisierten Person."
            ),
        },
        {
            "q": "Gibt es feste Pakete oder Preise?",
            "a": (
                "Der IT-Basischeck startet bei CHF 190. Weitere Leistungen werden je nach Umfang als "
                "Festpreis, wiederkehrender Service oder bei zusätzlichem Spezialaufwand nach vorheriger "
                "Freigabe angeboten. Vor Beginn erhalten Sie den vereinbarten Umfang und Preis. Remote "
                "ist der Standard; Vor-Ort-Termine im Raum Zürich werden separat vereinbart."
            ),
        },
        {
            "q": "Wie schnell reagiert BIT?",
            "a": (
                "In der Regel erhalten Sie innerhalb von zwei Arbeitstagen eine erste Rückmeldung mit "
                "einer Einschätzung zu Machbarkeit und nächstem Schritt."
            ),
        },
        {
            "q": "Muss unsere IT bereits dokumentiert sein?",
            "a": (
                "Nein. Gerade wenn Benutzer, Zugänge oder Zuständigkeiten nicht vollständig dokumentiert "
                "sind, kann der IT-Basischeck als Ausgangspunkt dienen."
            ),
        },
    ]

    de["examples_page"]["title"] = "Typische Servicefälle"
    de["ui"]["special_line"] = "zusätzlicher Spezialaufwand nur nach vorheriger Freigabe"
    de["ui"]["hourly_line"] = "Richtwert bei separat abgerechnetem Sonderaufwand: CHF 120/h"
    de["ui"]["travel_line"] = (
        "Remote ist der Standard. Vor-Ort-Termine im Raum Zürich werden vorab vereinbart und separat "
        "ausgewiesen."
    )


def patch_en(en: dict) -> None:
    """Apply English marketing copy updates."""
    en["home"]["why_bit"]["items"] = [
        "One central service entry instead of multiple parallel vendor contacts",
        "Clear scope before work starts",
        "Documented process from inquiry to close-out",
        "Specialist expertise when required within the BIT service",
        "A fitting scope for smaller businesses without in-house IT",
        "BIT remains the contractual partner and steers quality and billing",
    ]
    en["home"]["partner"] = {
        "title": "You engage BIT — not multiple providers",
        "text": (
            "You commission the defined service from BIT. When specialist expertise is required, BIT "
            "coordinates it within the agreed service and remains your contact through to documented "
            "completion. Additional costs are stated up front and only triggered after your approval."
        ),
    }

    en["services"]["intro"] = (
        "Three clearly defined services for recurring user, access and workplace tasks. "
        "Remote is the default; Zurich-area on-site appointments are agreed in advance and listed "
        "separately in the quote."
    )
    en["services"]["scope_note"] = "Scope and responsibility are agreed up front."

    c0 = en["services"]["cards"][0]
    c0["what"] = (
        "BIT implements defined user and access processes in a structured way and coordinates the "
        "required approvals."
    )
    c0["text"] = (
        "BIT implements defined user and access processes in a structured way and coordinates the "
        "required approvals. Outcome: an overview of handled and open points."
    )
    c0["detail"]["boundaries"] = (
        "Specialist technical cases outside the agreed scope are reviewed before work starts. "
        "No 24/7 cover and no unlimited scope. BIT does not replace an internal IT department and "
        "does not take unlimited retainer work. Before accepting an engagement, BIT reviews whether "
        "the requested service is feasible."
    )

    c1 = en["services"]["cards"][1]
    c1["what"] = (
        "BIT handles and coordinates standardised Microsoft 365 and workplace cases — "
        "for example sign-in, Outlook, Teams and typical workplace blockers."
    )
    c1["text"] = c1["what"]
    c1["outcome"] = "At the end you receive a documented result and a clear overview of open points."
    c1["detail"]["intro"] = (
        "When sign-in, Outlook or Teams stalls at a workstation, work time is lost immediately. "
        "BIT narrows whether the account, device or service is affected and handles clearly scoped "
        "standard cases. Result first: less disruption and one contact through to documented close-out. "
        "Remote is the default; Zurich-area on-site visits only by agreement and listed separately."
    )

    en["limits"]["items"] = [
        "no 24/7 incident cover",
        "no unlimited support retainers",
        "additional services only after prior alignment and approval",
    ]

    for ex in en["process"]["extras"]:
        if ex["title"] == "Extra effort":
            ex["text"] = (
                "Additional special effort is stated up front and only carried out after your approval."
            )
        if ex["title"] == "Documented close-out":
            ex["text"] = (
                "At the end you receive a clear outcome with completed items, open points and — where "
                "needed — recommended next steps."
            )

    en["audience"]["services"] = [
        "employee onboarding and offboarding",
        "user accounts, roles and access changes",
        "Microsoft 365 and workplace services",
        "coordination of specialist work when required",
        "documentation and follow-up",
    ]
    en["audience"]["nofit_note"] = (
        "Before accepting an engagement, BIT reviews whether the requested service is feasible. "
        "Additional specialist services may be coordinated inside the BIT service when needed."
    )
    en["role"]["owns"] = (
        "Intake, service coordination, quality control, communication, documentation and close-out."
    )
    en["role"]["tech"] = (
        "Before accepting an engagement, BIT reviews feasibility. If specialist expertise is required, "
        "it is coordinated within the agreed BIT service. BIT remains your central contact."
    )
    en["examples"] = {
        "title": "Typical service cases",
        "note": "Illustrative sample flows — not client references — are on the examples page.",
        "cta": "View typical cases",
        "href": "/en/examples/",
        "items": [],
    }

    en["about"]["body"] = [
        (
            "I know day-to-day operations from hotel and front-desk environments: user changes, access, "
            "handovers, ownership and everyday workplace and system questions in small businesses."
        ),
        (
            "BIT is an owner-led service provider in Zurich. As owner I am responsible for intake, "
            "coordination, quality and documented close-out of commissioned services, and I remain your "
            "central contact from inquiry through to completion."
        ),
        "Working languages: German and English.",
    ]
    en["about"]["credentials_title"] = "Qualifications"

    en["faq"]["items"] = [
        {
            "q": "Which companies is BIT for?",
            "a": (
                "Smaller companies with about 5–50 employees without in-house IT, mostly on Windows and "
                "Microsoft 365 — Zurich and remote across Switzerland."
            ),
        },
        {
            "q": "Does BIT replace an in-house IT department?",
            "a": (
                "BIT is for smaller companies that do not need a full internal IT role, but want one "
                "central contact for defined user, access and workplace services."
            ),
        },
        {
            "q": "Can every IT problem be covered?",
            "a": (
                "No. BIT focuses on user, access, Microsoft 365 and standardised workplace services. For "
                "more complex specialist topics, BIT first checks whether they can be handled or "
                "coordinated within the service."
            ),
        },
        {
            "q": "Does BIT only work with hotels?",
            "a": (
                "No. Hotels and front desk are part of the operational background. The offer is aimed "
                "across industries at smaller Swiss companies without in-house IT."
            ),
        },
        {
            "q": "Who makes technical changes?",
            "a": (
                "BIT owns the commissioned service and remains your contact. Standardised tasks are "
                "delivered inside the BIT service. When specialist expertise is required, BIT coordinates "
                "suitable specialist work within the agreed engagement."
            ),
        },
        {
            "q": "How are access changes approved?",
            "a": (
                "Access and permission changes only happen after approval by a person authorised by the "
                "company."
            ),
        },
        {
            "q": "Are there fixed packages or prices?",
            "a": (
                "The IT basics check starts at CHF 190. Further services are offered by scope as a fixed "
                "price, recurring service, or — for additional special effort — after prior approval. "
                "Before work starts, you receive the agreed scope and price. Remote is the default; "
                "Zurich-area on-site visits are agreed separately."
            ),
        },
        {
            "q": "How quickly does BIT respond?",
            "a": (
                "As a rule you receive a first reply within two working days with an assessment of "
                "feasibility and the next step."
            ),
        },
        {
            "q": "Must our IT already be documented?",
            "a": (
                "No. Especially when users, access or ownership are not fully documented, the IT basics "
                "check can serve as a starting point."
            ),
        },
    ]

    en["examples_page"]["title"] = "Typical service cases"
    en["ui"]["special_line"] = "additional special effort only after prior approval"
    en["ui"]["hourly_line"] = "Guideline for separately billed special effort: CHF 120/h"
    en["ui"]["travel_line"] = (
        "Remote is the default. Zurich-area on-site appointments are agreed in advance and listed "
        "separately."
    )


def patch_legal_de(lp: dict) -> None:
    """Apply careful German legal/privacy copy updates."""
    lp["lead"] = "Anbieterkennzeichnung und Hinweise zur Nutzung dieser Website."
    lp["terms_title"] = "Allgemeine Geschäftsbedingungen"
    lp["terms"] = "Die vollständigen Vertragsbedingungen finden Sie in den AGB."
    detail = lp["privacy_detail"]
    detail["purpose"] = (
        "Bearbeitung Ihrer Anfrage, Bedarfsabklärung und Kontaktaufnahme im Hinblick auf eine mögliche "
        "Geschäftsbeziehung."
    )
    detail["basis_title"] = "Hinweis zur Anfrage"
    detail["basis"] = (
        "Mit dem Absenden des Formulars und der Checkbox bestätigen Sie die Kenntnisnahme der "
        "Datenschutzerklärung für die Bearbeitung Ihrer Anfrage."
    )
    detail["processors"] = (
        "Das Anfrageformular wird über die Website an einen Cloudflare-Endpunkt übermittelt. Die Angaben "
        "werden dort für die Bedarfsabklärung gespeichert und an admin@boksitsupport.ch per E-Mail "
        "weitergeleitet (Versanddienst Resend, sofern aktiv). Hosting der Website: Cloudflare Pages."
    )
    detail["abroad"] = (
        "Cloudflare und Resend können Personendaten insbesondere in den USA und weiteren Ländern "
        "bearbeiten. Für internationale Datenübermittlungen werden die jeweils anwendbaren "
        "datenschutzrechtlichen Garantien eingesetzt. WhatsApp kann Kontakt-, Geräte- und "
        "Kommunikationsmetadaten ausserhalb der Schweiz verarbeiten, wenn Sie diesen Kanal nutzen."
    )


def patch_legal_en(lp: dict) -> None:
    """Apply careful English legal/privacy copy updates."""
    lp["lead"] = "Provider identification and notes on the use of this website."
    lp["terms_title"] = "Terms and Conditions"
    lp["terms"] = "The full contractual terms are set out in the Terms and Conditions."
    detail = lp["privacy_detail"]
    detail["purpose"] = (
        "Processing your inquiry, assessing needs and contacting you with a view to a possible business "
        "relationship."
    )
    detail["basis_title"] = "Note on the inquiry"
    detail["basis"] = (
        "By submitting the form and the checkbox, you acknowledge the privacy notice for processing your "
        "inquiry."
    )
    detail["processors"] = (
        "The inquiry form is submitted from the website to a Cloudflare endpoint. The details are stored "
        "there for needs assessment and forwarded by email to admin@boksitsupport.ch (email delivery "
        "service Resend, if enabled). Website hosting: Cloudflare Pages."
    )
    detail["abroad"] = (
        "Cloudflare and Resend may process personal data particularly in the United States and other "
        "countries. Applicable data-protection safeguards are used for international transfers. WhatsApp "
        "may process contact, device and communication metadata outside Switzerland if you use that "
        "channel."
    )


def main() -> None:
    """Patch configs and locales."""
    de_path = ROOT / "config" / "de_v2.json"
    en_path = ROOT / "config" / "en_v2.json"
    de = load(de_path)
    en = load(en_path)
    patch_de(de)
    patch_en(en)
    save(de_path, de)
    save(en_path, en)

    de_loc_path = ROOT / "locales" / "de.json"
    en_loc_path = ROOT / "locales" / "en.json"
    de_loc = load(de_loc_path)
    en_loc = load(en_loc_path)
    patch_legal_de(de_loc["legal_page"])
    patch_legal_en(en_loc["legal_page"])
    save(de_loc_path, de_loc)
    save(en_loc_path, en_loc)


if __name__ == "__main__":
    main()
