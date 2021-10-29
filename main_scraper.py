#!/usr/bin/env python
# coding: utf-8

# In[8]:


import wgScraper
import IdealistaScraper
import pandas as pd
import os

os.system("wgScraper.py")
os.system("IdealistaScraper.py")

combined_csv = []

wg = pd.read_csv("wg-gesucht.csv")
combined_csv.append(wg)

id = pd.read_csv("idealista.csv")
combined_csv.append(id)

scraping_result = pd.concat(combined_csv, axis=0, ignore_index=True)
df.to_csv("./scraping_result.csv", sep=',', encoding="utf-8", index=False)

os.remove("wg-gesucht.csv")
os.remove("idealista.csv")

print("El proceso de scraping ha finalizado")


# In[ ]:




