from utils.db import DB
from psycopg2.extras import execute_values
from configparser import ConfigParser
from wsl import Wsl

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from random import randint
from time import sleep


def _get_current_time():
    return datetime.now().date()

def get_athletes_url(xml_url):
    res = requests.get(xml_url)

    xml_data = res.text

    root = ET.fromstring(xml_data)
    namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    athletes_urls = [elem.text for elem in root.findall('.//ns:loc', namespaces)]

    return athletes_urls

def insert_athlete(athlete_page):
    try:
        html = wsl.fetch_page(athlete_page)
        athlete = wsl.get_athlete(html)
        athlete.append(_get_current_time())

        db = DB('postgres', 'wsl', 'changeme', 'localhost')
        cursor = db.connect_cursor()
        cursor.execute(
            'INSERT INTO athletes(name, country, name_country, stance, age, height, weight, hometown, created_at) \
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)', athlete)
        db.commit()
        db.close_connection()

        return f'{athlete[0]} inserted'

    except Exception as e:
        print(f"An error occurred: {e}")

    return None  
    
def insert_ranking(year):
    try:
        ranking_df = wsl.get_ranking(year)
        ranking_df['Year'] = year

        db = DB('postgres', 'wsl', 'changeme', 'localhost')
        cursor = db.connect_cursor()

        tuples = [tuple(x) for x in ranking_df[['Ranking', 'Athlete', 'Number', 'Score', 'updated_at', 'Year']].to_numpy()]
        query = """
        INSERT INTO rankings (ranking, athlete, event, score, created_at, year)
        VALUES %s;
        """
        execute_values(cursor, query, tuples)

        db.commit()
        cursor.close()
        db.close_connection()

        return f'ranking of year {year} inserted'

    except Exception as e:
        print(f"An error occurred: {e}")

        return None
    
# Only use when rebuilding DB
def building_historic_rankings():
    START_YEAR = 2010
    END_YEAR = _get_current_time().year

    for year in range(START_YEAR, END_YEAR + 1):
        insert_ranking(year)
        print(f'{year} inserted')
        sleep(randint(1, 5))

    db.close_connection()

# Only use when rebuilding DB
def building_historic_athletes():
    xml_athletes = 'https://www.worldsurfleague.com/rss/sitemap_athletes.xml'
    urls = get_athletes_url(xml_athletes)
    current_time = _get_current_time()

    for url in urls:
        cursor.execute('SELECT * FROM cache_logs WHERE link = %s', (url, ))
        link_exists = cursor.fetchone()

        if link_exists:
            print(f'Record {url} already exists')
        else:
            cursor.execute('INSERT INTO cache_logs(link, updated_at) VALUES(%s, %s)',
                           (url, current_time))
            db.commit()
            print(insert_athlete(url))
            sleep(randint(1, 5))

    db.close_connection()

if __name__ == '__main__':
    wsl = Wsl()
    db = DB('postgres', 'wsl', 'changeme', 'localhost')
    cursor = db.connect_cursor()
    
    cursor.execute("SELECT MAX(created_at) FROM rankings;")
    max_value = cursor.fetchone()[0]

    if wsl.get_last_update_ranking() > max_value:
        insert_ranking(_get_current_time.year)
        print('ranking updated')
    else:
        print('not necessary to update ranking')

    building_historic_athletes()



    
