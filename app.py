from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import argparse
from album import Album
import datetime

# Ajout d'un paramètre facultatif permettant de sélectionner une autre semaine que la semaine courante
parser = argparse.ArgumentParser()
parser.add_argument('--year', help='(optional) year between "2001" and the current year (current year by default)')
parser.add_argument('--week', help='(optional) week number between "1" and "53" (current week by default)')
args = parser.parse_args()

url = 'https://snepmusique.com/les-tops/le-top-de-la-semaine/top-albums/'

try:
    if args.year:
        if args.year.isdigit() and int(args.year) > 2001 and int(args.year) <= datetime.date.today().year:
            print(f'year: {args.year}')
            url = url.append(f'?annee={args.year}')
        else:
            print('Invalid year: must be between "2001" and the current year')
    else:
        print(f'year: {datetime.date.today().year}')

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
        print(f'week: {datetime.date.today().strftime("%V")}')

except Exception:
    print(f'An error has occured')
    print(f'year: {datetime.date.today().year}')
    print(f'week: {datetime.date.today().strftime("%V")}')
    url = 'https://snepmusique.com/les-tops/le-top-de-la-semaine/top-albums/'

request_text = requests.get(url)

soup = BeautifulSoup(request_text.content, 'html.parser')

df = pd.DataFrame(columns=['rank','trend','title','artist','editor','last_week_rank','week_in','best_rank'])
df['rank'] = df['rank'].astype('int')
df['trend'] = df['trend'].astype('string')
df['title'] = df['title'].astype('string')
df['artist'] = df['artist'].astype('string')
df['editor'] = df['editor'].astype('string')
df['last_week_rank'] = df['last_week_rank'].astype('int')
df['week_in'] = df['week_in'].astype('int')
df['best_rank'] = df['best_rank'].astype('int')

for element in soup.find_all('div', class_='item'):
    
    rank = element.find('div', class_='rang')
    title = element.find('div', class_='titre')
    artist = element.find('div', class_='artiste')
    editor = element.find('div', class_='editeur')
    last_week_rank = element.find('div', class_='rang_precedent')
    week_in = element.find('div', class_='week_in')
    best_rank = element.find('div', class_='best_pos')

    album = Album(
        rank.get_text(),
        'Up' if(element.find('div', class_='rang_up icon-bigarrowup') != None) else ('Down' if(element.find('div', class_='rang_down icon-bigarrowdown') != None) else 'Neutral'),
        title.get_text(),
        artist.get_text(),
        editor.get_text(),
        -1 if last_week_rank == None else int(last_week_rank.find('strong').get_text()[0:-2 if 'er' in last_week_rank.find('strong').get_text() else -1]),
        0 if week_in.find('strong').get_text() == 'Nouvelle entrée' else int(week_in.find('strong').get_text()[0:-2 if 'er' in week_in.find('strong').get_text() else -1]),
        int(best_rank.find('strong').get_text()[0:-2 if 'er' in best_rank.find('strong').get_text() else -1]),
    )
    
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

print('ended')