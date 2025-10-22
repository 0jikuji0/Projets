import os
import subprocess
import sys

def install_dependencies():
    """Installe les dépendances nécessaires"""
    packages = ['yt-dlp', 'ffmpeg-python']
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"Installation de {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_dependencies()

import yt_dlp
import ffmpeg

def download_youtube_video(url, output_format='mp4'):
    """
    Télécharge une vidéo YouTube et la convertit au format demandé
    
    Formats supportés: mp4, mov, mkv
    CapCut supporte bien: mp4, mov
    """
    
    formats_caput = ['mp4', 'mov', 'mkv']
    
    if output_format.lower() not in formats_caput:
        print(f"Format non supporté. Utilisez: {', '.join(formats_caput)}")
        return False
    
    try:
        # Créer un dossier pour les téléchargements
        output_dir = "videos_telechargees"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Options pour yt-dlp
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
        }
        
        print("📥 Téléchargement de la vidéo...")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)
        
        # Si le format n'est pas mp4, convertir
        file_ext = os.path.splitext(video_path)[1][1:]
        
        if file_ext.lower() != output_format.lower():
            print(f"🔄 Conversion de {file_ext} à {output_format}...")
            output_video = os.path.splitext(video_path)[0] + f'.{output_format}'
            
            ffmpeg.input(video_path).output(output_video, vcodec='libx264', acodec='aac').run(quiet=False, overwrite_output=True)
            
            # Supprimer l'ancien fichier
            os.remove(video_path)
            video_path = output_video
            print(f"✅ Fichier converti: {output_video}")
        
        print(f"✅ Vidéo téléchargée avec succès!")
        print(f"📍 Chemin: {video_path}")
        print(f"📱 Compatible CapCut: OUI")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    print("=" * 50)
    print("   TÉLÉCHARGEUR YOUTUBE → CapCut Compatible")
    print("=" * 50)
    
    url = input("\n📌 Colle l'URL YouTube: ").strip()
    
    if not url:
        print("❌ URL vide!")
        return
    
    print("\nFormats disponibles (CapCut-compatible):")
    print("1. MP4 (recommandé)")
    print("2. MOV")
    print("3. MKV")
    
    choice = input("\nChoisis le format (1/2/3) [défaut: 1]: ").strip()
    
    format_map = {'1': 'mp4', '2': 'mov', '3': 'mkv'}
    output_format = format_map.get(choice, 'mp4')
    
    download_youtube_video(url, output_format)
    
    input("\n✅ Appuie sur Entrée pour terminer...")

if __name__ == "__main__":
    main()