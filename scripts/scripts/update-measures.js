const fetch = require("node-fetch");
const fs = require("fs");
const path = require("path");

// URL da cui prendere i bandi (sorgente ufficiale)
const BANDS_SOURCE_URL = "https://example.com/api/bandi"; // <-- qui metteremo il vero endpoint

// Percorso locale del dataset
const DATA_PATH = path.join(__dirname, "..", "public", "measures.json");

async function updateMeasures() {
  try {
    console.log("🔄 Aggiornamento dataset bandi in corso...");

    // Prende i dati dall'API
    const response = await fetch(BANDS_SOURCE_URL);
    const data = await response.json();

    // Salva i dati nel file locale
    fs.writeFileSync(DATA_PATH, JSON.stringify(data, null, 2));

    console.log("✅ Dataset aggiornato con successo!");
  } catch (error) {
    console.error("❌ Errore nell'aggiornamento del dataset:", error);
    process.exit(1);
  }
}

updateMeasures();
