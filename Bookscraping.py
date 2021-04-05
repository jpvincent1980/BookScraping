import requests
from bs4 import BeautifulSoup
from math import ceil
import urllib
import csv
import os

forbiddencharacters = {60: None, 62: None, 58: None, 8220: None, 47: None, 92: None, 124: None, 63: None, 42: None, 46: None, 39: None, 34: None}

def books_data_without_export(url):
    """ This function will return book url, UPC, title, price including tax, price excluding tax, quantity available, description, category, rating and image url. """

    r = requests.get(url)
    if r.status_code != 200:
        print("Connexion avec le site impossible. Veuillez réessayer plus tard.")
    else:
        page = r.text
        soup = BeautifulSoup(page, features="html.parser")

        book_dict = {}
        book_dict["product_page_url"] = url
        book_dict["universal_product_code"] = (soup.find("th", text="UPC").next_sibling.text \
                                                   if soup.find("th", text="UPC").next_sibling else "UPC non disponible.")
        book_dict["title"] = (soup.find("div", {"class":"col-sm-6 product_main"}).find("h1").text \
                                  if soup.find("div", {"class":"col-sm-6 product_main"}).find("h1") else "Titre non disponible.")
        book_dict["price_including_tax"] = (soup.find("th", text="Price (incl. tax)").next_sibling.text \
                                                if soup.find("th", text="Price (incl. tax)").next_sibling else "Prix TTC non disponible.")
        book_dict["price_excluding_tax"] = (soup.find("th", text="Price (excl. tax)").next_sibling.text \
                                                if soup.find("th", text="Price (excl. tax)").next_sibling else "Prix HT non disponible.")
        book_dict["number_available"] = (soup.find("th", text="Availability").next_sibling.next_sibling.text.split()[2][1:] \
                                             if soup.find("th", text="Availability").next_sibling.next_sibling else "Quantité non disponible.")
        book_dict["product_description"] = (soup.find("div", {"id":"product_description"}).next_sibling.next_sibling.text.replace(",","") \
                                                if soup.find("div", {"id":"product_description"}) else "Description non disponible.")
        book_dict["category"] = (soup.find("ul", {"class":"breadcrumb"}).select("li > a", limit=3)[2].text \
                                     if soup.find("ul", {"class":"breadcrumb"}) else "Catégorie non disponible.")
        book_dict["review_rating"] = (soup.find("div", {"class": "col-sm-6 product_main"}).find("p",{"class":"star-rating"})["class"][1] \
                                          if soup.find("div", {"class": "col-sm-6 product_main"}).find("p",{"class":"star-rating"}) else "Note non disponible.")
        book_dict["image_url"] = (soup.find("div",{"class":"item active"}).find("img")["src"].replace("../..","http://books.toscrape.com/") \
                                      if soup.find("div",{"class":"item active"}).find("img") else "Image non disponible.")

        return book_dict

def export_books_data(dictionary):
    """ This function will export book url, UPC, title, price including tax, price excluding tax, quantity available, description, category, rating and image url in a csv file by the name of the book and saved in adirectory by the name of the category to which the book belongs to. """

    # Retrieve current directory path
    current_path = os.getcwd()

    # Checks if a directory by the name of the books category already exists and if not, creates one
    if not os.path.exists(current_path + "\\" + dictionary["category"].translate(forbiddencharacters)):
        os.makedirs(current_path + "\\" + dictionary["category"].translate(forbiddencharacters))

    with open(current_path + "\\" + dictionary["category"].translate(forbiddencharacters) + "\\" + dictionary[
        "title"].translate(forbiddencharacters) + ".csv", "w", newline="", encoding="utf-8") as csvfile:
        columns = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
                   "number_available", "product_description", "category", "review_rating", "image_url"]
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows([dictionary])

    print("Le fichier " + dictionary["title"].translate(forbiddencharacters) + ".csv vient d'être créé dans le répertoire /" + dictionary["category"].translate(forbiddencharacters) + ".")

