# Inquiry notify (optional) + KV + HTML viewer

**Standard ops path (recommended):** WhatsApp/mailto direct + form → Cloudflare KV (`INQUIRY_LOG`) + **HTML viewer bookmark** — see [INQUIRY_VIEWER.md](./INQUIRY_VIEWER.md).

Push notify (Telegram / Slack webhook / Resend) stays in the codebase for later use. It is **optional** and **not** the recommended daily path.

**No FormSubmit.**

**Parallel zero-backend path:** WhatsApp / mailto templates — [INQUIRY_DIRECT.md](./INQUIRY_DIRECT.md). Keep both; do not remove the form.

Full delivery model: [INQUIRY_KV_WEBHOOK.md](./INQUIRY_KV_WEBHOOK.md).

---

## Viewer (recommended)

Bookmark (replace placeholder after setting the secret):

```
https://boksitsupport.ch/api/inquiries/view?token=TOKEN_PLACEHOLDER
```

Setup steps and success criteria: **[INQUIRY_VIEWER.md](./INQUIRY_VIEWER.md)**.

JSON for scripts:

```powershell
.\scripts\list_inquiries.ps1 -Token "SECRET" -Limit 20
```

---

## Robustness

- KV write without push notify → visitor success (**OK**)
- When KV is bound: storage failure → **no** visitor success (502)
- KV TTL ≈ 12 months — aligned with privacy retention wording
- Notify failure after successful KV → logged (`INQUIRY_STORED_BUT_NOTIFY_FAILED`); visitor still sees success

---

## Optional: Telegram (code present, not recommended now)

Telegram remains implemented (`TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`). Prefer the HTML viewer unless you explicitly want push messages.

### Schritt A — Bot anlegen

1. [@BotFather](https://t.me/BotFather) → `/newbot`
2. Copy bot token → secret `TELEGRAM_BOT_TOKEN`

### Schritt B — Chat-ID

1. Message the bot once
2. Open `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Note `message.chat.id` → secret `TELEGRAM_CHAT_ID`

### Schritt C — Secrets + redeploy

Cloudflare → Workers & Pages → **`website`** → Settings → Production secrets, then redeploy.

### Schritt D — Notify-Test (no KV write)

```http
POST https://boksitsupport.ch/api/inquiry-notify-test
Authorization: Bearer <INQUIRY_VIEW_TOKEN>
```

Success: `"ok":true,"stored":false,"notified":true` and a Telegram message.

---

## Optional: Slack webhook

Set `INQUIRY_WEBHOOK_URL` (Incoming Webhook), redeploy, run notify-test.

---

## Optional: Resend

- **Without own domain verify:** `from: onboarding@resend.dev` can send **only** to the Resend account owner email. Usable as a short test; not production-grade for arbitrary recipients.
- **Production to any mailbox:** verify `boksitsupport.ch` in Resend — DNS **Proxy DNS only** (grey cloud). See [RESEND_GOLIVE.md](./RESEND_GOLIVE.md).

Secrets (when ready): `RESEND_API_KEY`, optional `INQUIRY_FROM`, `INQUIRY_TO`.

---

## Health check

```http
GET https://boksitsupport.ch/api/inquiry-health
```

Public booleans only: `ok`, `hasKv`, `hasResendKey`, `hasWebhook`, `hasTelegram`, `hasPushNotify`.

---

## What Stefan does himself

1. Generate `INQUIRY_VIEW_TOKEN` and set it on Production for project **`website`** ([INQUIRY_VIEWER.md](./INQUIRY_VIEWER.md)).
2. Redeploy.
3. Bookmark the HTML viewer URL (keep private).
4. Optional later: Telegram / Resend.
5. Ana 5-second test — [5-SEKUNDEN-TEST.md](./5-SEKUNDEN-TEST.md).
