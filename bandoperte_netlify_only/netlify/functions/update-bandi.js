import { schedule } from '@netlify/functions';
import { getStore } from '@netlify/blobs';

async function fetchJSON(url) {
  const r = await fetch(url, { headers: { 'User-Agent': 'bandoperte-bot' }});
  if (!r.ok) throw new Error('HTTP '+r.status);
  const txt = await r.text();
  return { ok: true, html: txt };
}

function baseMeasure(id, name, url, scoreBase, tags, rules = {}, check = []) {
  return { id, name, scoreBase, tags, rules, check, official: { title: name.split('–')[0], url } };
}

async function buildMeasures() {
  const sources = [
    ['resto-al-sud','Resto al Sud','https://www.invitalia.it/incentivi-e-strumenti/resto-al-sud',70,['Under56','Sud/Crateri/Isole'],{etaMax:55,areaSud:true},['Documento identità e CF','Business plan e preventivi']],
    ['nuova-sabatini','Beni Strumentali – Nuova Sabatini','https://www.mimit.gov.it/it/incentivi/agevolazioni-per-gli-investimenti-delle-pmi-in-beni-strumentali-nuova-sabatini',60,['PMI','Macchinari/4.0/Green'],{stato:['PMI'],beni:true,importoMin:5000},['Preventivi beni strumentali','Dichiarazioni PMI']],
    ['zes-unica','Credito d\'imposta ZES Unica Mezzogiorno','https://www.agenziaentrate.gov.it/portale/credito-imposta-per-investimenti-in-zes-unica/infogen-credito-imposta-per-investimenti-in-zes-unica-imprese',58,['Sud','Investimenti'],{areaSud:true,areazes:true,importoMin:10000},['Ubicazione in ZES','Prospetto investimenti','Impegni 5 anni']],
    ['smartstart-italia','Smart&Start Italia','https://www.invitalia.it/cosa-facciamo/sosteniamo-le-imprese/smartstart-italia',56,['Startup innovativa','R&S'],{stato:['Startup innovativa'],ricerca:true,importoMin:30000},['Business plan innovazione']],
    ['nuove-imprese-tasso-zero','ON – Nuove Imprese a Tasso Zero','https://www.invitalia.it/cosa-facciamo/creiamo-nuove-aziende/nuove-imprese-a-tasso-zero',57,['Giovani/Donne','Investimenti'],{stato:['Costituenda','PMI'],importoMin:10000},['Business plan','Preventivi']]
  ];
  // Optionally, here we could fetch and parse pages to detect changes; for now we just verify reachability
  await Promise.allSettled(sources.map(s => fetchJSON(s[2]))); // warm check
  return {
    name: 'Bandi Italia – dataset auto (Netlify)',
    updated: new Date().toISOString().slice(0,10),
    measures: sources.map(s => baseMeasure(...s))
  };
}

export const handler = schedule('25 4 * * *', async () => {
  const store = getStore('bandi');
  const payload = await buildMeasures();
  await store.set('measures.json', JSON.stringify(payload), { metadata: { updated: payload.updated }});
  return { statusCode: 200, body: 'updated '+payload.updated };
});
