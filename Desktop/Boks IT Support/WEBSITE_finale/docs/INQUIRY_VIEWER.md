# Inquiry HTML Viewer (bookmarkable)

**Recommended ops path:** WhatsApp/mailto direct + form → KV + this HTML viewer bookmark.  
Push notify (Telegram / Resend / webhook) remains optional in code; it is **not** required for daily lead checks.

## Bookmark URL (Stefan)

```
https://boksitsupport.ch/api/inquiries/view?token=TOKEN_PLACEHOLDER&format=html
```

(`format=html` is optional on this path — the endpoint always returns HTML. Keep `token=` in the query so the URL is bookmarkable.)

JSON for scripts remains at:

```
https://boksitsupport.ch/api/inquiries?token=TOKEN_PLACEHOLDER&limit=20
```

## Auth

| Situation | Result |
|-----------|--------|
| `INQUIRY_VIEW_TOKEN` (or fallback `INQUIRY_DIAG_TOKEN`) not set | **503** |
| Missing or wrong token | **401** |
| Valid token | HTML list, newest first |

Token via query `?token=` (primary). `Authorization: Bearer …` also works.

**Do not share the bookmark URL.** Anyone with the token can read inquiry data.

## Generate a secure token

PowerShell:

```powershell
$bytes = New-Object byte[] 32
[System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
($bytes | ForEach-Object { $_.ToString("x2") }) -join ""
```

Use 32+ random bytes (64 hex chars). Store only as a Cloudflare secret — never in public git.

## Set the secret (Cloudflare Pages → project `website`)

**Dashboard**

1. [Cloudflare Dashboard](https://dash.cloudflare.com/) → **Workers & Pages** → project **`website`**
2. **Settings** → **Environment variables** / Variables and Secrets
3. Environment: **Production**
4. Add secret name: `INQUIRY_VIEW_TOKEN` → paste the token → Save

**Wrangler (local, logged in)**

```powershell
# Pipe the token (Windows). Prefer Dashboard if stdin is awkward.
npx wrangler pages secret put INQUIRY_VIEW_TOKEN --project-name website
```

## Redeploy required

After setting or rotating the secret:

```powershell
npx wrangler pages deploy . --project-name website --branch=main
```

or `deploy.bat`.

**Success criterion:** Opening the bookmark URL shows the HTML viewer (header with 7-day count). Without token → 503 or 401. Wrong token → 401.

## What the viewer shows

- Count of entries in the **last 7 days**
- Date/time of the **newest** inquiry
- Per entry: datetime, company, contact, business email (`mailto:`), phone (`tel:`), location/canton, industry, employees, workstations, M365, internal IT, external IT, area, start, description, language version (or —)
- Entries newer than **48 hours** are visually highlighted
- Mobile-first, no horizontal scroll, no framework, `noindex` / `nofollow`, `Cache-Control: no-store`

## Related

- Direct WhatsApp/mailto: [INQUIRY_DIRECT.md](./INQUIRY_DIRECT.md)
- Optional Telegram / Resend: [INQUIRY_NOTIFY.md](./INQUIRY_NOTIFY.md)
- Resend DNS later: [RESEND_GOLIVE.md](./RESEND_GOLIVE.md)
- Ops overview: [BETRIEB.md](./BETRIEB.md)
