import os
from yt_dlp import YoutubeDL

def telecharger_video(url, dossier_destination="videos"):
    """
    Télécharge une vidéo YouTube
    
    Args:
        url: L'URL de la vidéo YouTube
        dossier_destination: Dossier où sauvegarder la vidéo
    """
    
    # Créer le dossier s'il n'existe pas
    if not os.path.exists(dossier_destination):
        os.makedirs(dossier_destination)
    
    # Configuration de yt-dlp
    options = {
        'format': 'best',  # Meilleure qualité disponible
        'outtmpl': os.path.join(dossier_destination, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
    }
    
    try:
        print(f"Téléchargement de: {url}")
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            nom_fichier = ydl.prepare_filename(info)
            print(f"✓ Vidéo téléchargée avec succès: {nom_fichier}")
    
    except Exception as e:
        print(f"✗ Erreur lors du téléchargement: {e}")

def main():
    """Menu principal"""
    print("=" * 50)
    print("   Téléchargeur de vidéos YouTube")
    print("=" * 50)
    
    while True:
        url = input("\nEntrez l'URL YouTube (ou 'quitter' pour arrêter): ").strip()
        
        if url.lower() == 'quitter':
            print("Au revoir!")
            break
        
        if not url:
            print("Veuillez entrer une URL valide.")
            continue
        
        # Demander le dossier de destination (optionnel)
        dossier = input("Dossier de destination (Entrée pour 'videos'): ").strip()
        if not dossier:
            dossier = "videos"
        
        telecharger_video(url, dossier)
        print()

if __name__ == "__main__":
    main()