def books_data(url):
    """ This function will return book url, UPC, title, price including tax, price excluding tax, quantity available, description, category, rating and image url and export those data in a csv file by the name of the book title. """
    book_dict = books_data_without_export(url)
    export_books_data(book_dict)
    return

def categories_list(url):
    """ This function will return the list of categories with their name and url existing on the website. """
    r = requests.get(url)
    if r.status_code != 200:
        print("Site non disponible. Merci de réessayer plus tard.")
    soup = BeautifulSoup(r.text, features="html.parser")
    categories_dictionary = {}
    categories = soup.find("div", class_="side_categories").find("ul", class_="nav nav-list").find("ul").findAll("li")
    for i in range(len(categories)):
        category_name = soup.find("div", class_="side_categories").find("ul", class_="nav nav-list").find("ul").findAll("li")[i].text.strip()
        category_url = "http://books.toscrape.com/" + soup.find("div", class_="side_categories").find("ul", class_="nav nav-list").find("ul").findAll("li")[i].find("a")["href"]
        categories_dictionary[category_name] = category_url
    return categories_dictionary

def categories_count(url):
    """ This function will return the number of categories existing on the website called by the function. """
    r = requests.get(url)
    if r.status_code != 200:
        print("Site non disponible. Merci de réessayer plus tard.")
    soup = BeautifulSoup(r.text, features="html.parser")
    categories = soup.find("div",class_="side_categories").find("ul",class_="nav nav-list").text.replace(" ","").split("\n")
    return len([category for category in categories if category != "" and category != "Books"])

def books_count_by_category(category):
    """ This function will return the number of books for the category called by the function. """
    category = category.capitalize()
    url = categories_list("http://books.toscrape.com/index.html").get(category)
    r = requests.get(url)
    soup = BeautifulSoup(r.text,features="html.parser")
    books_count = soup.find("form",class_="form-horizontal").find("strong").text
    return books_count

def books_data_by_category_without_export(category):
    """ This function will return book title and url for all books belonging to the category called in this function. """
    check = 0
    for element in categories_list("http://books.toscrape.com/index.html"):
        if element.lower() == category.lower():
            category = element
            check = 1
        else:
            continue
    if check == 0:
        print("Cette catégorie n'existe pas. Merci de renseigner un nom de catégorie valide.")
    else:
        url = categories_list("http://books.toscrape.com/index.html").get(category)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features="html.parser")

        books_count = int(soup.find("form", class_="form-horizontal").find("strong").text)
        if books_count <= 20:
            books_number = len(soup.find("ol", class_="row").findAll("li"))
            books_list = []
            for i in range(books_number):
                books_dict = {}
                books_name = soup.find("ol", class_="row").findAll("li")[i].find("h3").text.replace(",", "").strip()
                books_url = soup.find("ol", class_="row").findAll("li")[i].find("a")["href"].replace("../../..",
                                                                                                     "http://books.toscrape.com/catalogue")
                books_dict["books_title"] = books_name
                books_dict["books_url"] = books_url
                books_list.append(books_dict)
        else:
            books_list = []

            for i in range(1, ceil(books_count / 20) + 1):
                url = categories_list("http://books.toscrape.com/index.html").get(category).replace("index",
                                                                                                    "page-" + str(i))
                r = requests.get(url)
                soup = BeautifulSoup(r.text, features="html.parser")
                books_number = len(soup.find("ol", class_="row").findAll("li"))
                for i in range(books_number):
                    books_dict = {}
                    books_name = soup.find("ol", class_="row").findAll("li")[i].find("h3").text.replace(",", "").strip()
                    books_url = soup.find("ol", class_="row").findAll("li")[i].find("a")["href"].replace("../../..",
                                                                                                         "http://books.toscrape.com/catalogue")
                    books_dict["books_title"] = books_name
                    books_dict["books_url"] = books_url
                    books_list.append(books_dict)

        books_data_list = []
        for book in books_list:
            books_data_list.append(books_data_without_export(book["books_url"]))

        return books_data_list

