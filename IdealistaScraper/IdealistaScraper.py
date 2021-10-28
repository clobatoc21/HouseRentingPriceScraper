#!/usr/bin/env python
# coding: utf-8

# In[80]:


# Import libraries

import requests
import time
from bs4 import BeautifulSoup
import re
import pandas as pd

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

namelist = []
pricelist = []
sizelist = []
floorlist = []

# Script

for i in range(10):
    
    # Scrape the web and obtain IDs
    
    url = "https://www.idealista.com/alquiler-viviendas/madrid-madrid/"
    #url = "https://www.idealista.com/alquiler-viviendas/madrid-madrid/pagina-" + str(i) + ".htm"
        
    for term in ["web scraping", "web crawling", "scrape this site"]:
            t0 = time.time() # Obtenemos momento de inicio
            
            data = requests.get(url, headers=headers)
            
            response_delay = time.time() - t0 # Estimamos el tiempo de respuesta (s)

            time.sleep(10 * response_delay) # Espera basada en el tiempo de respuesta (10x)

    soup = BeautifulSoup(data.text, 'html.parser')

    id = soup.find('body', attrs={'class':'', 'id':''})

    ids = re.findall('"adId":"([0-9]{,8})",', 
                      id.find('script').contents[0], re.DOTALL) # Obtención de los IDs de los anuncios
    

    # Scrape individual advertisements
    
    for id in ids:
        time.sleep(10 * response_delay) # Espera basada en el tiempo de respuesta (10x)
    
        url_id = 'https://www.idealista.com/inmueble/' + id + '/'
    
        entry = requests.get(url_id, headers=headers)

        soup_id = BeautifulSoup(entry.text, 'html.parser')

        name = soup_id.find('head').find('title').contents
        namelist.append(name)
    
        # prop_type = soup.find('strong', attrs={'class':'typology'}).contents
    
        price = soup_id.find('strong', attrs={'class':'price'})
        if price != None:
            price = price.contents
        
        pricelist.append(price)
    
        size_floor = []
        size_floor_obj = soup_id.find('p', attrs={'class':'info-data txt-big'}).find('span').next_siblings

        for el in size_floor_obj:
            if el.find('span') != -1:
                element = el.find('span').contents
                size_floor.append(element)
    
        size = size_floor[0]
        # floor = size_floor[1]
    
        sizelist.append(size)
        # floorlist.append(floor)


# Fill dataframe and export to csv

df = pd.DataFrame(data={"Descripcion": namelist, "Precio": pricelist, "Superficie": sizelist})

df.to_csv("./idealista.csv", sep=',',index=False)

print("El scraping de Idealista ha finalizado")


# In[ ]:





# In[ ]:




