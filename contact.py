import requests
from bs4 import BeautifulSoup
import csv
import re

def check_information_presence(soup, keywords):
    
    status = {}
    for keyword in keywords:
        element = soup.find(string=lambda text: text and keyword.lower() in text.lower())
        if element:
        
            status[keyword] = element.parent.get_text(strip=True) if element.parent else 'ok'
        else:
            status[keyword] = 'not ok'
    return status


def extract_contacts(soup):
   
    contacts = {
        "adresses": [],
        "emails": [],
        "telephones": []
    }

    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    emails = email_pattern.findall(soup.get_text())
    if emails:
        contacts["emails"] = emails

    phone_pattern = re.compile(r'(?:\+\d{1,3})?\s?\(?\d{2,4}\)?[\s.-]?\d{2,4}[\s.-]?\d{2,4}[\s.-]?\d{0,4}')
    phones = phone_pattern.findall(soup.get_text())
    if phones:
        contacts["telephones"] = phones

    address_tags = soup.find_all(string=lambda text: text and "Adresse" in text)
    if address_tags:
        contacts["adresses"] = [address.strip() for address in address_tags]

    return contacts


def save_to_csv(filename, data, headers):
  
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


def format_contact_info(contact_info):
   
    return {
        "adresses": ", ".join(contact_info["adresses"]),
        "emails": ", ".join(contact_info["emails"]),
        "telephones": ", ".join(contact_info["telephones"])
    }


url = "https://www.gouv.ci/Main2.php"

response = requests.get(url)
response.raise_for_status() 

soup = BeautifulSoup(response.content, 'html.parser')

keywords = ["mission", "vision", "organigramme"]
status_info = check_information_presence(soup, keywords)

status_data = [status_info]
save_to_csv("status_information.csv", status_data, headers=keywords)

contact_info = extract_contacts(soup)
formatted_contact_info = format_contact_info(contact_info)

print("Extraction terminée. Les fichiers CSV ont été générés.")
