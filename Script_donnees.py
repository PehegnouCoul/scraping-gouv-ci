import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import pandas as pd
import re

def get_soup(url):
    """Effectue une requête et retourne un objet BeautifulSoup."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de la page {url}: {e}")
        return None

def get_all_links(url):
    """Récupère toutes les URLs présentes sur un site web et les stocke dans une variable."""
    urls = set()  
    soup = get_soup(url)
    
    if soup is None:
        return urls  

    for link in soup.find_all('a', href=True):  
        full_link = urljoin(url, link['href'])  
        if full_link.startswith(url):  
            urls.add(full_link)

    urls.add(url)  
    return urls

def extract_content(url):
    """Extrait les informations pertinentes du site web donné."""
    data = []
    seen_texts = set()  
    soup = get_soup(url)

    if soup is None:
        return []

    nom_site = soup.title.string.strip() if soup.title else "Nom du site non trouvé"
    heure_extraction = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    mots_cles = {
        'mission', 'vision', 'organigramme', 'organisation', 'mécanismes', 'programmes de santé publique',
        'adresse', 'téléphone', 'email', 'contact', 'parcours patient',
        'loi', 'décret', 'arrêté', 'document réglementaire',
        'rapport d\'activité', 'rapport annuel',
        'prestation', 'service', 'formulaire', 'demande administrative',
        'accessibilité', 'handicap', 'ergonomie', 'langue simple', 'politiques',
        'actualité', 'news', 'nouvelle', 'localisation', 'modalités d’accès', 'coûts', 'objectif'
    }

    balises_analyser = ['div', 'p', 'section', 'article', 'li', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'textarea', 'footer', 'main']

    for balise in balises_analyser:
        elements = soup.find_all(balise)
        
        for element in elements:
            texte = element.get_text(strip=True)
        
            for mot_cle in mots_cles:
                if re.search(rf'\b{re.escape(mot_cle)}\b', texte, re.IGNORECASE):
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

def save_to_excel(data, filename='donnees.xlsx'):
    """Sauvegarde les données extraites dans un fichier Excel."""
    if data:
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Extraction terminée. Les données ont été enregistrées dans {filename}.")
    else:
        print("Aucune donnée extraite.")

# URL de départ
base_url = "https://www.gouv.ci/Main2.php"

print("Récupération des URLs...")
urls = get_all_links(base_url)

print("Début de l'extraction...")
all_content_data = []
for url in urls:
    print(f"Extraction des données depuis : {url}")
    all_content_data.extend(extract_content(url))

save_to_excel(all_content_data)
