# BIT Website

**BIT – Boks IT Support**, Zürich.  
Zustand A: IT-Support für kleine Unternehmen ohne eigene IT.

## Stack

- Semantisches HTML5 / CSS / JS (kein Framework)
- Python-Build: `scripts/build_site.py` + `scripts/build_v2_de.py`
- Content: `config/de_v2.json`, `config/en_v2.json`, `config/agb_de.json`, `config/agb_en.json`, `locales/de.json`, `locales/en.json`
- Cloudflare Pages (`website`) + Pages Function `/api/inquiry`
- Lead-Speicherung: **Cloudflare KV** (`INQUIRY_LOG`, TTL ~12 Monate)
- Optional: Webhook (`INQUIRY_WEBHOOK_URL`), später Resend (`RESEND_API_KEY`)

## Öffentliche Struktur

**Aktiv:** Deutsch + Englisch

| Route | Inhalt |
|---|---|
| `/` | 301 → `/de/` |
| `/de/`, `/en/` | Start |
| `/de/leistungen/`, `/en/services/` | 3 Produkte |
| `/de/beispiele/`, `/en/examples/` | Musterfälle |
| `/de/so-funktioniert-es/`, `/en/how-it-works/` | Ablauf |
| `/de/fuer-unternehmen/`, `/en/for-businesses/` | Zielgruppe |
| `/de/ueber-bit/`, `/en/about-bit/` | Über BIT |
| `/de/faq/`, `/en/faq/` | FAQ |
| `/de/anfrage/`, `/en/inquiry/` | Formular (primärer CTA) |
| `/de/legal/`, `/en/legal/` | Impressum & Datenschutz |
| `/de/agb/`, `/en/terms/` | AGB / Terms and Conditions |

FR / IT / SR / BS / HR → **302** auf `/de/`.  
Alte Market-/Hospitality-URLs → **301** auf aktuelle Seiten.

## Produkte

1. Benutzer & Zugänge  
2. Microsoft 365 & Arbeitsplatz  
3. IT-Basischeck (Einstieg ab CHF 190)

CTA überall: **IT-Anliegen prüfen lassen**

## Kontakt

- Primär: Formular `/de/anfrage/`
- Footer: E-Mail, Telefon, optional WhatsApp (kein Viber)
- E-Mail: `admin@boksitsupport.ch`
- Telefon: `+41 78 263 27 01`
- Adresse: Schaffhauserstrasse 457, 8052 Zürich

## Setup / Quickstart

```powershell
python scripts/build_site.py
python -m http.server 8000
```

Öffnen: `http://localhost:8000/de/`

## Tests

```powershell
python -m pytest scripts/test_build_v2.py
```

## Formular / Leads

Health: `GET /api/inquiry-health` → `{ hasKv, hasResendKey, hasWebhook }`

Anfragen in KV listen:

```powershell
npx wrangler kv key list --remote --namespace-id d6f0c62cf7a14b199355315aa0dec76c --prefix inquiry:
```

Optional E-Mail später: Domain bei Resend verifizieren, dann  
`npx wrangler pages secret put RESEND_API_KEY --project-name website` und neu deployen.

Details: `docs/INQUIRY_KV_WEBHOOK.md`, `docs/RESEND_GOLIVE.md`, `docs/PUBLIC_CLEANUP.md`

## Deployment

```powershell
.\deploy.bat
```

Projekt: Cloudflare Pages `website` → `boksitsupport.ch`

## Screenshots

_Platzhalter: Startseite, Leistungen, Anfrageformular, Beispiele_
