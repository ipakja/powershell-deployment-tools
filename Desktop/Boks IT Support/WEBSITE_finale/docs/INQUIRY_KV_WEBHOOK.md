# Inquiry delivery – KV + HTML viewer + optional push

**Standard ops:** KV stores leads; Stefan checks them via the **HTML viewer** — [INQUIRY_VIEWER.md](./INQUIRY_VIEWER.md).  
Push notify (Telegram / webhook / Resend) is **optional**.

**No FormSubmit.** Delivery paths:

| Path | Config | Role |
|------|--------|------|
| **KV `INQUIRY_LOG`** | Binding in `wrangler.toml` | Primary durable store (TTL ~12 months) → visitor HTTP 200 when write succeeds |
| **HTML viewer** | `INQUIRY_VIEW_TOKEN` | Bookmarkable review of recent leads |
| **Telegram** | `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` | Optional push (code kept) |
| **Webhook** | `INQUIRY_WEBHOOK_URL` | Optional Slack / Discord / JSON |
| **Resend** | optional `RESEND_API_KEY` | Optional email (domain DNS for production) |

`POST /api/inquiry` returns **200** when KV write succeeds (KV bound).  
When KV is bound, storage failure → **no** visitor success.  
Push runs after KV; notify failure is **logged** and does **not** fail the visitor if KV wrote.  
If no durable path is configured → **503** `delivery_not_configured`.

## Health

```
GET /api/inquiry-health
→ { "ok": true, "hasKv": true, "hasResendKey": false, "hasWebhook": false, "hasTelegram": false, "hasPushNotify": false }
```

## Viewer

```
GET /api/inquiries/view?token=TOKEN_PLACEHOLDER
GET /api/inquiries?token=TOKEN_PLACEHOLDER&limit=20
```

Requires `INQUIRY_VIEW_TOKEN` (or fallback `INQUIRY_DIAG_TOKEN`).

## KV

- Binding: `INQUIRY_LOG`
- Namespace id: see `wrangler.toml`
- `expirationTtl`: `60 * 60 * 24 * 365` (~12 months), aligned with privacy retention.

## Client

Browser submits only to `/api/inquiry`. Mailto fallback on failure. No third-party form endpoints.
