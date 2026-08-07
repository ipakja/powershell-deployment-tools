# Inquiry push notify (Telegram / Slack) + KV viewer

**Mandatory for ops:** KV alone stores leads; Stefan is **not** notified unless push notify is configured. Set Telegram (recommended) or Slack before relying on the form in production.

**No FormSubmit.** Paths: Cloudflare KV (`INQUIRY_LOG`) + Telegram and/or webhook + optional Resend.

**Parallel zero-backend path:** WhatsApp / mailto with pre-filled templates on the inquiry pages — see [INQUIRY_DIRECT.md](./INQUIRY_DIRECT.md). Keep both; do not remove the form.

Full delivery model: see [INQUIRY_KV_WEBHOOK.md](./INQUIRY_KV_WEBHOOK.md).

---

## Nummerierte Schritte für Stefan (Telegram empfohlen)

### Schritt 1 — Bot anlegen

1. In Telegram [@BotFather](https://t.me/BotFather) öffnen → `/newbot` → Name und Username wählen.
2. BotFather liefert den **Bot-Token** (Format `123456:ABC…`).

**Erfolgskriterium:** Sie haben den Token kopiert und speichern ihn nur als Secret (nicht in Git).

**Secret-Name:** `TELEGRAM_BOT_TOKEN`

---

### Schritt 2 — Chat-ID ermitteln

1. Den neuen Bot in Telegram einmal anschreiben (beliebiger Text).
2. Im Browser öffnen:  
   `https://api.telegram.org/bot<TOKEN>/getUpdates`  
   (`<TOKEN>` durch den echten Token ersetzen).
3. In der JSON-Antwort `message.chat.id` notieren (Zahl, ggf. negativ bei Gruppen).

**Erfolgskriterium:** Sie sehen eine numerische `chat.id` und haben sie kopiert.

**Secret-Name:** `TELEGRAM_CHAT_ID`

---

### Schritt 3 — Secrets in Cloudflare setzen (Dashboard)

1. [Cloudflare Dashboard](https://dash.cloudflare.com/) → **Workers & Pages** → Projekt **`website`**.
2. **Settings** → **Environment variables** (bzw. Variables and Secrets) → Umgebung **Production**.
3. Anlegen bzw. aktualisieren:

| Secret / Variable | Pflicht | Zweck |
|-------------------|---------|--------|
| `TELEGRAM_BOT_TOKEN` | ja (für Telegram) | Bot-Token von BotFather |
| `TELEGRAM_CHAT_ID` | ja (für Telegram) | Numerische Chat-ID |
| `INQUIRY_VIEW_TOKEN` | empfohlen | Langer Zufallsstring (32+ Zeichen) für Viewer und Notify-Test |
| `INQUIRY_DIAG_TOKEN` | optional | Fallback-Auth für Health/Viewer/Notify-Test, falls VIEW fehlt |
| `INQUIRY_WEBHOOK_URL` | optional | Alternative/Zusatz: Slack Incoming Webhook, Discord oder generisches JSON |

**Wrangler-Alternative** (lokal, eingeloggt):

```bat
npx wrangler pages secret put TELEGRAM_BOT_TOKEN --project-name website
npx wrangler pages secret put TELEGRAM_CHAT_ID --project-name website
npx wrangler pages secret put INQUIRY_VIEW_TOKEN --project-name website
```

(Jeder Befehl fragt den Wert interaktiv ab.)

**Erfolgskriterium:** Die drei Namen erscheinen unter Production für Projekt `website` (Werte bleiben verborgen).

---

### Schritt 4 — Redeploy

Nach dem Setzen von Production-Variablen/Secrets:

```bat
deploy.bat
```

oder:

```bat
python scripts\build_site.py
npx wrangler pages deploy . --project-name website --branch=main --commit-dirty=true
```

**Erfolgskriterium:** Deploy endet ohne Fehler; Production zeigt den neuen Deployment-Zeitpunkt.

**Hinweis:** Secrets gelten erst zuverlässig nach einem erfolgreichen Pages-Deploy (oder wenn Cloudflare die Vars sofort an die laufenden Functions bindet — Redeploy ist der sichere Weg).

---

### Schritt 5 — Notify-Test ohne KV-Eintrag

**Auth Pflicht:** `INQUIRY_VIEW_TOKEN` (oder Fallback `INQUIRY_DIAG_TOKEN`). Ohne konfiguriertes Secret → **503** `auth_not_configured`. Falsches Token → **401**. Endpoint ist **nie öffentlich**.

```http
POST https://boksitsupport.ch/api/inquiry-notify-test
Authorization: Bearer <INQUIRY_VIEW_TOKEN>
Content-Type: application/json

{"note":"Notify-Test Stefan"}
```

Alternativ Query: `POST …/api/inquiry-notify-test?token=<INQUIRY_VIEW_TOKEN>`

curl (PowerShell):

```powershell
curl.exe -X POST "https://boksitsupport.ch/api/inquiry-notify-test" `
  -H "Authorization: Bearer $env:INQUIRY_VIEW_TOKEN" `
  -H "Content-Type: application/json" `
  -d "{\"note\":\"Notify-Test Stefan\"}"
```

Invoke-RestMethod:

```powershell
Invoke-RestMethod -Method Post `
  -Uri "https://boksitsupport.ch/api/inquiry-notify-test" `
  -Headers @{ Authorization = "Bearer $env:INQUIRY_VIEW_TOKEN" } `
  -ContentType "application/json" `
  -Body '{"note":"Notify-Test Stefan"}'
```

**Erfolgskriterium:** HTTP 200 mit `"ok":true,"stored":false,"notified":true`; Telegram (oder Webhook) erhält die Testnachricht; unter `/api/inquiries` erscheint **kein** neuer KV-Eintrag für diesen Test.

---

### Schritt 6 — Echten Formular-Submit prüfen

1. Formular auf `https://boksitsupport.ch/de/anfrage/` ausfüllen und senden.
2. Telegram prüfen.
3. Optional Viewer:

```powershell
.\scripts\list_inquiries.ps1 -Token "SECRET" -Limit 5
```

**Erfolgskriterium:** Besuchermeldung Erfolg; Telegram-Nachricht; Eintrag in `/api/inquiries`. Wenn Notify fehlschlägt, bleibt KV-Erfolg für den Besucher erhalten (im Log: `INQUIRY_STORED_BUT_NOTIFY_FAILED`).

---

## Slack-Alternative

1. Slack **Incoming Webhook** für den gewünschten Kanal erstellen.
2. Production: `INQUIRY_WEBHOOK_URL` = Webhook-URL.
3. Redeploy (Schritt 4), dann Notify-Test (Schritt 5).

---

## Viewer (letzte Anfragen ohne wrangler)

**Auth Pflicht:** `INQUIRY_VIEW_TOKEN` (oder Fallback `INQUIRY_DIAG_TOKEN`). Ohne Secret → **503** `auth_not_configured`. Falsches/fehlendes Token → **401**. **Nie** Inquiry-Daten ohne gültiges Token.

```http
GET https://boksitsupport.ch/api/inquiries?token=SECRET&limit=20
```

oder Header: `Authorization: Bearer SECRET`

- Default `limit` 20, Maximum 50
- Secrets nicht gesetzt → **503** `auth_not_configured`
- Falsches/fehlendes Token → **401**
- KV nicht gebunden → **503** `kv_not_bound`

curl:

```powershell
curl.exe "https://boksitsupport.ch/api/inquiries?token=$env:INQUIRY_VIEW_TOKEN&limit=20"
# oder:
curl.exe "https://boksitsupport.ch/api/inquiries?limit=20" `
  -H "Authorization: Bearer $env:INQUIRY_VIEW_TOKEN"
```

```powershell
.\scripts\list_inquiries.ps1 -Token $env:INQUIRY_VIEW_TOKEN -Limit 20
```

Optional: `-BaseUrl "https://boksitsupport.ch"`

---

## Health check

```http
GET https://boksitsupport.ch/api/inquiry-health
```

Öffentlich (Booleans only): `ok`, `hasKv`, `hasResendKey`, `hasWebhook`, `hasTelegram`, `hasPushNotify`.

Keine Secrets, Tokens, Chat-IDs oder Inquiry-Inhalte. `hasPushNotify` ist `true`, sobald Telegram **oder** Webhook **oder** Resend gesetzt ist.

Wenn `INQUIRY_DIAG_TOKEN` gesetzt ist: `?token=…` mitgeben (sonst 401).

---

## Fallback-Verhalten (technisch)

- KV-Schreiben ist der primäre Erfolgspfad für den Besucher.
- Push-Notify (Telegram/Webhook/Resend) läuft danach; Fehler werden geloggt und **setzen den Besuchererfolg nicht zurück**, wenn KV ok ist.
- Formular-Client: bei API-Fehler **keine** Erfolgsmeldung, Felder bleiben, Mailto-Alternative wird angeboten.

---

## Was Stefan selbst erledigen muss

Cursor/Deploy kann den Telegram-Bot und die privaten Secrets nicht für Sie anlegen.

1. Bot + `chat_id` (Schritte 1–2).
2. Secrets in Cloudflare Production für Projekt **`website`** (Schritt 3).
3. Redeploy (Schritt 4).
4. Notify-Test + ein echter Formular-Test (Schritte 5–6).
