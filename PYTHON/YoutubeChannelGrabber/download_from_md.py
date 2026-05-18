"""
⬇️  PARTIE 2 — TÉLÉCHARGEMENT DEPUIS UN FICHIER .md

On choisit un fichier .md (une chaîne), on télécharge UNE vidéo de la
liste, puis la ligne correspondante est retirée du .md.

-> Le .md reste à jour : il ne contient que ce qu'il reste à télécharger.
"""

import re
import sys
from pathlib import Path

import yt_dlp

LINKS_FOLDER = Path(__file__).parent / "links"
DOWNLOADS_FOLDER = Path(__file__).parent / "downloads"

# Reconnaît une ligne du type :  - [ ] [Titre](https://...)
LINE_RE = re.compile(r"^- \[[ x]\] \[(?P<title>.+?)\]\((?P<url>https?://[^\s)]+)\)\s*$")


def list_md_files():
    """Liste les fichiers .md disponibles dans links/."""
    if not LINKS_FOLDER.exists():
        return []
    return sorted(LINKS_FOLDER.glob("*.md"))


def choose_md_file():
    files = list_md_files()
    if not files:
        print("❌ Aucun fichier .md dans 'links/'. Lance d'abord grab_links.py.")
        sys.exit(1)

    print("📂 Fichiers disponibles :\n")
    for i, f in enumerate(files, 1):
        print(f"  {i}. {f.name}")

    try:
        choice = int(input("\n👉 Numéro du fichier : ").strip())
        return files[choice - 1]
    except (ValueError, IndexError):
        print("❌ Choix invalide.")
        sys.exit(1)


def parse_videos(md_path):
    """
    Lit le .md et renvoie la liste des (index_ligne, titre, url)
    pour chaque vidéo encore présente.
    """
    lines = md_path.read_text(encoding="utf-8").splitlines()
    videos = []
    for idx, line in enumerate(lines):
        m = LINE_RE.match(line)
        if m:
            videos.append((idx, m.group("title"), m.group("url")))
    return lines, videos


def download_video(url, output_folder):
    """Télécharge une vidéo avec yt-dlp."""
    output_folder.mkdir(exist_ok=True)
    ydl_opts = {
        "format": "best",
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        "quiet": False,
        "no_warnings": False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def remove_line(md_path, lines, line_index):
    """Retire la ligne téléchargée du .md et réécrit le fichier."""
    del lines[line_index]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    print("=" * 60)
    print("⬇️  TÉLÉCHARGEUR DEPUIS .md")
    print("=" * 60 + "\n")

    md_path = choose_md_file()
    lines, videos = parse_videos(md_path)

    if not videos:
        print(f"\n✅ '{md_path.name}' est vide : tout est déjà téléchargé !")
        return

    print(f"\n📋 {len(videos)} vidéo(s) restante(s) dans {md_path.name}\n")
    for i, (_, title, _) in enumerate(videos[:10], 1):
        print(f"  {i}. {title}")
    if len(videos) > 10:
        print(f"  ... (+{len(videos) - 10} autres)")

    raw = input("\n👉 Numéro à télécharger (Entrée = la 1ère) : ").strip()
    try:
        pick = 1 if raw == "" else int(raw)
        line_index, title, url = videos[pick - 1]
    except (ValueError, IndexError):
        print("❌ Choix invalide.")
        sys.exit(1)

    print(f"\n⏳ Téléchargement : {title}\n")
    try:
        download_video(url, DOWNLOADS_FOLDER)
    except Exception as e:
        print(f"\n❌ Échec du téléchargement : {e}")
        print("   La ligne est conservée dans le .md.")
        sys.exit(1)

    remove_line(md_path, lines, line_index)

    _, restantes = parse_videos(md_path)
    print("\n" + "=" * 60)
    print(f"✅ Téléchargé : {title}")
    print(f"📁 Dossier : {DOWNLOADS_FOLDER}")
    print(f"📝 Retiré de : {md_path.name}  ({len(restantes)} restante(s))")
    print("=" * 60)


if __name__ == "__main__":
    main()
