# Strategie-Analyse BIT – Service-Operator vs. Ist-Zustand

**Dokumentstatus:** Analyse only (kein Produktions-Content geändert)  
**Stand der Quellen:** `config/de_v2.json`, `config/en_v2.json`, `config/site.json`, gebaute Seiten unter `de/` / `en/`, Legal `de/legal/`, Templates `templates/v2/base.html`, Build `scripts/build_v2_de.py`  
**Realität / Gate:** **Kein verbindlicher Partner vorhanden → Zustand A.**  
**Leitregel (absolut):** *BIT darf nicht zu einem Job werden, den Stefan sich selbst gebaut hat.*

BIT soll besitzen: Marke, Kunden, Verträge, Prozesse, Partnernetz, Daten, Automation, Marge.  
Partner erbringen spezialisierte Arbeit im Hintergrund (White Label).  
Nicht das Produkt: Freelancer-Stunden, Helpdesk-Persönlichkeit, Vor-Ort-Techniker, «M365-Spezialist Stefan», blosse Ticket-Weiterleitung.

**Empfehlungs-Tags in diesem Dokument:**

| Tag | Bedeutung |
|---|---|
| **heute umsetzbar** | Ohne Partnervertrag möglich (Text, Struktur, Qualifikation, Preise zurücknehmen, Prozesse/Automation vorbereiten) |
| **nach Partner** | Braucht mindestens einen verbindlichen, white-label-fähigen Fachpartner (oder belastbare Ersatzstruktur) |

---

## A. Soll-Modell vs. Ist-Signale

### A1. Soll: Service-Operator / White-Label-Owner

| BIT besitzt | Partner liefert |
|---|---|
| Marke & Kundenschnittstelle | Spezialisierte Ausführung hinter der Marke |
| Vertrag & Rechnung | Kapazität / Facharbeit nach BIT-Auftrag |
| Prozess, Freigaben, Dokumentation | Keine eigene Kundenbeziehung zum Endkunden |
| Daten & Automation | Austauschbare Rolle (partner-swappable) |
| Marge (Produktisierung, wiederkehrend) | Keine «Stefan verkauft Stunden»-Ökonomie |

Kunde soll denken: *ein organisierter Anbieter unter einer Marke* — nicht: *BIT reicht Tickets weiter* und nicht: *Stefan ist mein persönlicher IT-Mitarbeiter*.

### A2. Ist: Zustand A mit starken Freelancer-/Personen-Signalen

| Dimension | Befund | Beleg |
|---|---|---|
| Gate | Zustand A, begrenzter Einführungsbetrieb | `config/de_v2.json` → `"state": "A"`; Home: «BIT prüft derzeit ausgewählte Anfragen im Rahmen eines begrenzten Einführungsbetriebs.» |
| Vertragspartner = Person | «Vertragspartner bleibe ich» | `config/de_v2.json` → `role.contract`; Legal: «Vertragspartner bleibe ich — als Einzelunternehmen.» (`de/legal/index.html`) |
| Ich-Perspektive About | Mehrfach «Ich …» | `about.body`: «Ich kenne operative Abläufe…»; «Ich arbeite als operativer Ansprechpartner…»; «Als Einzelunternehmen bin ich Ihr Ansprechpartner…» |
| Stundenpreis als Leitpreis | CHF 120 / Stunde prominent | `prices.hourly`: «CHF 120»; FAQ: «Richtwerte (Arbeitszeit CHF 120 pro Stunde)»; `de/leistungen/index.html`: «Arbeitszeit: CHF 120 pro Stunde» |
| Dual-Path Anfrage | WhatsApp/E-Mail als «am schnellsten», Formular sekundär | `direct_path.intro`: «Am schnellsten geht es so…»; `form_heading`: «Oder über das Formular»; Closing CTA «Per WhatsApp schildern» |
| Fachperson beigezogen | Koordination/Beizug formuliert, **ohne** benannten Partner | FAQ: «ob eine geeignete externe Fachperson beigezogen werden kann.»; Home partner: «Wird für ein Spezialthema zusätzliche Fachkompetenz benötigt…» |
| Kein Partnervertrag | Kein Name, kein SLA, kein White-Label-Nachweis im Repo | Durchsucht: `config/`, `docs/` — kein verbindlicher Partner |

