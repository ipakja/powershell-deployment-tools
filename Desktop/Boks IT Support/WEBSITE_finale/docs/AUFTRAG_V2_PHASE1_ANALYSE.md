# Abschlussbericht Phase 1 – Analyse Auftrag v2

## 1. Zustands-Gate

**Ergebnis: Zustand A (Pilot- und Bedarfsabklärungsseite)**

| Kriterium | Befund | Beleg |
|---|---|---|
| 1 Rechtsform | **NEIN** | `locales/*/legal_page.entity_type` = „Rechtsform beziehungsweise selbstständiger Status wird derzeit geklärt“; keine UID/HR; `registration` sagt „auf Anfrage“ |
| 2 Partner | **NEIN** | Kein benannter, vertraglich abgesicherter Partner in `config/`, `locales/`, README |

Default Zustand A gilt. Alle Texte der Umsetzung müssen Pilot-/Prüfsprache verwenden.

---

## 2. Ist-Architektur

| Aspekt | Ist |
|---|---|
| Stack | Statisches HTML/CSS/JS, Build `scripts/build_site.py`, Content `config/path_content.json` + `locales/*.json`, Cloudflare Pages `website` |
| Routing | Gateway `/{lang}/` mit **zwei Kacheln** (Hospitality + Market Access) |
| Pfade A | `/{lang}/hospitality/` (7 Sprachen) |
| Pfade B | `/de/markt/`, `/en/market/`, `/fr/marche/`, `/it/mercato/`, `/{sr\|bs\|hr}/trziste/` |
| Shared | `/{lang}/about/`, `/{lang}/legal/` |
| Formular | **keines** (README: bewusst kein Formular; Kontakt WhatsApp/Viber/E-Mail/Telefon auf Service-Seiten) |
| Framework | Kein React/Next – reine Templates |

Auftrag-Sollstruktur (`/leistungen/`, `/anfrage/`, …) **existiert nicht**. Umbau = neue Templates + Build-Erweiterung, kein Framework-Wechsel nötig.

---

## 3. Market-Access-Inventar (nicht löschen)

| Typ | Pfade / Quellen |
|---|---|
| Gateway-Kachel B | `config/path_content.json` → `gateway.*.market_*`; gerendert in `templates/gateway.html` → `/{lang}/index.html` |
| Marktseiten HTML | `de/markt/`, `en/market/`, `fr/marche/`, `it/mercato/`, `sr|bs|hr/trziste/` |
| Content | `path_content.json` → `*.market` (Pilot CHF 4'900, Unterlagen-Check CHF 190, Sample-Block, Deliverables) |
| Preise zentral | `site.json` → `prices.pilot`, `pilot_payment` |
| Brand/Schema | `site.json` → `brand` enthält „Market Access Switzerland“ |
| Locales (Altlast) | `locales/*.json` Hero/Services mit Markteintritt-Keywords |
| About | `about_text` erwähnt „BIT Market Access Switzerland“ / Pilotmandate |
| Legal activity | „Schweizer Marktentwicklung und Vertretung…“ |
| README | „Swiss Market Development & Representation“ |
| Redirects | `_redirects` (keine Market-spezifischen Alt-URLs ausser Sprach-Slugs) |

**Empfehlung Umsetzung:** Content behalten unter Archiv-Slug z. B. `/de/market-access/` (301 von alten Slugs), aus Gateway und Hauptnav entfernen.

---

## 4. Widersprüche zum Auftrag v2

| Thema | Ist | Soll v2 |
|---|---|---|
| Startseite | 50/50 Weiche IT + Market | Ein Geschäftsmodell, IT-Koordination |
| Positionierung | Hospitality/PMS + KMU-IT + Market Pilot | Benutzer-/Zugangs-/Arbeitsplatz-Koordination |
| CTA | WhatsApp/Viber dominant | Formular primär; Kanäle nur Footer |
| Preise | CHF 120 / 190 / 35 / 4'900 live | Zustand A: nur bestätigte Preise; Pilot-Framing |
| Sprachen | 7 live mit alter Positionierung | Phase 1 nur DE fertig; andere nicht halb online lassen |
| SIZ | Auftrag nennt SIZ | **nicht** im Repo hinterlegt → Bestätigung nötig |
| Formular | fehlt | `/anfrage/` Pflicht |

---

## 5. Bestätigungen vor Veröffentlichung (Stefan)

1. Rechtsform / AHV / Rechnung / Haftpflicht (Launch-Blocker)
2. SIZ-Abschlüsse: welche genau, öffentlich nennbar?
3. Preise CHF 120 / 190 / 35: in Zustand A belassen oder nur „nach Absprache“?
4. CHF 4'900 Market-Pilot: archivieren / entfernen aus Sichtbarkeit?
5. Formular-Backend: Cloudflare Pages Functions + E-Mail? Resend? Formspree? (kein unnötiger Drittanbieter)
6. EN/FR/IT/SR/BS/HR: deaktivieren (Redirect auf DE) oder offline lassen?
7. Hotels/PMS-Unterseite behalten als `/de/hospitality/` Archiv oder streichen?

---

## 6. Launch-Blocker (rechtlich)

- AHV-/Selbstständigkeitsstatus
- Rechnungsstellung und steuerliche Behandlung
- Haftpflichtversicherung
- Vertrags-/Haftungsfragen bei Zugangsdaten
- Datenschutz bei Formular + Zugangsdaten
- Impressum erst nach Klärung anpassen (keine kosmetische „Lösung“)
