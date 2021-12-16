from bs4 import BeautifulSoup
from album import Album
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
import requests
import datetime
import time

# Ajout de divers paramètres facultatifs
parser = argparse.ArgumentParser()
parser.add_argument('--year', help='(optional) year between "2001" and the current year (current year by default)')
parser.add_argument('--week', help='(optional) week number between "1" and "53" (current week by default)')
parser.add_argument('--limit', help='(optional) limit of firsts top albums between "1" and "199" (all 200 albums shown by default)')
parser.add_argument('--with-certification', help='(optional) use this parameter to show the columns related to album certifications', action="store_true")
args = parser.parse_args()

# Paramètres par défaut
url = 'https://snepmusique.com/les-tops/le-top-de-la-semaine/top-albums/'
limit: int = 200
with_certification = False

# Vérification de la conformité des paramètres saisis par l'utilisateur
try:
    print()
    print('+--- Args ---+')
    # --year
    if args.year:
        if args.year.isdigit() and int(args.year) > 2001 and int(args.year) <= datetime.date.today().year:
            print(f'year: {args.year}')
            url = url.append(f'?annee={args.year}')
        else:
            print('Invalid year: must be between "2001" and the current year')
    else:
        print(f'year: default ({datetime.date.today().year})')

    # --week
    if args.week:
        if args.week.isdigit() and int(args.week) >= 1 and int(args.year) <= 53:
            print(f'week: {args.week}')
            if args.year in url :
                url = url.append(f'&semaine={args.week}')
            else:
                url = url.append(f'?semaine={args.week}')
        else:
            print('Invalid week: must be between "1" and "53"')
    else:
        print(f'week: default ({datetime.date.today().strftime("%V")})')
    
    # --limit
    if args.limit:
        if args.limit.isdigit() and int(args.limit) >= 1 and int(args.limit) <= 199:
            print(f'limit: {args.limit}')
            limit = int(args.limit)
        else:
            print('Invalid limit: must be between "1" and "199"')
    else:
        print(f'limit: none')

    # --with-certification
    if args.with_certification:
        print(f'with-certification: yes')
        with_certification = True
    else:
        print(f'with-certification: no')

# Rétablissement des paramètres par défaut en cas d'erreur non gérée
except Exception:
    print()
    print(f'An error has occured, default parameters will be used')
    print(f'year: {datetime.date.today().year}')
    print(f'week: {datetime.date.today().strftime("%V")}')
    print(f'limit: none')
    print(f'with-certification: no')
    url = 'https://snepmusique.com/les-tops/le-top-de-la-semaine/top-albums/'
    limit = 200
    with_certification = False

# Préparation du scraping
request_text = requests.get(url)
soup = BeautifulSoup(request_text.content, 'html.parser')

# Gestion de la limite d'affichage du top albums
if limit != 200:
    items = soup.find_all('div', class_='item', limit=limit)
else:
    items = soup.find_all('div', class_='item')

# Tableau d'objets "Album"
top_albums = []

# Bouclage sur les div "item" de la liste sur la page html
for item in items:

    rank = item.find('div', class_='rang')
    trend_up = item.find('div', class_='rang_up icon-bigarrowup')
    trend_down = item.find('div', class_='rang_down icon-bigarrowdown')
    title = item.find('div', class_='titre')
    artist = item.find('div', class_='artiste')
    editor = item.find('div', class_='editeur')
    last_week_rank = item.find('div', class_='rang_precedent')
    week_in = item.find('div', class_='week_in')
    best_rank = item.find('div', class_='best_pos')

    # Création d'un nouvel objet "Album"
    top_albums.append(Album(
        rank.get_text(),
        'Up' if(trend_up != None) else ('Down' if(trend_down != None) else 'Neutral'),
        title.get_text(),
        artist.get_text(),
        editor.get_text(),
        0 if last_week_rank == None else int(last_week_rank.find('strong').get_text()[0:-2 if 'er' in last_week_rank.find('strong').get_text() else -1]),
        0 if week_in.find('strong').get_text() == 'Nouvelle entrée' else int(week_in.find('strong').get_text()[0:-2 if 'er' in week_in.find('strong').get_text() else -1]),
        int(best_rank.find('strong').get_text()[0:-2 if 'er' in best_rank.find('strong').get_text() else -1])
    ))

# Gestion de l'affichage des données relatives aux certifications
if with_certification:
    df = pd.DataFrame(columns=['rank','trend','title','artist','editor','last_week_rank','week_in','best_rank','certification','certification_date'])

    for album in top_albums:

        print('', end='\r')
        print(f'[.  ] Scraping certification (album {album.rank}/{limit}).', end='\r')
        time.sleep(1)
        print(f'[.. ] Scraping certification (album {album.rank}/{limit}).', end='\r')
        time.sleep(1)
        print(f'[...] Scraping certification (album {album.rank}/{limit}).', end='\r')
        time.sleep(1)
        
        # Récupération des certifications de l'album
        request_text = requests.get(f'https://snepmusique.com/les-certifications/?categorie=Albums&interprete={album.artist}&titre={album.title}')
        soup = BeautifulSoup(request_text.content, 'html.parser')

        album.certification = soup.find('div', class_='certif').get_text() if soup.find('div', class_='certification') else ''
        album.certification_date = soup.find_all('div', class_='date')[1].get_text()[15:] if soup.find('div', class_='certification') else ''

        df = df.append({
            'rank': album.rank,
            'trend': album.trend,
            'title': album.title,
            'artist': album.artist,
            'editor': album.editor,
            'last_week_rank': album.last_week_rank,
            'week_in': album.week_in,
            'best_rank': album.best_rank,
            'certification': album.certification,
            'certification_date': album.certification_date
        }, ignore_index=True)
    
    print()

    no_certification = df.certification.where(df.certification == '').count()
    gold = df.certification.where(df.certification == 'Or').count()
    platinium = df.certification.where(df.certification == 'Platine').count()
    double_platinium = df.certification.where(df.certification == 'Double Platine').count()
    triple_platinium = df.certification.where(df.certification == 'Triple Platine').count()
    diamond = df.certification.where(df.certification == 'Diamant').count()
    double_diamond = df.certification.where(df.certification == 'Double Diamant').count()
    triple_diamond = df.certification.where(df.certification == 'Triple Diamant').count()
    quad_diamond = df.certification.where(df.certification == 'Quadruple Diamant').count()

    array = np.array([no_certification, gold, platinium, double_platinium, triple_platinium, diamond, double_diamond, triple_diamond, quad_diamond])
    labels = ["Aucune", "Or", "Platine", "Double Platine", "Triple Platine", "Diamant", "Double Diamant", "Triple Diamant", "Quadruple Diamant"]

    plt.pie(array, autopct='%1.1f%%')
    plt.title(f"Répartition des certifications pour les {limit} premières places du Top Albums (semaine courante, année courante)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, labels = labels)
    plt.savefig(f"results/certifications_{datetime.datetime.now().isoformat()}.jpg", bbox_inches="tight")
    plt.show()
        
else:
    df = pd.DataFrame(columns=['rank','trend','title','artist','editor','last_week_rank','week_in','best_rank'])

    for album in top_albums:

        df = df.append({
            'rank': album.rank,
            'trend': album.trend,
            'title': album.title,
            'artist': album.artist,
            'editor': album.editor,
            'last_week_rank': album.last_week_rank,
            'week_in': album.week_in,
            'best_rank': album.best_rank
        }, ignore_index=True)
    

df.to_csv('results/SNEP_Top_Albums.csv')
df.to_excel('results/SNEP_Top_Albums.xls')
print()
print("Result saved on \"results\" directory.")