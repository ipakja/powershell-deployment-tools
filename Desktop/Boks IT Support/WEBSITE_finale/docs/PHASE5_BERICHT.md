# Phase 5 Bericht — Abschnitte 4 → 3 → 5 → 6 → 7

**Deploy:** Cloudflare Pages Projekt `website`, Branch `main`  
**Preview-Deploy:** `https://70db4965.website-5db.pages.dev` (erster Deploy dieses Laufs; Folgedeploy für M365-Wortanzahl)  
**Repo-HEAD:** `4de017534cb58a17f7686d1603c61dd9b8fc4f4a` (**dirty** — Änderungen nicht committed)  
**Live-Check (UTC):** 2026-08-07 ca. 21:32Z (mit Cache-Bust-Query)

---

## 1. Live vs Repo Abweichungen (post-deploy)

| Thema | Status |
|-------|--------|
| Partner-Sektion, Musterfälle, FAQ-Abgrenzung, Prozess-`<ul>` | Live und Repo deckungsgleich (nach kurzer Edge-Propagation; ohne Query ggf. kurz stale) |
| `_headers` HTML `no-store` | Live gesetzt |
| Market Access 301 → Home | Live OK |
| Push-Notify | Live: `hasPushNotify: false` — Secrets noch nicht gesetzt (erwartet) |
| Notify-Test-Endpoint | Code deployed; ohne Token/Secrets nicht nutzbar |

Keine inhaltliche Drift zwischen gebautem Repo und Production nach Cache-Bust.

---

## 2. Geänderte / neue Dateien

**Neu**

- `docs/PHASE2_PLAN.md`
- `functions/api/inquiry-notify-test.js`
- `docs/PHASE5_BERICHT.md` (dieser Bericht)

**Aktualisiert (Auswahl)**

- `config/de_v2.json`, `config/en_v2.json`
- `scripts/build_v2_de.py`, `scripts/test_build_v2.py`
- `assets/universal.css`, `assets/js/inquiry-form.js`
- `templates/v2/base.html` (CSS `?v=15`)
- `functions/api/inquiry.js` (export `deliverPushNotify` / Telegram+Webhook)
- `functions/api/test_inquiry_contract.py`
- `docs/INQUIRY_NOTIFY.md`
- `locales/de.json`, `locales/en.json` (AGB-Eckpunkte)
- `wrangler.toml` (Kommentar Notify-Test)
- Regenerierte HTML unter `de/**`, `en/**`, `_headers`, `_redirects`, `sitemap.xml`

---

## 3. Redirect-Tabelle (Kern)

| Von | Nach | Code |
|-----|------|------|
| `/`, `/index.html` | `/de/` | 301 |
| `/de/market-access`, `/de/market-access/` | `/de/` | 301 |
| `/en/market-access`, `/en/market-access/` | `/en/` | 301 |
| `/de/markt/`, `/en/market/` | jeweilige Home | 301 |
| Market-Slugs FR/IT/SR/BS/HR | `/de/` | 301 |
| `/de/hospitality/` | `/de/leistungen/` | 301 |
| `/en/hospitality/` | `/en/services/` | 301 |
| Hospitality andere Locales | `/de/leistungen/` | 301 |
| Legacy Service-Slugs (onboarding, offboarding, …) | neue Leistungs-URLs bzw. Übersicht | 301 |
| `/fr/*`, `/it/*`, `/sr/*`, `/bs/*`, `/hr/*` | `/de/` | 302 |
| `www.boksitsupport.ch/*` | `boksitsupport.ch/:splat` | 301 |

Vollständige Liste: generiert in `_redirects`.

---

## 4. Marker-Fundstellen (Frontend nach Fix)

Visitor-HTML (`de/**`, `en/**`): **keine** Treffer für

- Zustand A / State A / Zustand B  
- MVP / Phase 1 / Phase 2  
- Alles-inklusive / all-inclusive  
- FormSubmit / Viber (Footer/Seiten)

