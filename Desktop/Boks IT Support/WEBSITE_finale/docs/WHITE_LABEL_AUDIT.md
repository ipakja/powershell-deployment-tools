# White-Label-Audit BIT (Analyse only)

**Stand:** 2026-08-08  
**Scope:** Repo `WEBSITE_finale` + Live-Fetch `https://boksitsupport.ch` mit `Cache-Control: no-cache`  
**Status:** Analyse und Umbauplan — **keine** Produktiv-Codeänderungen, **kein** Deploy, **kein** Commit durch diesen Audit.  
**Gate:** `"state": "A"` in `config/de_v2.json` / `config/en_v2.json` — kein verbindlicher White-Label-Partner im Repo belegt.  
**Oberste Regel:** BIT darf nicht zu einem Job werden, den der Inhaber sich selbst gebaut hat.

**Quellen (primär):**
- `config/de_v2.json`, `config/en_v2.json`, `config/site.json`
- Gebaute Seiten `de/**`, `en/**` (Live 200 OK, inhaltlich deckungsgleich mit Repo-HTML)
- Abgleich: `docs/STRATEGIE_ANALYSE.md`
- Bereits verbessert: Commit `629b1bb` — `/de/fuer-unternehmen/` Richtung What → Whom

**Ana-Klarheitstest (Kriterien):**
1. Zuerst konkrete Leistungen, dann Zielgruppe («was, dann für wen»).
2. Keine abstrakte Frame-/Framework-/Scope-Beratungssprache als Leitidee.
3. Unternehmensgrösse und Alltagssituationen verständlich (5–50, M365/Windows, keine interne IT).

**Spaltenbedeutung:**
- **KLASSISCHER-IT-SUPPORT-EINDRUCK:** Besucher denkt primär «persönlicher Techniker / Stundenhilfe».
- **WHITE-LABEL-KOMPATIBEL:** Text/Struktur unterstützt «Leistung bei BIT kaufen; BIT organisiert; Facharbeit kann hinter der Marke laufen» — ohne erfundene Partner.

---

## Executive Summary

Die Live-Site ist **Zustand A** mit mehreren **bereits guten Operator-Bausteinen** (drei Servicefamilien, Musterfälle ohne Kundenfiktion, Partner-Block ohne Partnernamen, No-Fits als «aktuelles Standardangebot», Prozessschritte). Gleichzeitig dominieren **Freelancer- und klassische IT-Support-Signale**: H1 «IT-Support», öffentlicher Stundenpreis **CHF 120**, Ich-Ton («Vertragspartner bleibe ich»), WhatsApp-First-CTA, Personenhero auf «Über BIT».

**Ana-Klarheit:** `/de/fuer-unternehmen/` (nach `629b1bb`) besteht den Test weitgehend (Leistungen vor Fit). Die **Startseite und der globale H1/Meta** bestehen ihn nicht: Marke und erster Viewport lesen sich wie klassischer IT-Support; Services kommen erst nach Hero, Anliegen und Problemkarten.

**Abnahme §20 heute:** 5-Sekunden-Satz teilweise («IT für KMU»), aber mit Techniker-Bias. 30-Sekunden-Satz («ich kaufe bei BIT, Fachpartner möglich») ist angelegt im Partner-Block, wird aber durch CHF 120/h, Ich-Ton und H1 «IT-Support» überdeckt.

---

## Part 1 — Audit-Tabelle

