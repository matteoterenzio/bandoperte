BandoPerTe – Auto (SOLO Netlify, senza GitHub)
==============================================
Cosa ottieni:
- Il sito legge i bandi da `/.netlify/functions/measures` (JSON lato server).
- Una funzione pianificata aggiorna ogni giorno i dati e li salva in **Netlify Blobs**.
- Un pulsante "Forza aggiornamento (server)" ti permette di aggiornare manualmente senza fare deploy.

Cosa fai tu (1 minuto):
1) Scarica e scompatta questo pacchetto.
2) Su Netlify → bandoperte → Deploys → **Drag & Drop** dell'intera cartella.
3) Vai su Site configuration → Functions e assicurati che le **Scheduled Functions** siano abilitate (nei piani che le supportano).
4) Apri il sito: la scritta in alto mostrerà il dataset lato server. L'aggiornamento giornaliero partirà automaticamente.

Nota: Il job giornaliero è impostato alle 04:25 UTC (~06:25 Italia).


Aggiornato: 2025-08-12
