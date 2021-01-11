from bs4 import BeautifulSoup
import requests
import csv
from Classes import Webshop
from datetime import datetime

Sourceurl = "https://www.dagvandewebshop.be/belgische-webshops?category=All"
webshoplist = []

# WEBSCRAPING
for x in range(5000):
    page_url = Sourceurl + "&page=" + str(x)
    source = requests.get(page_url).text
    soup = BeautifulSoup(source, 'lxml')
    page_div = soup.find_all('div', class_='region-content')
    print("----PAGINA " + str(x) + "----")
    if page_div:
        for x in page_div:
            naam = x.h3.text
            link = x.a['href']
            categorydiv = x.find('div', class_='field field--name-field-categorie field--type-entity-reference field--label-hidden field__items')
            category = categorydiv.find('div', class_='field__item').text
            webshop = Webshop(naam, link, category)
            webshoplist.append(webshop)
            print(naam + " ADDED")
    else:
        print("EMPTY")
        break

# GET TIME FOR FILENAMESTRING
now = datetime.now()
now = str(now).replace(" ","_")
now = now[:len(now)-10]

# CREATE FILENAME
csvfilename = "csv_files/webscraped_webshops/webshops_webscraped" + str(now) + ".csv"

# SAVE TO CSV
with open(csvfilename, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['naam', 'url', 'categorie'])
    for webshop in webshoplist:
        writer.writerow([webshop.name, webshop.url, webshop.category])
print("\nYour file: " + csvfilename + " has been created")

