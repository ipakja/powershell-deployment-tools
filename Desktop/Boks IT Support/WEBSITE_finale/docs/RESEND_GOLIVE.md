# Resend Go-Live – Checkliste für Stefan

Ziel: E-Mail-Notify über Resend nur wenn gewünscht.  
**Standard ops path bleibt:** KV + HTML-Viewer ([INQUIRY_VIEWER.md](./INQUIRY_VIEWER.md)).

Code-Absender (Default): `BIT Anfrage <anfrage@boksitsupport.ch>`  
Empfänger (Default): `admin@boksitsupport.ch`  
Diagnose: `GET /api/inquiry-health` → `{ hasResendKey, hasKv, hasWebhook, hasTelegram, hasPushNotify }` (nur Booleans).

---

## A. Ohne eigene Domain (nur Test)

Resend erlaubt `from: onboarding@resend.dev` **ohne** Verifikation der eigenen Domain, aber:

- Empfänger darf **nur** die E-Mail-Adresse des Resend-Account-Inhabers sein
- Andere Empfänger → typisch **403** ([Resend KB](https://resend.com/docs/knowledge-base/403-error-resend-dev-domain))
- Nicht für Produktion an beliebige Postfächer geeignet

**Schritte (optionaler Kurztest):**

1. Resend-Konto anlegen (Account-E-Mail = gewünschte Test-Inbox, z. B. `admin@boksitsupport.ch`)
2. API-Key erzeugen
3. Cloudflare Pages → Projekt **`website`** → Production Secrets:
   - `RESEND_API_KEY`
   - `INQUIRY_FROM` = `BIT Anfrage <onboarding@resend.dev>`
   - optional `INQUIRY_TO` = Account-E-Mail
4. Redeploy
5. Formular-Test oder Health: `hasResendKey: true`

**Erfolgskriterium:** Resend-Dashboard zeigt Delivered an die Account-E-Mail.

---

## B. Produktion mit eigener Domain (DNS only)

Für Versand von `@boksitsupport.ch` an beliebige Empfänger: Domain in Resend verifizieren.

### 1. Domain in Resend

1. https://resend.com → Domains → **Add Domain** → `boksitsupport.ch`
2. Angezeigte Records notieren (DKIM, SPF-Hinweis, ggf. Ownership)

### 2. DNS in Cloudflare — **Proxy DNS only (graue Wolke)**

| Typ | Name | Value | Proxy |
|-----|------|-------|-------|
| `TXT` oder `CNAME` (DKIM) | exakt wie Resend (oft `resend._domainkey`) | Wert exakt aus Resend | **DNS only** (grau) |
| `TXT` (SPF) | `@` / Root | Bestehendes SPF **erweitern** (Resend-`include:` ergänzen, nicht ersetzen) | **DNS only** |
| optional Ownership `TXT` | wie Resend | Wert aus Dashboard | **DNS only** |
| optional DMARC `TXT` | `_dmarc` | Policy nach Bedarf (später) | **DNS only** |

**Wichtig:** Nie „Proxied“ (orange) für Mail-Verifikationsrecords. Cloudflare Email Routing / bestehendes SPF nicht löschen.

**Erfolgskriterium:** Resend zeigt Domain **Verified**.

### 3. Secrets + From-Adresse

```powershell
npx wrangler pages secret put RESEND_API_KEY --project-name website
npx wrangler pages secret put INQUIRY_FROM --project-name website
# Wert z. B. BIT Anfrage <anfrage@boksitsupport.ch>
```

Redeploy Pflicht.

### 4. Prüfen

1. Formular-Submit
2. Resend → Emails → Subject `BIT Anfrage: …`
3. Pages Function Logs: `INQUIRY_RESEND_HTTP` / `INQUIRY_RESEND_FAILED`

---

## Kurz: Zustellungslogik

1. Client POSTet `/api/inquiry`
2. KV-Schreiben = primärer Erfolgspfad (wenn Binding vorhanden)
3. Resend/Telegram/Webhook danach optional; Notify-Fehler setzen den Besuchererfolg nicht zurück, wenn KV ok ist
4. Ohne jeden konfigurierten Pfad → **503**

**Empfehlung:** Viewer-Bookmark zuerst; Resend nach Domain-Verify ergänzen.