def export_books_data_by_category(books_data_list):
    """ This function will export book title and url of the list of books called by this function in a csv file by the name of the category and saved in a directory by the name of the category. """
    category = books_data_list[0]["category"]

    # Retrieves current directory path
    current_path = os.getcwd()

    # Checks if a directory by the name of the books category already exists and if not, creates one
    if not os.path.exists(current_path + "\\" + category.translate(forbiddencharacters)):
        os.makedirs(current_path + "\\" + category.translate(forbiddencharacters))

    # Exports the list of books names and urls to a csv file with the name of category
    with open(current_path + "\\" + category + "\\" + category + ".csv", "w", newline="", encoding="utf-8") as csvfile:
        columns = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
                   "number_available", "product_description", "category", "review_rating", "image_url"]
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(books_data_list)

    print("Les données de tous les livres appartenant à la catégorie " + category.translate(forbiddencharacters) + " ont été exportées dans le fichier " + category.translate(forbiddencharacters) + ".csv créé dans le répertoire /" + category.translate(forbiddencharacters))

def books_data_by_category(category):
    """ This function will return book title and url for all books belonging to the category called in this function and exports them in a csv file by the name of the category and saved in a directory by the name of the category. """
    books_list = books_data_by_category_without_export(category)
    if books_list is None:
        print("** Fin du traitement **")
    else:
        export_books_data_by_category(books_list)

def products_images_url(url):
    """ This function will return the image url of the book which url is called by the function. """
    r = requests.get(url)
    soup = BeautifulSoup(r.text,features="html.parser")
    image_url = soup.find("div",class_="item active").find("img")["src"].replace("../..","http://books.toscrape.com")
    return image_url

def products_image_size(url):
    """ This function will return the size in Ko of the image which url is called by the function. """
    r = requests.head(url)
    image_size = r.headers["Content-Length"]
    image_size = str(int(image_size)/100)
    return image_size + " Ko"

def download_products_images(url):
    """ This function will download the image from the url called by this function. """
    urllib.request.urlretrieve(url,url.split("/")[-1])
    return

def books_data_by_website_without_export(url):
    """ This function will return book url, UPC, title, price including tax, price excluding tax, quantity available, description, category, rating and image url for all books sold on the website. """
    categories_dictionary = categories_list(url)
    url_list = []
    for category in categories_dictionary.keys():
        url_list.append(books_data_by_category_without_export(category))
    return url_list

def books_data_by_website(url):
    """ This function will return book url, UPC, title, price including tax, price excluding tax, quantity available, description, category, rating and image url for all books sold on the website and export those data in csv files by the name of the categories to whoch books belong and saved in directories by the name of each category. """
    categories_dictionary = categories_list(url)
    url_list = []
    for category in categories_dictionary.keys():
        print("Chargement en cours ...")
        url_list.append(books_data_by_category(category))
    print("** Fin du traitement  ")
    return url_list

def download_all_products_images(url):
    """ This function will download all books images from the website and save them in directories by the name of the category to which books belong to. """
    print("Chargement en cours ...")
    a = 0
    allbooks = books_data_by_website_without_export(url)
    for books in allbooks:
        for book in books:
            picture_url = book["image_url"]
            category = book["category"]
            # Retrieve current directory path
            current_path = os.getcwd()
            # Check if a directory by the name of the books category already exists and if not, creates one
            if not os.path.exists(current_path + "\\" + category.translate(forbiddencharacters)):
                os.makedirs(current_path + "\\" + category.translate(forbiddencharacters))
            urllib.request.urlretrieve(picture_url, current_path + "\\" + category.translate(forbiddencharacters) + "\\" + picture_url.split("/")[-1])
            a += 1
            print("Téléchargement de l'image " + str(a))
    print("** Fin du traitement **")

# books_data("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
# books_data_by_category("poetry")
# books_data_by_website("http://books.toscrape.com/")
# download_all_products_images("http://books.toscrape.com/")

help(download_all_products_images)