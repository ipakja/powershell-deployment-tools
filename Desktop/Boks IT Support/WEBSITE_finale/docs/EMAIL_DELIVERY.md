# E-Mail / Inquiry delivery

| Path | Status | Role |
|------|--------|------|
| **KV `INQUIRY_LOG`** | Binding gesetzt | Dauerhafter Store (primär), TTL ~12 Monate |
| **Webhook** | optional `INQUIRY_WEBHOOK_URL` | Optionaler zweiter dauerhafter Pfad |
| **Resend API** | optional `RESEND_API_KEY` | E-Mail nur wenn Key gesetzt |

HTTP **200**, wenn **mindestens ein dauerhafter Pfad** (KV / Webhook / Resend) gelingt.
`emailQueued: true|false` zeigt, ob Resend die Mail angenommen hat.

**FormSubmit.co ist entfernt** und wird nicht mehr verwendet.

## Diagnose

`GET /api/inquiry-health` → `hasResendKey`, `hasKv`, `hasWebhook`

## Resend (optional Upgrade)

Siehe `docs/RESEND_GOLIVE.md`. Ohne Key bleibt KV der verbindliche Store.
