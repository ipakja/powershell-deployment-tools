# Public site cleanup (crawlers & Search Console)

## What we fixed
- Build no longer emits crawlable hospitality/market HTML (`de/hospitality`, `de/markt`, and all language equivalents).
- After Zustand-A (`build_v2`), those folders are deleted from the deploy root so Cloudflare Pages cannot serve old static bodies ahead of redirects.
- Inactive locale trees (`fr/`, `it/`, `sr/`, `bs/`, `hr/`) are **deleted entirely** after build — no stub HTML in deploy.
- `_redirects` + `functions/_middleware.js`: root `/` → `/de/` (301); market slugs → `/de/` or `/en/` **directly** (no archive hop); hospitality → Leistungen/Services; inactive locales → `/de/` (302).
- www → apex 301.
- Sitemap: DE + EN current routes only (no hospitality, no markt, no market-access, no FR/IT/…).
- No public Market Access HTML (noindex stub not needed — path removed, 301 only).
- HTML `_headers`: `no-cache, no-store, must-revalidate` + `CDN-Cache-Control: no-store`, plus CSP / nosniff / Referrer-Policy / Permissions-Policy.
- robots.txt: `Allow: /`, sitemap URL set; admin blocked.

## Market Access redirect table (301, direct to home)

| From | To | Code |
|------|----|------|
| `/de/market-access` | `/de/` | 301 |
| `/de/market-access/` | `/de/` | 301 |
| `/en/market-access` | `/en/` | 301 |
| `/en/market-access/` | `/en/` | 301 |
| `/de/markt` | `/de/` | 301 |
| `/de/markt/` | `/de/` | 301 |
| `/en/market` | `/en/` | 301 |
| `/en/market/` | `/en/` | 301 |
| `/fr/marche` | `/de/` | 301 |
| `/fr/marche/` | `/de/` | 301 |
| `/it/mercato` | `/de/` | 301 |
| `/it/mercato/` | `/de/` | 301 |
| `/sr/trziste` | `/de/` | 301 |
| `/sr/trziste/` | `/de/` | 301 |
| `/bs/trziste` | `/de/` | 301 |
| `/bs/trziste/` | `/de/` | 301 |
| `/hr/trziste` | `/de/` | 301 |
| `/hr/trziste/` | `/de/` | 301 |

Sources of truth: `_redirects` (written by `scripts/build_v2_de.py` → `write_redirects()`) and `functions/_middleware.js` (`MARKET_SLUGS` → lang home).

## Cloudflare cache (required after deploy)

Wrangler Pages has no one-click “purge everything” for the custom domain cache. Sticky CDN responses are the most common reason a re-audit still shows the old dual-gateway or old EN tiles.

**Stefan — after each cleanup deploy:**
1. Cloudflare Dashboard → **Caching** → **Configuration** → **Purge Everything** for zone `boksitsupport.ch` (preferred), **or**
2. Caching → **Custom Purge** for at least:
   - `https://boksitsupport.ch/`
   - `https://boksitsupport.ch/de/`
   - `https://boksitsupport.ch/en/`
   - `https://boksitsupport.ch/fr/`
   - `https://boksitsupport.ch/it/`
   - `https://www.boksitsupport.ch/`
   - `https://www.boksitsupport.ch/de/`
   - `https://boksitsupport.ch/de/hospitality/`
   - `https://boksitsupport.ch/de/markt/`
   - `https://boksitsupport.ch/de/market-access/`
   - `https://boksitsupport.ch/de/legal/`
   - `https://boksitsupport.ch/sitemap.xml`

Also hard-refresh the browser (or use a private window) after purge.

## Google Search Console (required)
1. Property: `https://boksitsupport.ch` (Domain property preferred).
2. **Sitemaps** → submit `https://boksitsupport.ch/sitemap.xml`.
3. **URL inspection** → request indexing for:
   - `https://boksitsupport.ch/de/`
   - `https://boksitsupport.ch/en/`
   - `https://boksitsupport.ch/de/leistungen/`
   - `https://boksitsupport.ch/de/legal/`
4. For old URLs (`/de/hospitality/`, `/de/markt/`, `/de/market-access/`, `/fr/`): inspect → confirm redirect; do not request indexing of old paths.
5. Optional: **Removals** only if Google still shows stale snippets after redirects propagate (temporary hide).

## Local verify before/after deploy
```bat
python scripts\build_site.py
pytest scripts\test_build_v2.py -q
curl.exe -sI -H "Cache-Control: no-cache" -A Googlebot https://boksitsupport.ch/
curl.exe -sI -H "Cache-Control: no-cache" -A Googlebot https://boksitsupport.ch/en/
curl.exe -sI -H "Cache-Control: no-cache" -A Googlebot https://boksitsupport.ch/fr/
curl.exe -sI -H "Cache-Control: no-cache" -A Googlebot https://boksitsupport.ch/de/markt/
curl.exe -sI -H "Cache-Control: no-cache" -A Googlebot https://boksitsupport.ch/de/market-access/
```
Expect: `/` → **301** `/de/`; `/en/` → **200** IT-support home (no Hospitality/Market tiles); `/fr/` → **302** `/de/`; `/de/markt/` and `/de/market-access/` → **301** `/de/`.
