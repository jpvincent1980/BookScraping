![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)
![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)

# Projet Bookscraping

Ce projet a pour but de récupérer toutes les données utiles relatives aux livres vendus sur le site
[Books To Scrape](http://books.toscrape.com/index.html) ainsi que récupérer leurs images.

## Pré-requis

Une version de Python >= 3.0 doit être installée sur votre poste.

## Installation

Depuis un terminal de type GitBash, déplacez-vous dans le répertoire dans lequel vous souhaitez récupérer le script ainsi que les fichiers *readme.md* et *requirements.txt*  et saisissez la commande ci-dessous:

``git clone https://github.com/jpvincent1980/BookScraping``

Une fois les fichiers téléchargés sur votre poste de travail, vous devez au préalable créer et activer un environnement virtuel sur votre poste.
Pour se faire, suivez les étapes suivantes :
1. Depuis votre terminal et toujours dans le même répertoire que précédemment, créer un environnement virtuel en saisissant la commande suivante:
  `` python -m venv env`` (``env`` sera le nom de votre environnement virtuel)
  

2. Activez votre environnement virtuel en saisissant la commande suivante:
   
   *sous Windows* -> ``env/Scripts/activate.bat``
   
   *sous Mac/Linux* -> ``source/env/bin/activate``
   

Lorsque votre environnement virtuel est activé, installez les modules Python nécessaires à la bonne exécution du script grâce au fichier *requirements.txt* précédemment téléchargé en saisissant la commande ci-dessous toujours depuis le terminal:

``pip install -r requirements.txt``

## Démarrage

Depuis votre terminal de commande et toujours depuis le répertoire dans lequel les fichiers ont été téléchargés, saisissez la commande suivante:

``python Bookscraping.py``

Ceci démarrera le téléchargement de toutes les informations relatives aux livres du site [Books To Scrape](http://books.toscrape.com/index.html) ainsi que leurs images.

Les informations seront regroupées par catégories de livres dans un fichier *.csv* portant le nom de la catégorie à laquelle appartiennent les livres et accessible depuis le sous-répertoire **/Export/*nomDeLaCatégorie***.

Les images seront téléchargées par catégorie dans ces mêmes sous-répertoires.

## IDE utilisé

[PyCharm Community Edition](https://www.jetbrains.com/fr-fr/pycharm/)

## Auteur

[Jean-Philippe Vincent](https://twitter.com/JeanPhilippeV15)