| SEITE / ABSCHNITT | AKTUELLER TEXT (kurz, Zitat) | PROBLEM | ANA-KLARHEITSTEST BESTANDEN JA/NEIN | KLASSISCHER-IT-SUPPORT-EINDRUCK JA/NEIN | WHITE-LABEL-KOMPATIBEL JA/NEIN | EMPFOHLENE ÄNDERUNG |
|---|---|---|---|---|---|---|
| **Start — Hero** `/de/` | H1: «IT-Support für kleine Unternehmen ohne eigene IT»; Lead: «…Benutzerkonten, Microsoft 365, Zugängen und wiederkehrenden Arbeitsplatzproblemen»; Trust: «ca. 5–50 Mitarbeitenden» (`home.h1` / live) | Kategorie «IT-Support» + Zielgruppe vor Serviceprodukt; klingt nach Techniker-Marke | **NEIN** (Audience/Kategorie zuerst, nicht «wir bieten X/Y») | **JA** | **NEIN** | H1 Richtung «Digitale Betriebsservices / Benutzer-, Zugangs- und Arbeitsplatzservices…»; Lead: 3 Servicefamilien + «BIT organisiert»; Zielgruppe eine Zeile darunter |
| **Start — Meta/Title** | `meta_title`: «IT-Support für kleine Unternehmen…» | SEO/Tab verstärkt Support-Label | **NEIN** | **JA** | **NEIN** | Title/Description auf Servicekatalog + KMU, ohne «IT-Support» als Leitwort |
| **Start — Eyebrow** | «IT-Koordination für Zürich und remote…» | «Koordination» allein kann Vermittler klingen; besser nach Services | Teilweise | Nein | Teilweise | Nach Hero-Services belassen oder «Service für Zürich / remote CH» |
| **Start — Outcome** | «klaren Ansprechpartner, schriftlich vereinbarten Umfang, dokumentierten Abschluss» | Operator-nah, aber «Umfang»-Last; ok als Ergebniszeile | Teilweise | Nein | **JA** (Richtung) | Behalten; «vereinbarter Service / Leistungsrahmen» statt Dauer-«Umfang»-Jargon |
| **Start — Pilot** | «begrenzten Einführungsbetriebs» | Passend Zustand A | **JA** (ehrlich) | Nein | **JA** | Behalten |
| **Start — Typische Anliegen** | «Outlook oder Microsoft 365 funktioniert…»; «neuer Mitarbeiter…» | Gut konkret, aber **vor** Serviceblock → Reihenfolge falsch vs. Soll §15 | **NEIN** (Reihenfolge) | Teilweise (Outlook-Störung = Helpdesk) | Teilweise | Nach Servicekarten verschieben; Formulierungen als «Service-Situationen» |
| **Start — Problem-Karten** | «Outlook, Drucker und Rechtefragen bleiben liegen» | Verstärkt klassischen Support; kommt vor Services | **NEIN** | **JA** | **NEIN** | Kürzen/streichen oder nach «Warum BIT»; Drucker nicht im Hero-Pfad |
| **Start — Services** | «Drei klare Einstiege» + 3 Karten Benutzer / M365 / Basischeck | Inhalt Ana-nah; Intro mischt Zielgruppe + Umfang-Sprache vor Nutzen | **JA** (Inhalt) / Reihenfolge auf Home zu spät | Teilweise (M365-Karte «Alltagsstörungen») | Teilweise → **JA** nach Textfeile | Block direkt unter Hero; Intro: «BIT bietet diese Services für kleinere Unternehmen»; Benefit-first |
| **Start — Preis-Hinweis** | «IT-Basischeck ab CHF 190» | Festpreis ok; Stundenpreis nicht hier — gut | **JA** | Nein | **JA** | Behalten; Stundenpreis nicht auf Home nachziehen |
| **Start — Vertragspartner** | «Ein Vertragspartner, ein Ansprechpartner… Wird für ein Spezialthema zusätzliche Fachkompetenz benötigt, wird das vorab besprochen» | Sehr WL-nah, Zustand-A-konform (keine erfundenen Partner) | **JA** | Nein | **JA** | Behalten; optional expliziter: «Sie beauftragen BIT — nicht mehrere Anbieter» |
| **Start — Limits** | «keine 24/7…» | Gut; steht vor Prozess — ok | **JA** | Nein | **JA** | Behalten; Titel «Aktueller Standardservice nicht gedacht für…» (Ana §10) |
| **Start — Ablauf (Teaser)** | 5 Schritte inkl. «Bearbeitung koordinieren» | WL-fähig; «koordinieren» ohne «Vermittlung»-Klarstellung riskant | Teilweise | Nein | Teilweise | Schritt 4: «Service ausführen bzw. freigegebene Facharbeit steuern» |
| **Start — Wer dahintersteht** | «Stefan Bogdanovic, Zürich…» | Personen-Signal im Kernpfad; Job-für-sich-selbst | **NEIN** (Personen vor Produktlogik) | **JA** | **NEIN** | Auf `/ueber-bit/` belassen; Home: «Warum BIT» (6 Punkte Soll §8), Person nur kurz |
| **Start — CTA** | Primary «IT-Anliegen prüfen lassen»; WhatsApp «Per WhatsApp schildern» | CTA ok; WhatsApp-First = Freelancer-Erreichbarkeit | Teilweise | **JA** (Messenger-Helpdesk) | **NEIN** | Primary Formular; WhatsApp sekundär/Footer; CTA-Text «Bedarf prüfen lassen» |
| **Leistungen Index** `/de/leistungen/` | H1 «Drei klare Einstiege»; Panel «Arbeitszeit: CHF 120 pro Stunde» | CHF 120 = Zeitverkauf Stefan | Teilweise (Services klar) | **JA** | **NEIN** | Stundenpreis entfernen/zurückstufen; Festpreis/Paketrhetorik; H1 «Services für kleinere Unternehmen» |
| **Leistung Benutzer & Zugänge** | Benefit «Eintritt bereit…»; Steps inkl. «oder … mit der zuständigen Fachstelle koordinieren» | Inhalt stark; «Fachstelle» Zustand-A-ok | **JA** | Nein | **JA** | Leicht: Kundenergebnis-Satz Ana §5A; Ich-Ton vermeiden |
| **Leistung M365 & Arbeitsplatz** | «Outlook, Teams, Windows, Drucker… Alltagsstörungen» | Drift zu klassischem Break/Fix | Teilweise | **JA** | Teilweise | Auf «standardisierte Arbeitsplatzprozesse» schärfen; Drucker/Reparatur-Ton dämpfen; klar: Standardfälle im Serviceprozess, nicht «Stefan repariert» |
| **Leistung IT-Basischeck** | «Ab CHF 190 als Festpreis-Einstieg»; «Kein Cybersecurity-Audit» | Festpreis + Abgrenzung gut | **JA** | Nein | **JA** | Behalten; als Assessment-Produkt führen |
| **Beispiele** `/de/beispiele/` | Lead: «illustrative Musterfälle und keine Kundenreferenzen»; Steps mit Fachstelle | Struktur Soll §13 weitgehend erfüllt; «Zustand A»-Hinweis live **nicht** mehr im Kunden-HTML | **JA** | Nein | **JA** | Behalten; vierte Karte «Anbieterzuständigkeit» auf Home-Teaser prüfen (Vermittler-Risiko) |
| **Ablauf** `/de/so-funktioniert-es/` | «Anliegen schildern → … koordinieren → dokumentieren» | Fehlt explizit: Kunde→BIT→ggf. Fachpartner→QA→Abschluss | Teilweise | Nein | Teilweise | Diagramm/Absatz Soll §15.5; «kein Weiterleiten der Kundenbeziehung» |
| **Für Unternehmen** `/de/fuer-unternehmen/` | Nach `629b1bb`: «Typische Leistungen» vor Fit; No-Fit «Ausserhalb des aktuellen Standardangebots»; Role: «Vertragspartner bleibe ich» | **Bereits gut** What→Whom; H1 noch Audience-first; Ich-Satz; Bullet «Übergabe an … Fachpartner» kann wie Vermittlung wirken | **JA** (Seitenlogik) / H1 teilweise | Nein (ausser Ich-Satz) | Teilweise | H1 service-first; «Übergabe» → «Facharbeit innerhalb des BIT-Service, BIT bleibt Vertragspartner»; Ich → BIT |
| **Über BIT** `/de/ueber-bit/` | H1 = «Stefan Bogdanovic · Inhaber…»; Body «Ich kenne…», «Vertragspartner bleibe ich» | Stärkstes Freelancer-Signal | **NEIN** | **JA** | **NEIN** | Seite: Marke/Prozess/Qualität zuerst; Person als Inhaber/QA; rechtlich Einzelunternehmen belassen, Ton «BIT» |
| **FAQ** | Preise: «Arbeitszeit CHF 120 pro Stunde»; Technik: «externe Fachperson beigezogen werden kann» | Stundenpreis; sonst Zielgruppe/Limits gut | Teilweise | **JA** (Preis-FAQ) | Teilweise | Preis-FAQ ohne Stundenleitpreis; Partner-FAQ Zustand-A-Formulierung beibehalten |
| **Anfrage** `/de/anfrage/` | Notice Einführungsbetrieb; «Per WhatsApp schildern» prominent | Formular gut; WhatsApp gleichwertig = Helpdesk | Teilweise | **JA** | Teilweise | Formular primary; WhatsApp optional; Copy «Servicebedarf prüfen» |
| **AGB** `/de/agb/` | 6.1 «Abrechnung nach Aufwand zum jeweils gültigen Stundenansatz» | Rechtlich ok; stützt Stundenmodell wahrnehmung | n/a (Recht) | Teilweise | Teilweise | Später Klauseln für Festpreis/Pakete vorbereiten; öffentlich nicht mit CHF 120 verdoppeln |
| **Legal / Datenschutz** `/de/legal/` | «IT-Support für kleine…»; «Vertragspartner bleibe ich»; WhatsApp-Hinweis | Support-Label + Ich; Datenschutz WhatsApp transparent (gut) | Teilweise | **JA** (Label) | Teilweise | Positionsbeschreibung an neue H1 anpassen; Ich wo möglich institutionell |
| **EN Home** `/en/` | H1 «IT support for small businesses…»; Preise/WhatsApp analog | Gleiche Strukturprobleme wie DE | **NEIN** | **JA** | **NEIN** | Parallel zu DE umbauen (eine Content-Quelle) |
| **EN Services / Examples / How it works / For businesses / About / FAQ / Inquiry / Terms / Legal** | Spiegel von DE (`en_v2.json`); About «I remain the contractual counterparty»; FAQ hourly CHF 120 | Parität: gleiche Freelancer-Signale | wie DE | wie DE | wie DE | Immer DE+EN synchron aus `*_v2.json` |
| **Navigation** | Start, Leistungen, Beispiele, Ablauf, Für Unternehmen, Über BIT, FAQ, Anfrage | Vollständig; «IT-Support» nicht in Nav — gut | **JA** | Nein | **JA** | Optional Nav-Label «Services»; «Über BIT» nicht übergewichten |
| **Footer** | «Direktweg per WhatsApp oder E-Mail, oder das Anfrageformular» | WhatsApp vor Formular genannt | Teilweise | **JA** | **NEIN** | Reihenfolge: Formular → E-Mail/Telefon → WhatsApp optional |
| **Preise (global)** | `prices.hourly`: «CHF 120»; `small_job`: «CHF 190»; `site.json` zusätzlich travel/pilot | Stundenpreis öffentlich = Anti-WL | **NEIN** (Ana will konkrete Services, nicht Stundensatz) | **JA** | **NEIN** | CHF 120 von öffentlichen Flächen; CHF 190 Assessment behalten oder «ab / nach Prüfung»; Pakete später ohne Erfindung |
| **CTAs (global)** | `cta_primary`: «IT-Anliegen prüfen lassen»; Secondary Leistungen; Closing + WhatsApp | «IT-Anliegen» = Ticket-Sprache | Teilweise | Teilweise | Teilweise | «Bedarf prüfen lassen» / «Service anfragen»; WhatsApp nicht primary |

