# 🎬 YoutubeChannelGrabber — Présentation du projet

> Un mini-projet Python en ligne de commande (CLI) pour **récupérer tous les
> liens des vidéos d'une chaîne YouTube**, puis **les télécharger un par un**
> en gardant la liste toujours à jour.

---

## 1. 🎯 Objectif

Le projet répond à 2 besoins, en 2 outils complémentaires :

| Étape | Outil | Ce que ça fait |
|-------|-------|----------------|
| **1** | `grab_links.py` | Tu donnes une chaîne YouTube → il écrit tous les liens des vidéos dans un fichier `.md` |
| **2** | `download_from_md.py` | Tu choisis un `.md` → il télécharge une vidéo **et retire sa ligne du fichier** |

➡️ Résultat : un fichier `.md` par chaîne, qui ne contient **que ce qu'il reste à télécharger**. Tout reste rangé et organisé.

---

## 2. 🗂️ Organisation des fichiers

```
YoutubeChannelGrabber/
├── grab_links.py          # Étape 1 : récupère les liens
├── download_from_md.py    # Étape 2 : télécharge + nettoie le .md
├── requirements.txt       # Dépendance : yt-dlp
├── README.md              # Doc rapide
├── PRESENTATION.md        # Ce document
│
├── links/                 # 📄 1 fichier .md par chaîne (à télécharger)
│   ├── mrbeast.md
│   └── joueur_du_grenier.md
│
└── downloads/             # 🎞️ les vidéos téléchargées
```

---

## 3. ⚙️ Installation

> Pré-requis : **Python 3** installé.

```bash
cd PYTHON/YoutubeChannelGrabber
pip install -r requirements.txt
```

Cela installe **`yt-dlp`** (la bibliothèque qui récupère et télécharge les vidéos YouTube).

---

## 4. 🚀 Utilisation — les commandes

### Étape 1 — Récupérer les liens d'une chaîne

```bash
python grab_links.py
```

Le script te pose 2 questions :

```
🔑 Nom / @handle / URL de la chaîne : mrbeast
📊 Nombre de vidéos max à lister (ex: 100) : 100
```

✅ Résultat : un fichier `links/mrbeast.md` est créé avec 100 liens.

**Formats acceptés pour la chaîne :**

| Tu peux taper… | Exemple |
|----------------|---------|
| Un simple nom | `mrbeast` |
| Un @handle | `@mrbeast` |
| L'URL complète | `https://www.youtube.com/@mrbeast` |

---

### Étape 2 — Télécharger une vidéo

```bash
python download_from_md.py
```

Déroulé :

```
📂 Fichiers disponibles :
  1. mrbeast.md
  2. joueur_du_grenier.md

👉 Numéro du fichier : 1

📋 100 vidéo(s) restante(s) dans mrbeast.md
  1. Ma première vidéo
  2. Deuxième vidéo
  ...

👉 Numéro à télécharger (Entrée = la 1ère) : 1

⏳ Téléchargement : Ma première vidéo
✅ Téléchargé : Ma première vidéo
📁 Dossier : downloads/
📝 Retiré de : mrbeast.md  (99 restante(s))
```

➡️ La vidéo va dans `downloads/`, **et sa ligne disparaît du `.md`**.
Tu peux relancer la commande autant de fois que tu veux : la liste se vide au fur et à mesure.

---

## 5. 📝 À quoi ressemble un fichier `.md`

`links/mrbeast.md` :

```markdown
# 🎬 Vidéos de mrbeast

> 100 vidéo(s) — coche/supprime au fur et à mesure des téléchargements.

- [ ] [Ma première vidéo](https://www.youtube.com/watch?v=abc123)
- [ ] [Deuxième vidéo](https://www.youtube.com/watch?v=def456)
- [ ] [Troisième vidéo](https://www.youtube.com/watch?v=ghi789)
```

Après téléchargement de la 1ère, la ligne est **supprimée** du fichier.

---

## 6. 🔧 Fonctionnement technique (résumé)

| Point | Détail |
|-------|--------|
| Récupération des liens | `yt-dlp` en mode `extract_flat` → **rapide**, ne télécharge rien, juste la liste |
| Un `.md` par chaîne | Nom de fichier « nettoyé » (slug) pour rester rangé |
| Format des lignes | Cases à cocher Markdown : `- [ ] [Titre](url)` |
| Sécurité | Si un téléchargement **échoue**, la ligne est **conservée** (rien n'est perdu) |
| Compteur | Le nombre de vidéos restantes s'affiche après chaque téléchargement |

---

## 7. ⚡ Récapitulatif des commandes

```bash
# Installation (une seule fois)
pip install -r requirements.txt

# Étape 1 : générer la liste des liens
python grab_links.py

# Étape 2 : télécharger une vidéo (à répéter autant de fois que voulu)
python download_from_md.py
```
