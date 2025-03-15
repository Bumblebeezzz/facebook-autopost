# Remplacez les fonctions generate_content_with_chatgpt et generate_image_with_dalle par:

def get_content_from_repository():
    """Obtient du contenu depuis les fichiers du dépôt"""
    try:
        # Trouver tous les fichiers de contenu
        content_files = [f for f in os.listdir('content') if f.endswith('.txt')]
        
        if not content_files:
            logger.error("Aucun fichier de contenu trouvé dans le dossier 'content'")
            return "L'arithmétique sacrée révèle les mystères de l'univers.", None
        
        # Sélectionner un fichier aléatoire ou en séquence
        # (vous pouvez implémenter une logique pour suivre quel fichier a été utilisé en dernier)
        content_file = random.choice(content_files)
        
        # Lire le contenu du fichier
        with open(f'content/{content_file}', 'r', encoding='utf-8') as file:
            content = file.read().strip()
        
        logger.info(f"Contenu lu depuis le fichier: {content_file}")
        
        # Vérifier s'il y a une image correspondante
        image_name = content_file.replace('.txt', '.jpg')
        image_path = None
        if os.path.exists(f'images/{image_name}'):
            image_path = f'images/{image_name}'
            logger.info(f"Image trouvée: {image_path}")
        
        return content, image_path
    
    except Exception as e:
        logger.error(f"Erreur lors de la lecture du contenu: {str(e)}")
        return "L'arithmétique sacrée révèle les mystères de l'univers.", None

# Puis modifiez la fonction main() pour utiliser cette nouvelle fonction:
def main():
    try:
        logger.info(f"Début du processus de publication automatisée: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 1. Obtenir le contenu et l'image
        content, image_path = get_content_from_repository()
        
        # 2. Publier sur Facebook
        success, result = post_to_facebook(content, image_path)
        
        if success:
            logger.info("Processus de publication automatisée terminé avec succès")
            # Optionnel: marquer ce fichier comme "utilisé" ou le déplacer
        else:
            logger.error(f"Échec du processus de publication automatisée: {result}")
        
        return success
    
    except Exception as e:
        logger.error(f"Erreur inattendue dans le processus principal: {str(e)}")
        return False