### Bereits gut (nicht «kaputt reden»)

| Block | Warum behalten |
|---|---|
| Drei Servicekarten (Benutzer, M365/Workplace, Basischeck) | Entspricht Ana §5 A–C |
| `/de/fuer-unternehmen/` Reihenfolge Leistungen → Fit → No-Fit (`629b1bb`) | What → Whom |
| No-Fit-Titel «Ausserhalb des aktuellen Standardangebots» | Ana §10, erweiterbar später |
| Partner-Home-Block ohne Partnername/-netzwerk | Zustand A korrekt |
| Beispiele-Lead ohne «Zustand A»-Interna | Soll §13 |
| Pilot-/Einführungsbanner | Ehrlichkeit Zustand A |
| FAQ «Wer führt technische Änderungen aus?» (Prüfung vor Beizug) | Keine erfundenen Kapazitäten |

### Verbleibende Freelancer-Signale (Inventar)

| Signal | Beleg |
|---|---|
| CHF 120 / Stunde | `config/de_v2.json` → `prices.hourly`; FAQ; `de/leistungen/index.html` Preispanel; `config/site.json` |
| H1 «IT-Support…» | `home.h1`, live `/de/`, `/en/` |
| Ich-Ton / «Vertragspartner bleibe ich» | `role.contract`, `about.body`, `de/legal/`, EN Pendants |
| WhatsApp-First | `closing.whatsapp_label`, `footer_channels_note`, Anfrage-Direct-Path |
| Personen-H1 Über BIT | `about.lead` als sichtbares H1 |
| Break/Fix-Wortlaut | Problem-Karten, M365-Intro (Outlook/Drucker) |

