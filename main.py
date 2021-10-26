# -*- coding: utf-8 -*-
import builtwith
import whois
# from scraper import wgScraper

_url = 'https://www.wg-gesucht.de/'
output_file = "datasetwg.csv"

# Conocer la tecnologia del Sitio
print(builtwith.builtwith(_url))

# Propietario
# En este caso no se va a mostrar porque toda la información que devuelve es "null"
# print(whois.whois(_url))

# Scraping
# scraper = wgScraper(_url)
# scraper.scrape()
# scraper.data2csv(output_file)
