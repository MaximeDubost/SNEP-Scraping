![](img/440px-SNEP_Logo.png)

# Projet de scraping du site du SNEP

<br>

## Sommaire
- [Le projet](#le-projet)
- [Le site du SNEP](#le-site-du-snep)
- [Le fonctionnement](#le-fonctionnement)
- [Le résultat](#le-résultat)

<br>

## Le projet

Le projet conciste a effectuer du scraping sur le site web du SNEP (Syndicat National de l'Edition Phonographique) afin de récupérer le classement français des meilleures albums de musique de la semaine courante ou d'une semaine spécifique, ainsi que les certifications liées à ces albums.

L'outil de scraping utilisé est BeautifulSoupe 4 (Python).

<br>

## Le site du SNEP

Deux URL du site du SNEP seront utilisées pour procéder au scraping :
- Top Albums hebdomadaire (https://snepmusique.com/les-tops/le-top-de-la-semaine/top-albums/)

![](img/top_albums.PNG)

- Certifications (https://snepmusique.com/les-certifications/)

![](img/certifications.PNG)

Les données récupérées seront réunies dans un seul DataFrame (avec la librairie pandas) afin d'être analisées

<br>

## Le fonctionnement

Pour faire fonctionner le projet en local, exécuter le fichier app.py :

```
python app.py
```

Ceci aura pour effet de lancer le scraping avec les paramètres par défaut, mais il est possible de modifier 4 paramètres dont il est possible de voir les détails grace à la commande suivante :

```
python app.py --help
```

![](img/help.PNG)

Attention, le paramètre `--with-certification` augmente proportionnellement le temps de traitement par rapport à la valeur du paramètre `--limit` : cela ajoute un temps d'attente de 3s entre chaque scraping de certification d'album.

<br>

## Le résultat

Le résultat est généré sous forme de fichier CSV et XLS. Voici le résultat généré pour la commande suivante :

```
python app.py --limit 20 --with-certification
```

![](img/result.PNG)