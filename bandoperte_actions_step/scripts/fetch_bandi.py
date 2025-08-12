#!/usr/bin/env python3
import json, os, re, requests
from datetime import datetime, timezone
from dateutil import tz
from bs4 import BeautifulSoup as BS

ROME = tz.gettz('Europe/Rome')

def now_iso():
    return datetime.now(tz=ROME).date().isoformat()

# Funzioni semplici per prendere le pagine ufficiali
def probe(url):
    try:
        r = requests.get(url, timeout=30, headers={'User-Agent':'bandoperte-bot'})
        r.raise_for_status()
        return r.text[:10000]  # non serve tutta la pagina
    except Exception as e:
        return ""

def build_dataset():
    measures = []

    # Resto al Sud (Invitalia)
    measures.append({
        "id":"resto-al-sud",
        "name":"Resto al Sud",
        "scoreBase":70,
        "tags":["Under56","Sud/Crateri/Isole"],
        "rules":{"etaMax":55,"areaSud":True},
        "check":["Documento identità e CF","Business plan e preventivi","Certificazioni (crateri/isole)","Dichiarazione rapporto di lavoro"],
        "official":{"title":"Invitalia","url":"https://www.invitalia.it/incentivi-e-strumenti/resto-al-sud"}
    })

    # Nuova Sabatini (MIMIT)
    measures.append({
        "id":"nuova-sabatini",
        "name":"Beni Strumentali – Nuova Sabatini",
        "scoreBase":60,
        "tags":["PMI","Macchinari/4.0/Green"],
        "rules":{"stato":["PMI"],"beni":True,"importoMin":5000},
        "check":["Preventivi beni strumentali","Delibera finanziamento/leasing","Dichiarazioni PMI","Prospetto investimenti"],
        "official":{"title":"MIMIT","url":"https://www.mimit.gov.it/it/incentivi/agevolazioni-per-gli-investimenti-delle-pmi-in-beni-strumentali-nuova-sabatini"}
    })

    # ZES Unica (Agenzia Entrate)
    measures.append({
        "id":"zes-unica",
        "name":"Credito d'imposta ZES Unica Mezzogiorno",
        "scoreBase":58,
        "tags":["Sud","Investimenti"],
        "rules":{"areaSud":True,"areazes":True,"importoMin":10000},
        "check":["Ubicazione in ZES","Prospetto investimenti","Impegni 5 anni"],
        "official":{"title":"Agenzia Entrate","url":"https://www.agenziaentrate.gov.it/portale/credito-imposta-per-investimenti-in-zes-unica/infogen-credito-imposta-per-investimenti-in-zes-unica-imprese"}
    })

    # Smart&Start (Invitalia)
    measures.append({
        "id":"smart-start",
        "name":"Smart&Start Italia",
        "scoreBase":56,
        "tags":["Startup innovativa","Innovazione","R&S"],
        "rules":{"stato":["Startup innovativa"],"ricerca":True,"importoMin":30000},
        "check":["Business plan innovazione","Iscrizione sezione startup innovativa","Preventivi R&S"],
        "official":{"title":"Invitalia","url":"https://www.invitalia.it/cosa-facciamo/sosteniamo-le-imprese/smartstart-italia"}
    })

    # ON – Nuove imprese a tasso zero (Invitalia)
    measures.append({
        "id":"on-nuove-imprese",
        "name":"ON – Oltre Nuove Imprese a Tasso Zero",
        "scoreBase":57,
        "tags":["Giovani/Donne","Investimenti"],
        "rules":{"stato":["Costituenda","PMI"],"importoMin":10000},
        "check":["Business plan","Dichiarazioni compagine (giovani/donne)","Preventivi","Dichiarazioni PMI"],
        "official":{"title":"Invitalia","url":"https://www.invitalia.it/cosa-facciamo/creiamo-nuove-aziende/nuove-imprese-a-tasso-zero"}
    })

    # (Qui puoi aggiungere altre fonti: ISMEA, ICE, Regioni, ecc.)

    return {
        "name":"Bandi Italia – dataset auto",
        "updated": now_iso(),
        "measures": measures
    }

def main():
    payload = build_dataset()
    os.makedirs("data", exist_ok=True)
    with open("data/measures.json","w",encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("Scritto data/measures.json con", len(payload["measures"]), "misure.")

if __name__ == "__main__":
    main()
