import express from "express";
import fetch from "node-fetch";
import cors from "cors";

const app = express();
const PORT = 3000;

app.use(cors());

// 🔑 Remplace ici par ta clé API PandaScore
const API_KEY = "mon api key panda score";

// Route proxy pour PandaScore
app.get("/api/matches", async (req, res) => {
  try {
    const status = req.query.status; // "finished" ou undefined
    let url = "https://api.pandascore.co/matches";
    if (status) url += `?filter[status]=${status}`;

    const response = await fetch(url, {
      headers: {
        "Accept": "application/json",
        "Authorization": `Bearer ${API_KEY}`
      }
    });

    const data = await response.json();
    res.json(data);

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Erreur serveur" });
  }
});

app.listen(PORT, () => console.log(`✅ Serveur lancé sur http://localhost:${PORT}`));
