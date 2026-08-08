# Inquiry direct path (WhatsApp / mailto)

Zero-backend lead capture runs **in parallel** with the form.

## Direct path (no backend)

On `/de/anfrage/` and `/en/inquiry/`:

1. **WhatsApp** — `wa.me` link with a pre-filled message template (company, contact, location, employees, M365, topic, start).
2. **E-Mail** — `mailto:` with subject and the same body template.

Visitors complete the placeholders and send. Nothing is stored in KV for this path.

Number and mailbox come from `config/site.json` (`whatsapp_url`, `email`) — currently WhatsApp `41782632701`, email `admin@boksitsupport.ch`.

Visible email addresses use the harvest-protection pattern (`data-contact="email"` + `data-email-user` / `data-email-domain`); the direct **E-Mail** button builds `mailto:` in JavaScript (`data-direct-mailto`) so Cloudflare Email Obfuscation cannot strip the pre-filled subject/body.

The homepage closing CTA (`#cta`) keeps the primary form button and adds the same WhatsApp button as secondary.

## Form path

The inquiry form posts to `/api/inquiry` → Cloudflare KV (`INQUIRY_LOG`).  
Stefan checks leads via the HTML viewer bookmark — [INQUIRY_VIEWER.md](./INQUIRY_VIEWER.md).  
Telegram / webhook / Resend remain optional — [INQUIRY_NOTIFY.md](./INQUIRY_NOTIFY.md).
