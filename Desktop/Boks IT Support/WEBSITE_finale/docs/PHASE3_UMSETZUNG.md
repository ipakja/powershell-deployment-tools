# Phase 3 / Positioning update (2026-08-07)

## P1 – Leadweg
- FormSubmit vollständig entfernt (API, Client, Privacy, Docs, Health).
- Delivery: Cloudflare KV (`INQUIRY_LOG`, TTL ~12 Monate) + optional Webhook + optional Resend.
- Privacy: kein „dauerhaft“, keine Env-Var-Namen, 12-Monats-Löschung.
- Legal: Adresse/Telefon/E-Mail nur einmal im Anbieter-Block.
- `_headers`: HTML `max-age=0, must-revalidate`.
- Root `/` → 301 `/de/` (Middleware + `_redirects` + Index-Stub).

## P2 – Positionierung
- Linie: „IT-Support für kleine Unternehmen ohne eigene IT“.
- CTA sitewide: „IT-Anliegen prüfen lassen“ / „Have your IT need reviewed“.
- Drei Produkte: Benutzer & Zugänge · Microsoft 365 & Arbeitsplatz · IT-Basischeck (ab CHF 190).
- Anbieterkoordination als Hinweis unter den Karten, kein viertes Produkt.
- Alte Slugs `zugang-sicherheit` / `ansprechpartner` → 301.

## P3 – Vertrauen
- `/de/beispiele/` und `/en/examples/` mit zwei Musterfällen + Musterbericht-Struktur.
- Rückmeldungserwartung: „in der Regel innerhalb von zwei Arbeitstagen.“

## P4 – Formular + SEO
- Pflichtfelder: company, name, email, employees, area, description, privacy.
- Optional: phone, location, industry, workstations, m365, IT-Situation, start.
- JSON-LD: ProfessionalService (Home), FAQPage (FAQ).

## Deploy
```
python -m scripts.build_site   # or: python scripts/build_site.py
npx wrangler pages deploy . --project-name=website
```