**Gap-Kurzfazit:** Die Seite beschreibt bereits Koordination und schriftlichen Rahmen (Operator-nahe), verkauft und signalisiert aber gleichzeitig **persönliche Stundenarbeit + persönliche Erreichbarkeit** (Freelancer-/Job-für-sich-selbst). Das widerspricht dem wirtschaftlichen Soll (Marge + Standardisierung + wiederkehrend + Partner + Automation).

### A3. Warnpunkte (Pflicht)

#### 1) Preissignal

| Signal | Ort | Quote / Wert |
|---|---|---|
| Stundenansatz | `config/de_v2.json` → `prices.hourly`; `config/site.json` → `prices.hourly` | **CHF 120** |
| Basischeck | `prices.small_job`; UI `from_small_job` | **CHF 190** / «IT-Basischeck ab CHF 190» |
| FAQ-Verstärkung | `faq.items` (Preise) | «Arbeitszeit CHF 120 pro Stunde» + Basischeck ab CHF 190 |
| Leistungen-Panel | `de/leistungen/index.html` | «Arbeitszeit: CHF 120 pro Stunde» |
| Altlast Site | `config/site.json` | zusätzlich `zurich_travel`: **CHF 35**, Market-Pilot **CHF 4'900** (nicht v2-Hauptfokus, aber noch in Site-Config) |

**Konflikt:** CHF 120/h positioniert BIT als **Verkauf von Stefans Zeit**. Das untergräbt Pakete, wiederkehrende Retainer und Operator-Marge.  
**Basischeck CHF 190:** als klar abgegrenzter Einstieg näher am Produkt — aber als «ab CHF 190» neben Stundenpreis wirkt er wie Einstiegsjob, nicht wie Produktfamilie.

| Empfehlung | Tag |
|---|---|
| Stundenpreis **CHF 120 von öffentlichen Flächen entfernen oder stark zurückstufen** (FAQ/Leistungen-Panel), solange das Modell Operator heisst; verbindliche Preise nur in Offerte | **heute umsetzbar** |
| Basischeck **behalten als begrenztes Zustand-A-Produkt**, aber als «schriftlicher Einstieg / Befund» ohne Stunden-Narrativ; Preishöhe erst nach Marge-Inputs finalisieren | **heute umsetzbar** (Text); Preishöhe final **nach Partner** / nach Marge-Rechnung |
| CHF 35 / CHF 4'900 in `site.json` nicht wieder in die IT-Hauptseite ziehen | **heute umsetzbar** |

**Wann entfernen vs. behalten (Entscheidungshilfe):**

- **Entfernen (öffentlich):** Stundenpreis, sobald die Kommunikation «Service-Operator / organisierte Leistung» heisst — sonst dominiert das Freelancer-Signal.
- **Behalten (Zustand A):** Basischeck-Festpreis *oder* «nach schriftlicher Prüfung» ohne Zahl, wenn Marge unklar.
- **Erst nach Partner + Marge:** Pakete / Retainer / «ab CHF X / Monat» mit Leistungsgrenzen.

#### 2) Erreichbarkeit

| Signal | Quote |
|---|---|
| Footer | «Für eine Bedarfsabklärung nutzen Sie den Direktweg per WhatsApp oder E-Mail, oder das Anfrageformular.» (`footer_channels_note`) |
| Anfrage Direct | «Am schnellsten geht es so» + WhatsApp/E-Mail vor Formular (`direct_path`) |
| Offline-Texte | «erreichen Sie mich derzeit direkt…» (`footer_channels_note_offline`, `inquiry.offline_banner`) |
| Closing | «Per WhatsApp schildern» + «Rückmeldung in der Regel innerhalb von zwei Arbeitstagen.» |

