import requests
from bs4 import BeautifulSoup
from math import ceil
import urllib
import csv
import os

# Dictionary of characters that can't be used for folders or files names
forbiddencharacters = {60: None, 62: None, 58: None, 8220: None, 47: None, 92: None, 124: None, 63: None, 42: None, 46: None, 39: None, 34: None}
# Retrieve current directory path
current_path = os.getcwd()

def categories_list(url):
    """ This function will return the list of categories with their name and url and create a directory in the /Export
    subfolder for each category. """
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
        # Check if a directory by the name of category already exists and if not, creates one
        if not os.path.exists(current_path + "/Export/" + category_name.translate(forbiddencharacters)):
            os.makedirs(current_path + "/Export/" + category_name.translate(forbiddencharacters))
    return categories_dictionary

def books_data(url):
    """ This function will return book url, UPC, title, price including tax, price excluding tax, quantity available,
    description, category, rating and image url. """
    r = requests.get(url)
    if r.status_code != 200:
        print("Connexion avec le site impossible. Veuillez réessayer plus tard.")
    else:
        page = r.text
        soup = BeautifulSoup(page, features="html.parser")

        image_url = (soup.find("div", {"class": "item active"}).find("img")["src"].replace("../..","http://books.toscrape.com/") if soup.find("div", {"class": "item active"}).find("img") else "")
        category = (soup.find("ul", {"class": "breadcrumb"}).select("li > a", limit=3)[2].text if soup.find("ul", {"class": "breadcrumb"}) else "")
        universal_product_code = (soup.find("th", text="UPC").next_sibling.text if soup.find("th", text="UPC").next_sibling else "")
        title = (soup.find("div", {"class":"col-sm-6 product_main"}).find("h1").text if soup.find("div", {"class":"col-sm-6 product_main"}).find("h1") else "")
        price_including_tax = (soup.find("th", text="Price (incl. tax)").next_sibling.text[1:] if soup.find("th", text="Price (incl. tax)").next_sibling else "")
        price_excluding_tax = (soup.find("th", text="Price (excl. tax)").next_sibling.text[1:] if soup.find("th", text="Price (excl. tax)").next_sibling else "")
        number_available = (soup.find("th", text="Availability").next_sibling.next_sibling.text.split()[2][1:] if soup.find("th", text="Availability").next_sibling.next_sibling else "")
        product_description = (soup.find("div", {"id":"product_description"}).next_sibling.next_sibling.text.replace(",","") if soup.find("div", {"id":"product_description"}) else "")
        review_rating = (soup.find("div", {"class": "col-sm-6 product_main"}).find("p",{"class":"star-rating"})["class"][1] if soup.find("div", {"class": "col-sm-6 product_main"}).find("p",{"class":"star-rating"}) else "")

        urllib.request.urlretrieve(image_url,current_path + "/Export/" + category.translate(forbiddencharacters) + "/" +image_url.split("/")[-1])

        book_dict = {}
        book_dict["product_page_url"] = url
        book_dict["universal_product_code"] = universal_product_code
        book_dict["title"] = title
        book_dict["price_including_tax"] = price_including_tax
        book_dict["price_excluding_tax"] = price_excluding_tax
        book_dict["number_available"] = number_available
        book_dict["product_description"] = product_description
        book_dict["category"] = category
        book_dict["review_rating"] = review_rating
        book_dict["image_url"] = image_url

        return book_dict

def books_data_by_category(category):
    """ This function will return requested data from all books belonging to the category called in the function and
    save them in one csv file by the name of the category in a subfolder by the name of the category. """
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
            books_url = soup.find("ol", class_="row").findAll("li")[i].find("a")["href"].replace("../../..","http://books.toscrape.com/catalogue")
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
                books_url = soup.find("ol", class_="row").findAll("li")[i].find("a")["href"].replace("../../..","http://books.toscrape.com/catalogue")
                books_dict["books_title"] = books_name
                books_dict["books_url"] = books_url
                books_list.append(books_dict)

    books_data_list = []
    for book in books_list:
        books_data_list.append(books_data(book["books_url"]))

    category = books_data_list[0]["category"]

    with open(current_path + "/Export/" + category + "/" + category + ".csv", "w", newline="",
              encoding="utf-8") as csvfile:
        columns = ["product_page_url", "universal_product_code", "title", "price_including_tax",
                   "price_excluding_tax",
                   "number_available", "product_description", "category", "review_rating", "image_url"]
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(books_data_list)

    print("Les données et les images de tous les livres appartenant à la catégorie " + category.translate(
        forbiddencharacters) + " ont été exportées dans le  répertoire /Export/" + category.translate(forbiddencharacters))
    return

def all_books_data():
    """ This function will return book url, UPC, title, price including tax, price excluding tax, quantity available,
    description, category, rating and image url for all books sold on the website and export those data in csv files by
    the name of the categories to whoch books belong and saved in directories by the name of each category. """
    url = "http://books.toscrape.com/"
    categories_dictionary = categories_list(url)
    for category in categories_dictionary.keys():
        print("Chargement en cours ...")
        books_data_by_category(category)
    print("** Fin du traitement  ")
    return

all_books_data()