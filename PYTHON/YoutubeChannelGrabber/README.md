# 🎬 YoutubeChannelGrabber

Deux outils CLI complémentaires :

1. **`grab_links.py`** — demande une chaîne YouTube (nom, `@handle` ou URL)
   et écrit tous les liens des vidéos dans `links/<chaine>.md`
   (un fichier `.md` par chaîne).
2. **`download_from_md.py`** — choisit un `.md`, télécharge une vidéo de la
   liste dans `downloads/`, puis retire sa ligne du `.md`.

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
# 1) Générer la liste des liens
python grab_links.py

# 2) Télécharger une vidéo (et la retirer du .md)
python download_from_md.py
```

## Organisation

```
YoutubeChannelGrabber/
├── grab_links.py
├── download_from_md.py
├── links/        # 1 fichier .md par chaîne (à télécharger)
└── downloads/    # vidéos téléchargées
```
