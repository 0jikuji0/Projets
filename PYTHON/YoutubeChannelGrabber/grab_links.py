"""
🎬 PARTIE 1 — RÉCUPÉRATION DES LIENS D'UNE CHAÎNE YOUTUBE

On lance le script en CLI, il demande le nom (ou le @handle, ou l'URL)
d'une chaîne YouTube et écrit tous les liens des vidéos dans un fichier
Markdown dédié à cette chaîne, dans le dossier "links/".

Un fichier .md par chaîne -> tout reste rangé.
"""

import re
import sys
from pathlib import Path

import yt_dlp

# Dossier où sont rangés les fichiers .md (un par chaîne)
LINKS_FOLDER = Path(__file__).parent / "links"


def slugify(name):
    """Transforme un nom de chaîne en nom de fichier propre."""
    slug = name.strip().lstrip("@").lower()
    slug = re.sub(r"[^a-z0-9._-]+", "_", slug)
    return slug.strip("_") or "chaine"


def build_channel_url(user_input):
    """
    Construit l'URL de la page "vidéos" de la chaîne.

    Accepte : une URL complète, un @handle, ou un simple nom.
    Si ce n'est pas une URL, on tente le format @handle.
    """
    text = user_input.strip()
    if text.startswith("http://") or text.startswith("https://"):
        # On force l'onglet /videos si l'utilisateur a collé l'URL de la chaîne
        if "/videos" not in text and ("/@" in text or "/channel/" in text or "/c/" in text or "/user/" in text):
            return text.rstrip("/") + "/videos"
        return text
    handle = text.lstrip("@")
    return f"https://www.youtube.com/@{handle}/videos"


def fetch_video_links(channel_url, max_videos):
    """
    Récupère la liste des vidéos de la chaîne (sans rien télécharger).

    extract_flat -> rapide, on ne récupère que les métadonnées de la liste.
    """
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "playlistend": max_videos,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)

    entries = info.get("entries") or []
    videos = []
    for entry in entries:
        if not entry:
            continue
        video_id = entry.get("id")
        title = entry.get("title") or "Sans titre"
        url = entry.get("url") or (f"https://www.youtube.com/watch?v={video_id}" if video_id else None)
        if url:
            videos.append((title, url))
    return videos


def write_markdown(channel_name, videos):
    """Écrit (ou écrase) le fichier .md de la chaîne."""
    LINKS_FOLDER.mkdir(exist_ok=True)
    md_path = LINKS_FOLDER / f"{slugify(channel_name)}.md"

    lines = [
        f"# 🎬 Vidéos de {channel_name}",
        "",
        f"> {len(videos)} vidéo(s) — coche/supprime au fur et à mesure des téléchargements.",
        "",
    ]
    for title, url in videos:
        lines.append(f"- [ ] [{title}]({url})")
    lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path


def main():
    print("=" * 60)
    print("🎬 RÉCUPÉRATEUR DE LIENS — CHAÎNE YOUTUBE")
    print("=" * 60 + "\n")

    channel = input("🔑 Nom / @handle / URL de la chaîne : ").strip()
    if not channel:
        print("❌ Erreur : il faut entrer une chaîne.")
        sys.exit(1)

    try:
        max_videos = int(input("📊 Nombre de vidéos max à lister (ex: 100) : ").strip())
        if max_videos <= 0:
            print("❌ Erreur : le nombre doit être supérieur à 0.")
            sys.exit(1)
    except ValueError:
        print("❌ Erreur : entrez un nombre valide.")
        sys.exit(1)

    channel_url = build_channel_url(channel)
    print(f"\n⏳ Récupération depuis : {channel_url}\n")

    try:
        videos = fetch_video_links(channel_url, max_videos)
    except Exception as e:
        print(f"❌ Impossible de récupérer les vidéos : {e}")
        print("   Astuce : essaie avec l'URL complète de la chaîne (.../@nom/videos).")
        sys.exit(1)

    if not videos:
        print("❌ Aucune vidéo trouvée pour cette chaîne.")
        sys.exit(1)

    md_path = write_markdown(channel, videos)

    print("=" * 60)
    print(f"✅ {len(videos)} lien(s) enregistré(s)")
    print(f"📁 Fichier : {md_path}")
    print("=" * 60)
    print("\n➡️  Étape suivante : python download_from_md.py")


if __name__ == "__main__":
    main()
