import { getStore } from '@netlify/blobs';
export async function handler() {
  const store = getStore('bandi');
  const data = await store.get('measures.json', { type: 'json' });
  const payload = data || { name: 'Dataset iniziale', updated: new Date().toISOString().slice(0,10), measures: [] };
  return { statusCode: 200, headers: {'Content-Type':'application/json','Cache-Control':'no-store'}, body: JSON.stringify(payload) };
}