---

## Part 2 — Umbauplan (Antworten zu §19)

### 1. Welche Texte werden geändert?

**Priorität hoch (heute umsetzbar, Zustand A):**
- Hero H1/Lead/Meta DE+EN (`home.*`)
- Home-Reihenfolge: Services direkt unter Hero; Anliegen/Situationen danach; «Wer dahintersteht» → «Warum BIT»
- CTA-Labels (`cta_primary`, Closing, Anfrage)
- Öffentliche Stundenpreis-Stellen (FAQ, Leistungen-Panel, `prices.hourly` Anzeige)
- Über-BIT Body: Ich → BIT/Inhaber-Rolle ohne Technikerversprechen
- `role.contract` / Legal-Positionierungston (rechtlich Einzelunternehmen bleibt Tatsache)
- Footer-Hinweis: Formular vor WhatsApp
- M365-Leistungsintro: weniger Reparatur-, mehr Prozesssprache
- Für-Unternehmen: H1 service-first; «Übergabe an Fachpartner»-Bullet schärfen

**Priorität mittel:**
- Ablauf-Seite: explizite Kette Kunde→BIT→(Fachpartner)→Abschluss
- Problem-Karten kürzen oder verschieben
- AGB später: Festpreis-/Paketoptionen vorbereiten (kein Blindpreis)

