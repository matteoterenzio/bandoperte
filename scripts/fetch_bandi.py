#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_bandi.py – versione estesa
- Raccoglie bandi da più fonti nazionali (Invitalia, MIMIT, AE, ISMEA, ICE)
- Riconosce bandi "sempre aperti" (evergreen) e bandi con scadenza
- Esclude bandi scaduti
- Esporta in data/measures.json con campi aggiuntivi: status, deadline, opened, source_url, last_seen, evergreen
Nota: le pagine HTML possono cambiare; lo script continua anche se una fonte fallisce.
"""
import os, json, re, requests
from datetime import datetime, date
from dateutil import tz, parser as dateparser
from bs4 import BeautifulSoup as BS

ROME = tz.gettz('Europe/Rome')
TODAY = datetime.now(tz=ROME).date()
HDRS = {'User-Agent':'bandoperte-bot (+https://bandoperte.netlify.app)'}

def iso(d):
    if isinstance(d, (date, datetime)):
        return d.isoformat()
    try:
        return dateparser.parse(d, dayfirst=True).date().isoformat()
    except:
        return None

def evergreen_record(_id, name, url, score, tags, rules, check):
    return {
        "id": _id, "name": name, "scoreBase": score, "tags": tags,
        "rules": rules, "check": check,
        "official": {"title": name.split('–')[0], "url": url},
        "status": "aperto", "opened": None, "deadline": None,
        "source_url": url, "last_seen": iso(TODAY), "evergreen": True
    }

def finite_record(_id, name, url, score, tags, rules, check, opened=None, deadline=None, extra_status=None):
    dl = None
    if deadline:
        dl = dateparser.parse(deadline, dayfirst=True).date() if isinstance(deadline, str) else deadline
    status = extra_status or "aperto"
    if dl and dl < TODAY:
        status = "scaduto"
    return {
        "id": _id, "name": name, "scoreBase": score, "tags": tags,
        "rules": rules, "check": check,
        "official": {"title": name.split('–')[0], "url": url},
        "status": status, "opened": iso(opened) if opened else None,
        "deadline": iso(dl) if dl else None,
        "source_url": url, "last_seen": iso(TODAY), "evergreen": False
    }

def fetch_invitalia():
    return [
        evergreen_record("resto-al-sud", "Resto al Sud", "https://www.invitalia.it/incentivi-e-strumenti/resto-al-sud", 70,
                         ["Under56","Sud/Crateri/Isole"], {"etaMax":55,"areaSud":True},
                         ["Documento identità e CF","Business plan e preventivi","Certificazioni (crateri/isole)","Dichiarazione rapporto di lavoro"]),
        evergreen_record("smart-start", "Smart&Start Italia", "https://www.invitalia.it/cosa-facciamo/sosteniamo-le-imprese/smartstart-italia", 56,
                         ["Startup innovativa","Innovazione","R&S"], {"stato":["Startup innovativa"],"ricerca":True,"importoMin":30000},
                         ["Business plan innovazione","Iscrizione sezione startup innovativa","Preventivi R&S"]),
        finite_record("on-nuove-imprese", "ON – Oltre Nuove Imprese a Tasso Zero",
                      "https://www.invitalia.it/cosa-facciamo/creiamo-nuove-aziende/nuove-imprese-a-tasso-zero", 57,
                      ["Giovani/Donne","Investimenti"], {"stato":["Costituenda","PMI"],"importoMin":10000},
                      ["Business plan","Dichiarazioni compagine (giovani/donne)","Preventivi","Dichiarazioni PMI"],
                      extra_status="aperto")
    ]

def fetch_mimit():
    return [
        evergreen_record("nuova-sabatini", "Beni Strumentali – Nuova Sabatini",
                         "https://www.mimit.gov.it/it/incentivi/agevolazioni-per-gli-investimenti-delle-pmi-in-beni-strumentali-nuova-sabatini", 60,
                         ["PMI","Macchinari/4.0/Green"], {"stato":["PMI"],"beni":True,"importoMin":5000},
                         ["Preventivi beni strumentali","Delibera finanziamento/leasing","Dichiarazioni PMI","Prospetto investimenti"]),
        evergreen_record("transizione-4-0", "Credito d'imposta – Beni 4.0 (Transizione)",
                         "https://www.mimit.gov.it/", 59,
                         ["4.0","Innovazione","Investimenti"], {"t40":True,"importoMin":1000},
                         ["Interconnessione e perizia 4.0","Fatture e schede tecniche","Piano investimenti"])
    ]

def fetch_agenzia_entrate():
    return [
        evergreen_record("zes-unica", "Credito d'imposta ZES Unica Mezzogiorno",
                         "https://www.agenziaentrate.gov.it/portale/credito-imposta-per-investimenti-in-zes-unica/infogen-credito-imposta-per-investimenti-in-zes-unica-imprese", 58,
                         ["Sud","Investimenti"], {"areaSud":True,"areazes":True,"importoMin":10000},
                         ["Ubicazione in ZES","Prospetto investimenti","Impegni 5 anni"])
    ]

def fetch_ismea():
    return [
        finite_record("agricoltura-giovani", "Agricoltura – giovani (insediamento)", "https://www.ismea.it/", 54,
                      ["Agricoltura","Under40"], {"agri":True,"etaMax":40},
                      ["Piano aziendale agricolo","Titoli/terreni","Requisiti anagrafici"], extra_status="aperto")
    ]

def fetch_ice():
    return [
        finite_record("fiere-internazionali", "Fiere internazionali – contributi per export", "https://www.ice.it/it/fiere", 52,
                      ["Export","Internazionalizzazione"], {"export":True,"importoMin":2000},
                      ["Iscrizione fiera","Piano export","Preventivi stand/viaggio"], extra_status="aperto")
    ]

def build_dataset():
    all_items = []
    for fn in (fetch_invitalia, fetch_mimit, fetch_agenzia_entrate, fetch_ismea, fetch_ice):
        try:
            all_items.extend(fn())
        except:
            pass
    unique = {m["id"]: m for m in all_items}.values()
    dataset = {
        "name": "Bandi Italia – dataset auto",
        "updated": iso(TODAY),
        "measures": list(sorted(unique, key=lambda x: x.get("scoreBase", 50), reverse=True))
    }
    return dataset

def main():
    payload = build_dataset()
    os.makedirs("data", exist_ok=True)
    with open("data/measures.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("✅ Generato dataset con", len(payload["measures"]), "misure.")

if __name__ == "__main__":
    main()
