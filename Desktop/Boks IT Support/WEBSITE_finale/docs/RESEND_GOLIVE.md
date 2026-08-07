# Resend Go-Live – Checkliste für Stefan

Ziel: E-Mail-Zustellung über Resend als **Upgrade** aktivieren.  
**Interim ohne Domain-Verify:** KV (+ optional Webhook) – siehe `docs/INQUIRY_KV_WEBHOOK.md`.  
`inquiry.live = true` ist erlaubt, sobald Health `hasKv` oder `hasWebhook` (oder Resend) nachweislich greift.

Code-Absender (Default): `BIT Anfrage <anfrage@boksitsupport.ch>`  
Empfänger (Default): `admin@boksitsupport.ch`  
Diagnose: `GET /api/inquiry-health` → `{ hasResendKey, hasKv, hasWebhook }` (nur Booleans, kein Secret).

---

## 1. Resend-Domain für `boksitsupport.ch` verifizieren

**Was:** Domain in Resend anlegen und DNS-Einträge setzen, bis Status **Verified**.

**Schritte:**
1. https://resend.com → Domains → **Add Domain** → `boksitsupport.ch`
2. Angezeigte Records notieren (meist DKIM `TXT` / `CNAME`, ggf. SPF-Hinweis)
3. In Cloudflare DNS eintragen (siehe Schritt 2)
4. In Resend auf **Verify** klicken und warten, bis die Domain grün/verified ist

**Erfolgskriterium:** Domain `boksitsupport.ch` in Resend zeigt **Verified**. Ohne das schlagen Sends mit `from: anfrage@boksitsupport.ch` fehl (typisch **403** oder **422**).

---

## 2. DNS-Records in Cloudflare (DNS only / graue Wolke)

**Was:** Genau die von Resend angezeigten Records setzen. Proxy **aus** (nur DNS, graue Wolke).

| Typ (Beispiel) | Name (Beispiel) | Value | Proxy |
|---|---|---|---|
| `TXT` oder `CNAME` | wie in Resend (oft `resend._domainkey` o. ä.) | Wert **exakt** aus Resend-Dashboard kopieren | **DNS only** (grau) |
| `TXT` (SPF) | `@` bzw. Root | Bestehendes SPF **erweitern**, nicht ersetzen: Resend-`include:` ergänzen (z. B. `include:amazonses.com` – **den aktuellen Include aus dem Resend-Dashboard verwenden**) | **DNS only** |
| optional `TXT` | wie Resend für Domain-Ownership | Wert aus Dashboard | **DNS only** |

**Wichtig:**
- Cloudflare Email Routing / bestehendes SPF (`include:_spf.mx.cloudflare.net`) **nicht löschen** – Resend-Include **hinzufügen**.
- Nie „Proxied“ (orange) für DKIM/TXT-Verifikation.

**Erfolgskriterium:** Resend Verify erfolgreich; Dig/Cloudflare zeigt die neuen Records.

---

## 3. API-Key in Cloudflare Pages (Production)

**Was:** Secret nur in der Pages-Function-Umgebung, nicht im Repo.

**CLI (empfohlen), im Projektordner:**

```powershell
npx wrangler pages secret put RESEND_API_KEY --project-name website
```

Optional:

```powershell
npx wrangler pages secret put INQUIRY_TO --project-name website
npx wrangler pages secret put INQUIRY_FROM --project-name website
npx wrangler pages secret put INQUIRY_MIRROR_TO --project-name website
npx wrangler pages secret put INQUIRY_DIAG_TOKEN --project-name website
```

**Dashboard-Alternative:** Cloudflare → Workers & Pages → Projekt **website** → Settings → Environment variables → **Production** → Secret `RESEND_API_KEY`.

**Erfolgskriterium:** Nach Deploy liefert `https://boksitsupport.ch/api/inquiry-health` → `"hasResendKey": true` (bei gesetztem `INQUIRY_DIAG_TOKEN`: `?token=…`).

---

## 4. Nach Secret: neuer Deploy erforderlich

**Was:** Secrets gelten für neue Deployments; altes Deployment ohne Key bleibt ohne Resend-Pfad.

```powershell
npx wrangler pages deploy . --project-name website
```

**Erfolgskriterium:** Health zeigt `hasResendKey: true` auf Production. KV/Webhook können parallel aktiv sein (`hasKv` / `hasWebhook`).

---

## 5. Resend Emails-Log prüfen

**Was:** Nach einem echten Test-POST auf `/api/inquiry` (wenn Key + Domain ok).

1. Resend Dashboard → **Emails**
2. Eintrag mit Subject `BIT Anfrage: …` suchen

| Beobachtung | Bedeutung |
|---|---|
| Kein Eintrag | Request erreicht Resend nicht (Key fehlt, Function nimmt nur KV/Webhook) |
| Failed / bounced | Domain/from/API-Problem – Status im Log / Pages Function Log (`INQUIRY_RESEND_HTTP`) |
| Delivered | Versand ok – in `docs/PHASE3_UMSETZUNG.md` mit Zeitstempel dokumentieren |

**Pages Function Logs:** Cloudflare → website → Logs → Suche `INQUIRY_RESEND_HTTP` / `INQUIRY_RESEND_FAILED` (enthält HTTP-Status + Body, kein API-Key).

---

## Kurz: Zustellungslogik

1. Client POSTet `/api/inquiry`
2. Function validiert, `console.log` der Submission
3. Erfolg wenn **KV-Schreiben** ODER **Webhook 2xx** ODER **Resend** gelingt
4. Ohne jeden konfigurierten Pfad → **503**; UI offline = Submit HTML `disabled`

**Empfehlung:** Erst KV/Webhook live; Resend nach Domain-Verify ergänzen (`docs/INQUIRY_KV_WEBHOOK.md`).
