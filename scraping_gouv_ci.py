import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

def extract_content(url):
   
    data = []
    
    try:
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
       
        soup = BeautifulSoup(response.text, 'html.parser')
        
       
        menus = soup.find_all(['nav', 'ul', 'li', 'a'])
        for menu in menus:
            if menu.get_text().strip():
                data.append({
                    'Type': 'Menu',
                    'Titre': menu.get_text().strip(),
                    'URL': urljoin(url, menu.get('href', '')) if menu.get('href') else '',
                    'Texte': '',
                    'Image_URL': ''
                })
        
        
        paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div'])
        for p in paragraphs:
            if p.get_text().strip():
                data.append({
                    'Type': 'Texte',
                    'Titre': '',
                    'URL': '',
                    'Texte': p.get_text().strip(),
                    'Image_URL': ''
                })
        
        
        images = soup.find_all('img')
        for img in images:
            src = img.get('src', '')
            if src:
                data.append({
                    'Type': 'Image',
                    'Titre': img.get('alt', ''),
                    'URL': '',
                    'Texte': '',
                    'Image_URL': urljoin(url, src)
                })
        
        return data
    
    except Exception as e:
        print(f"Erreur lors de l'extraction: {str(e)}")
        return []

def save_to_csv(data, filename):
   
    fieldnames = ['Type', 'Titre', 'URL', 'Texte', 'Image_URL']
    
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


url = "https://www.gouv.ci/Main2.php"


print("Début de l'extraction...")
content_data = extract_content(url)


output_file = 'contenu_gouv_ci.csv'
save_to_csv(content_data, output_file)

print(f"Extraction terminée. Les données ont été sauvegardées dans '{output_file}'")