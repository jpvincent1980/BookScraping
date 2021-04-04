Avant d'exécuter le script, merci de bien vouloir créer votre environnement virtuel et y installer les packages listés dans le fichier requirements.txt
****
Tous les scripts sont contenus dans le fichier Bookscraping.py
****
Pour extraire toutes les données d'un livre, merci de bien vouloir exécuter la fonction books_data("liendelaficheproduitdulivre").
Les données du livre seront exportées dans un fichier .csv portant le nom du livre et enregistrées dans un répertoire portant le nom de la catégorie à laquelle le livre appartient.
****
Pour extraire toutes les données de tous les livres appartenant à une catégorie, merci de bien vouloir exécuter la fonction books_data_by_category("nomDeLaCatégorie").
Les données de tous les livres de cette catégorie seront exportées dans un fichier .csv portant le nom de la catégorie enregistré dans un répertoire portant le nom de la catégorie en question.
****
Pour extraire toutes les données de tous les livres du site http://books.toscrape.com/, merci de bien vouloir exécuter la fonction books_data_by_website("http://books.toscrape.com/").
Les données de tous les livres seront exportées dans un fichier .csv portant le nom de la catégorie à laquelle ils appartiennent enregistré dans un répertoire portant le nom de chaque catégorie.
****
Pour télécharger les images de tous les livres, merci d'exécuter la fonction download_all_products_images("http://books.toscrape.com/").
Toutes les images seront téléchargées dans le répertoire portant le nom de la catégorie à laquelle leur livre appartient.