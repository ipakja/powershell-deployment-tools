# White-Label Skalierbarkeit (intern)

**Stand:** 2026-08-08  
**Zustand:** A (kein verbindlicher Partnervertrag im Repo)  
**Kennzeichnung:** A = weitgehend automatisierbar · P = partnerfähig · S = stark Stefan-abhängig

Ziel: Kernprodukte langfristig überwiegend **A/P**, nicht linear mit Stefans persönlicher Technikzeit.

---

## 1. Benutzer & Zugänge

| Volumen | A | P | S | Kurzfazit |
|---|---|---|---|---|
| 1 Kunde | Checklisten, Freigabeformulare | Spezialsysteme an Fachperson | Aufnahme/QA durch BIT | Machbar; S akzeptabel |
| 10 Kunden | Templates, Ticketstatus, Standardrollen | Wiederkehrende Herstellerfälle | Eskalationen / Ausnahmen | Braucht Prozess + leichte Automation |
| 50 Kunden | Workflow-Tooling, Self-Service-Intake | Standardausführung an Partner | Nur QA/Ausnahmen bei BIT | Nur mit A+P skalierbar; S darf nicht Linearfaktor bleiben |

**Kernprodukt-Eignung:** hoch (A/P). Nicht als persönliches Stefan-Ticketprodukt ausbauen.

---

## 2. Microsoft 365 & Arbeitsplatz (standardisierte Fälle)

| Volumen | A | P | S | Kurzfazit |
|---|---|---|---|---|
| 1 Kunde | Diagnoseleitfaden | Tiefere Herstellerfälle | Standardfälle ggf. Stefan | S-Risiko bei Break/Fix-Ton |
| 10 Kunden | Kategorisierung, Runbooks | Standardfälle an Partner | Nur Grenz-/QA-Fälle | Drift zu Helpdesk vermeiden |
| 50 Kunden | Routing, Wissensbasis | Mehrheit der Standardfälle | Nur Steuerung/Qualität | Nur A/P; S-lastige Reparaturen nicht Kern |

**Kernprodukt-Eignung:** mittel–hoch, wenn strikt auf **Standardfälle** begrenzt. Offene Störungsflut = S-Falle.

---

## 3. IT-Basischeck (Assessment / Festpreis-Einstieg)

| Volumen | A | P | S | Kurzfazit |
|---|---|---|---|---|
| 1 Kunde | Berichtsvorlage | Datenerhebung unterstützend | Analyse/Priorisierung | Gut als Produkt |
| 10 Kunden | Fragebogen, Report-Generator | Teilaufnahme | Befund/QA | Skaliert mit Templates |
| 50 Kunden | Semi-automatisierte Erhebung | Feldarbeit/Partner | Stichproben-QA | A/P-fähig; S nur Qualitätsrolle |

**Kernprodukt-Eignung:** hoch (A/P). Festpreis-Assessment stützt White-Label besser als Stundenverkauf.

---

## Leitregel

Öffentlich prominent nur halten, was bei 10–50 Kunden ohne lineare Stefan-Technikzeit tragfähig ist. Stark S-abhängige Leistungen nicht als strategisches Kernprodukt ausbauen.
