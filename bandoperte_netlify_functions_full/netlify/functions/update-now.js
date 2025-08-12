import { getStore } from '@netlify/blobs';
export async function handler(event){
  if(event.httpMethod!=='POST') return { statusCode:405, body:'POST only' };
  const store = getStore('bandi');
  const payload = { name:'Bandi Italia – manual', updated: new Date().toISOString().slice(0,10), measures:[{ id:'test', name:'Prova', scoreBase:50, tags:[], rules:{}, check:[], official:{title:'',url:''} }] };
  await store.set('measures.json', JSON.stringify(payload), { metadata: { updated: payload.updated }});
  return { statusCode:200, body:'ok' };
}
