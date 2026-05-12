#!/usr/bin/env python3
"""Télécharge une vidéo ou un carrousel d'images TikTok + sa description."""

import sys
import re
import os
import json
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("yt-dlp n'est pas installé. Lance : pip3 install -r requirements.txt")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("requests n'est pas installé. Lance : pip3 install -r requirements.txt")
    sys.exit(1)


DOWNLOAD_DIR = Path(__file__).parent / "downloads"


def sanitize(name: str) -> str:
    name = re.sub(r"[^\w\-_. ]", "_", name)
    return name[:80].strip() or "tiktok"


def normalize_url(url: str) -> str:
    # Les URL TikTok /photo/ (carrousels) ne sont pas reconnues par yt-dlp,
    # mais TikTok accepte /video/ comme alias pour le même post.
    return re.sub(r"/photo/(\d+)", r"/video/\1", url)


def extract_info(url: str) -> dict:
    opts = {"quiet": True, "no_warnings": True, "skip_download": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)


def write_description(folder: Path, info: dict) -> None:
    desc = info.get("description") or info.get("title") or ""
    uploader = info.get("uploader") or info.get("creator") or ""
    url = info.get("webpage_url") or ""
    content = f"URL : {url}\nAuteur : {uploader}\n\nDescription :\n{desc}\n"
    (folder / "description.txt").write_text(content, encoding="utf-8")


TIKTOK_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
}


def scrape_tiktok_post(url: str) -> dict:
    """Récupère le JSON intégré à la page TikTok pour extraire les images d'un slideshow."""
    r = requests.get(url, headers=TIKTOK_HEADERS, timeout=30)
    r.raise_for_status()
    m = re.search(
        r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>',
        r.text,
        re.DOTALL,
    )
    if not m:
        return {}
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError:
        return {}
    return (
        data.get("__DEFAULT_SCOPE__", {})
        .get("webapp.video-detail", {})
        .get("itemInfo", {})
        .get("itemStruct", {})
    )


def slideshow_images_from_html(url: str) -> list:
    item = scrape_tiktok_post(url)
    image_post = item.get("imagePost") or {}
    images = image_post.get("images") or []
    urls = []
    for img in images:
        candidates = img.get("imageURL", {}).get("urlList") or []
        if candidates:
            urls.append(candidates[0])
    return urls


def download_images(folder: Path, info: dict, url: str) -> int:
    image_urls = slideshow_images_from_html(url)

    # Fallback : si le scrape échoue, on prend les thumbnails de yt-dlp
    if not image_urls and info.get("thumbnails"):
        seen = set()
        for t in info["thumbnails"]:
            u = t.get("url")
            if u and u not in seen:
                seen.add(u)
                image_urls.append(u)

    for i, img_url in enumerate(image_urls, 1):
        try:
            r = requests.get(img_url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            ext = ".jpg"
            if "png" in r.headers.get("Content-Type", "").lower():
                ext = ".png"
            elif "webp" in r.headers.get("Content-Type", "").lower():
                ext = ".webp"
            (folder / f"image_{i:02d}{ext}").write_bytes(r.content)
            print(f"  ✓ image {i}/{len(image_urls)}")
        except Exception as e:
            print(f"  ✗ image {i} : {e}")
    return len(image_urls)


def download_video(folder: Path, url: str) -> None:
    opts = {
        "outtmpl": str(folder / "video.%(ext)s"),
        "format": "best",
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])


def is_slideshow(info: dict, url: str) -> bool:
    # yt-dlp renvoie un audio-only (vcodec=none) pour les slideshows TikTok
    if info.get("vcodec") == "none":
        return True
    if "/photo/" in url:
        return True
    if info.get("_type") == "playlist" and info.get("entries"):
        first = info["entries"][0] if info["entries"] else {}
        if first.get("ext") in ("jpg", "jpeg", "png", "webp"):
            return True
    return False


def download_one(url: str) -> None:
    url = normalize_url(url)
    print(f"  → Analyse de {url}")
    info = extract_info(url)

    title = sanitize(info.get("title") or info.get("id") or "tiktok")
    folder = DOWNLOAD_DIR / f"{info.get('id', 'tiktok')}_{title}"
    folder.mkdir(parents=True, exist_ok=True)

    write_description(folder, info)
    print(f"  → Description sauvegardée dans {folder}/description.txt")

    if is_slideshow(info, url):
        print("  → Carrousel d'images détecté")
        n = download_images(folder, info, url)
        print(f"  → {n} image(s) téléchargée(s) dans {folder}")
    else:
        print("  → Vidéo détectée")
        download_video(folder, info.get("webpage_url") or url)
        print(f"  → Vidéo téléchargée dans {folder}")


def read_urls_from_file(path: Path) -> list:
    urls = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            urls.append(line)
    return urls


def process_urls(urls: list) -> None:
    total = len(urls)
    if total == 0:
        print("Aucune URL à traiter.")
        return

    print(f"→ {total} URL(s) à télécharger\n")
    successes, failures = 0, []

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{total}] {url}")
        try:
            download_one(url)
            successes += 1
            print(f"  ✓ Terminé ({i}/{total})\n")
        except yt_dlp.utils.DownloadError as e:
            failures.append((url, str(e)))
            print(f"  ✗ Erreur de téléchargement : {e}\n")
        except Exception as e:
            failures.append((url, str(e)))
            print(f"  ✗ Erreur : {e}\n")

    print("=" * 50)
    print(f"Résumé : {successes}/{total} réussi(s), {len(failures)} échec(s)")
    if failures:
        print("\nÉchecs :")
        for url, err in failures:
            print(f"  - {url} : {err}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python3 tiktok_download.py <url_tiktok | fichier.txt>")
        sys.exit(1)

    arg = sys.argv[1]
    path = Path(arg)
    if path.is_file():
        urls = read_urls_from_file(path)
        print(f"→ Lecture de {path} : {len(urls)} URL(s) trouvée(s)")
    else:
        urls = [arg]

    process_urls(urls)