**Konflikt:** Persönliche Sofortkanäle als Primärweg skalieren nicht und machen Stefan zum Helpdesk.  
**Operative Tatsache:** Dual-Path (Formular + WhatsApp/Telefon/E-Mail) ist heute live — Analyse bewertet das als **Betriebsfakt**, nicht als strategisches Ziel.

| Empfehlung | Tag |
|---|---|
| Primärziel der Website: **B2B qualifizieren** für produktisierbare Leistungen; WhatsApp/Telefon als Fallback im Footer, nicht als «am schnellsten»-Hero der Conversion | **heute umsetzbar** |
| Response-Erwartung an Prozess koppeln («Prüfung Eingang → schriftliche Einschätzung»), nicht an persönliche Erreichbarkeit als USP | **heute umsetzbar** |
| Nach Partner: Intake-Automation / Ticketsystem hinter BIT-Marke, Partner ohne Kundentelefon | **nach Partner** |

#### 3) Vertrauensbasis (ohne Partner- und Kundenfälle)

Was in Zustand A **halten** kann:

| Stütze | Beleg | Bewertung |
|---|---|---|
| Pilot-/Einführungsbanner | «begrenzten Einführungsbetriebs» | ehrlich, passend Zustand A |
| Musterfälle (explizit keine Referenzen) | `examples.note`: «Musterabläufe, keine dokumentierten Kundenfälle.»; `examples_page.lead` analog | stark — behalten |
| Schriftlicher Rahmen / Grenzen | Limits, Scope-Notes, «kein Auftrag durch Formular» | stark |
| Klarer B2B-Fit / No-Fit | `audience.fit` / `nofit` (keine Privatpersonen, kein 24/7) | stark |
| Person + SIZ als Hintergrund | About / Credentials | nur **low-key**; nicht als Produkt |

Was **nicht** vortäuschen:

- benannte Partner, SLAs, «Team», Kundenlogos, erfundene Case Studies  
- «Wir»-Sprache ohne Organisation dahinter  

| Empfehlung | Tag |
|---|---|
| Vertrauen über Prozess, Grenzen, Musterfälle, Pilot-Klarheit — nicht über erfundene Partner | **heute umsetzbar** |
| Sobald Partner verbindlich: White-Label-Fähigkeit kommunizieren («BIT bleibt Vertragspartner; Fachausführung nach Absprache») ohne Partnernamen, bis Freigabe | **nach Partner** |

#### 4) Marge (Zahlen nötig vor Paketen)

Ohne diese Inputs keine seriösen öffentlichen Pakete:

| Input | Warum |
|---|---|
| Ziel-Deckungsbeitrag pro Auftrag / Monat | Operator ≠ Stundenverkauf |
| Interne Zeit Stefan (Intake, QA, Doku, Abrechnung) in Minuten pro Standardfall | zeigt, was standardisierbar ist |
| Partner-Einkaufspreis bzw. Kapazitätskosten (sobald vorhanden) | White-Label-Kalkulation |
| Ausschuss / Nacharbeit / Wartezeit auf Kundemitwirkung | Realität Zustand A |
| Fixkosten (Versicherung, Tools, Domains, Buchhaltung) | Untergrenze Retainer |
| Zahlungsziel / Ausfallrisiko (AGB: 30 Tage) | Cashflow |

| Empfehlung | Tag |
|---|---|
| Interne Marge-Tabelle führen (nicht auf der Website) bevor «Pakete» live gehen | **heute umsetzbar** |
| Öffentliche Paketpreise erst nach belastbarer Kalkulation + Partnerkapazität | **nach Partner** (oder nach klarer Solo-Kapazitätsgrenze mit bewusstem Cap) |

### A4. Kommunikations-Constraints (Regeln für künftige Texte — hier nicht verletzt)

