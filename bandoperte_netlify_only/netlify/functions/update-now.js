import { getStore } from '@netlify/blobs';

async function buildMeasures() {
  // same minimal dataset as scheduled job (to keep it short)
  return {
    name: 'Bandi Italia – dataset auto (manual)',
    updated: new Date().toISOString().slice(0,10),
    measures: [
      { id:'resto-al-sud', name:'Resto al Sud', scoreBase:70, tags:['Under56','Sud/Crateri/Isole'], rules:{etaMax:55,areaSud:true}, check:['Documento identità e CF','Business plan e preventivi'], official:{title:'Invitalia', url:'https://www.invitalia.it/incentivi-e-strumenti/resto-al-sud'} }
    ]
  };
}

export async function handler(event) {
  if (event.httpMethod !== 'POST') return { statusCode: 405, body: 'POST only' };
  const store = getStore('bandi');
  const payload = await buildMeasures();
  await store.set('measures.json', JSON.stringify(payload), { metadata: { updated: payload.updated }});
  return { statusCode: 200, body: 'ok' };
}
