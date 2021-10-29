#!/usr/bin/env python
# coding: utf-8


# Import libraries

import requests
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
from random import randint

# Modify headers

headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
*/*;q=0.8",
"Accept-Encoding": "gzip, deflate, sdch, br",
"Accept-Language": "en-US,en;q=0.8",
"Cache-Control": "no-cache",
"dnt": "1",
"Pragma": "no-cache",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}

# Create empty lists

IDlist = []
namelist = []
pricelist = []
sizelist = []
citylist = []

# Script

for city in ["madrid", "barcelona", "valencia", "sevilla", "zaragoza"]:
    
    # Scrape the web and obtain IDs
    
    url = "https://www.idealista.com/alquiler-viviendas/" + city + "-" + city + "/"
        
    for term in ["web scraping", "web crawling", "scrape this site"]:
            
            data = requests.get(url, headers=headers)

            time.sleep(randint(5,20))

    soup = BeautifulSoup(data.text, 'html.parser')

    id = soup.find('body', attrs={'class':'', 'id':''})

    ids = re.findall('"adId":"([0-9]{,8})",', 
                      id.find('script').contents[0], re.DOTALL) # Obtención de los IDs de los anuncios
    
    for id in ids:
        IDlist.append(id)
        citylist.append(city.title())
        title = soup.find('a', attrs={'aria-level':'2', "class":"item-link", "href":"/inmueble/" + id + "/"})["title"]
        namelist.append(title)
    
    price = soup.find_all('span', attrs={'class':'item-price h2-simulated'})
    
    for els in price:
        pricelist.append(els.contents[0])
        
    details = soup.find_all('div', attrs={'class':'price-row'})

    for els in details:
        size = list(els.next_siblings)[3].contents[0]
        sizelist.append(size)

# Fill dataframe and export to csv

df = pd.DataFrame(data={"Ciudad": citylist, "Descripcion": namelist, "Precio": pricelist, "Superficie": sizelist})

df.to_csv("./idealista.csv", sep=',', encoding="utf-8", index=False)

print("El scraping de Idealista ha finalizado")