1. **Keine erfundenen Partner**, keine erfundenen Kundenfälle, keine Fake-SLAs.  
2. **Kein «Wir»**, solange Organisation/Team nicht real ist — Marke «BIT» / neutrale Formulierung.  
3. **Zustand A-Sprache:** Prüfung, ausgewählte Anfragen, Einführungsbetrieb, schriftlicher Rahmen.  
4. **Hotellerie** = Erfahrungsbeispiel im Hintergrund, nicht Alleinstellungs-Zielgruppe.  
5. **SIZ** low-key (Credentials), nicht Hero.  
6. **Musterfälle bleiben Muster** — Label behalten.  
7. **Schweizer ss** in DE-Texten.  
8. **Impressum / Rechtsform** nicht kosmetisch «lösen» ohne Bestätigung.  
9. Kunde darf nicht denken: *BIT leitet nur Tickets weiter* — Delivery unter einer Marke, organisiert.  
10. Wirtschaftliches Narrativ: **nicht** «Stefan verkauft Stunden», sondern Rahmenleistung / produktisierbare Services.

---

## B. Was BIT besitzen muss vs. was Partner tun

| BIT (Owner) | Partner (White Label) | Heute im Content |
|---|---|---|
| Marke, Anfrage, Qualifikation | — | Anfrage + Direct-Path vorhanden |
| Vertrag, Offerte, Abrechnung | — | «Vertragspartner bleibe ich» (Person) — rechtlich Zustand A ok, strategisch als *Brand-Owner* formulieren | 
| Prozess / Freigaben / Doku | Ausführung Spezialfälle | Process-Steps + Freigabe-FAQ vorhanden |
| Kundendaten & Automation | Kein Direktkontakt Endkunde | Formular/KV — Automation ausbaubar **heute umsetzbar** |
| Marge & Produktkatalog | Kapazität nach Auftrag | Preise = Stunden → Konflikt |
| Partnernetz austauschbar | Spezialarbeit | Nur hypothetische «Fachperson» — **nach Partner** |

**Empfehlung:** Rolle so schärfen, dass `role.owns` (Aufnahme, Strukturierung, Koordination…) das **Produkt** ist; technische Ausführung als austauschbare Schicht. Tag: Textschärfung **heute umsetzbar**; echte Austauschbarkeit **nach Partner**.

---

## C. Freelancer- / Job-für-sich-selbst-Inventar (mit Pfad + Zitat)

| # | Signal | Datei | Zitat |
|---|---|---|---|
| C1 | Ich als Vertragspartner | `config/de_v2.json` → `role.contract` | «Vertragspartner bleibe ich.» |
| C2 | Ich-About | `config/de_v2.json` → `about.body[0–2]` | «Ich kenne…»; «Ich arbeite als operativer Ansprechpartner…»; «Als Einzelunternehmen bin ich Ihr Ansprechpartner…» |
| C3 | EN analog | `config/en_v2.json` → `role.contract` | «I remain the contractual counterparty.» |
| C4 | Stundenpreis | `config/de_v2.json` → `prices.hourly` | «CHF 120» |
| C5 | Stunden in FAQ | `config/de_v2.json` → FAQ Preise | «Arbeitszeit CHF 120 pro Stunde» |
| C6 | Leistungen-Panel | `de/leistungen/index.html` | «Arbeitszeit: CHF 120 pro Stunde» |
| C7 | Persönliche Erreichbarkeit | `inquiry.offline_banner` | «erreichen Sie mich bitte direkt per E-Mail» |
| C8 | WhatsApp als Speed-Path | `direct_path.intro` | «Am schnellsten geht es so» |
| C9 | Legal Ich-Form | `de/legal/index.html` (AGB-Eckpunkte / Haftung / Datenschutz) | «Vertragspartner bleibe ich»; «erstelle ich»; «damit ich Ihren Bedarf einschätzen…» |
| C10 | Lead = Person | `about.lead` | «Stefan Bogdanovic · Inhaber und zentrale Ansprechperson» |
| C11 | Trust-Block Person | `home.trust_block.text` | «Stefan Bogdanovic, Zürich. Operative Erfahrung aus Hotel- und Rezeptionsumfeld.» |

**Gegengewichte (bereits Operator-nah — behalten/ausbauen):**