**Nicht ändern (erfinden):** Partnernetzwerk, «unsere Spezialisten», Garantien zur technischen Umsetzungskapazität.

### 2. Welche Karten werden zusammengeführt?

| Ist | Soll |
|---|---|
| Home: 4 Anliegen-Links + 3 Problem-Karten + 3 Servicekarten | **Eine** Service-Zone (3 Karten) + darunter **Situationen** (max. 4, aus heutigen Anliegen); Problem-Karten entfallen oder 1 Satz |
| Home-Beispiele-Teaser vs. 4 Kurzbeispiele auf Audience-Seite | Teaser bleibt Link zu `/beispiele/`; Audience-Kurzbeispiele behalten oder auf 3 Kernmuster reduzieren (Eintritt/Austritt/Arbeitsplatz) |
| Vierte Musteridee «Unklare Anbieterzuständigkeit» | Nicht als eigenes Verkaufsprodukt; nur als Prozesshinweis innerhalb der 3 Services |
| Optional später | Karte D nur nach Partner + Standardisierung (Soll §5D) — **jetzt nicht** |

Keine Fusion der drei Kernservices — die Trennung ist Ana-kompatibel.

### 3. Welche Freelancer-Signale verschwinden?

1. Öffentliches **CHF 120 / Stunde** als Leitpreis  
2. H1-/Meta-Leitwort **«IT-Support»** zugunsten Serviceformulierung  
3. **Ich**-Verkaufston auf Kernseiten (`bleibe ich`, «Ich arbeite als…») → Marke BIT  
4. **WhatsApp als Erstkontakt** gleichwertig zum Formular  
5. Home-Block **«Wer dahintersteht»** als Vertrauensersatz für Serviceklarheit  
6. Break/Fix-Betonung (Drucker/Outlook als Markenkern)  
7. Implizites «Stefan löst das Ticket» in Benefits/CTAs  

Rechtliche Identität als Einzelunternehmen und echte Kontaktdaten bleiben — aber nicht als Produktversprechen «Stunden von Stefan».

