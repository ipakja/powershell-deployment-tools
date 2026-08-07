# -*- coding: utf-8 -*-
"""Apply Phase B trust-building content across all languages."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Shared editorial payloads per language.
CONTENT = {
    "de": {
        "common": {
            "about_lead": "Stefan Bogdanovic · BIT – Boks IT Support · Zürich",
            "about_text": (
                "Ich unterstütze kleine und mittlere Betriebe bei klar abgegrenzten "
                "IT- und Digitalaufgaben. Für den Schweizer B2B-Markt führe ich "
                "strukturierte Pilotmandate unter der Bezeichnung BIT Market Access "
                "Switzerland durch. Ich prüfe zuerst Ausgangslage, Abhängigkeiten und "
                "Grenzen und dokumentiere die vereinbarten Ergebnisse. Wenn ein Auftrag "
                "zusätzliches Fachwissen verlangt, benenne ich das vor Beginn und "
                "beziehe externe Fachpersonen nur nach Absprache ein. Vertragspartner "
                "bleibe ich."
            ),
            "about_practice": (
                "Meine Arbeit verbindet operative Hotelpraxis in der Schweiz mit "
                "konkreter IT-Unterstützung: Front Office, PMS-Abläufe, Folio- und "
                "Buchungswege sowie Microsoft 365, Geräte und Benutzerzugänge in "
                "kleinen Teams. Von Zürich aus arbeite ich mit Schweizer Betriebsrealität "
                "und mit der Sprachbrücke zum südosteuropäischen Markt."
            ),
            "about_languages": (
                "Arbeitssprachen: Deutsch, Englisch sowie Serbisch, Bosnisch und "
                "Kroatisch. Französisch und Italienisch nach Vereinbarung beziehungsweise "
                "mit externer Sprachunterstützung."
            ),
            "about_independent": (
                "Ich arbeite unabhängig und bin keine offizielle Vertretung eines "
                "PMS- oder Softwareherstellers."
            ),
        },
        "hospitality": {
            "meta_title": "IT & Hospitality Support Zürich | BIT",
            "meta_description": (
                "Abgegrenzte IT- und Hospitality-Unterstützung sowie Prüfung von "
                "Buchungs-, Raten- und Abrechnungsdaten für KMU, Hotels und Gastronomie "
                "in Zürich."
            ),
            "eyebrow": "IT & Hospitality · Zürich",
            "lead": (
                "Ich unterstütze KMU, Hotels und Gastronomiebetriebe bei konkreten "
                "Störungen, Systemfragen, digitalen Arbeitsabläufen und der Prüfung "
                "von Buchungs-, Raten- und Abrechnungsdaten."
            ),
            "block0_text": (
                "Ich prüfe klar abgegrenzte Abläufe zwischen Rezeption, Reservierung, "
                "Kasse, Betrieb und Abrechnung."
            ),
            "revenue_item": (
                "Buchungs-, Raten- und Abrechnungsdaten: Belegung, ADR/RevPAR-Abweichungen "
                "und Ratenlogik anhand gelieferter Daten prüfen"
            ),
            "process_intro": "Jeder Auftrag folgt fünf klaren Arbeitsschritten.",
            "steps": [
                ("Vorbereitung", None),
                ("Arbeitsbeginn", None),
                ("Umsetzung", (
                    "Ich bearbeite die schriftlich vereinbarten Aufgaben, etwa PMS-, "
                    "Folio- oder Channel-Fälle, Microsoft 365 oder Geräte. Änderungen "
                    "und Befunde halte ich innerhalb des vereinbarten Umfangs fest."
                )),
                ("Sonderaufgaben", None),
                ("Abschluss und Übergabe", (
                    "Ich übergebe Befunde, offene Punkte und den nächsten Schritt und "
                    "schliesse den Einsatz ab. Vertrauliche Zugangsdaten sende ich nie "
                    "über Messenger und fordere sie dort auch nicht an."
                )),
            ],
        },
        "market": {
            "meta_title": "BIT Market Access Switzerland | Schweiz-Pilot",
            "eyebrow": "BIT Market Access Switzerland",
            "title": "Vom Unterlagen-Check zum Schweiz-Pilot.",
            "document_title": "Unterlagen-Check",
            "nav0": "Unterlagen-Check",
            "deliverable_last": (
                "Abschlussbericht mit Beobachtungen und einer sachlichen Empfehlung "
                "zum weiteren Vorgehen"
            ),
            "pricing_start": "Zahlung Pilot: 50 % bei Auftragserteilung, 50 % nach Abschlussbericht",
            "exclusion0": "Keine Zusage von Kunden, Umsatz, Aufträgen oder Markterfolg",
            "sample_title": "Beispiel: Form des Ergebnisses",
            "sample_note": (
                "Anonymisiertes Musterformat – kein echter Kundenfall und keine "
                "Erfolgsversprechen."
            ),
            "sample_targets_title": "Muster einer Zielkundenliste",
            "sample_targets": [
                "Hotellerie · Kanton Zürich · Betriebsleitung / Front Office",
                "B2B-Dienstleistung · Kanton Bern · Geschäftsführung",
                "Fachhandel · Kanton Aargau · Einkauf / IT-Verantwortung",
            ],
            "sample_criteria_title": "Prüfkriterien",
            "sample_criteria": [
                "Klarheit von Angebot und Nutzenargumentation",
                "Passung zu Segment, Preislogik und vorhandenen Unterlagen",
                "Erreichbarkeit und Qualität der ersten Rückmeldungen",
            ],
            "sample_findings_title": "Typische Finding-Kategorien",
            "sample_findings": [
                "Positionierung unklar oder zu breit für den Schweizer Markt",
                "Unterlagen unvollständig für eine belastbare Erstansprache",
                "Zielsegment zu weit oder Ansprechrollen nicht belastbar",
            ],
            "sample_report_title": "Gliederung des Abschlussberichts",
            "sample_report": [
                "Ausgangslage und schriftlicher Umfang",
                "Beobachtungen aus Prüfung und Erstansprache",
                "Offene Fragen und Risiken",
                "Sachliche Empfehlung zum weiteren Vorgehen",
            ],
        },
        "gateway_hospitality": "IT & Hospitality",
    },
    "en": {
        "common": {
            "about_lead": "Stefan Bogdanovic · BIT – Boks IT Support · Zurich",
            "about_text": (
                "I support small and medium-sized businesses with clearly scoped IT and "
                "digital tasks. For the Swiss B2B market, I run structured pilot mandates "
                "under BIT Market Access Switzerland. I first assess the starting point, "
                "dependencies and limits, then document the agreed results. If an "
                "engagement requires additional expertise, I state this before work "
                "starts and involve external specialists only by agreement. I remain "
                "the contractual counterparty."
            ),
            "about_practice": (
                "My work combines operational Swiss hotel practice with concrete IT "
                "support: front office, PMS workflows, folio and booking paths, as well "
                "as Microsoft 365, devices and user access for small teams. From Zurich "
                "I work with Swiss operating reality and with the language bridge to "
                "the South-East European market."
            ),
            "about_languages": (
                "Working languages: German, English, and Serbian, Bosnian and Croatian. "
                "French and Italian by arrangement or with external language support."
            ),
            "about_independent": (
                "I work independently and am not an official representative of any PMS "
                "or software vendor."
            ),
        },
        "hospitality": {
            "meta_title": "IT & Hospitality Support Zurich | BIT",
            "meta_description": (
                "Scoped IT, hospitality and booking, rate and billing-data review for "
                "SMEs, hotels and restaurants in Zurich."
            ),
            "eyebrow": "IT & Hospitality · Zurich",
            "lead": (
                "I support SMEs, hotels and restaurants with specific incidents, system "
                "questions, digital workflows and scoped review of booking, rate and "
                "billing data."
            ),
            "block0_text": (
                "I review clearly scoped workflows across reception, reservations, "
                "point of sale, operations and billing."
            ),
            "revenue_item": (
                "Booking, rate and billing data: review occupancy, ADR/RevPAR deviations "
                "and rate logic from provided data"
            ),
            "process_intro": "Each engagement follows five clearly defined steps.",
            "steps": [
                ("Preparation", None),
                ("Engagement start", (
                    "I start remotely or on site as agreed. I first verify the working "
                    "environment and confirm the goal for that session."
                )),
                ("Execution", (
                    "I complete the tasks agreed in writing, such as PMS, folio or "
                    "channel cases, Microsoft 365 or device work. I record changes and "
                    "findings within the agreed scope."
                )),
                ("Special tasks", None),
                ("Completion and handover", (
                    "I hand over findings, open items and the next step, then close the "
                    "engagement. I never send confidential credentials through messaging "
                    "apps or request them there."
                )),
            ],
        },
        "market": {
            "meta_title": "BIT Market Access Switzerland | market pilot",
            "eyebrow": "BIT Market Access Switzerland",
            "title": "From document review to a Swiss market pilot.",
            "document_title": "Document review",
            "nav0": "Document review",
            "deliverable_last": (
                "Final report with observations and an objective recommendation for "
                "next steps"
            ),
            "pricing_start": (
                "Pilot payment: 50% at project start, 50% after the final report"
            ),
            "exclusion0": "No guarantee of customers, revenue, orders or market success",
            "sample_title": "Example: form of the deliverable",
            "sample_note": (
                "Anonymised sample format – not a real client case and no promise of "
                "results."
            ),
            "sample_targets_title": "Sample target-business list",
            "sample_targets": [
                "Hospitality · Canton of Zurich · operations / front office",
                "B2B services · Canton of Bern · managing director",
                "Specialist trade · Canton of Aargau · purchasing / IT lead",
            ],
            "sample_criteria_title": "Review criteria",
            "sample_criteria": [
                "Clarity of offer and value proposition",
                "Fit with segment, pricing logic and existing materials",
                "Reachability and quality of first responses",
            ],
            "sample_findings_title": "Typical finding categories",
            "sample_findings": [
                "Positioning unclear or too broad for the Swiss market",
                "Materials incomplete for a solid first outreach",
                "Target segment too wide or contact roles not reliable",
            ],
            "sample_report_title": "Final-report structure",
            "sample_report": [
                "Starting point and written scope",
                "Observations from review and initial outreach",
                "Open questions and risks",
                "Objective recommendation for next steps",
            ],
        },
        "gateway_hospitality": "IT & Hospitality",
    },
    "fr": {
        "common": {
            "about_lead": "Stefan Bogdanovic · BIT – Boks IT Support · Zurich",
            "about_text": (
                "J’accompagne les petites et moyennes entreprises pour des tâches "
                "informatiques et numériques clairement délimitées. Pour le marché B2B "
                "suisse, je mène des mandats pilotes structurés sous le nom BIT Market "
                "Access Switzerland. J’examine d’abord la situation, les dépendances et "
                "les limites, puis je documente les résultats convenus. Si une mission "
                "exige une expertise supplémentaire, je l’indique avant le début et ne "
                "fais intervenir des spécialistes externes qu’après accord. Je reste "
                "votre cocontractant."
            ),
            "about_practice": (
                "Mon travail relie la pratique hôtelière opérationnelle en Suisse à un "
                "soutien informatique concret : réception, processus PMS, folios et "
                "parcours de réservation, ainsi que Microsoft 365, appareils et accès "
                "utilisateurs pour les petites équipes. Depuis Zurich, je travaille avec "
                "la réalité opérationnelle suisse et avec le pont linguistique vers le "
                "marché d’Europe du Sud-Est."
            ),
            "about_languages": (
                "Langues de travail : allemand, anglais, ainsi que serbe, bosniaque et "
                "croate. Français et italien sur accord ou avec un soutien linguistique "
                "externe."
            ),
            "about_independent": (
                "Je travaille de manière indépendante et ne représente officiellement "
                "aucun fournisseur PMS ou logiciel."
            ),
        },
        "hospitality": {
            "meta_title": "Support IT & Hospitality Zurich | BIT",
            "meta_description": (
                "Support informatique, hospitality et contrôle délimité des données de "
                "réservation, tarifs et facturation pour PME, hôtels et restaurants à "
                "Zurich."
            ),
            "eyebrow": "IT & Hospitality · Zurich",
            "lead": (
                "J’accompagne PME, hôtels et restaurants pour des incidents concrets, "
                "des questions relatives aux systèmes, des flux numériques et le "
                "contrôle délimité des données de réservation, tarifs et facturation."
            ),
            "block0_text": (
                "Je contrôle des processus clairement délimités entre réception, "
                "réservation, caisse, exploitation et facturation."
            ),
            "revenue_item": (
                "Données de réservation, tarifs et facturation : contrôler occupation, "
                "écarts ADR/RevPAR et logique tarifaire à partir des données fournies"
            ),
            "process_intro": "Chaque mandat suit cinq étapes clairement définies.",
            "steps": [
                ("Préparation", None),
                ("Début de l’intervention", (
                    "Je commence à distance ou sur site selon accord. Je vérifie d’abord "
                    "l’environnement de travail et confirme l’objectif de la session."
                )),
                ("Exécution", (
                    "J’exécute les tâches convenues par écrit, par exemple les cas PMS, "
                    "folio ou channel, Microsoft 365 ou les appareils. Je consigne les "
                    "changements et constats dans le périmètre convenu."
                )),
                ("Tâches spéciales", None),
                ("Clôture et remise", (
                    "Je remets les constats, les points ouverts et l’étape suivante, "
                    "puis je clos le mandat. Je n’envoie jamais d’identifiants "
                    "confidentiels via messagerie et ne les demande pas non plus."
                )),
            ],
        },
        "market": {
            "meta_title": "BIT Market Access Switzerland | pilote marché",
            "eyebrow": "BIT Market Access Switzerland",
            "title": "Du contrôle de documents au pilote marché suisse.",
            "document_title": "Contrôle de documents",
            "nav0": "Contrôle de documents",
            "deliverable_last": (
                "Rapport final avec observations et recommandation objective sur la "
                "suite"
            ),
            "pricing_start": (
                "Paiement du pilote : 50 % au démarrage, 50 % après le rapport final"
            ),
            "exclusion0": (
                "Aucune garantie de clients, de chiffre d’affaires, de mandats ou de "
                "succès commercial"
            ),
            "sample_title": "Exemple : forme du résultat",
            "sample_note": (
                "Format d’exemple anonymisé – pas un cas client réel et aucune promesse "
                "de résultat."
            ),
            "sample_targets_title": "Exemple de liste d’entreprises cibles",
            "sample_targets": [
                "Hôtellerie · canton de Zurich · direction / réception",
                "Services B2B · canton de Berne · direction",
                "Commerce spécialisé · canton d’Argovie · achats / IT",
            ],
            "sample_criteria_title": "Critères de contrôle",
            "sample_criteria": [
                "Clarté de l’offre et de la proposition de valeur",
                "Adéquation au segment, à la logique de prix et aux documents existants",
                "Accessibilité et qualité des premiers retours",
            ],
            "sample_findings_title": "Catégories de constats typiques",
            "sample_findings": [
                "Positionnement flou ou trop large pour le marché suisse",
                "Documents incomplets pour une première prise de contact solide",
                "Segment cible trop large ou rôles de contact peu fiables",
            ],
            "sample_report_title": "Structure du rapport final",
            "sample_report": [
                "Situation de départ et périmètre écrit",
                "Observations issues du contrôle et des premiers contacts",
                "Questions ouvertes et risques",
                "Recommandation objective pour la suite",
            ],
        },
        "gateway_hospitality": "IT & Hospitality",
    },
    "it": {
        "common": {
            "about_lead": "Stefan Bogdanovic · BIT – Boks IT Support · Zurigo",
            "about_text": (
                "Supporto piccole e medie imprese in compiti IT e digitali chiaramente "
                "delimitati. Per il mercato B2B svizzero conduco mandati pilota "
                "strutturati con il nome BIT Market Access Switzerland. Prima verifico "
                "situazione di partenza, dipendenze e limiti, poi documento i risultati "
                "concordati. Se un incarico richiede competenze aggiuntive, lo indico "
                "prima dell'inizio e coinvolgo specialisti esterni solo previo accordo. "
                "Rimango l'unica controparte contrattuale."
            ),
            "about_practice": (
                "Il mio lavoro unisce la pratica operativa alberghiera in Svizzera al "
                "supporto IT concreto: front office, processi PMS, folio e percorsi di "
                "prenotazione, nonché Microsoft 365, dispositivi e accessi utente per "
                "piccoli team. Da Zurigo lavoro con la realtà operativa svizzera e con "
                "il ponte linguistico verso il mercato dell'Europa sud-orientale."
            ),
            "about_languages": (
                "Lingue di lavoro: tedesco, inglese nonché serbo, bosniaco e croato. "
                "Francese e italiano su accordo oppure con supporto linguistico esterno."
            ),
            "about_independent": (
                "Lavoro in modo indipendente e non rappresento ufficialmente alcun "
                "fornitore PMS o software."
            ),
        },
        "hospitality": {
            "meta_title": "Supporto IT & Hospitality Zurigo | BIT",
            "meta_description": (
                "Supporto IT, hospitality e verifica delimitata di dati di prenotazione, "
                "tariffe e fatturazione per PMI, hotel e ristoranti a Zurigo."
            ),
            "eyebrow": "IT & Hospitality · Zurigo",
            "lead": (
                "Supporto PMI, hotel e ristoranti per incidenti concreti, questioni "
                "relative ai sistemi, flussi digitali e verifica delimitata di dati di "
                "prenotazione, tariffe e fatturazione."
            ),
            "block0_text": (
                "Verifico flussi chiaramente delimitati tra reception, prenotazioni, "
                "cassa, operativa e fatturazione."
            ),
            "revenue_item": (
                "Dati di prenotazione, tariffe e fatturazione: verificare occupazione, "
                "scostamenti ADR/RevPAR e logica tariffaria sui dati forniti"
            ),
            "process_intro": "Ogni incarico segue cinque passi chiaramente definiti.",
            "steps": [
                ("Preparazione", None),
                ("Avvio dell’incarico", (
                    "Inizio da remoto o in loco come concordato. Prima verifico "
                    "l'ambiente di lavoro e confermo l'obiettivo della sessione."
                )),
                ("Esecuzione", (
                    "Eseguo i compiti concordati per iscritto, ad esempio casi PMS, "
                    "folio o channel, Microsoft 365 o dispositivi. Registro modifiche e "
                    "rilievi entro l'ambito concordato."
                )),
                ("Compiti speciali", None),
                ("Chiusura e consegna", (
                    "Consegno rilievi, punti aperti e il passo successivo, poi chiudo "
                    "l'incarico. Non invio mai credenziali riservate via messaggistica "
                    "e non le richiedo lì."
                )),
            ],
        },
        "market": {
            "meta_title": "BIT Market Access Switzerland | pilota mercato",
            "eyebrow": "BIT Market Access Switzerland",
            "title": "Dal controllo documenti al pilota di mercato svizzero.",
            "document_title": "Controllo documenti",
            "nav0": "Controllo documenti",
            "deliverable_last": (
                "Rapporto finale con osservazioni e raccomandazione obiettiva sui "
                "prossimi passi"
            ),
            "pricing_start": (
                "Pagamento pilota: 50% all'avvio, 50% dopo il rapporto finale"
            ),
            "exclusion0": (
                "Nessuna garanzia di clienti, fatturato, incarichi o successo di mercato"
            ),
            "sample_title": "Esempio: forma del risultato",
            "sample_note": (
                "Formato di esempio anonimizzato – non un caso cliente reale e nessuna "
                "promessa di risultato."
            ),
            "sample_targets_title": "Esempio di elenco imprese target",
            "sample_targets": [
                "Hospitality · Cantone di Zurigo · direzione / front office",
                "Servizi B2B · Cantone di Berna · direzione",
                "Commercio specializzato · Cantone di Argovia · acquisti / IT",
            ],
            "sample_criteria_title": "Criteri di verifica",
            "sample_criteria": [
                "Chiarezza dell'offerta e della proposta di valore",
                "Adattamento a segmento, logica di prezzo e documenti esistenti",
                "Raggiungibilità e qualità delle prime risposte",
            ],
            "sample_findings_title": "Categorie tipiche di rilievi",
            "sample_findings": [
                "Posizionamento poco chiaro o troppo ampio per il mercato svizzero",
                "Documenti incompleti per un primo contatto solido",
                "Segmento target troppo ampio o ruoli di contatto non affidabili",
            ],
            "sample_report_title": "Struttura del rapporto finale",
            "sample_report": [
                "Situazione di partenza e ambito scritto",
                "Osservazioni da verifica e primo contatto",
                "Domande aperte e rischi",
                "Raccomandazione obiettiva sui prossimi passi",
            ],
        },
        "gateway_hospitality": "IT & Hospitality",
    },
    "sr": {
        "common": {
            "about_lead": "Stefan Bogdanović · BIT – Boks IT Support · Cirih",
            "about_text": (
                "Podržavam mala i srednja preduzeća u jasno ograničenim IT i digitalnim "
                "zadacima. Za švajcarsko B2B tržište vodim strukturisane pilot-mandate "
                "pod nazivom BIT Market Access Switzerland. Prvo proveravam početnu "
                "situaciju, zavisnosti i granice, a zatim dokumentujem dogovorene "
                "rezultate. Ako mandat zahteva dodatno stručno znanje, to navodim pre "
                "početka i uključujem spoljne stručnjake samo uz dogovor. Ugovorna "
                "strana ostajem ja."
            ),
            "about_practice": (
                "Moj rad povezuje operativnu hotelsku praksu u Švajcarskoj sa konkretnom "
                "IT podrškom: front office, PMS procese, folio i puteve rezervacija, kao "
                "i Microsoft 365, uređaje i korisničke pristupe u malim timovima. Iz "
                "Ciriha radim sa švajcarskom poslovnom realnošću i jezičkim mostom ka "
                "jugoistočnoevropskom tržištu."
            ),
            "about_languages": (
                "Radni jezici: nemački, engleski, kao i srpski, bosanski i hrvatski. "
                "Francuski i italijanski po dogovoru ili uz spoljnu jezičku podršku."
            ),
            "about_independent": (
                "Radim nezavisno i nisam zvanični predstavnik proizvođača PMS-a ili "
                "softvera."
            ),
        },
        "hospitality": {
            "meta_title": "IT i ugostiteljstvo Cirih | BIT",
            "meta_description": (
                "Ograničena IT i ugostiteljska podrška te provera podataka o rezervacijama, "
                "cenama i obračunu za mala i srednja preduzeća, hotele i restorane u Cirihu."
            ),
            "eyebrow": "IT i ugostiteljstvo · Cirih",
            "title": "Rešavam jasno definisane IT i digitalne zadatke.",
            "lead": (
                "Pomažem malim i srednjim preduzećima, hotelima i restoranima pri "
                "rešavanju konkretnih tehničkih problema, sistemskih pitanja, digitalnih "
                "tokova rada i proveri podataka o rezervacijama, cenama i obračunu."
            ),
            "block0_text": (
                "Proveravam jasno ograničene tokove između recepcije, rezervacija, kase, "
                "poslovanja i obračuna."
            ),
            "revenue_item": (
                "Podaci o rezervacijama, cenama i obračunu: proveravam popunjenost, "
                "odstupanja ADR/RevPAR i logiku cena na osnovu dostavljenih podataka"
            ),
            "process_intro": "Svaki angažman vodim kroz pet jasno definisanih koraka.",
            "steps": [
                ("Priprema", None),
                ("Početak angažmana", None),
                ("Realizacija", (
                    "Obavljam pisano dogovorene zadatke, na primer PMS-, folio- ili "
                    "channel-slučajeve, Microsoft 365 ili uređaje. Beležim izmene i "
                    "nalaze u dogovorenom obimu."
                )),
                ("Posebni zadaci", None),
                ("Završetak i predaja", (
                    "Predajem nalaze, otvorene tačke i sledeći korak, a zatim formalno "
                    "zaključujem angažman. Poverljive pristupne podatke nikad ne šaljem "
                    "preko aplikacija za poruke i ne tražim ih tamo."
                )),
            ],
        },
        "market": {
            "meta_title": "BIT Market Access Switzerland | švajcarski pilot",
            "eyebrow": "BIT Market Access Switzerland",
            "title": "Od provere dokumentacije do švajcarskog pilota.",
            "document_title": "Provera dokumentacije",
            "nav0": "Provera dokumentacije",
            "deliverable_last": (
                "Završni izveštaj sa zapažanjima i trezvenom preporukom za dalji rad"
            ),
            "sample_title": "Primer: oblik rezultata",
            "sample_note": (
                "Anonimni format primera – nije stvarni klijentski slučaj i nije obećanje "
                "uspeha."
            ),
            "sample_targets_title": "Primer liste ciljnih firmi",
            "sample_targets": [
                "Ugostiteljstvo · kanton Cirih · rukovodstvo / front office",
                "B2B usluge · kanton Bern · direktor",
                "Specijalizovana trgovina · kanton Argau · nabavka / IT",
            ],
            "sample_criteria_title": "Kriterijumi provere",
            "sample_criteria": [
                "Jasnoća ponude i argumentacije koristi",
                "Usklađenost sa segmentom, cenovnom logikom i postojećim materijalima",
                "Dostupnost i kvalitet prvih povratnih informacija",
            ],
            "sample_findings_title": "Tipične kategorije nalaza",
            "sample_findings": [
                "Pozicioniranje nejasno ili preširoko za švajcarsko tržište",
                "Dokumentacija nepotpuna za pouzdanu prvu kontaktnu poruku",
                "Ciljni segment preširok ili uloge kontakata nisu pouzdane",
            ],
            "sample_report_title": "Struktura završnog izveštaja",
            "sample_report": [
                "Početna situacija i pisani obim",
                "Zapažanja iz provere i prve kontaktne aktivnosti",
                "Otvorena pitanja i rizici",
                "Trezvena preporuka za dalji rad",
            ],
        },
        "gateway_hospitality": "IT i ugostiteljstvo",
    },
    "bs": {
        "common": {
            "about_lead": "Stefan Bogdanović · BIT – Boks IT Support · Cirih",
            "about_text": (
                "Podržavam mala i srednja preduzeća u jasno ograničenim IT i digitalnim "
                "zadacima. Za švicarsko B2B tržište vodim strukturirane pilot-mandate "
                "pod nazivom BIT Market Access Switzerland. Prvo provjeravam početnu "
                "situaciju, zavisnosti i granice, a zatim dokumentujem dogovorene "
                "rezultate. Ako mandat zahtijeva dodatno stručno znanje, to navodim "
                "prije početka i uključujem vanjske stručnjake samo uz dogovor. "
                "Ugovorna strana ostajem ja."
            ),
            "about_practice": (
                "Moj rad povezuje operativnu hotelsku praksu u Švicarskoj sa konkretnom "
                "IT podrškom: front office, PMS procese, folio i puteve rezervacija, kao "
                "i Microsoft 365, uređaje i korisničke pristupe u malim timovima. Iz "
                "Ciriha radim sa švicarskom poslovnom realnošću i jezičkim mostom ka "
                "jugoistočnoevropskom tržištu."
            ),
            "about_languages": (
                "Radni jezici: njemački, engleski, kao i srpski, bosanski i hrvatski. "
                "Francuski i italijanski po dogovoru ili uz vanjsku jezičku podršku."
            ),
            "about_independent": (
                "Radim nezavisno i nisam zvanični predstavnik proizvođača PMS-a ili "
                "softvera."
            ),
        },
        "hospitality": {
            "meta_title": "IT i ugostiteljstvo Cirih | BIT",
            "meta_description": (
                "Ograničena IT i ugostiteljska podrška te provjera podataka o "
                "rezervacijama, cijenama i obračunu za mala i srednja preduzeća, hotele "
                "i restorane u Cirihu."
            ),
            "eyebrow": "IT i ugostiteljstvo · Cirih",
            "title": "Rješavam jasno definirane IT i digitalne zadatke.",
            "lead": (
                "Pomažem malim i srednjim preduzećima, hotelima i restoranima pri "
                "rješavanju konkretnih tehničkih problema, sistemskih pitanja, digitalnih "
                "tokova rada i provjeri podataka o rezervacijama, cijenama i obračunu."
            ),
            "block0_text": (
                "Provjeravam jasno ograničene tokove između recepcije, rezervacija, kase, "
                "poslovanja i obračuna."
            ),
            "revenue_item": (
                "Podaci o rezervacijama, cijenama i obračunu: provjeravam popunjenost, "
                "odstupanja ADR/RevPAR i logiku cijena na osnovu dostavljenih podataka"
            ),
            "process_intro": "Svaki angažman vodim kroz pet jasno definiranih koraka.",
            "steps": [
                ("Priprema", None),
                ("Početak angažmana", None),
                ("Realizacija", (
                    "Obavljam pisano dogovorene zadatke, na primjer PMS-, folio- ili "
                    "channel-slučajeve, Microsoft 365 ili uređaje. Bilježim izmjene i "
                    "nalaze u dogovorenom obimu."
                )),
                ("Posebni zadaci", None),
                ("Završetak i predaja", (
                    "Predajem nalaze, otvorene tačke i sljedeći korak, a zatim formalno "
                    "zaključujem angažman. Povjerljive pristupne podatke nikad ne šaljem "
                    "preko aplikacija za poruke i ne tražim ih tamo."
                )),
            ],
        },
        "market": {
            "meta_title": "BIT Market Access Switzerland | švicarski pilot",
            "eyebrow": "BIT Market Access Switzerland",
            "title": "Od provjere dokumentacije do švicarskog pilota.",
            "document_title": "Provjera dokumentacije",
            "nav0": "Provjera dokumentacije",
            "deliverable_last": (
                "Završni izvještaj sa zapažanjima i trezvenom preporukom za dalji rad"
            ),
            "sample_title": "Primjer: oblik rezultata",
            "sample_note": (
                "Anonimni format primjera – nije stvarni klijentski slučaj i nije "
                "obećanje uspjeha."
            ),
            "sample_targets_title": "Primjer liste ciljnih firmi",
            "sample_targets": [
                "Ugostiteljstvo · kanton Cirih · rukovodstvo / front office",
                "B2B usluge · kanton Bern · direktor",
                "Specijalizovana trgovina · kanton Aargau · nabavka / IT",
            ],
            "sample_criteria_title": "Kriteriji provjere",
            "sample_criteria": [
                "Jasnoća ponude i argumentacije koristi",
                "Usklađenost sa segmentom, cjenovnom logikom i postojećim materijalima",
                "Dostupnost i kvalitet prvih povratnih informacija",
            ],
            "sample_findings_title": "Tipične kategorije nalaza",
            "sample_findings": [
                "Pozicioniranje nejasno ili preširoko za švicarsko tržište",
                "Dokumentacija nepotpuna za pouzdanu prvu kontaktnu poruku",
                "Ciljni segment preširok ili uloge kontakata nisu pouzdane",
            ],
            "sample_report_title": "Struktura završnog izvještaja",
            "sample_report": [
                "Početna situacija i pisani obim",
                "Zapažanja iz provjere i prve kontaktne aktivnosti",
                "Otvorena pitanja i rizici",
                "Trezvena preporuka za dalji rad",
            ],
        },
        "gateway_hospitality": "IT i ugostiteljstvo",
    },
    "hr": {
        "common": {
            "about_lead": "Stefan Bogdanović · BIT – Boks IT Support · Cirih",
            "about_text": (
                "Podržavam mala i srednja poduzeća u jasno ograničenim IT i digitalnim "
                "zadacima. Za švicarsko B2B tržište vodim strukturirane pilot-mandate "
                "pod nazivom BIT Market Access Switzerland. Najprije provjeravam "
                "početno stanje, ovisnosti i granice, a zatim dokumentiram dogovorene "
                "rezultate. Ako mandat zahtijeva dodatno stručno znanje, to navodim "
                "prije početka i uključujem vanjske stručnjake samo uz dogovor. "
                "Ugovorna strana ostajem ja."
            ),
            "about_practice": (
                "Moj rad povezuje operativnu hotelsku praksu u Švicarskoj s konkretnom "
                "IT podrškom: front office, PMS procese, folio i puteve rezervacija, "
                "kao i Microsoft 365, uređaje i korisničke pristupe u malim timovima. "
                "Iz Ciriha radim sa švicarskom poslovnom stvarnošću i jezičnim mostom "
                "prema jugoistočnoeuropskom tržištu."
            ),
            "about_languages": (
                "Radni jezici: njemački, engleski te srpski, bosanski i hrvatski. "
                "Francuski i talijanski prema dogovoru ili uz vanjsku jezičnu podršku."
            ),
            "about_independent": (
                "Radim neovisno i nisam službeni predstavnik proizvođača PMS-a ili "
                "softvera."
            ),
        },
        "hospitality": {
            "meta_title": "IT i ugostiteljstvo Cirih | BIT",
            "meta_description": (
                "Ograničena IT i ugostiteljska podrška te provjera podataka o "
                "rezervacijama, cijenama i obračunu za mala i srednja poduzeća, hotele "
                "i restorane u Cirihu."
            ),
            "eyebrow": "IT i ugostiteljstvo · Cirih",
            "title": "Rješavam jasno definirane IT i digitalne zadatke.",
            "lead": (
                "Pomažem malim i srednjim poduzećima, hotelima i restoranima pri "
                "rješavanju konkretnih tehničkih problema, pitanja sustava, digitalnih "
                "tokova rada i provjeri podataka o rezervacijama, cijenama i obračunu."
            ),
            "block0_text": (
                "Provjeravam jasno ograničene tokove između recepcije, rezervacija, "
                "blagajne, poslovanja i obračuna."
            ),
            "revenue_item": (
                "Podaci o rezervacijama, cijenama i obračunu: provjeravam popunjenost, "
                "odstupanja ADR/RevPAR i logiku cijena na temelju dostavljenih podataka"
            ),
            "process_intro": "Svaki angažman vodim kroz pet jasno definiranih koraka.",
            "steps": [
                ("Priprema", None),
                ("Početak angažmana", None),
                ("Provedba", (
                    "Obavljam pisano dogovorene zadatke, na primjer PMS-, folio- ili "
                    "channel-slučajeve, Microsoft 365 ili uređaje. Bilježim izmjene i "
                    "nalaze u dogovorenom opsegu."
                )),
                ("Posebni zadaci", None),
                ("Završetak i predaja", (
                    "Predajem nalaze, otvorene točke i sljedeći korak, a zatim formalno "
                    "zaključujem angažman. Povjerljive pristupne podatke nikad ne šaljem "
                    "preko aplikacija za poruke i ne tražim ih tamo."
                )),
            ],
        },
        "market": {
            "meta_title": "BIT Market Access Switzerland | švicarski pilot",
            "eyebrow": "BIT Market Access Switzerland",
            "title": "Od provjere dokumentacije do švicarskog pilota.",
            "document_title": "Provjera dokumentacije",
            "nav0": "Provjera dokumentacije",
            "deliverable_last": (
                "Završno izvješće sa zapažanjima i trezvenom preporukom za daljnji rad"
            ),
            "sample_title": "Primjer: oblik rezultata",
            "sample_note": (
                "Anonimni format primjera – nije stvarni klijentski slučaj i nije "
                "obećanje uspjeha."
            ),
            "sample_targets_title": "Primjer popisa ciljnih tvrtki",
            "sample_targets": [
                "Ugostiteljstvo · kanton Cirih · rukovodstvo / front office",
                "B2B usluge · kanton Bern · direktor",
                "Specijalizirana trgovina · kanton Aargau · nabava / IT",
            ],
            "sample_criteria_title": "Kriteriji provjere",
            "sample_criteria": [
                "Jasnoća ponude i argumentacije koristi",
                "Usklađenost sa segmentom, cjenovnom logikom i postojećim materijalima",
                "Dostupnost i kvaliteta prvih povratnih informacija",
            ],
            "sample_findings_title": "Tipične kategorije nalaza",
            "sample_findings": [
                "Pozicioniranje nejasno ili preširoko za švicarsko tržište",
                "Dokumentacija nepotpuna za pouzdanu prvu kontaktnu poruku",
                "Ciljni segment preširok ili uloge kontakata nisu pouzdane",
            ],
            "sample_report_title": "Struktura završnog izvješća",
            "sample_report": [
                "Početno stanje i pisani opseg",
                "Zapažanja iz provjere i prve kontaktne aktivnosti",
                "Otvorena pitanja i rizici",
                "Trezvena preporuka za daljnji rad",
            ],
        },
        "gateway_hospitality": "IT i ugostiteljstvo",
    },
}

ENTITY = {
    "de": "Rechtsform nach Schweizer Recht in Klärung",
    "en": "legal form under Swiss law being clarified",
    "fr": "forme juridique selon le droit suisse en cours de clarification",
    "it": "forma giuridica secondo il diritto svizzero in chiarimento",
    "sr": "pravni oblik po švajcarskom pravu u razjašnjenju",
    "bs": "pravni oblik po švicarskom pravu u razjašnjenju",
    "hr": "pravni oblik po švicarskom pravu u razjašnjenju",
}

COUNTERPARTY = {
    "fr": ("Je reste la partie contractuelle", "Je reste votre cocontractant"),
    "it": ("Il partner contrattuale rimango io", "Rimango l'unica controparte contrattuale"),
}


def apply_language(data: dict, code: str, payload: dict) -> None:
    common = data[code]["common"]
    common.update(payload["common"])

    hosp = data[code]["hospitality"]
    h = payload["hospitality"]
    for key in ("meta_title", "meta_description", "eyebrow", "lead", "title"):
        if key in h:
            hosp[key] = h[key]
    hosp["blocks"][0]["text"] = h["block0_text"]
    # Keep first item, replace revenue-ish second item when present.
    items = hosp["blocks"][0]["items"]
    if len(items) >= 2:
        items[1] = h["revenue_item"]
    hosp["process"]["intro"] = h["process_intro"]
    for idx, (title, text) in enumerate(h["steps"]):
        hosp["process"]["steps"][idx]["title"] = title
        if text is not None:
            hosp["process"]["steps"][idx]["text"] = text

    market = data[code]["market"]
    m = payload["market"]
    for key in (
        "meta_title",
        "eyebrow",
        "title",
        "document_title",
        "sample_title",
        "sample_note",
        "sample_targets_title",
        "sample_targets",
        "sample_criteria_title",
        "sample_criteria",
        "sample_findings_title",
        "sample_findings",
        "sample_report_title",
        "sample_report",
    ):
        if key in m:
            market[key] = m[key]
    if "nav0" in m:
        market["nav"][0] = m["nav0"]
    if "deliverable_last" in m:
        market["deliverables"][-1] = m["deliverable_last"]
    if "pricing_start" in m:
        # Replace payment line if present.
        for i, line in enumerate(market["pricing"]):
            if "50" in line or "Payment" in line or "Zahlung" in line or "Paiement" in line or "Pagamento" in line:
                market["pricing"][i] = m["pricing_start"]
                break
    if "exclusion0" in m:
        market["exclusions"][0] = m["exclusion0"]

    # Soften leftover revenue-management labels in hospitality honesty/process texts.
    for step in hosp["process"]["steps"]:
        step["text"] = step["text"].replace("revenue management", "booking and billing data")
        step["text"] = step["text"].replace("Revenue Management", "Buchungs- und Abrechnungsdaten")

    if code in data.get("gateway", {}):
        data["gateway"][code]["hospitality_title"] = payload["gateway_hospitality"]


def main() -> None:
    path = ROOT / "config" / "path_content.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for code, payload in CONTENT.items():
        apply_language(data, code, payload)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for code, entity in ENTITY.items():
        loc_path = ROOT / "locales" / f"{code}.json"
        locale = json.loads(loc_path.read_text(encoding="utf-8"))
        locale["legal_page"]["entity_type"] = entity
        # Soften FR/IT contractual phrasing leftovers in locales if present.
        if code in COUNTERPARTY:
            old, new = COUNTERPARTY[code]
            for key in ("terms",):
                if old in locale["legal_page"].get(key, ""):
                    locale["legal_page"][key] = locale["legal_page"][key].replace(old, new)
        loc_path.write_text(
            json.dumps(locale, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print("Phase B content applied.")


if __name__ == "__main__":
    main()
