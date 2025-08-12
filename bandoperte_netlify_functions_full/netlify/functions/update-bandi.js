import { schedule } from '@netlify/functions';
import { getStore } from '@netlify/blobs';

function buildMeasures(){
  return {
    name: 'Bandi Italia – dataset auto',
    updated: new Date().toISOString().slice(0,10),
    measures: [
      { id:'resto-al-sud', name:'Resto al Sud', scoreBase:70, tags:['Under56','Sud/Crateri/Isole'], rules:{etaMax:55,areaSud:true}, check:['Documento identità e CF','Business plan e preventivi'], official:{title:'Invitalia', url:'https://www.invitalia.it/incentivi-e-strumenti/resto-al-sud'} }
    ]
  };
}

export const handler = schedule('25 4 * * *', async () => {
  const store = getStore('bandi');
  const payload = buildMeasures();
  await store.set('measures.json', JSON.stringify(payload), { metadata: { updated: payload.updated }});
  return { statusCode: 200, body: 'updated '+payload.updated };
});
