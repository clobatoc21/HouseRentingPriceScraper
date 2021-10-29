import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import pandas as pd

# Initialize variables
urllist =['https://www.wg-gesucht.de/wohnungen-in-Berlin.8.2.1.', 'https://www.wg-gesucht.de/wohnungen-in-Hamburg.55.2.1.', 
          'https://www.wg-gesucht.de/wohnungen-in-Munchen.90.2.1.', 'https://www.wg-gesucht.de/wohnungen-in-Koeln.73.2.1.', 
          'https://www.wg-gesucht.de/wohnungen-in-Frankfurt-am-Main.41.2.1.']
namecitylist = ['Berlin', 'Hamburgo', 'Munich', 'Colonia', 'Frankfurt']
citylist = []
namelist = []
pricelist = []
sizelist = []
df = pd.DataFrame()
df['Descripcion'] = None
df['Precio'] = None
df['Superficie'] = None
counter = 0

# Script
for url_i in urllist:
    for i in range(2):
        url = url_i + str(i) + '.html'

        # get data
        data = requests.get(url)

        # load data into bs4
        soup = BeautifulSoup(data.text, "html.parser")

        # locates every listed flat
        flat_data = soup.find_all("div", {"class": "col-sm-8 card_body"})
        for flat in flat_data:
            size = flat.find("b", text=lambda t: t and "m²" in t)
            size = size.text if size else '0'
            for word in size.split():
                        if word.isdigit():
                            sizelist.append(int(word))
            # to avoid ads
            if size == '0':
                city = 'null'
                citylist.append(city)
                name = 'null'
                namelist.append(name)
                price = 0
                pricelist.append(price)
            else:
                city = namecitylist[counter]
                citylist.append(city)
                name = flat.h3["title"]
                namelist.append(name)
                price = flat.select_one(".col-xs-6, .col-xs-3").get_text(strip=True, separator=" ")
                for word in price.split():
                    if word.isdigit():
                        pricelist.append(int(word))
        # sleep to avoid being banned
        sleep(randint(2,10))
    # add to counter
    counter = counter + 1

# create dataframe
df = pd.DataFrame(data={"Ciudad": citylist, "Descripcion": namelist, "Precio": pricelist, "Superficie": sizelist})
# clean null values
boolean_series = df.Ciudad.isin(namecitylist)
df = df[boolean_series]
# export to csv
df.to_csv("./wg-gesucht.csv", sep=',',index=False)
print("El scraping de WG-gesucht ha finalizado")
