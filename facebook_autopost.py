import os
import random
import requests
import logging
import time
from datetime import datetime
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.page import Page
from openai import OpenAI
from PIL import Image
import io

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Chargement des variables d'environnement
load_dotenv()

# Configuration des API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
GRAPH_API_VERSION = "v18.0"  # Vérifier la version actuelle de l'API

# Répertoire des images de secours (facultatif)
IMAGE_DIR = "images/"

# Initialisation des API
client = OpenAI(api_key=OPENAI_API_KEY)
FacebookAdsApi.init(access_token=FB_ACCESS_TOKEN, api_version=GRAPH_API_VERSION)

# Création du répertoire d'images s'il n'existe pas
os.makedirs(IMAGE_DIR, exist_ok=True)

# Thèmes pour les publications sur l'arithmétique sacrée
THEMES = [
    "La signification du nombre 3-6-9 et son importance dans l'univers",
    "Les séquences de Fibonacci et leur relation avec le nombre d'or",
    "Les cycles numériques et leur manifestation dans la nature",
    "La géométrie sacrée et ses applications pratiques",
    "Les nombres premiers et leur rôle dans l'arithmétique sacrée",
    "Les fréquences vibratoires des nombres et leur impact sur notre conscience",
    "Le nombre Pi et sa signification cosmique",
    "Le code vortex mathématique et les structures toroïdales",
    "Les structures fractales et l'auto-similarité dans l'univers",
    "La relation entre les nombres et les dimensions supérieures",
    "Le tétraèdre et son importance dans la géométrie sacrée",
    "La suite de Fibonacci et les spirales dorées dans la nature",
    "Le nombre 432 Hz et son harmonie avec l'univers",
    "La matrice 3x3 et les carrés magiques",
    "Les proportions sacrées dans l'architecture ancienne"
]

def generate_content_with_chatgpt(theme=None):
    """Génère du contenu original avec ChatGPT sur l'arithmétique sacrée"""
    if not theme:
        theme = random.choice(THEMES)
    
    try:
        logger.info(f"Génération de contenu sur le thème: {theme}")
        
        prompt = f"""
        Crée un post Facebook captivant et profond (maximum 3 paragraphes) sur l'arithmétique sacrée, 
        en te concentrant sur le thème suivant: {theme}.
        
        Le post doit être:
        1. Inspirant et informatif
        2. Adapté à un public intéressé par la numérologie et la géométrie sacrée
        3. Utilisant un ton mystique mais basé sur des principes mathématiques authentiques
        4. Incluant 2-3 hashtags pertinents à la fin
        5. Se terminant par une question inspirante ou une réflexion pour encourager l'engagement
        
        N'utilise pas plus de 400 mots.
        """
        
        response = client.chat.completions.create(
            model="gpt-4",  # ou un autre modèle disponible
            messages=[
                {"role": "system", "content": "Tu es un expert en arithmétique sacrée, numérologie et mathématiques ésotériques qui sait créer du contenu captivant pour les réseaux sociaux."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7
        )
        
        content = response.choices[0].message.content.strip()
        logger.info("Contenu généré avec succès")
        return content, theme
    
    except Exception as e:
        logger.error(f"Erreur lors de la génération de contenu: {str(e)}")
        # Contenu de secours en cas d'erreur
        return f"L'arithmétique sacrée révèle les mystères vibratoires de l'univers. Aujourd'hui, explorons {theme}. #ArithmétiqueSacrée #NombresEtVibrations", theme

def generate_image_with_dalle(theme):
    """Génère une image pertinente avec DALL-E basée sur le thème"""
    try:
        logger.info(f"Génération d'image pour le thème: {theme}")
        
        prompt = f"Une belle image conceptuelle représentant {theme}, dans le style de la géométrie sacrée, art numérique, couleurs vibrantes, sans texte"
        
        response = client.images.generate(
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard"
        )
        
        image_url = response.data[0].url
        
        # Télécharger l'image
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            image_filename = f"dalle_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            image_path = os.path.join(IMAGE_DIR, image_filename)
            
            with open(image_path, "wb") as img_file:
                img_file.write(image_response.content)
            
            logger.info(f"Image générée et sauvegardée: {image_path}")
            return image_path
        else:
            logger.error(f"Erreur lors du téléchargement de l'image: {image_response.status_code}")
            return None
    
    except Exception as e:
        logger.error(f"Erreur lors de la génération d'image: {str(e)}")
        return None

def post_to_facebook(content, image_path=None):
    """Publie le contenu et l'image sur Facebook"""
    try:
        logger.info("Tentative de publication sur Facebook")
        page = Page(FB_PAGE_ID)
        
        if image_path:
            # Publication avec image
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
            
            response = page.create_photo(
                params={
                    'message': content,
                },
                files={
                    'source': image_data,
                }
            )
        else:
            # Publication sans image
            response = page.create_feed(
                params={
                    'message': content,
                }
            )
        
        post_id = response.get('id', 'unknown')
        logger.info(f"Publication réussie! ID: {post_id}")
        return True, post_id
    
    except Exception as e:
        logger.error(f"Erreur lors de la publication sur Facebook: {str(e)}")
        return False, str(e)

def main():
    """Fonction principale qui orchestre le processus de publication"""
    try:
        logger.info(f"Début du processus de publication automatisée: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 1. Sélectionner un thème aléatoire
        theme = random.choice(THEMES)
        
        # 2. Générer du contenu avec ChatGPT
        content, theme = generate_content_with_chatgpt(theme)
        
        # 3. Générer une image avec DALL-E
        image_path = generate_image_with_dalle(theme)
        
        # 4. Publier sur Facebook
        success, result = post_to_facebook(content, image_path)
        
        if success:
            logger.info("Processus de publication automatisée terminé avec succès")
        else:
            logger.error(f"Échec du processus de publication automatisée: {result}")
        
        return success
    
    except Exception as e:
        logger.error(f"Erreur inattendue dans le processus principal: {str(e)}")
        return False

if __name__ == "__main__":
    # Ajouter un délai aléatoire pour éviter des publications à heure fixe (facultatif)
    random_delay = random.randint(0, 60)  # 0-1 minute de délai aléatoire
    logger.info(f"Délai aléatoire de {random_delay} secondes avant publication")
    time.sleep(random_delay)
    
    main()
