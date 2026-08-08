# Copy 9/10 – Abschlussbericht

Stand: August 2026  
Quellen: `config/de_v2.json`, `config/en_v2.json`, `locales/de.json`, `locales/en.json`, `scripts/build_v2_de.py`, `scripts/build_site.py`, `scripts/test_build_v2.py`

## Kernmodell (unverändert)

Kunde → BIT → ggf. Fachpartner innerhalb des BIT-Service → Qualitätskontrolle → dokumentierter Abschluss.  
Kein Freelancer-, Vermittlungs- oder MSP-/24/7-Versprechen. Zielgruppe 5–50, Zürich + remote, drei Services, CHF 190 Einstieg, CTA «Bedarf prüfen lassen».

## Top-Änderungen

1. Service-Karten: aktive BIT-Verben (Benutzer/Zugänge, Microsoft 365); «kein offener Dauerauftrag» entfernt.
2. Scope-Hinweis ohne «Nicht jeder Fall automatisch enthalten»; Partnerumfang-Formulierungen durch Machbarkeit ersetzt.
3. Warum-BIT-Bullets geschärft; kurzer Abschlussabsatz ohne Partnerumfang-Phrase.
4. Preise: CHF 190 nur einmal im Preisblock auf `/leistungen/`; CHF 120/h nur als Sonderaufwand-Richtwert.
5. Für Unternehmen: Rolle von BIT (Servicekoordination/QC); Musterfälle auf Link zur Beispielseite gekürzt.
6. Über BIT: ein Inhaberabsatz, Überschrift «Qualifikationen», Sprachen kurz.
7. Ablauf: Abschluss-/Zusatzaufwand-Texte präzisiert; keine doppelte 2-Tage-Rückmeldung in denselben Blöcken.
8. Beispiele: Titel «Typische Servicefälle»; bestehende Freigabe-/Vergleichsrolle-/Prozesssprache und Musterbericht behalten.
9. FAQ kompakter und in der Prompt-Reihenfolge; Remote-Doppler entfernt.
10. Legal: «Primäre Rechtsordnung» und AGB-Eckpunkte-Disclaimer entfernt; Verweis mit Link auf AGB; Datenschutzzweck statt «Rechtsgrundlage: Einwilligung»; Auslandbearbeitung Cloudflare/Resend vorsichtig präzisiert.

## Build / Qualität

- `python scripts/build_site.py`
- `python -m pytest scripts/test_build_v2.py` → 25 passed
- Repo-Grep: keine Treffer mehr für Einführungsbetrieb, Anbieterzuständigkeit-Verkaufsprodukt, Kundenbeziehung-Weiterleitung, kein offener Dauerauftrag, verfügbaren Leistungs- und Partnerumfang

## Bewusst nicht geändert

- Design, Navigation, URLs, Formular/API/Resend
- AGB-Volltext unter `/de/agb/` und `/en/terms/`
- Unternehmensform «Einzelunternehmen» (nur Prüfpunkt für Stefan)
- Keine neuen Referenzen, Zertifikate, Partnernamen oder SLAs

## Prüfpunkte für Stefan

1. Status **Einzelunternehmen** weiterhin korrekt?
2. Cloudflare-/Resend-Auslandbearbeitung (USA u. a.) und eingesetzte Garantien mit der Live-Konfiguration abstimmen.
3. Kontaktangaben (Adresse, Telefon, E-Mail) und AGB-Link auf `/de/legal/` kurz gegenlesen.
4. Live: `/de/`, `/de/leistungen/`, `/de/ueber-bit/`, `/de/faq/`, `/de/legal/` und EN-Pendants.
