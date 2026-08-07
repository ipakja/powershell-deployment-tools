# Betrieb – BIT Website (boksitsupport.ch)

Kurzreferenz für den laufenden Betrieb.

## Live

- Production: Cloudflare Pages Projekt **`website`**, Branch **`main`**
- Domain: `https://boksitsupport.ch` (www → apex 301)

## Leadweg (Standard)

1. Besucher: WhatsApp/mailto **oder** Formular `/de/anfrage/` / `/en/inquiry/`
2. Formular → `POST /api/inquiry` → KV `INQUIRY_LOG` (TTL ~12 Monate)
3. Stefan prüft Leads über HTML-Viewer-Bookmark: siehe [INQUIRY_VIEWER.md](./INQUIRY_VIEWER.md)

Push (Telegram/Resend/Webhook) = optional, Code vorhanden.

## Secrets (Production)

| Name | Pflicht für Viewer | Zweck |
|------|-------------------|--------|
| `INQUIRY_VIEW_TOKEN` | ja | Auth Viewer + Notify-Test |
| `INQUIRY_DIAG_TOKEN` | optional | Fallback-Auth |
| `TELEGRAM_*` | nein | Optional Push |
| `RESEND_API_KEY` | nein | Optional E-Mail |
| `INQUIRY_WEBHOOK_URL` | nein | Optional Slack/Discord |

Nach Secret-Änderung: **Redeploy**.

## Deploy

```powershell
cd "C:\Users\41765\Desktop\Boks IT Support\WEBSITE_finale"
python scripts\build_site.py
python -m pytest scripts\test_build_v2.py functions\api\test_inquiry_contract.py -q
npx wrangler pages deploy . --project-name website --branch=main --commit-dirty=true
```

## Health

`https://boksitsupport.ch/api/inquiry-health` — nur Booleans, keine Secrets.

## Docs

| Doc | Inhalt |
|-----|--------|
| [INQUIRY_VIEWER.md](./INQUIRY_VIEWER.md) | Bookmark, Token, Auth |
| [INQUIRY_NOTIFY.md](./INQUIRY_NOTIFY.md) | Optional Push |
| [INQUIRY_DIRECT.md](./INQUIRY_DIRECT.md) | WhatsApp/mailto |
| [RESEND_GOLIVE.md](./RESEND_GOLIVE.md) | Resend Test + DNS |
| [5-SEKUNDEN-TEST.md](./5-SEKUNDEN-TEST.md) | Ana-Test |
| [ABSCHLUSSBERICHT_FINAL.md](./ABSCHLUSSBERICHT_FINAL.md) | Abschluss |
