import requests
from bs4 import BeautifulSoup
import urllib

#Retrieve requested data from a specific book
def book_data(url):

    r = requests.get(url)

    if r.ok:
        print("Connexion avec la page établie.")
    else:
        print("Connexion avec le site impossible. Veuillez réessayer plus tard.")

    page = r.text
    soup = BeautifulSoup(page, features="html.parser")

    product_page_url = url
    universal_product_code = soup.find("th", text="UPC").next_sibling.text
    title = soup.find("div", {"class":"col-sm-6 product_main"}).find("h1").text
    price_including_tax = soup.find("th", text="Price (incl. tax)").next_sibling.text
    price_excluding_tax = soup.find("th", text="Price (excl. tax)").next_sibling.text
    number_available = soup.find("th", text="Availability").next_sibling.next_sibling.text.split()[2][1:]
    product_description = soup.find("div", {"id":"product_description"}).next_sibling.next_sibling.text
    category = soup.find("ul", {"class":"breadcrumb"}).select("li > a", limit=3)[2].text
    review_rating = soup.find("div", {"class": "col-sm-6 product_main"}).find("p",{"class":"star-rating"})["class"][1]
    image_url = soup.find("div",{"class":"item active"}).find("img")["src"].replace("../..",url)

    return (product_page_url + "\n" + universal_product_code + "\n" + title.replace(",","") + "\n" + price_including_tax + "\n" + price_excluding_tax + "\n" + number_available + "\n" + product_description.replace(",","") + "\n" + category + "\n" + review_rating + "\n" + image_url)

# print(book_data("http://books.toscrape.com/catalogue/the-requiem-red_995/index.html"))

# #with permet d'avoir la fermeture dynamique du fichier à la fin du bloc with
# with open("Extraction.csv", "w") as extraction:
#     extraction.write("product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url\n")
#     extraction.write(product_page_url + "," + universal_product_code + "," + title.replace(",","") + "," + price_including_tax + "," + price_excluding_tax + "," + number_available + "," + product_description.replace(",","") + "," + category + "," + review_rating + "," + image_url)

#TODO Retrieve the list of books categories from the website first as a list then as a dictionary
def categories_list(url):
    r = requests.get(url)
    if r.status_code != 200:
        print("Site non disponible. Merci de réessayer plus tard.")
    soup = BeautifulSoup(r.text, features="html.parser")
    categories = soup.find("div",class_="side_categories").find("ul",class_="nav nav-list").text.replace(" ","").split("\n")
    categories_list = []
    i = 1
    for category in categories:
        if category != "":
            categories_list.append([i,category.lower()])
            i += 1
        else:
            continue
    categories_dictionary = {}
    for category in categories_list:
        categories_dictionary[category[1]] = category[0]
    return categories_dictionary
print(categories_list("http://books.toscrape.com/index.html"))

#Retrieve the total number of categories
def categories_count(url):
    r = requests.get(url)
    if r.status_code != 200:
        print("Site non disponible. Merci de réessayer plus tard.")
    soup = BeautifulSoup(r.text, features="html.parser")
    categories = soup.find("div",class_="side_categories").find("ul",class_="nav nav-list").text.replace(" ","").split("\n")
    return len([category for category in categories if category != "" and category != "Books"])

# with open("Temp.txt", "w") as temp:
#     temp.write(str(categories_count("http://books.toscrape.com/index.html")))
#     temp.write(str(len(categories_count("http://books.toscrape.com/index.html"))))

# for category in categories_list("http://books.toscrape.com/index.html"):
#     if category == "Books":
#         continue
#     print(category)
#
# print(categories_count("http://books.toscrape.com/index.html"))

#TODO Retrieve total count of books for a specific category
def books_count_by_category(category):
    category = category.lower()
    url = "http://books.toscrape.com/catalogue/category/books/"+category+"_"+str(categories_list("http://books.toscrape.com/index.html")[category])+"/index.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text,features="html.parser")
    books_count = soup.find("form",class_="form-horizontal").find("strong").text
    return books_count

print(books_count_by_category("Romance"))

#Retrieve all books urls belonging to a specific category
def books_url_by_category(category):
    category = category.lower()
    url = "http://books.toscrape.com/catalogue/category/books/"+category+"_"+str(categories_list("http://books.toscrape.com/index.html")[category])+"/index.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text,features="html.parser")
    books_url = soup.find("ol",class_="row")
    books_url = str(books_url.select("h3"))
    debut = books_url.find("../")
    fin = books_url.find(".html")
    return "http://books.toscrape.com/catalogue"+books_url[debut+8:fin+5]

print(books_url_by_category("Romance"))

#Retrieve product image url from product page
def products_images_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,features="html.parser")
    image_url = soup.find("div",class_="item active").find("img")["src"].replace("../..","http://books.toscrape.com")
    return image_url

print(products_images_url("http://books.toscrape.com/catalogue/pet-sematary_726/index.html"))

#Download product image from website to the working directory
def download_products_images(url):
    urllib.request.urlretrieve(url,url.split("/")[-1])
    return

download_products_images("http://books.toscrape.com/media/cache/99/ef/99ef2f3987ee016bdd120a4579ef98f5.jpg")



# import time

# url = "http://books.toscrape.com/"
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

# #with permet d'avoir la fermeture dynamique du fichier à la fin du bloc with
# with open("BookScraping.csv", "w") as extraction:
#     for alt in books:
#         extraction.write(alt + "\n")

