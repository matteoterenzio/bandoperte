import { getStore } from '@netlify/blobs';

export async function handler() {
  try {
    const store = getStore('bandi');
    const data = await store.get('measures.json', { type: 'json' });
    if (!data) {
      // fallback empty payload
      return {
        statusCode: 200,
        headers: {'Content-Type':'application/json','Cache-Control':'no-store'},
        body: JSON.stringify({ name:'Bandi – vuoto', updated: new Date().toISOString(), measures: [] })
      };
    }
    return {
      statusCode: 200,
      headers: {'Content-Type':'application/json','Cache-Control':'no-store'},
      body: JSON.stringify(data)
    };
  } catch (e) {
    return { statusCode: 500, body: 'error: '+e.message };
  }
}
