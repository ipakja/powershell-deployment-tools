# Inquiry push notify (Telegram / Slack) + KV viewer

**Mandatory for ops:** KV alone stores leads; Stefan is **not** notified unless push notify is configured. Set Telegram (recommended) or Slack before relying on the form in production.

**No FormSubmit.** Paths: Cloudflare KV (`INQUIRY_LOG`) + Telegram and/or webhook + optional Resend.

Full delivery model: see [INQUIRY_KV_WEBHOOK.md](./INQUIRY_KV_WEBHOOK.md).

---

## Telegram (recommended)

Exact steps:

1. Talk to [@BotFather](https://t.me/BotFather) on Telegram → create a bot → copy the bot **token**.
2. Message your new bot once (any text). Then open  
   `https://api.telegram.org/bot<TOKEN>/getUpdates`  
   in the browser and copy your **chat_id** from the JSON (`message.chat.id`).
3. Cloudflare Dashboard → **Workers & Pages** → project **`website`** → **Settings** → **Environment variables** → **Production**:
   - `TELEGRAM_BOT_TOKEN` = *(bot token from BotFather)*
   - `TELEGRAM_CHAT_ID` = *(numeric chat id)*
4. Redeploy the site, or wait for the next deploy so Production picks up the vars.
5. Test with a **real form submit** from the phone or browser on  
   `https://boksitsupport.ch/de/anfrage/`  
   You should get a Telegram message; the visitor still sees success if KV wrote even when notify fails (failures are logged).

Optional (same Production env):

| Variable | Purpose |
|----------|---------|
| `INQUIRY_VIEW_TOKEN` | Secret for listing recent inquiries (see Viewer below) |
| `INQUIRY_DIAG_TOKEN` | Optional gate for `/api/inquiry-health`; also fallback auth for the viewer if `INQUIRY_VIEW_TOKEN` is unset |
| `INQUIRY_WEBHOOK_URL` | Slack/Discord/generic webhook (alternative or addition to Telegram) |
| `RESEND_API_KEY` | Optional email notify |

---

## Slack alternative

1. Create a Slack **Incoming Webhook** for the channel that should receive leads.
2. In Cloudflare Pages → project **`website`** → Settings → Environment variables → Production:
   - `INQUIRY_WEBHOOK_URL` = *(Incoming Webhook URL)*
3. Redeploy / wait, then submit a real test inquiry.

Discord webhooks and generic JSON endpoints also work via `INQUIRY_WEBHOOK_URL`.

---

## Viewer (list recent inquiries without wrangler)

1. Set `INQUIRY_VIEW_TOKEN` in Production to a **long random secret** (e.g. 32+ chars).
2. List recent leads:

```http
GET https://boksitsupport.ch/api/inquiries?token=SECRET&limit=20
```

Or with header: `Authorization: Bearer SECRET`

- Default `limit` is 20; maximum is 50.
- Wrong/missing token → **401**
- KV not bound → **503**
- Response: `{ ok, count, items: [{ key, receivedAt, requestId, company, contact, email, area, start, description, … }] }`

### PowerShell helper

```powershell
.\scripts\list_inquiries.ps1 -Token "SECRET" -Limit 20
```

Optional: `-BaseUrl "https://boksitsupport.ch"`

---

## Health check

```http
GET https://boksitsupport.ch/api/inquiry-health
```

Returns booleans only (no secrets):

`hasKv`, `hasResendKey`, `hasWebhook`, `hasTelegram`, `hasPushNotify`

`hasPushNotify` is true if webhook **or** Telegram **or** Resend is configured.

If `INQUIRY_DIAG_TOKEN` is set, pass `?token=…`.

---

## What Stefan must do himself

Cursor / deploy cannot create your Telegram bot or set private secrets for you.

1. Create the bot with BotFather and obtain `chat_id`.
2. Enter `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` (and `INQUIRY_VIEW_TOKEN`) in the Cloudflare Dashboard for project **`website`** / Production.
3. Redeploy if vars do not apply immediately.
4. Send one real test from the phone and confirm Telegram + `/api/inquiries`.
