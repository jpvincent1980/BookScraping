import requests
from bs4 import BeautifulSoup
# import time
#
url = "http://books.toscrape.com/"
# r = requests.get(url)
#
# if r.ok:
#     print("Connexion établie avec le site books.toscrape.com\n")
# else:
#     print("Connexion avec le site impossible. Veuillez réessayer plus tard.")
#
# #r.headers -> récupère l'ensemble des headers du serveur de l'url
# headers = r.headers
# # print(headers)
#
# #r.text -> récupère tout le contenu html de l'url
# page = r.text
# # print(page)
#
# soup = BeautifulSoup(page,features="html.parser")
# # print(soup)
#
# title = soup.find("title")
# #Contenu de la première balise title
# print(title)
#
# #Contenu sans les balises html
# print(title.text)
# #Contenu sans les balises html sous forme de liste
# print(title.contents)
#
# #Récupère le contenu de toutes les balises article de l'url
# #Différence entre find et findAll -> première balise trouvée et toutes les balises trouvées
# article = soup.findAll("article")
#
# #Compte toutes les balises article de l'url
# print(len(article))
# print("\n")
#
# #Affiche la balise à l'indice 1 de toutes les balises trouvées
# # print(article[2])
#
# #Affiche toutes les balises article de l'url
# # [print(str(book) + "\n") for book in article]
#
# books = []
# for book in article:
#     img = book.find("img")
#     alt = img["alt"]
#     books.append(alt)
#
# #Force le script à faire une pause de 1 seconde
# time.sleep(1)
#
# print(books)
#
# #with permet d'avoir la fermeture dynamique du fichier à la fin du bloc with
# with open("BookScraping.csv", "w") as extraction:
#     for alt in books:
#         extraction.write(alt + "\n")

url2 = "http://books.toscrape.com/catalogue/1000-places-to-see-before-you-die_1/index.html"
r2 = requests.get(url2)

if r2.ok:
    print("Connexion avec la page établie.")
else:
    print("Connexion avec le site impossible. Veuillez réessayer plus tard.")

page2 = r2.text
soup2 = BeautifulSoup(page2, features="html.parser")

product_page_url = url2
print(url2)
universal_product_code = soup2.find("th", text="UPC").next_sibling.text
print(universal_product_code)
title = soup2.find("div", {"class":"col-sm-6 product_main"}).find("h1").text
print(title)
price_including_tax = soup2.find("th", text="Price (incl. tax)").next_sibling.text
print(price_including_tax)
price_excluding_tax = soup2.find("th", text="Price (excl. tax)").next_sibling.text
print(price_excluding_tax)
number_available = soup2.find("th", text="Availability").next_sibling.next_sibling.text.split()[2][1:]
print(number_available)
product_description = soup2.find("div", {"id":"product_description"}).next_sibling.next_sibling.text
print(product_description)
category = soup2.find("ul", {"class":"breadcrumb"}).select("li > a", limit=3)[2].text
print(category)
review_rating = soup2.find("div", {"class": "col-sm-6 product_main"}).find("p",{"class":"star-rating"})["class"][1]
print(review_rating)
image_url = soup2.find("div",{"class":"item active"}).find("img")["src"].replace("../..",url)
print(image_url)

#with permet d'avoir la fermeture dynamique du fichier à la fin du bloc with
with open("Extraction.csv", "w") as extraction:
    extraction.write("product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url\n")
    extraction.write(product_page_url + "," + universal_product_code + "," + title.replace(",","") + "," + price_including_tax + "," + price_excluding_tax + "," + number_available + "," + product_description.replace(",","") + "," + category + "," + review_rating + "," + image_url)

