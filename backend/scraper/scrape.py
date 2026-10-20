from bs4 import BeautifulSoup
import requests
from urls import WEBSITES



def scrape_text(url):
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
     
    try:
        res=requests.get(url,headers=headers)
        res.raise_for_status()
        extract=BeautifulSoup(res.text,"html.parser")
        return extract.get_text(separator=" ",strip=True)
    
    except Exception as e:
        return str(e)
    


for name, url in WEBSITES.items():

    text = scrape_text(url)

    with open("data/raw/raw.txt", "a", encoding="utf-8") as file:

        
        file.write(f"Website: {name}\n")
        file.write(f"URL: {url}\n")
        file.write(text)
        file.write("\n\n")
    
print("Data Saved")