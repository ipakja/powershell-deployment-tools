# -*- coding: utf-8 -*-
"""Tighten pilot scope, BIT outreach role, and hospitality approval wording."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

UPDATES = {
    "de": {
        "pilot_intro": (
            "Der Pilot ist ein abgegrenztes Prüfmandat mit dokumentierten Ergebnissen. "
            "Der genaue Umfang der Zielkundenrecherche, der Erstansprache und des "
            "Abschlussberichts wird vor Auftragserteilung schriftlich festgelegt."
        ),
        "outreach": (
            "Transparente Erstansprache durch BIT als beauftragter Marktprüfer; "
            "Identität, Angebot und Unterlagen des Auftraggebers nur im vorher "
            "schriftlich vereinbarten Umfang. Vertretung nur mit ausdrücklichem "
            "schriftlichem Mandat"
        ),
        "honesty": (
            "Der Pilot liefert keine erfundenen Erfolgsnachweise und ersetzt keine "
            "Marktnachfrage. Er schafft eine dokumentierte Entscheidungsgrundlage; "
            "auch ein begründetes negatives Ergebnis ist ein verwertbares Ergebnis. "
            "Stellt sich früh heraus, dass das Angebot ungeeignet ist, halte ich das "
            "schriftlich fest und beende den vereinbarten Restumfang nicht als "
            "Scheinaktivität."
        ),
        "folio": (
            "No-Show-, Storno-, Gebühren- und Folio-Fälle nachvollziehen und "
            "vereinbarte Korrekturen nach Freigabe umsetzen"
        ),
        "m365": (
            "Microsoft 365, MFA und Outlook prüfen; Berechtigungsänderungen nur nach "
            "dokumentierter Freigabe"
        ),
    },
    "en": {
        "pilot_intro": (
            "The pilot is a scoped validation mandate with documented outputs. "
            "The exact scope of target-company research, initial outreach and the "
            "final report is agreed in writing before work starts."
        ),
        "outreach": (
            "Transparent initial outreach by BIT as an appointed market reviewer; "
            "the client’s identity, offer and materials are used only within the "
            "scope agreed in writing beforehand. Representation only under an "
            "explicit written mandate"
        ),
        "honesty": (
            "The pilot does not use invented performance evidence and cannot create "
            "market demand. It provides a documented basis for a decision; a reasoned "
            "negative result is also useful. If it becomes clear early that the offer "
            "is unsuitable, I record this in writing and do not continue the remaining "
            "agreed scope as empty activity."
        ),
        "folio": (
            "Trace no-show, cancellation, fee and folio cases and implement agreed "
            "corrections after approval"
        ),
        "m365": (
            "Review Microsoft 365, MFA and Outlook; change permissions only after "
            "documented approval"
        ),
    },
    "fr": {
        "pilot_intro": (
            "Le pilote est un mandat de validation délimité avec des résultats "
            "documentés. L’étendue exacte de la recherche d’entreprises cibles, du "
            "premier contact et du rapport final est fixée par écrit avant le mandat."
        ),
        "outreach": (
            "Premier contact transparent par BIT en tant que vérificateur de marché "
            "mandaté ; l’identité, l’offre et les documents du mandant ne sont utilisés "
            "que dans le périmètre convenu par écrit au préalable. Représentation "
            "uniquement avec mandat écrit explicite"
        ),
        "honesty": (
            "Le pilote n’utilise aucune preuve de succès inventée et ne crée pas de "
            "demande de marché. Il fournit une base documentée pour décider ; un "
            "résultat négatif motivé est aussi un résultat utile. S’il apparaît tôt "
            "que l’offre n’est pas adaptée, je le consigne par écrit et je ne poursuis "
            "pas le reste du périmètre convenu comme activité de façade."
        ),
        "folio": (
            "Retracer les cas de no-show, d’annulation, de taxes et de folio et "
            "mettre en œuvre les corrections convenues après validation"
        ),
        "m365": (
            "Contrôler Microsoft 365, MFA et Outlook ; modifier les autorisations "
            "uniquement après validation documentée"
        ),
    },
    "it": {
        "pilot_intro": (
            "Il pilota è un mandato di verifica delimitato con risultati documentati. "
            "L’esatto ambito della ricerca di imprese target, del primo contatto e del "
            "rapporto finale viene definito per iscritto prima dell’incarico."
        ),
        "outreach": (
            "Primo contatto trasparente da parte di BIT come verificatore di mercato "
            "incaricato; identità, offerta e documenti del committente solo nell’ambito "
            "concordato per iscritto in precedenza. Rappresentanza solo con mandato "
            "scritto esplicito"
        ),
        "honesty": (
            "Il pilota non usa prove di successo inventate e non crea domanda di "
            "mercato. Fornisce una base documentata per decidere; anche un esito "
            "negativo motivato è un risultato utile. Se emerge presto che l’offerta "
            "non è adatta, lo documento per iscritto e non proseguo il resto "
            "dell’ambito concordato come attività apparente."
        ),
        "folio": (
            "Ricostruire casi di no-show, cancellazione, tasse e folio e attuare le "
            "correzioni concordate dopo approvazione"
        ),
        "m365": (
            "Verificare Microsoft 365, MFA e Outlook; modificare le autorizzazioni "
            "solo dopo approvazione documentata"
        ),
    },
    "sr": {
        "pilot_intro": (
            "Pilot je ograničen mandat provere sa dokumentovanim rezultatima. Tačan "
            "obim istraživanja ciljnih firmi, prvog kontakta i završnog izveštaja "
            "utvrđuje se pismeno pre početka mandata."
        ),
        "outreach": (
            "Transparentan prvi kontakt od strane BIT-a kao angažovanog proveravača "
            "tržišta; identitet, ponuda i dokumentacija naručioca samo u prethodno "
            "pismeno dogovorenom obimu. Zastupanje samo uz izričit pisani mandat"
        ),
        "honesty": (
            "Pilot ne koristi izmišljene rezultate i ne može da stvori tržišnu "
            "tražnju. Daje dokumentovanu osnovu za odluku; i obrazložen negativan "
            "rezultat je koristan. Ako se rano pokaže da ponuda nije pogodna, to "
            "beležim pismeno i ne nastavljam preostali dogovoreni obim kao "
            "prividnu aktivnost."
        ),
        "folio": (
            "Pratim no-show, otkazivanja, naknade i folio-slučajeve i sprovodim "
            "dogovorene korekcije tek nakon odobrenja"
        ),
        "m365": (
            "Proveravam Microsoft 365, MFA i Outlook; dozvole menjam samo nakon "
            "dokumentovanog odobrenja"
        ),
    },
    "bs": {
        "pilot_intro": (
            "Pilot je ograničen mandat provjere s dokumentovanim rezultatima. Tačan "
            "obim istraživanja ciljnih firmi, prvog kontakta i završnog izvještaja "
            "utvrđuje se pismeno prije početka mandata."
        ),
        "outreach": (
            "Transparentan prvi kontakt od strane BIT-a kao angažovanog provjeravača "
            "tržišta; identitet, ponuda i dokumentacija naručioca samo u prethodno "
            "pismeno dogovorenom obimu. Zastupanje samo uz izričit pisani mandat"
        ),
        "honesty": (
            "Pilot ne koristi izmišljene rezultate i ne može stvoriti tržišnu "
            "potražnju. Daje dokumentovanu osnovu za odluku; i obrazložen negativan "
            "rezultat je koristan. Ako se rano pokaže da ponuda nije pogodna, to "
            "bilježim pismeno i ne nastavljam preostali dogovoreni obim kao "
            "prividnu aktivnost."
        ),
        "folio": (
            "Pratim no-show, otkazivanja, naknade i folio-slučajeve i provodim "
            "dogovorene korekcije tek nakon odobrenja"
        ),
        "m365": (
            "Provjeravam Microsoft 365, MFA i Outlook; dozvole mijenjam samo nakon "
            "dokumentovanog odobrenja"
        ),
    },
    "hr": {
        "pilot_intro": (
            "Pilot je ograničen mandat provjere s dokumentiranim rezultatima. Točan "
            "opseg istraživanja ciljnih tvrtki, prvog kontakta i završnog izvješća "
            "utvrđuje se pisano prije početka mandata."
        ),
        "outreach": (
            "Transparentan prvi kontakt od strane BIT-a kao angažiranog provjeravatelja "
            "tržišta; identitet, ponuda i dokumentacija naručitelja samo u unaprijed "
            "pisano dogovorenom opsegu. Zastupanje samo uz izričit pisani mandat"
        ),
        "honesty": (
            "Pilot ne koristi izmišljene rezultate i ne može stvoriti tržišnu "
            "potražnju. Daje dokumentiranu osnovu za odluku; koristan je i obrazložen "
            "negativan rezultat. Ako se rano pokaže da ponuda nije pogodna, to "
            "bilježim pisano i ne nastavljam preostali dogovoreni opseg kao "
            "prividnu aktivnost."
        ),
        "folio": (
            "Pratim no-show, otkazivanja, naknade i folio-slučajeve i provodim "
            "dogovorene korekcije tek nakon odobrenja"
        ),
        "m365": (
            "Provjeravam Microsoft 365, MFA i Outlook; ovlasti mijenjam samo nakon "
            "dokumentiranog odobrenja"
        ),
    },
}


def main() -> None:
    path = ROOT / "config" / "path_content.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for code, payload in UPDATES.items():
        market = data[code]["market"]
        hosp = data[code]["hospitality"]
        market["pilot_intro"] = payload["pilot_intro"]
        market["honesty"] = payload["honesty"]
        # outreach is typically deliverable index 3
        market["deliverables"][3] = payload["outreach"]
        # folio item ~ index 2 in hospitality block 0, m365 in block 1 item 0
        items0 = hosp["blocks"][0]["items"]
        items1 = hosp["blocks"][1]["items"]
        for i, item in enumerate(items0):
            if any(k in item.lower() for k in ("folio", "no-show", "no show")):
                items0[i] = payload["folio"]
                break
        for i, item in enumerate(items1):
            if "Microsoft 365" in item or "365" in item:
                items1[i] = payload["m365"]
                break
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Scope, outreach role and approval wording applied.")


if __name__ == "__main__":
    main()
