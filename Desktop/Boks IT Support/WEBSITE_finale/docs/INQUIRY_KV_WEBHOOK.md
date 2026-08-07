# Inquiry delivery – KV + push notify + optional Resend

**Push notify is mandatory for ops.** KV stores leads durably, but Stefan is **not** alerted unless Telegram and/or a webhook (or Resend) is configured. Setup: **[INQUIRY_NOTIFY.md](./INQUIRY_NOTIFY.md)**.

**No FormSubmit.** Delivery paths only:

| Path | Config | Role |
|------|--------|------|
| **KV `INQUIRY_LOG`** | Binding in `wrangler.toml` | Primary durable store (TTL ~12 months) → visitor HTTP 200 when write succeeds |
| **Telegram** | `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` | Immediate operator notify (recommended) |
| **Webhook** | `INQUIRY_WEBHOOK_URL` | Slack Incoming Webhook / Discord / generic JSON |
| **Resend** | optional `RESEND_API_KEY` | Optional email when key present |

`POST /api/inquiry` returns **200** when at least one durable path succeeds (KV preferred).  
Push notify runs **after** KV; notify failure is **logged** and does **not** fail the visitor if KV wrote.  
JSON includes `stored`, `notified`, `notifyVias`.  
If no durable path is configured → **503** `delivery_not_configured`.

## Health

```
GET /api/inquiry-health
→ { "ok": true, "hasKv": true, "hasResendKey": false, "hasWebhook": false, "hasTelegram": false, "hasPushNotify": false }
```

## Viewer

Protected list without wrangler CLI — see [INQUIRY_NOTIFY.md](./INQUIRY_NOTIFY.md):

```
GET /api/inquiries?token=SECRET&limit=20
```

Requires `INQUIRY_VIEW_TOKEN` (or fallback `INQUIRY_DIAG_TOKEN`).

## KV

- Binding: `INQUIRY_LOG`
- Namespace id: see `wrangler.toml`
- `expirationTtl`: `60 * 60 * 24 * 365` (~12 months), aligned with privacy retention.

## Client

Browser submits only to `/api/inquiry`. Mailto fallback on failure. No third-party form endpoints.
