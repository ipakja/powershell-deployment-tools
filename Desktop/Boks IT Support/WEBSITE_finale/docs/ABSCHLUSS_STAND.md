# Abschlussstand Website (2026-08-07)

## Fertig (live geprüft)

| Punkt | Status |
|---|---|
| Root `/` → `/de/` | 301 |
| `/de/` neues Modell | OK |
| `/en/` neues Modell | OK |
| FR/IT/SR/BS/HR | 302 → `/de/` |
| Market/Hospitality alt | 301 auf aktuelle Seiten |
| FormSubmit | entfernt |
| Lead-Zustellung | Cloudflare KV (TTL ~12 Monate) |
| `inquiry.live` | **true** |
| CTA | „IT-Anliegen prüfen lassen“ |
| 3 Produkte + Basischeck ab CHF 190 | OK |
| Beispiele `/de/beispiele/` | OK |
| Privacy ohne „dauerhaft“ / ohne Env-Namen | OK |
| HTML Cache-Control | no-store / must-revalidate |
| Viber im Footer | entfernt |
| JSON-LD ProfessionalService + FAQPage | OK |
| Tests | 20 grün |

## Zustellung klar

- Absendung → Validierung → **KV-Write** = Erfolg für den Nutzer  
- E-Mail nur, wenn später `RESEND_API_KEY` gesetzt ist  
- Optional Webhook: `INQUIRY_WEBHOOK_URL`  
- Health: `https://boksitsupport.ch/api/inquiry-health`

**Aktuell:** Anfragen kommen **nicht** als E-Mail – sie liegen in KV.

## Nur Stefan (nicht Website-Code)

1. Cloudflare Cache ggf. noch einmal „Purge Everything“
2. Google Search Console: Sitemap + Reindex `/de/`, `/de/leistungen/`, `/de/legal/`
3. Resend (Domain + Key), wenn E-Mail-Notify gewünscht
4. Google-Business-Profil
5. 5-Sekunden-Test mit Ana
6. Partnervertrag / AHV-Status / echte Cases – ausserhalb der Website
7. Aufbewahrungs-/Rechtsfragen bei Bedarf mit Fachperson

## Deploy

```powershell
python scripts/build_site.py
echo n | npx wrangler pages deploy . --project-name=website --branch=main --commit-dirty=true
```
