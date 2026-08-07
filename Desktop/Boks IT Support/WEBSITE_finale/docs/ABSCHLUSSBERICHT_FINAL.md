# Abschlussbericht Final – boksitsupport.ch

**Datum:** 2026-08-07  
**Branch:** `bit-website-sync` → Deploy Production `website` / `main`  
**Deploy-Zeit:** 2026-08-07 ca. 23:58 +02:00 (letzter Functions-Deploy `e80482ce`)  
**Preview:** https://e80482ce.website-5db.pages.dev

---

## 1. Leadweg / Viewer

- HTML-Viewer: `GET /api/inquiries/view?token=TOKEN_PLACEHOLDER`
- JSON: `GET /api/inquiries?token=TOKEN_PLACEHOLDER&limit=20`
- Auth: Secret fehlt → 503; Token falsch/fehlt (Secret gesetzt) → 401
- Secret `INQUIRY_VIEW_TOKEN` in Production gesetzt (Wert nicht in Git)
- Docs: [INQUIRY_VIEWER.md](./INQUIRY_VIEWER.md), [BETRIEB.md](./BETRIEB.md)

**Bookmark (Platzhalter in Git):**  
`https://boksitsupport.ch/api/inquiries/view?token=TOKEN_PLACEHOLDER`

## 2. Stefan-Schritte (mit Erfolgskriterien)

1. Token ist bereits gesetzt; Bookmark-URL mit dem echten Token lokal speichern (nicht teilen).  
   **Erfolg:** Viewer zeigt «Einträge der letzten 7 Tage» und «Neueste Anfrage».
2. Optional Resend später: [RESEND_GOLIVE.md](./RESEND_GOLIVE.md) (Test mit `onboarding@resend.dev` nur an Account-E-Mail; Produktion braucht DNS only).
3. Telegram optional – Code bleibt, Docs empfehlen Viewer.
4. Ana 5-Sekunden-Test: [5-SEKUNDEN-TEST.md](./5-SEKUNDEN-TEST.md) — **noch offen**.

## 3. Resend-Ergebnis

- Ohne Domain-Verify: Versand von `onboarding@resend.dev` **nur** an die Resend-Account-E-Mail möglich.
- Für `@boksitsupport.ch` an beliebige Empfänger: Domain verify + DNS **Proxy DNS only** (grau) — Tabelle in RESEND_GOLIVE.md.

## 4. Content

- Vertragspartner-Sektion DE/EN Home + Über-BIT verifiziert.
- Vor-Ort: remote-first, Zürich, **ohne Anfahrtspauschale** (explizit).
- Verbleibende «Übergabe»-Stellen: vor allem Legacy-Locales (`locales/de.json` Prozess-Titel); Musterfälle in v2 auf «Abschluss/dokumentieren» entschärft.
- Service-Haupttexte DE: ca. 300–338 Wörter (`<main>`).

## 5. Legal

- Shared Build via locales; kein FormSubmit; keine API-Internals; Retention 12 Monate / KV TTL 365 Tage; kein Viber im Live-Footer/Legal; Adresse nicht verdoppelt; Entity unverändert; Stand August 2026.

## 6. Tech/SEO

- HTML `Cache-Control: no-store`; Assets 86400
- `/de/market-access/` → 301 `/de/`
- JSON-LD ProfessionalService (+ FAQPage)
- Sitemap DE+EN
- `robots.txt` Disallow `/api/inquiries`, `/api/inquiries/view`, `/api/inquiry-notify-test`
- Tests: **35 passed**

## 7. Robustheit Inquiry

- KV ohne Notify = OK für Besucher
- KV gebunden + Write fail → kein Erfolg (502)
- Sprachfeld `language` (hidden) + Source-Pfad DE/EN

## 8. Git / Deploy

- Commit-Hash: *(nach Commit eintragen / siehe git log)*
- Production-Deploy Branch `main` durchgeführt
- `main` vs Live: Production trackt Pages Deployments von diesem Workspace; Git-Branch der Sync-Arbeit ist `bit-website-sync`. Falls `origin/main` hinter dem Sync-Branch liegt → PR `bit-website-sync` → `main` empfohlen.

## 9. Geprüfte URLs

| URL | Ergebnis |
|-----|----------|
| `/api/inquiries/view` ohne Token | 401 |
| `/api/inquiries/view?token=…` | 200 HTML, 7-Tage-Zähler |
| `/api/inquiries?token=…` | 200 JSON |
| `/api/inquiry-health` | hasKv true, hasPushNotify false |
| `/de/market-access/` | 301 → `/de/` |
| `/de/` | Vertragspartner-Sektion |

## 10. Offen für Stefan

1. Bookmark-URL privat halten  
2. Ana 5-Sekunden-Test  
3. Optional Resend/Telegram  
4. Ggf. Cloudflare Email Obfuscation für `/api/*` prüfen (mailto-Workaround aktiv)
