# Phase 2+3 Plan — Abschnitte 4 → 3 → 5 → 6 → 7

Umsetzungsreihenfolge laut Auftrag. Quellen: `config/de_v2.json`, `config/en_v2.json`, `scripts/build_v2_de.py`, `assets/universal.css`, `functions/api/*`, `docs/INQUIRY_NOTIFY.md`, `locales/de.json` / `en.json`, `scripts/test_build_v2.py`.

## Abschnitt 4 — Sofortfehler

| Punkt | Dateien | Aktion |
|-------|---------|--------|
| 4.1 Marker | `config/de_v2.json`, `config/en_v2.json`, Build `examples_main` | `examples_page.note` (Zustand A / State A) entfernen; Formular-Hinweis nur noch wenn Text gesetzt. Visitor-HTML greifen. |
| 4.2 Nummerierung | `scripts/build_v2_de.py`, `assets/universal.css` | `process_list_html()` → `<ul class="process-list">` + Span-Nummern; CSS ohne doppelte Marker. Home, Beispiele, Ablauf, Leistungsdetails. |
| 4.3 Legal | Verify nach Rebuild | FormSubmit, `/api/inquiry` in Privacy, Viber, 12 Monate, shared Nav. |
| 4.6 Alles-inklusive | Config DE+EN | Kontextuell: CTA → Absenden-Satz; FAQ/Grenzen → Abgrenzung; Hero-Outcome neu ohne Phrase. Entscheidungen im Bericht. |

## Abschnitt 3 — Geschäftsmodell

| Punkt | Dateien | Aktion |
|-------|---------|--------|
| Partner-Sektion | Config `home.partner`, `home_main()` | Neu **oberhalb** „Klar abgegrenzt“ / „Clearly scoped“. |
| Hero | `home.lead` | Spezialthemen-Halbsatz entfernen. |
| Übergabe-Wording | Services-Intro, Role, Musterfälle | Einmal sachlich (Partner-Sektion); Rest kürzen. |
| Vertragspartner | `about.body`, `locales/*/legal_page.terms` | Sichtbarer auf Über-BIT und AGB-Eckpunkten. |

## Abschnitt 5 — Musterfälle

| Punkt | Dateien | Aktion |
|-------|---------|--------|
| 5.1 | `examples_page` | H1, Intro wie Auftrag; Eyebrow bleibt. |
| 5.2 | Cases + Report | Freigabe-/Konten-Formulierungen, Personendaten, Offene Punkte und Risiken. |
| 5.3 | Cases | Dritter Fall Outlook (DE+EN). |

## Abschnitt 6 — Lead/Notify (vor SEO)

| Punkt | Dateien | Aktion |
|-------|---------|--------|
| 6.1 | `docs/INQUIRY_NOTIFY.md` | Nummerierte Stefan-Schritte, Secrets, Redeploy, Erfolgskriterien. |
| 6.2 | `functions/api/inquiry.js` | Verify: KV-Erfolg trotz Notify-Fail. |
| 6.3 | `functions/api/inquiry-notify-test.js` | POST, Token-Schutz, kein KV. |
| 6.4 | Doc + `scripts/list_inquiries.ps1` | Viewer dokumentieren. |
| 6.5 | `assets/js/inquiry-form.js` | Kein Erfolg bei Fehler; Felder behalten; Mailto; Validation ≠ Sendefehler. |

## Abschnitt 7 — Technik/SEO

| Punkt | Dateien | Aktion |
|-------|---------|--------|
| Redirects | `_redirects` via Build | Market Access → Home; Tabelle im Bericht. |
| `_headers` | `write_headers()` | HTML nicht lang cachen; Duplikate vereinfachen. |
| JSON-LD | `build_v2_de.py` | ProfessionalService auf Kernseiten; FAQPage auf FAQ. |
| Service-Subpages | Config `detail` + Build | ~300–500 Wörter, Form-Link mit area. |
| Interne Links | bereits + ergänzen | Leistungen ↔ Beispiele ↔ FAQ ↔ Ablauf. |
| Sitemap | `write_sitemap` | DE/EN, lastmod. |
| Konsistenz | Grep | Kein Viber/Market Access im Frontend; CTA/Preis. |

## Build / Test / Deploy

1. `python scripts/build_site.py`
2. `pytest scripts/test_build_v2.py functions/api/test_inquiry_contract.py`
3. `npx wrangler pages deploy . --project-name website --branch=main` (via `deploy.bat`)
4. Live-Check ohne Cache
