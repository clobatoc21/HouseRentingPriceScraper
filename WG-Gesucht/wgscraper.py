import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import pandas as pd

# create empty lists and dataframe
namelist = []
pricelist = []
sizelist = []
df = pd.DataFrame()
df['Descripcion'] = None
df['Precio'] = None
df['Superficie'] = None

# Script
for i in range(10):
    url = 'https://www.wg-gesucht.de/es/wohnungen-in-Berlin.8.2.1.' + str(i) + '.html'
    
    # get data
    data = requests.get(url)
    
    # load data into bs4
    soup = BeautifulSoup(data.text, "html.parser")
    
    # locates every listed flat
    flat_data = soup.find_all("div", {"class": "col-sm-8 card_body"})
    
    # extract description, price and size
    for flat in flat_data:
        
        # extract description
        name = flat.h3["title"]
        namelist.append(name)
        
        # extract price
        price = flat.select_one(".col-xs-6, .col-xs-3").get_text(strip=True, separator=" ")
        for word in price.split():
            if word.isdigit():
                pricelist.append(int(word))
        
        # extract size
        size = flat.find("b", text=lambda t: t and "m²" in t)
        size = size.text if size else "0"
        for word in size.split():
                    if word.isdigit():
                        sizelist.append(int(word))
                        
    # sleep to avoid being banned
    sleep(randint(2,10))

# fill dataframe and export to csv
df = pd.DataFrame(data={"Descripcion": namelist, "Precio": pricelist, "Superficie": sizelist})
df.to_csv("./wg-gesucht.csv", sep=',',index=False)
print("finalizado")