| Signal | Datei | Zitat |
|---|---|---|
| Ein Vertragspartner-Abschnitt | `home.partner` | «BIT nimmt Ihr Anliegen auf… bleibt Ihr Ansprechpartner… Sie verhandeln nicht mit mehreren Anbietern…» |
| Role owns | `role.owns` | «Aufnahme, Strukturierung, Koordination, Kommunikation, Dokumentation, Nachverfolgung und Abrechnung.» |
| Grenzen | `limits.items` | keine 24/7, keine unbegrenzten Pauschalen, nichts ausserhalb des Umfangs |
| Muster statt Referenzen | `examples.note` | «Musterabläufe, keine dokumentierten Kundenfälle.» |
| Kein Auftrag durch Formular | `inquiry.notice` / `home.cta_subline` | «Durch das Formular entsteht noch kein Auftrag.» |

---

## D. Preissignal – Entscheidungslogik

```
Öffentlicher Stundenpreis CHF 120
        │
        ├─ Signal an Kunde: «Ich kaufe Stefans Stunde»
        ├─ Erschwert Retainer / Pakete / Automation-Marge
        └─ Empfehlung: von Marketing-Flächen nehmen  → heute umsetzbar

Basischeck CHF 190
        │
        ├─ Passt zu bounded / remote / wiederholbar
        ├─ Preis ggf. zu tief relativ zu Intake-Zeit (Marge prüfen)
        └─ Behalten als Zustand-A-Einstieg ODER «Festpreis nach Kurzklärung» → heute umsetzbar (Text); Zahl final nach Marge
```

**Nicht** vor Marge-Inputs: Mehrpakete «Benutzerverwaltung monatlich CHF X» öffentlich erfinden.

---

## E. Erreichbarkeit als USP – warum das scheitert

| Skala | Effekt bei «mich direkt / WhatsApp zuerst» |
|---|---|
| 1 Kunde | funktioniert, fühlt sich premium-persönlich an |
| 10 Kunden | Kontextverlust, Abend-/Wochenenddruck, Qualitätsrisiko |
| 50 Kunden | Helpdesk-Job; Operator-Modell tot |

Die Website maximiert heute implizit **Kanalvolumen** (`direct_path` «am schnellsten», Footer Direct, WhatsApp-Buttons in Closing via `cta_block(..., include_whatsapp=True)` in `scripts/build_v2_de.py`).

| Empfehlung | Tag |
|---|---|
| Conversion-Hierarchie: Formular (qualifiziert) > E-Mail-Vorlage > WhatsApp nur Fallback | **heute umsetzbar** |
| Keine Versprechen «jederzeit erreichbar»; bestehende «zwei Arbeitstage» beibehalten/schärfen | **heute umsetzbar** |

---

## F. Vertrauen ohne Partner und ohne Kundenfälle

**Haltbare Vertrauenspfeiler Zustand A:**

1. Ehrlicher Pilot-Rahmen (`pilot_banner` / `about.pilot`)  
2. Musterfälle mit Label (`/de/beispiele/`)  
3. Schriftlichkeit vor Start (Process + FAQ Freigaben)  
4. Explizite No-Fits (Privat, 24/7, kritische Infrastruktur)  
5. Sicherheitslinie Formular (`inquiry.security` — keine Passwörter)  

**Nicht haltbar / riskant:** «Fachperson beigezogen» so lesen, als existiere bereits ein Netz → immer als *Möglichkeit nach Prüfung* belassen, bis Vertrag existiert (**nach Partner** für stärkere Formulierung).

---

## G. Marge – Mindest-Inputs vor Produktkatalog

Vor öffentlichen Paketen intern klären (nicht auf Site publizieren):

1. Soll-Marge % nach Partnerkosten  
2. Stefan-Minuten je Standardfall (Eintritt / Austritt / Outlook-Muster / Basischeck)  
3. Max. parallele Aufträge ohne Qualitätsverlust (Cap Zustand A)  
4. Tooling-Kosten Automation  
5. Haftpflichtdeckung / Selbstbehalt (Betriebsrisiko)  

Ohne 1–3: **keine** Retainer-Preise live. Tag: Kalkulation **heute umsetzbar**; skalierende Pakete **nach Partner**.

---