Interne Docs dürfen Phase/Zustand weiter nennen.

---

## 5. Nummerierte Stefan-Schritte (Notify)

Siehe auch `docs/INQUIRY_NOTIFY.md`.

1. BotFather → Bot → Token → Secret **`TELEGRAM_BOT_TOKEN`** — Erfolg: Token vorhanden.  
2. Bot anschreiben → `getUpdates` → **`TELEGRAM_CHAT_ID`** — Erfolg: numerische ID.  
3. Cloudflare Pages → Projekt **`website`** → Production: Secrets setzen; optional **`INQUIRY_VIEW_TOKEN`**, alt. **`INQUIRY_WEBHOOK_URL`** — Erfolg: Namen sichtbar.  
4. Redeploy (`deploy.bat` / wrangler pages deploy `--branch=main`) — Erfolg: neues Deployment.  
5. `POST /api/inquiry-notify-test` mit Bearer-Token — Erfolg: Telegram-Nachricht, **`stored:false`**.  
6. Echtes Formular + `.\scripts\list_inquiries.ps1` — Erfolg: KV-Eintrag + Notify.

**Live jetzt:** `hasTelegram=false`, `hasPushNotify=false`.

---

## 6. Aussagen die Bestätigung brauchen

- SIZ-Credentials bleiben veröffentlicht (bereits Phase 1 bestätigt).  
- Antwortformulierung «in der Regel innerhalb von zwei Arbeitstagen» — unverändert; keine Garantie.  
- Richtwerte CHF 120 / Basischeck ab CHF 190 — unverändert.  
- Keine neuen Drittanbieter eingeführt.

---

## 7. Build / Test commands

```bat
python scripts\build_site.py
python -m pytest scripts\test_build_v2.py functions\api\test_inquiry_contract.py -q
deploy.bat
```

Ergebnis dieses Laufs: **32 passed**.

---

## 8. Commit-Hash, Deploy, geprüfte URLs

- **Git HEAD:** `4de017534cb58a17f7686d1603c61dd9b8fc4f4a` — Working tree **dirty** (kein Commit auf Wunsch).  
- **Deploy:** `npx wrangler pages deploy . --project-name website --branch=main --commit-dirty=true`  
- **Geprüfte URLs (erwartete Strings):**

| URL | Erwartung |
|-----|-----------|
| `/de/` | Partner-Sektion; Absenden-Satz; kein Spezialthemen-Halbsatz im Hero |
| `/de/beispiele/` | H1 Ablauf; 3. Muster Outlook; keine Zustand-A-Notice |
| `/en/examples/` | EN-Äquivalent + Outlook sample |
| `/de/ueber-bit/` | «Vertragspartner bleibe ich» |
| `/de/legal/` | Vertragspartner; 12 Monate; kein FormSubmit |
| `/de/faq/` | Abgrenzung ohne Alles-inklusive |
| `/de/so-funktioniert-es/` | `<ul class="process-list">` |
| `/de/leistungen/benutzer-und-zugaenge/` | JSON-LD + area-Link |
| `/de/market-access/` | 301 → `/de/` |
| `/api/inquiry-health` | hasKv true; hasPushNotify false bis Secrets |

---

## Alles-inklusive — Entscheidungen (4.6)

| Vorkommen (vorher) | Entscheidung |
|--------------------|--------------|
| Hero-Outcome | Neu: klarer Rahmen/Abschluss, ohne Phrase, ohne Garantie |
| Closing/CTA-Note | → «Durch das Absenden entsteht noch kein Auftrag.» / EN Absenden-Äquivalent |
| FAQ «Können alle IT-Probleme…» | Fakten-Abgrenzung (Rahmen ja / Spezial nein), **nicht** Absenden-Satz |
| Service boundaries / Audience nofit | Fakten («unbegrenzter Leistungsumfang» / «ohne klaren Leistungsumfang») |
| Phrase «Alles-inklusive» im Frontend | entfernt |
