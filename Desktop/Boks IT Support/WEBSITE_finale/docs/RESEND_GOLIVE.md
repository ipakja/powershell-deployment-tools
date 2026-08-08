# Resend Go-Live – Checkliste für Stefan

Ziel: E-Mail-Benachrichtigung für neue Anfragen an `admin@boksitsupport.ch`.  
**Speicherpfad bleibt immer:** Website → Cloudflare `/api/inquiry` → KV `INQUIRY_LOG` (TTL ~12 Monate) → HTML-Viewer.

Ohne `RESEND_API_KEY` funktioniert das Formular weiterhin (KV + Viewer), aber **keine E-Mail**.

---

## Status-Hinweis

Vor Go-Live prüfen:

```text
GET https://boksitsupport.ch/api/inquiry-health
→ hasKv: true, hasResendKey: true  (Ziel)
```

`hasResendKey: false` bedeutet: Codepfad ist bereit, Secret fehlt → E-Mail-Test = FAIL.

---

## A. Secrets setzen (Production, Projekt `website`)

```powershell
cd "C:\Users\41765\Desktop\Boks IT Support\WEBSITE_finale"

npx wrangler pages secret put RESEND_API_KEY --project-name website
# Wert: Resend API Key (re_…)

npx wrangler pages secret put INQUIRY_FROM --project-name website
# Wert z. B.: BIT Anfrage <anfrage@boksitsupport.ch>
# Alias ebenfalls unterstützt: INQUIRY_FROM_EMAIL

# Optional Empfänger (Default ist admin@boksitsupport.ch):
# npx wrangler pages secret put INQUIRY_NOTIFY_EMAIL --project-name website
# Alias ebenfalls unterstützt: INQUIRY_TO
```

Danach **Redeploy** (Pages Secrets greifen erst nach neuem Deployment).

---

## B. Domain in Resend verifizieren (Produktion)

1. https://resend.com → Domains → **Add Domain** → `boksitsupport.ch`
2. DNS in Cloudflare als **DNS only** (graue Wolke): DKIM / SPF-`include` / Ownership wie Resend angibt
3. Resend zeigt Domain **Verified**
4. From-Adresse muss zur verifizierten Domain gehören (nicht `onboarding@resend.dev` für beliebige Empfänger)

### Kurztest ohne Domain (nur Account-Inbox)

- `INQUIRY_FROM` = `BIT Anfrage <onboarding@resend.dev>`
- Empfänger darf nur die Resend-Account-E-Mail sein
- Nicht für Produktion an beliebige Postfächer

---

## C. Prüfen nach Deploy

1. Formular DE/EN absenden
2. Subject erwartet: `Neue BIT-Anfrage – [Unternehmen] – [Leistungsbereich]`
3. Reply-To = Lead-E-Mail
4. Viewer: Feld **E-Mail-Benachrichtigung** = `sent` (oder `failed` / `skipped`)
5. Function Logs: `INQUIRY_RESEND_HTTP` / `INQUIRY_DELIVERED_RESEND` bzw. `INQUIRY_RESEND_FAILED`
6. Health: `hasResendKey: true`

---

## Zustellungslogik (verbindlich)

1. Client POSTet nur `/api/inquiry` (kein FormSubmit)
2. Validierung → bei Fehler **400** (Werte bleiben im Formular)
3. KV-Schreiben zuerst; bei KV-Fehler → **500**, keine Erfolgsmeldung
4. Danach Resend; bei E-Mail-Fehler bleibt KV, Status `failed`, Besucher sieht trotzdem Erfolg (**200**)
5. Ohne Resend-Key: Status `skipped`, KV bleibt die Quelle der Wahrheit

**Empfehlung:** Viewer-Bookmark nutzen; Resend erst nach Domain-Verify und Secret aktivieren.
