from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import argparse
from album import Album

# Ajout d'un paramètre facultatif permettant de sélectionner une autre semaine que la semaine courante
parser = argparse.ArgumentParser()
parser.add_argument('--year', help='year "20XX" or "Tout" for all time (current year by default)')
parser.add_argument('--week', help='week number between 1 and 53 (current week by default)')
args = parser.parse_args()

url = 'https://snepmusique.com/les-tops/le-top-de-la-semaine/top-albums/'

if args.year:
    print(f'year: {args.year}')
    url = url.append(f'?annee={args.year}')

if args.week:
    print(f'week: {args.week}')
    if '?' in url:
        url = url.append(f'&semaine={args.week}')
    else:
        url = url.append(f'?semaine={args.week}')

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
    
    album = Album(
        element.find('div', class_='rang').get_text(),
        'Up' if(element.find('div', class_='rang_up icon-bigarrowup') != None) else ('Down' if(element.find('div', class_='rang_down icon-bigarrowdown') != None) else 'Neutral'),
        element.find('div', class_='titre').get_text(),
        element.find('div', class_='artiste').get_text(),
        element.find('div', class_='editeur').get_text(),
        -1 if element.find('div', class_='rang_precedent') == None else int(element.find('div', class_='rang_precedent').find('strong').get_text()[0:-2 if 'er' in element.find('div', class_='rang_precedent').find('strong').get_text() else -1]),
        0 if element.find('div', class_='week_in').find('strong').get_text() == 'Nouvelle entrée' else int(element.find('div', class_='week_in').find('strong').get_text()[0:-2 if 'er' in element.find('div', class_='week_in').find('strong').get_text() else -1]),
        int(element.find('div', class_='best_pos').find('strong').get_text()[0:-2 if 'er' in element.find('div', class_='best_pos').find('strong').get_text() else -1]),
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