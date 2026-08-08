# -*- coding: utf-8 -*-
"""Add Italian language support to the static site sources."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    site_path = ROOT / "config" / "site.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    codes = [item["code"] for item in site["languages"]]
    if "it" not in codes:
        languages = site["languages"]
        fr_idx = next(i for i, item in enumerate(languages) if item["code"] == "fr")
        languages.insert(
            fr_idx + 1,
            {"code": "it", "label": "IT", "hreflang": "it-CH"},
        )
        site["languages"] = languages

    for path_key in ("hospitality", "market"):
        langs = site["paths"][path_key]["languages"]
        if "it" not in langs:
            if path_key == "hospitality" and "fr" in langs:
                langs.insert(langs.index("fr") + 1, "it")
            elif path_key == "market" and "en" in langs:
                langs.insert(langs.index("en") + 1, "it")
            else:
                langs.append("it")
        site["paths"][path_key]["languages"] = langs
        site["paths"][path_key]["slugs"]["it"] = (
            "hospitality" if path_key == "hospitality" else "mercato"
        )

    site_path.write_text(
        json.dumps(site, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    it_locale = {
        "lang": "it-CH",
        "skip": "Vai al contenuto",
        "language_suggestion": {
            "prompt": "Vuole aprire questa pagina nella lingua del browser?",
            "switch": "Cambia lingua",
            "dismiss": "Chiudi",
        },
        "meta": {
            "title": "Supporto IT Zurigo e sviluppo mercato Svizzera | BIT",
            "description": (
                "Supporto IT per PMI e hospitality a Zurigo, nonché sviluppo "
                "e verifica del mercato svizzero per offerte B2B."
            ),
            "keywords": (
                "supporto IT Zurigo, IT PMI Svizzera, IT hotel, revenue management, "
                "Microsoft 365 Zurigo, ingresso mercato Svizzera"
            ),
        },
        "nav": {
            "aria": "Navigazione principale",
            "services": "Prestazioni",
            "market": "Mercato svizzero",
            "about": "Su BIT",
            "contact": "Contatto",
            "menu": "Menu",
            "languages": "Scegliere la lingua",
        },
        "hero": {
            "eyebrow": "",
            "title": "",
            "lead": "",
            "services_button": "",
            "trust": "",
        },
        "services": {"eyebrow": "", "title": "", "intro": "", "cards": []},
        "market": {"eyebrow": "", "title": "", "text": "", "items": []},
        "audiences": {"eyebrow": "", "title": "", "intro": "", "cards": []},
        "process": {"eyebrow": "", "title": "", "intro": "", "steps": []},
        "assurance": {"title": "", "text": "", "items": []},
        "faq": {"title": "", "items": []},
        "about": {
            "eyebrow": "Su di me",
            "title": "Stefan Bogdanovic",
            "text": "Vivo e lavoro a Zurigo.",
            "independent": (
                "Lavoro in modo indipendente e non rappresento ufficialmente "
                "alcun fornitore PMS o software."
            ),
            "image_alt": "Stefan Bogdanovic a Zurigo",
        },
        "contact": {
            "eyebrow": "Contatto diretto",
            "title": "Scrivetemi direttamente.",
            "text": "Nessun modulo. Descrivete brevemente la richiesta.",
            "whatsapp": "Scrivere su WhatsApp",
            "viber": "Scrivere su Viber",
            "email": "Inviare un'e-mail",
            "email_subject": "Richiesta via boksitsupport.ch",
            "quick_contact": "Contatto rapido",
        },
        "footer": {
            "location": "Zurigo, Svizzera",
            "legal": "Note legali",
            "privacy": "Protezione dei dati",
        },
        "legal_page": {
            "title": "Note legali",
            "eyebrow": "Informazioni legali",
            "lead": (
                "Identificazione del prestatore e informazioni sull'uso di questo sito. "
                "Diritto applicabile principale: Svizzera."
            ),
            "back": "Torna al sito",
            "provider_title": "Prestatore",
            "provider_name": "BIT – Boks IT Support",
            "entity_type": "Einzelfirma",
            "owner": "Responsabile dei contenuti: Stefan Bogdanovic",
            "activity_title": "Attività",
            "activity": (
                "Sviluppo del mercato svizzero nonché supporto IT e assistenza "
                "digitale per PMI e hospitality."
            ),
            "address_title": "Indirizzo",
            "city": "Zurigo",
            "country": "Svizzera",
            "contact_title": "Contatto",
            "registration_title": "Registro e fiscalità",
            "registration": (
                "Eventuali identificativi aziendali, del registro di commercio o IVA "
                "sono comunicati su richiesta. Qui vengono pubblicate solo informazioni "
                "note e verificate."
            ),
            "terms_title": "Condizioni generali – punti essenziali",
            "terms": (
                "Ambito, prezzo e calendario sono concordati per iscritto. Le spese di "
                "terzi richiedono un'autorizzazione; ogni rappresentanza richiede un "
                "mandato scritto esplicito. Si tratta di punti essenziali e non di una "
                "consulenza legale completa. Il partner contrattuale rimango io."
            ),
            "liability_title": "Responsabilità dei contenuti",
            "liability": (
                "I contenuti di questo sito sono preparati con cura. Non viene fornita "
                "alcuna assicurazione di completezza, esattezza o disponibilità continua. "
                "I contenuti dei siti esterni collegati restano di esclusiva responsabilità "
                "dei rispettivi gestori."
            ),
            "copyright_title": "Diritto d'autore",
            "copyright": (
                "© 2026 BIT – Boks IT Support. Tutti i diritti riservati. Testi, design e "
                "altri contenuti di questo sito non possono essere riprodotti, diffusi o "
                "utilizzati diversamente senza previa autorizzazione scritta."
            ),
            "privacy_title": "Protezione dei dati",
            "privacy": (
                "Questo sito statico non utilizza moduli di contatto né tracking "
                "proprietario. Il fornitore di hosting può elaborare i log tecnici "
                "necessari. In caso di contatto via WhatsApp, Viber o e-mail valgono "
                "anche le regole sulla riservatezza del rispettivo fornitore."
            ),
            "privacy_messaging": (
                "WhatsApp e Viber possono elaborare e trasferire metadati di contatto, "
                "dispositivo e comunicazione fuori dalla Svizzera. E-mail e telefono "
                "restano disponibili come alternative. Non inviate mai credenziali "
                "riservate tramite messaggistica."
            ),
            "jurisdiction_title": "Diritto applicabile e foro",
            "jurisdiction": (
                "Si applica il diritto svizzero. Nella misura consentita dalla legge, "
                "Zurigo è il foro per le controversie relative a questo sito e alle "
                "prestazioni proposte."
            ),
            "updated": "Aggiornamento: luglio 2026",
        },
    }
    (ROOT / "locales" / "it.json").write_text(
        json.dumps(it_locale, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    pc_path = ROOT / "config" / "path_content.json"
    pc = json.loads(pc_path.read_text(encoding="utf-8"))
    pc["gateway"]["it"] = {
        "meta_title": "BIT – Supporto IT e sviluppo del mercato svizzero",
        "meta_description": (
            "Due ambiti distinti: Digital & Hospitality per imprese svizzere e "
            "sviluppo di mercato per fornitori internazionali."
        ),
        "identity": "BIT — Stefan Bogdanovic, {city}",
        "title": "Due ambiti di prestazioni distinti.",
        "subtitle": "Scelga quello adatto.",
        "hospitality_title": "Digital & Hospitality",
        "hospitality_text": "per hotel, ristoranti e PMI svizzere",
        "hospitality_note": "",
        "market_title": "Sviluppo del mercato svizzero",
        "market_text": "per fornitori internazionali che valutano il mercato svizzero",
    }
    pc["it"] = {
        "common": {
            "skip": "Vai al contenuto",
            "menu": "Menu",
            "languages": "Scegliere la lingua",
            "about": "Su di me",
            "legal": "Note legali",
            "contact": "Contatto",
            "whatsapp": "Scrivere su WhatsApp",
            "viber": "Scrivere su Viber",
            "email": "Inviare un'e-mail",
            "warning": (
                "Non inviate password, codici di accesso o dati riservati dei clienti "
                "tramite app di messaggistica."
            ),
            "exclusions": "Cosa non faccio",
            "price": "Prezzo",
            "back": "Torna all'offerta",
            "about_title": "Su di me",
            "about_lead": (
                "Sono Stefan Bogdanovic e gestisco BIT come Einzelfirma a Zurigo."
            ),
            "about_text": (
                "Supporto piccole e medie imprese in compiti IT e digitali chiaramente "
                "delimitati. Per il mercato B2B svizzero conduco mandati pilota "
                "strutturati. Prima verifico situazione di partenza, dipendenze e limiti, "
                "poi documento i risultati concordati. Se un incarico richiede competenze "
                "aggiuntive, lo indico prima dell'inizio e coinvolgo specialisti esterni "
                "solo previo accordo. Il partner contrattuale rimango io."
            ),
            "about_independent": (
                "Lavoro in modo indipendente e non rappresento ufficialmente alcun "
                "fornitore PMS o software."
            ),
            "image_alt": "Stefan Bogdanovic a Zurigo",
        },
        "hospitality": {
            "meta_title": "Supporto Digital & Hospitality Zurigo | BIT",
            "meta_description": (
                "Supporto IT, hospitality e revenue management delimitato per PMI, "
                "hotel e ristoranti a Zurigo."
            ),
            "eyebrow": "Digital & Hospitality · Zurigo",
            "title": "Verificare e realizzare compiti IT e digitali definiti.",
            "lead": (
                "Supporto PMI, hotel e ristoranti con incidenti concreti, domande di "
                "sistema, flussi digitali e revenue management delimitato."
            ),
            "nav": ["Prestazioni", "Prezzi", "Limiti"],
            "blocks": [
                {
                    "title": "Hospitality: hotel e ristoranti",
                    "text": (
                        "Verifico flussi chiaramente delimitati tra reception, "
                        "prenotazioni, cassa, esercizio e revenue."
                    ),
                    "items": [
                        "Verificare percorsi PMS/OTA, tariffe, disponibilità e mapping",
                        (
                            "Revenue management: verificare occupazione, scostamenti "
                            "ADR/RevPAR e logica tariffaria sui dati forniti"
                        ),
                        (
                            "Ricostruire e correggere casi di no-show, cancellazione, "
                            "tasse e folio"
                        ),
                        (
                            "Isolare problemi di cassa, stampanti, Wi-Fi, dispositivi "
                            "e accessi utente"
                        ),
                        "Documentare in modo chiaro rilievi, modifiche e punti aperti",
                    ],
                },
                {
                    "title": "IT per PMI e compiti digitali",
                    "text": (
                        "Gestisco compiti IT concreti per piccoli team senza un "
                        "reparto IT interno."
                    ),
                    "items": [
                        "Verificare Microsoft 365, MFA, Outlook e autorizzazioni",
                        (
                            "Isolare incidenti di dispositivi Windows, stampanti, "
                            "Wi-Fi e e-mail"
                        ),
                        "Documentare account, ruoli, aggiornamenti e consegna",
                    ],
                },
            ],
            "process": {
                "title": "Come procedo",
                "intro": (
                    "Cinque punti di contatto fissi strutturano ogni intervento "
                    "concordato."
                ),
                "steps": [
                    {
                        "title": "Preparazione",
                        "text": (
                            "Chiarisco obiettivo, ambito scritto, materiali necessari e "
                            "modalità di accesso sicura. Registro anche ciò che non fa "
                            "parte dell'incarico."
                        ),
                    },
                    {
                        "title": "Arrivo al lavoro",
                        "text": (
                            "Inizio da remoto o in loco secondo accordo. Prima verifico "
                            "l'ambiente di lavoro e confermo l'obiettivo dell'intervento."
                        ),
                    },
                    {
                        "title": "Lavoro quotidiano",
                        "text": (
                            "Eseguo i compiti concordati per iscritto, ad esempio casi "
                            "PMS, folio o channel, Microsoft 365, dispositivi o revenue "
                            "management. Registro modifiche e rilievi entro l'ambito "
                            "concordato."
                        ),
                    },
                    {
                        "title": "Compiti speciali",
                        "text": (
                            "Prendo in carico eccezioni una tantum solo con un "
                            "mini-ambito separato concordato per iscritto. Ciò non crea "
                            "un supporto aperto o illimitato."
                        ),
                    },
                    {
                        "title": "Chiusura",
                        "text": (
                            "Consegno rilievi, punti aperti e il passo successivo, poi "
                            "chiudo l'intervento in modo pulito. Non invio mai "
                            "credenziali riservate tramite messaggistica e non le "
                            "richiedo lì."
                        ),
                    },
                ],
            },
            "pricing": [
                "Lavoro: {hourly} all'ora",
                "Piccolo incarico chiaramente delimitato: da {small_job}",
                "Spostamento entro Zurigo: {zurich_travel}",
            ],
            "exclusions": [
                "Nessuna disponibilità 24/7 né tempo di risposta garantito",
                "Nessun supporto illimitato di sistemi di terzi",
                "Nessuna rappresentanza di fornitore né acquisto senza mandato",
                (
                    "Nessuna garanzia di fatturato e nessun subentro della "
                    "responsabilità commerciale complessiva"
                ),
            ],
            "honesty": (
                "Prima dell'inizio delimito compito, impegno e accessi necessari. Se "
                "una realizzazione sicura e solida non è possibile, lo dico apertamente."
            ),
        },
        "market": {
            "meta_title": "Pilota svizzero per sviluppo mercato B2B | BIT",
            "meta_description": (
                "Sei settimane di verifica strutturata del mercato per un'offerta B2B "
                "chiaramente definita in Svizzera."
            ),
            "eyebrow": "Sviluppo del mercato svizzero",
            "title": "Dal controllo documenti al pilota sul mercato svizzero.",
            "lead": (
                "Verifico con voi se e come un'offerta chiaramente definita possa "
                "essere posizionata e testata presso imprese svizzere selezionate."
            ),
            "nav": ["Controllo documenti", "Prezzo", "Limiti"],
            "document_title": "Controllo documenti",
            "document_text": (
                "La vostra offerta, profilo di capacità o testo aziendale in tedesco "
                "commerciale svizzero. {small_job} per documento, 5 giorni lavorativi, "
                "un ciclo di correzioni."
            ),
            "pilot_eyebrow": "Secondo passo",
            "pilot_title": "Il pilota di sei settimane",
            "pilot_intro": (
                "Il pilota è un mandato di verifica delimitato con risultati "
                "documentati."
            ),
            "deliverables": [
                (
                    "Colloquio iniziale e delimitazione scritta di offerta, segmento "
                    "target e ipotesi"
                ),
                (
                    "Verifica di posizionamento, argomentazione di valore, logica dei "
                    "prezzi e documenti esistenti"
                ),
                "Elenco motivato di imprese target e referenti adatti",
                (
                    "Primo contatto concordato a nome di BIT; rappresentanza solo con "
                    "mandato scritto esplicito"
                ),
                "Documentazione settimanale di attività, risposte e domande aperte",
                (
                    "Rapporto finale con osservazioni e una raccomandazione sobria "
                    "sul seguito"
                ),
            ],
            "pricing": [
                "Controllo documenti: {small_job} per documento",
                "Prezzo fisso pilota: {pilot}",
                "Pagamento pilota: 50 % all'incarico, 50 % dopo il rapporto finale",
            ],
            "optional_title": "Opzionale dopo il pilota",
            "optional": (
                "Un mandato successivo viene concordato solo con interesse reciproco, "
                "ambito scritto e remunerazione separata. Il partner contrattuale "
                "rimango io."
            ),
            "exclusions": [
                (
                    "Nessuna promessa di clienti, fatturato, contratti o successo "
                    "di mercato"
                ),
                "Nessuna consulenza legale, fiscale, doganale o di certificazione",
                (
                    "Nessuna procura di rappresentanza, conclusione contratti o "
                    "riscossione senza mandato scritto esplicito"
                ),
                (
                    "Spese di viaggio, traduzioni o prestazioni di terzi non incluse "
                    "nel prezzo fisso"
                ),
            ],
            "honesty": (
                "Il pilota non usa prove di successo inventate e non crea domanda di "
                "mercato. Fornisce una base documentata per decidere; anche un esito "
                "negativo motivato è un risultato utile."
            ),
        },
    }
    pc_path.write_text(
        json.dumps(pc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Italian sources ready")
    print("languages", [item["code"] for item in site["languages"]])
    print("hospitality", site["paths"]["hospitality"]["languages"])
    print("market", site["paths"]["market"]["languages"])


if __name__ == "__main__":
    main()