## H. Leistungsportfolio – Preferenzraster

Bevorzugen, was **remote, bounded, wiederholbar, white-label-fähig, partner-swappable** ist:

| Leistung (Ist) | Remote | Bounded | Repeatable | WL-fähig | Bewertung vs. Operator |
|---|---|---|---|---|---|
| Benutzer & Zugänge | ja | ja (mit Freigaben) | hoch | hoch | **Kernprodukt** — ausbauen |
| M365 & Arbeitsplatz (Standard) | ja | mittel (Störungen variieren) | mittel | mittel–hoch | behalten als **Standardfälle**; Tiefentechnik Partner |
| IT-Basischeck | ja | hoch | hoch | mittel (Analyse oft in-house) | guter Zustand-A-Einstieg |
| Vor-Ort Zürich | nein | mittel | niedrig | niedrig | Ausnahme, nicht USP (`travel_line`) |
| Unbegrenzter Support / 24/7 | — | nein | — | — | korrekt ausgeschlossen (`limits`) |

| Empfehlung | Tag |
|---|---|
| Messaging: «organisierte Standardfälle unter BIT», nicht «M365-Spezialist» als Produktname der Marke | **heute umsetzbar** |
| Checklisten/Automation für Eintritt/Austritt (BIT-owned Process Assets) | **heute umsetzbar** |
| Partner-Playbooks für Spezialfälle hinter derselben Kundensprache | **nach Partner** |

---

## I. Zustand A vs. Zustand B – Kommunikationsregeln

| | Zustand A (heute, kein Partner) | Zustand B (nach verbindlichem Partner) |
|---|---|---|
| Angebot | Ausgewählte Anfragen, Prüfung, begrenzter Betrieb | Skalierbare Standardprodukte + klarere Kapazität |
| Partner-Sprache | «kann nach Absprache beigezogen werden» — hypothetisch | «BIT bleibt Vertragspartner; Ausführung nach internen Qualitätsregeln» (ohne Ticket-Forwarder-Optik) |
| Preise | Richtwerte sparsam / Basischeck; Stundenpreis kritisch | Pakete/Retainer nach Marge |
| Vertrauen | Muster + Prozess + Pilot | optional Referenzen **nur mit Freigabe**; Partner ungenannt oder freigegeben |
| «Ich» | rechtlich Einzelunternehmen ok; strategisch zurücknehmen zugunsten Marke BIT | Marke dominant; Inhaber im Impressum/About, nicht als Helpdesk-USP |
| Erreichbarkeit | Formular primär anstreben | Intake-System; Kanäle entkoppelt von Ausführung |

Kein Sprung A→B in Texten vortäuschen.

---

## J. Positionierung: Hotellerie, SIZ, Muster, B2B-Qualifikation

### J1. Hotellerie

| Ist | Quote |
|---|---|
| Trust/About | «Operative Erfahrung aus Hotel- und Rezeptionsumfeld» |
| FAQ | «Arbeitet BIT nur mit Hotels?» → «Nein. Hotels und Rezeption sind ein Erfahrungsbeispiel.» |

**Soll:** Hintergrundkompetenz, **nicht** alleinige Zielbranche. Ziel: kleinere Unternehmen ohne IT (Fit-Liste). Tag Anpassung Gewichtung **heute umsetzbar**.

### J2. SIZ

| Ist | `about.credentials`: «ICT Professional SIZ – Systems & Network», «ICT Power-User SIZ» |
|---|---|
| `siz_comment` | leer |

**Soll:** low-key behalten, nicht Hero/H1. Tag: **heute umsetzbar** (keine Aufwertung nötig).

### J3. Musterfälle

Bereits korrekt gelabelt (`examples.note`, `examples_page.lead`, Teaser «Musterfälle statt Referenzen»). **Regel:** Label nie streichen zugunsten unechter Referenzen. **heute umsetzbar** = Status halten.

### J4. Website-Ziel ≠ WhatsApp-Volumen

