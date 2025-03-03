import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import pandas as pd

def extract_content(url):
    data = []
    seen_texts = set()  # Pour éviter les doublons
    
    try:
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
         
        soup = BeautifulSoup(response.text, 'html.parser')
        
    
        nom_site = soup.title.string.strip() if soup.title else "Nom du site non trouvé"
        
        
        heure_extraction = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        
        mots_cles = [
            'mission', 'vision', 'organigramme','organisation', 'mécanismes', 'Les programmes de santé publique',  # Présentation de l'entité
            'adresse', 'téléphone', 'email', 'contact','parcours patien', '' 
            'loi', 'décret', 'arrêté', 'document réglementaire', 
            'rapport d\'activité', 'rapport annuel', 
            'prestation', 'service', 'formulaire', 'demande administrative',
            'accessibilité', 'handicap', 'ergonomie', 'langue simple', 'politiques',
            'actualité', 'news', 'nouvelle', 'localisation','modalités d’accès', 'coûts', 'objectif'
        ]
        
        
        balises_analyser = ['div', 'p', 'section', 'article', 'li', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6','ul','li','ol','textarea','footer','main']
        
        
        for balise in balises_analyser:
            elements = soup.find_all(balise)
            
            for element in elements:
                
                texte = element.get_text(strip=True)
               
                
                for mot_cle in mots_cles:
                    if mot_cle.lower() in texte.lower():
                        
                        if texte not in seen_texts:
                            seen_texts.add(texte)
                            
                            
                            lien_associe = ""
                            if element.name == 'a' and element.get('href'):
                                lien_associe = urljoin(url, element.get('href'))
                            elif element.find_parent('a') and element.find_parent('a').get('href'):
                                lien_associe = urljoin(url, element.find_parent('a').get('href'))
                            
                            
                            data.append({
                                'Nom du site': nom_site,
                                'Heure': heure_extraction,
                                'URL': url,
                                'Mot-clé': mot_cle,
                                'Contenu texte': texte,
                                'Lien associé': lien_associe
                            })
        
        return data
    
    except Exception as e:
        print(f"Erreur lors de l'extraction: {str(e)}")
        return []


url = "https://www.gouv.ci/Main2.php"


print("Début de l'extraction...")
content_data = extract_content(url)


df = pd.DataFrame(content_data)


print("Données extraites :")
print(df)
df.to_excel('donnees.xlsx', index=False)

print("Extraction terminée. Les données sont stockées dans un DataFrame Pandas et téléchargé dans un fichier Excel.")