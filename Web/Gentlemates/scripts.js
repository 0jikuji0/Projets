// scripts.js - Widget Gentle Mates
const PROXY_ENDPOINT = "http://localhost:3000/api/matches"; // appelle le proxy

const statusEl = document.getElementById("status");
const content = document.getElementById("content");

function escapeHtml(str){
  return String(str)
    .replaceAll("&","&amp;")
    .replaceAll("<","&lt;")
    .replaceAll(">","&gt;");
}

function formatDate(isoString){
  if(!isoString) return "Date inconnue";
  try { return new Date(isoString).toLocaleString(); } 
  catch { return isoString; }
}

async function getNextMatch() {
  try {
    statusEl.textContent = "Chargement du prochain match…";
    const res = await fetch(`${PROXY_ENDPOINT}`);
    if (!res.ok) throw new Error(`Erreur serveur: ${res.status}`);
    const matches = await res.json();

    const nextMatch = matches.find(m =>
      Array.isArray(m.opponents) &&
      m.opponents.some(o => (o.opponent?.name || "").toLowerCase().includes("gentle mates"))
    );

    if (!nextMatch) {
      content.innerHTML = `<div style="text-align:center;color:#aaa">Aucun prochain match trouvé.</div>`;
      return;
    }

    renderMatch(nextMatch, true);

  } catch (err) {
    statusEl.textContent = "Erreur";
    content.innerHTML = `<div class="error">Impossible de récupérer le prochain match : ${escapeHtml(err.message)}</div>`;
    console.error(err);
  }
}

async function getPastMatches(limit = 5) {
  try {
    const res = await fetch(`${PROXY_ENDPOINT}?status=finished`);
    if (!res.ok) throw new Error(`Erreur serveur: ${res.status}`);
    const matches = await res.json();

    const gmMatches = matches.filter(m =>
      Array.isArray(m.opponents) &&
      m.opponents.some(o => (o.opponent?.name || "").toLowerCase().includes("gentle mates"))
    ).slice(0, limit);

    if (!gmMatches.length) {
      content.innerHTML += `<div style="text-align:center;color:#aaa;margin-top:10px">Aucun match passé trouvé.</div>`;
      return;
    }

    content.innerHTML += `<h3 style="margin-top:12px;">Derniers matchs</h3>`;
    gmMatches.forEach(match => renderMatch(match, false));

  } catch (err) {
    content.innerHTML += `<div class="error">Impossible de récupérer les derniers matchs : ${escapeHtml(err.message)}</div>`;
    console.error(err);
  }
}

function renderMatch(match, isNext) {
  const opponents = match.opponents || [];
  const team1 = opponents[0]?.opponent || { name: "TBD", image_url: null, score: 0 };
  const team2 = opponents[1]?.opponent || { name: "TBD", image_url: null, score: 0 };
  const date = formatDate(match.scheduled_at || match.begin_at);
  const league = match.league?.name || "Tournoi inconnu";
  const game = match.videogame?.name || "Jeu inconnu";
  const score1 = team1.score ?? match.results?.[0]?.score ?? 0;
  const score2 = team2.score ?? match.results?.[1]?.score ?? 0;

  const html = `
    <div class="match-card">
      ${isNext ? `<div style="font-weight:700;color:#fff;margin-bottom:4px;">Prochain match</div>` : ""}
      <div style="font-size:12px;color:#aaa;margin-bottom:4px;">${escapeHtml(league)} — ${escapeHtml(game)}</div>
      <div class="teams">
        <div><strong>${escapeHtml(team1.name)}</strong> (${score1})</div>
        <div class="vs">VS</div>
        <div>(${score2}) <strong>${escapeHtml(team2.name)}</strong></div>
      </div>
      <div class="meta">${date}</div>
    </div>
  `;
  content.innerHTML += html;
}

// Lancer les deux récupérations
getNextMatch().then(() => getPastMatches(5));
