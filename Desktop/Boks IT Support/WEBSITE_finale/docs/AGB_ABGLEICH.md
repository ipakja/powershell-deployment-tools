# AGB-Abgleich vs. Website-Texte

**Stand:** August 2026  
**Quellen:** `config/agb_de.json` (AGB), `config/de_v2.json` / `config/en_v2.json`, `de/legal/` / `en/legal/`  
**Zweck:** Widersprüche und Doppelungen sichtbar machen. Keine rechtlichen Kürzungen auf der Legal-Seite, bis Stefan bestätigt.

---

## 1. Keine echten Widersprüche (Abgleich bestätigt)

| Thema | AGB | Website | Bewertung |
|---|---|---|---|
| **Zwei Arbeitstage** | AGB 3.4: Reaktionszeiten nur bei schriftlicher Zusicherung; sonst angemessene Frist | «Rückmeldung in der Regel innerhalb von zwei Arbeitstagen» auf Anfrage/Closing | **Kein Widerspruch.** Die zwei Arbeitstage betreffen die **Anfrage-Antwort** (Bedarfsabklärung), nicht eine SLA für Auftragsbearbeitung. |
| **Kein Vertrag durch Absenden** | AGB 2.2: Absenden ≠ Vertrag / keine Bearbeitungspflicht | Anfrage: «Durch das Formular entsteht noch kein Auftrag» / «Durch das Absenden entsteht noch kein Auftrag» | **Deckungsgleich.** |
| **Richtwerte** | AGB 6.2: Website-Angaben sind Richtwerte; verbindlich nur Schriftliches | `price_note`, FAQ Preise, Leistungen-Panel | **Deckungsgleich.** |
| **Dritte** | AGB 4: Beizug möglich; BIT bleibt Vertragspartner; Mehrkosten nur mit Zustimmung | Home «Ein Vertragspartner…»; Kosten Dritter nur nach schriftlicher Freigabe | **Deckungsgleich** in der Sache. |
| **Datensicherung** | AGB 5.3 / 10.5: Kundin/Kunde sichert; BIT schuldet keine Datensicherung ohne Vereinbarung | Website betont Freigaben und Passwort-Verbot, erwähnt Kundensicherung kaum explizit | **Kein Widerspruch**, aber Website schweigt weitgehend zur Backup-Pflicht (Klarheit möglich). |
| **Vor-Ort** | AGB 3.5 / 6.4: remote Grundsatz; Vor-Ort vorab vereinbart und separat ausgewiesen | `travel_line` / FAQ: remote Normalweg; Vor-Ort Zürich vorab und separat | **Deckungsgleich.** |

---

## 2. Spannungen / Präzisierungsbedarf (kein Soft-Rewrite der AGB)

| Punkt | Befund | Empfehlung |
|---|---|---|
| **Stundenansatz öffentlich** | AGB 6.1 nennt Abrechnung nach Aufwand zum gültigen Stundenansatz; Website zeigt CHF 120 prominent | Strateglich konsistent als Richtwert. Strategisch separat klären (Strategie-Analyse), nicht in der AGB. |
| **«Vertragspartner bleibe ich»** | AGB: Vertragspartner ist BIT (Marke/Inhaber); Legal/About: Ich-Form | Inhaltlich stimmig (Einzelunternehmen). Ton-Differenz, kein Rechtswiderspruch. |
| **Legal «AGB – wichtige Eckpunkte»** | Kurzfassung neben vollständigen AGB unter `/de/agb/` | Risiko doppelter Rechtsquellen – siehe Dedup-Vorschlag unten. |
| **Legal «Haftung für Inhalte»** | Website-Inhalts-Haftung vs. AGB §10 Vertragshaftung | Unterschiedliche Gegenstände; Besucher können sie vermischen. |
| **Zeittaktung (6.3)** | AGB verweist auf Offerte-Taktung; Website nennt keine Taktung | Marker gesetzt; Stefan muss Taktung in Offert-Vorlage festlegen. |
| **Betriebshaftpflicht** | AGB §10 begrenzt Haftung; Website erwähnt keine Versicherung | Marker gesetzt; Stefan bestätigt, ob Versicherung besteht und ob sie kommuniziert werden soll. |

---

## 3. Vorschlag Legal-Dedup (noch nicht umsetzen)

Ziel: eine klare Hierarchie ohne inhaltliche Lücken.

| Seite | Soll-Rolle |
|---|---|
| `/de/legal/` | Impressum + Datenschutz (+ Website-Inhalts-/Urheberrecht) |
| `/de/agb/` | Verbindliche Vertrags-AGB |
| `/en/legal/` / `/en/terms/` | Entsprechend EN |

**Vorgeschlagene Schnitte auf `/de/legal/` (nur nach Bestätigung):**

1. Abschnitt **«AGB – wichtige Eckpunkte»** ersetzen durch kurzen Verweis + Link auf `/de/agb/` (1–2 Sätze: Vertrag entsteht erst schriftlich; Details in den AGB).  
2. Abschnitt **«Haftung für Inhalte»** behalten als Website-Haftung; Vertragshaftung nicht dort wiederholen — Verweis auf AGB §10.  
3. Datenschutz-Block behalten (AGB §9 verweist ohnehin darauf).  
4. Impressum-Adresse/Rechtsform **unverändert** lassen.

**Nicht kürzen, bis Stefan bestätigt.**

---

## 4. Bestätigungspunkte für Stefan

1. **Zeittaktung** bei Abrechnung nach Aufwand (AGB 6.3) — welche Einheit gilt in der Offerte (z. B. 15 Min.)?  
2. **Betriebshaftpflicht** — besteht eine? Soll sie öffentlich erwähnt werden?  
3. Legal-Dedup wie oben — freigeben oder Eckpunkte vorerst belassen?
