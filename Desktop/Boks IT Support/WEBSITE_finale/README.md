# BIT Website

Statische, mehrsprachige Website für BIT – Boks IT Support und
BIT – Swiss Market Development & Representation.

## Stack

- semantisches HTML5
- gemeinsames CSS und JavaScript ohne Framework
- Python-Build für lokalisierte, SEO-fähige Seiten
- Cloudflare Pages

## Struktur

- `/de/` – Deutsch (Schweiz)
- `/en/` – English
- `/fr/` – Français (Suisse)
- `/sr/` – Srpski, latinica, ekavica
- `/bs/` – Bosanski, latinica, ijekavica
- `/hr/` – Hrvatski, latinica, ijekavica
- `locales/*.json` – Texte und Fachbegriffe
- `config/site.json` – Sprachen, Adresse und Kontaktkonfiguration
- `templates/` – gemeinsame Seiten- und Komponenten-Templates
- `assets/universal.css` – gemeinsames Design
- `assets/js/mobile-nav.js` – mobile Navigation
- `assets/js/language-preference.js` – Sprachvorschlag und Auswahl
- `assets/js/contact-links.js` – sichere Messenger-Links
- `assets/js/app.js` – gemeinsame Initialisierung
- `scripts/build_site.py` – erzeugt Sprach- und Legal-Seiten sowie Sitemap

Jede Sprache hat eine eigene Startseite und ein lokalisiertes Impressum unter
`/<sprache>/legal/`. Die Anbieteradresse lautet:
Schaffhauserstrasse 457, 8052 Zürich.

## Leistungen

1. Hospitality: Hotel und Gastronomie
2. KMU IT und digitale Lösungen
3. Prozess- und Projektunterstützung
4. Swiss Market Development & Representation

## Kontakt

Die Website hat bewusst kein Kontaktformular und kein eigenes Tracking.
Die Browsersprache wird nur vorgeschlagen. Die Website leitet nicht automatisch
dauerhaft um; eine bewusste Auswahl wird lokal im Browser gespeichert.

- WhatsApp: `https://wa.me/41782632701`
- Viber: `viber://chat?number=%2B41782632701`
- Telefon: `+41 78 263 27 01`
- E-Mail: `admin@boksitsupport.ch`

Keine vertraulichen Zugangsdaten über Messenger senden.

## Setup und Quickstart

```powershell
python scripts/build_site.py
python -m http.server 8000
```

Danach `http://localhost:8000/de/` öffnen.

## Tests

```powershell
python -m pytest scripts/test_build_site.py
npx --yes vitest@latest run assets/js/language-preference.test.js
```

## Deployment

Aus dem Ordner `Boks IT Support`:

```powershell
.\deploy-boksitsupport.ps1
```

Das Skript baut die Seiten neu und veröffentlicht `WEBSITE_finale` im
Cloudflare-Pages-Projekt `website`, an dem `boksitsupport.ch` hängt.
Nach dem Deployment `/de/`, alle weiteren Sprachpfade,
`sitemap.xml` und die Legacy-Redirects prüfen.

## Screenshots

- `[Platzhalter] Desktop – Startseite`
- `[Platzhalter] Mobile – Sprachwahl und Kontakt`
