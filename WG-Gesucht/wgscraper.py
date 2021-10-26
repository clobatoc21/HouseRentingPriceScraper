import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint


for i in range(10):
    url = 'https://www.wg-gesucht.de/es/wohnungen-in-Berlin.8.2.1.' + str(i) + '.html'

    # get data
    data = requests.get(url)

    # load data into bs4
    soup = BeautifulSoup(data.text, "html.parser")

    # locates every listed flat
    flat_data = soup.find_all("div", {"class": "col-sm-8 card_body"})
    for flat in flat_data:
        name = flat.h3["title"]
        price = flat.select_one(".col-xs-6, .col-xs-3").get_text(
            strip=True, separator=" "
        )
        size = flat.find("b", text=lambda t: t and "m²" in t)
        size = size.text if size else "-"
        print("{:<60} {:<10} {}".format(name[:59], price, size))  # añadir para que no pare: .encode("utf-8")

    # sleep to avoid being banned
    sleep(randint(2,10))