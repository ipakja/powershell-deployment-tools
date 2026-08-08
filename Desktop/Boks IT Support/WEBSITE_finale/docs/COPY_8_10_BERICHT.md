# Copy 8/10 – Änderungsbericht (Priority 10)

Stand: August 2026  
Quellen: `config/de_v2.json`, `config/en_v2.json`, `scripts/build_v2_de.py`, `scripts/test_build_v2.py`

## Kernmodell (unverändert)

Kunde beauftragt BIT → BIT steuert → ggf. Facharbeit innerhalb des BIT-Service → Qualitätskontrolle → dokumentierter Abschluss.  
Kein Vermittlungsversprechen, kein CHF-120/h-Kernprodukt.

## Umgesetzte Prioritäten

1. **Einführungsbetrieb entfernt**  
   Überall ersetzt durch:  
   DE «BIT nimmt derzeit eine begrenzte Anzahl neuer Serviceanfragen an.»  
   EN «BIT is currently accepting a limited number of new service requests.»

2. **Anbieterzuständigkeit-Formulierung entfernt**  
   Ersetzt durch:  
   DE «Falls weitere Fachanbieter benötigt werden, koordiniert BIT die notwendigen Schritte innerhalb des vereinbarten Service.»  
   EN-Äquivalent.

3. **«Kundenbeziehung wird nicht weitergeleitet» ersetzt**  
   DE «BIT bleibt während des gesamten Auftrags Ihr zentraler Ansprechpartner.»  
   EN-Äquivalent.

4. **Wiederholungen Leistungsrahmen/Freigabe/schriftlich/dokumentiert**  
   Auf Home, Leistungen und Prozess um ca. 25–30 % reduziert; Kernaussage bleibt einmal klar stehen.

5. **Preise und Abrechnung gekürzt**  
   Titel neu; Block mit CHF 190, Festpreis/wiederkehrend, Spezialaufwand nach Freigabe (Richtwert CHF 120/h), Remote-Standard, Vor-Ort Zürich.

6. **CHF 120/h** nur noch als Richtwert für Sonderaufwand, nicht als Produkt.

7. **Über BIT** positiv auf Owner-Rolle umgestellt  
   Defensive Ticket-Techniker-Formulierung entfernt.  
   Arbeitssprachen auf «Deutsch und Englisch» gekürzt.  
   SIZ + Hospitality-Hintergrund behalten.

8. **FAQ** gekürzt und geschärft  
   Neue/angepasste Fragen u. a. IT-Abteilung, alle IT-Probleme, technische Änderungen, Preise (ohne Remote-Doppler), Reaktionszeit (2 Arbeitstage), Dokumentationsstand für Basischeck.

9. **Prozesssprache** kundenfreundlicher  
   Schritte: Anfrage → Bedarf/Machbarkeit → Umfang und Preis → umsetzen/koordinieren → prüfen → dokumentieren.  
   `/de/so-funktioniert-es/` und `/en/how-it-works/` leicht angereichert (Erwartungen ohne erfundene SLAs).

10. **Beispiele / Grenzen umbenannt**  
    «Typische Servicefälle» / «So können Aufträge bei BIT ablaufen» mit ehrlichem Muster-Disclaimer.  
    «Leistungsgrenzen» mit weicheren Bullets.  
    Freigabe: autorisierte Person; Onboarding: Vergleichsrolle; Outlook-Ownership-Formulierungen.

## Weitere konkrete Tweaks

- Footer: «Für neue Serviceanfragen empfehlen wir das Anfrageformular.»
- «Durch das Formular entsteht noch kein Auftrag» vor allem bei Formular/CTA belassen, nicht in jedem Service-Closing.
- CTA «Bedarf prüfen lassen» / EN-Äquivalent unverändert.
- Design, 3 Services, Zielgruppe 5–50, CHF 190 Basischeck, Zürich+remote, Formular/API/Resend unverändert.

## Build / Qualität

- `python scripts/build_site.py`
- `python -m pytest scripts/test_build_v2.py` → 25 passed

## Nicht geändert (bewusst)

- Design-System / Layout
- Formular- und Notify-Technik
- AGB-/Legal-Kerntexte
- Neue Preise oder Partnernamen