| Soll laut Brief | Ist |
|---|---|
| B2B für produktisierbare Services qualifizieren | Dual-Path: WhatsApp/E-Mail als schnellster Weg + Formular |
| Nicht primär Kanalvolumen maximieren | Footer + Closing pushen Direktkanäle |

**Empfehlung:** Qualifikationsfragen des Formulars (`form.*` Employees, M365, Area, Start) als Hauptpfad stärken; Direct-Path als operative Notbrücke kennzeichnen. Tag: **heute umsetzbar**.

### J5. «Kein Ticket-Forwarder»

Risiko-Formulierungen:

- FAQ: Bearbeitung «oder … Fachperson beigezogen»
- Service-Steps: «bearbeiten oder … koordinieren»

Das ist operator-kompatibel **nur wenn** BIT Ownership (Briefing, Freigabe, QA, Doku, einzige Kundenschnittstelle) klar bleibt — Home-`partner`-Text ist dafür die beste Vorlage. Schärfen **heute umsetzbar**; echte Multi-Partner-Delivery **nach Partner**.

---

## K. Skalierung 1 / 10 / 50 Kunden

| Last | Wenn Ist-Modell (Stunden + persönliche Kanäle) | Wenn Operator-Soll |
|---|---|---|
| **1** | Machbar; Qualität hoch; Lerneffekt Musterfälle | Intake-Prozess und Checklisten härten |
| **10** | Stefan = Engpass; WhatsApp-Chaos; Marge = Stunden | Standardfälle produktisieren; Cap kommunizieren; Partner für Spitzen **nötig** |
| **50** | Scheitert oder wird reiner Job | Automation + ≥1 White-Label-Partner + Retainer; Stefan = QA/Owner nicht Dispatcher |

| Massnahme | Tag |
|---|---|
| Öffentliches Cap / Pilot-Banner beibehalten bis Prozesse sitzen | **heute umsetzbar** |
| Interne Kapazitätsgrenze (z. B. parallele Aufträge) festlegen | **heute umsetzbar** |
| Partnervertrag + Playbooks vor Wachstum >~10 | **nach Partner** |
| Automation (Status, Vorlagen, Checklisten) | **heute umsetzbar** starten |

---

## Priorisierte Massnahmenliste (nur Analyse — keine Site-Änderung hier)

| Prio | Massnahme | Tag |
|---|---|---|
| 1 | Stundenpreis CHF 120 von öffentlichen Flächen entfernen/zurückstufen | **heute umsetzbar** |
| 2 | Anfrage-Hierarchie: Formular vor WhatsApp; «Am schnellsten» entschärfen | **heute umsetzbar** |
| 3 | Ich-/Helpdesk-Ton zugunsten Marke BIT reduzieren (About/Role/Legal-Eckpunkte später mit AGB abstimmen) | **heute umsetzbar** |
| 4 | Operator-Ownership-Satz schärfen (kein Forwarder-Lesart) | **heute umsetzbar** |
| 5 | Interne Marge-Tabelle + Kapazitäts-Cap | **heute umsetzbar** |
| 6 | Ersten White-Label-Partner vertraglich binden | **nach Partner** |
| 7 | Retainer/Pakete öffentlich | **nach Partner** (+ Marge) |
| 8 | Partner-sichtbare Delivery ohne Kundenschnittstelle Partner | **nach Partner** |

---

## Kurzfazit (Executive)

Die Site ist **Zustand A** und hat bereits Operator-Bausteine (ein Vertragspartner, schriftlicher Rahmen, Limits, Musterfälle, B2B-No-Fits). Gleichzeitig dominieren **Freelancer-Signale**: CHF 120/h, Ich-Perspektive, persönliche Erreichbarkeit und WhatsApp-First. Das driftet zu «Job für Stefan», nicht zu Owner von Marke/Prozess/Marge. Ohne Partner keine erfundenen Kapazitätsversprechen; mit den **heute umsetzbaren** Text-/Pfadkorrekturen kann die Kommunikation dem Service-Operator-Soll angenähert werden, bevor **nach Partner** skaliert wird.

---

*Ende Analyse. Keine produktionsseitigen Content-Änderungen durch dieses Dokument.*