### 4. Wie wird das White-Label-Modell verständlich, ohne «White Label» zu sagen?

Kundenbotschaft in Alltagssprache:

1. **Sie kaufen den Service bei BIT.**  
2. **BIT bleibt Ansprechpartner, Vertrag und Abschluss.**  
3. **Facharbeit läuft im vereinbarten Serviceprozess** — bei Bedarf durch geeignete Fachpersonen, nur nach Absprache/Freigabe (Zustand A).  
4. **Warum BIT:** eine Beziehung, klarer Service, Ablauf, Dokumentation — nicht «Telefonnummer weitergeben».

Umsetzen über: Partner-Home-Block (geschärft), Ablauf-Kette, Service-Steps («bearbeiten oder freigegebene Umsetzung steuern»), FAQ Technik — **ohne** Partnernamen und ohne «Netzwerk».

### 5. Welche Aussagen sind aktuell zulässig (Zustand A)?

- Begrenzter Einführungsbetrieb / ausgewählte Anfragen  
- Drei konkrete Servicefamilien + Beispiele als Muster (keine Kundenreferenzen)  
- Zielgruppe 5–50, keine interne IT, Windows/M365, Zürich/remote CH  
- Schriftliche Vereinbarung vor Start; dokumentierter Abschluss  
- «Vor Annahme wird geprüft, ob die benötigte Fachleistung im verfügbaren Leistungs-/Partnerumfang erbracht werden kann» (sinngemäss schon in FAQ/Partner-Text)  
- Kosten Dritter nur nach Freigabe  
- Kein 24/7, keine unbegrenzten Pauschalen, Basischeck ≠ Cyber-Audit  
- Festpreis-Einstieg Basischeck ab CHF 190 (sofern intern kalkuliert haltbar)  
- Inhaber/Einzelunternehmen als rechtliche Tatsache  

### 6. Welche Aussagen dürfen erst nach Partnervertrag?

- «Unsere Spezialisten übernehmen…»  
- «Partnernetzwerk» / feste Kapazitätsversprechen  
- «Technische Umsetzung erfolgt garantiert…»  
- Skalierungsversprechen («beliebige Menge paralleler Tickets»)  
- Neue produktisierte Module (Soll §5D) mit Partnerabhängigkeit  
- Aggressive Formulierung «Fachpartner führen immer aus» ohne Prüfvorbehalt  

Technisch: `state` A→B Flag in Config vorsehen (wie Strategie-Doku), Texte umschalten — **jetzt nicht behaupten**.

### 7. Welche Preislogik unterstützt späteres White Label?

| Jetzt (Zustand A) | Später (mit Partner + Standard) |
|---|---|
| Assessment/Festpreis-Einstieg (Basischeck) sichtbar | Setup + standardisierte Festpreise |
| Stundenpreis **nicht** Leitpreis öffentlich | Stunden nur intern / Offerte Ausnahmen |
| «Richtwerte nach Prüfung des Serviceumfangs» | Wiederkehrende Pakete / Retainer |
| Marge = BIT besitzt Vertrag | Einkaufspartnerpreis vs. Verkaufspreis (intern) |

**Keine neuen Preise erfinden** auf der Website. CHF 120 aus der Wahrnehmung nehmen, ohne Fake-Pakete.

### 8. Wie wird Ana «erst Leistung, dann Zielgruppe» umgesetzt?

**Startseite (Soll-Reihenfolge):**  
Hero (Was + kurzes Für-wen in einer Zeile) → **Services (3)** → Für wen (Fit) → Situationen → Ablauf → Warum BIT → Musterfälle → CTA  

**Für Unternehmen:** H1 von Audience-only auf «Services für …»; bestehende Listenreihenfolge Leistungen→Fit beibehalten (`629b1bb`).  

**Leistungen-Index:** Intro zuerst «Was Sie beauftragen können», Zielgruppe sekundär.

### 9. Welche Begriffe werden vereinfacht?

| Vermeiden / zurückstufen | Ersetzen durch |
|---|---|
| IT-Support (als H1-Marke) | Digitale Betriebsservices / Benutzer- & Arbeitsplatzservices |
| Umfang / scope als Leitjargon | Was enthalten ist / Leistungsrahmen / schriftliche Vereinbarung |
| frame / framework / orchestration / service operator | — (intern ok) |
| IT-Anliegen (Ticket) | Bedarf / Anfrage zum Service |
| Koordination allein | BIT organisiert den Service / steuert die Ausführung |
| Übergabe an Partner (ohne Kontext) | Facharbeit im BIT-Service; BIT bleibt Vertragspartner |
| Wer dahintersteht (Hero-Pfad) | Warum BIT (Prozessnutzen) |

Behalten: Benutzer, Zugänge, Microsoft 365, Freigabe, Dokumentation, Ergebnis.

### 10. Wie verhindern wir den klassischen IT-Support-Look?

**Do:**
- Servicekatalog und Ergebnisse zuerst  
- Prozess und dokumentierter Abschluss  
- Facharbeit als Teil des BIT-Service, nicht Personen-Helpdesk  
- Festpreis/Assessment vor Stunden  
- Formular vor Messenger  

**Don't:**
- H1 «IT-Support» + Outlook/Drucker als Markenkern  
- CHF/h als Preishaupt  
- «Ich repariere / ich administriere»  
- WhatsApp = Produkt  
- Schema/Marketing als reiner Vor-Ort-Techniker ohne Serviceframe  

**Härtetest bei jedem Text:** Funktioniert der Satz noch, wenn Stefan nicht jedes Ticket selbst macht? Wenn nein → umformulieren.

---

## Part 3 — Abnahmekriterien (§20)

| Kriterium | Soll | Ist (Live 2026-08-08) | Urteil |
|---|---|---|---|
| **5 Sekunden** | «BIT bietet bestimmte digitale/IT-nahe Services für kleine Unternehmen ohne eigene IT.» | Besucher sieht zuerst **«IT-Support»** + KMU — Services erst scrollen | **Nicht bestanden** (nahe, aber Techniker-Bias) |
| **30 Sekunden** | «Ich kaufe bei BIT; BIT organisiert; Fachpartner möglich.» | Partner-Block und Servicekarten tragen das, wenn gelesen; CHF 120, WhatsApp, Stefan-Block konkurrieren | **Teilweise** |
| **Verboten:** «Stefan = stundenweise IT-Techniker» | Vermeiden | H1 Support + CHF 120 + Ich-Ton + Über-BIT Personen-H1 speisen genau das | **Risiko hoch** |
| **Verboten:** «BIT = blosse Vermittlung» | Vermeiden | Kein «wir vermitteln Freelancer»; aber «koordinieren»/«Fachstelle» ohne Schärfung kann so gelesen werden | **Risiko mittel** (mit Textfeile beherrschbar) |

**Gate für «Umbau erfolgreich»:** Erst wenn 5- und 30-Sekunden-Tests mit unbeteiligten Personen (Methode `docs/5-SEKUNDEN-TEST.md`) die Soll-Sätze treffen **und** die beiden Fehlinterpretationen nicht primär auftreten.

---

## Empfohlene Umsetzungsreihenfolge (nur Plan)

1. Content: `de_v2.json` / `en_v2.json` — Hero, Reihenfolge Home, Preise öffentlich, CTAs, About/Role-Ton  
2. Build/Templates: Section-Order Home; Footer-Note; WhatsApp-Hierarchie  
3. Leistungen-Panel ohne CHF 120; FAQ-Preistext  
4. Ablaufzussatz Fachpartner-in-BIT-Service  
5. Legal/Meta an neue Positionierung (ohne Faktenverdrehung)  
6. Manueller 5-/30-Sekunden-Test mit Fremden  
7. Erst danach: Partnervertrag → Zustand B Texte

---

## Live-Fetch Protokoll

Alle genannten URLs mit Header `Cache-Control: no-cache` → **HTTP 200** (DE + EN Äquivalente). Stichproben H1 identisch mit Repo-HTML (`de/index.html`, `de/fuer-unternehmen/index.html`, `de/leistungen/index.html`, usw.).

---

*Ende Audit. Keine Produktionsänderungen durch dieses Dokument.*
