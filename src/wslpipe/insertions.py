from utils.db import DB
from configparser import ConfigParser
from wsl import Wsl

import requests
from bs4 import BeautifulSoup
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
    
def insert_ranking(ranking_page):
    try:
        html = wsl.fetch_page(ranking_page)
        ranking_df = wsl.get_ranking(html)

        db = DB('postgres', 'wsl', 'changeme', 'localhost')
        cursor = db.connect_cursor()
        for row in ranking_df.reset_index().to_dict('rows'):
            query = """
            INSERT into rankings(ranking, athlete, event, score, created_at) values(%s, %s, %s, %s, %s);
            """ % (row['Ranking'], row['Athlete'], row['Number'], row['Score'], _get_current_time())
            cursor.execute(query)
        db.commit()
        db.close_connection()

        return f'{ranking_df[0]} inserted'

    except Exception as e:
        print(f"An error occurred: {e}")

        return None
    
# Only use when rebuilding all DBs
def building_historic():
    pass


if __name__ == '__main__':
    START_YEAR = 2010
    wsl = Wsl()
    db = DB('postgres', 'wsl', 'changeme', 'localhost')
    cursor = db.connect_cursor()

    xml_athletes = 'https://www.worldsurfleague.com/rss/sitemap_athletes.xml'
    urls = get_athletes_url(xml_athletes)
    current_time = _get_current_time()

    id = 1
    for url in urls:
        id += 1
        cursor.execute('SELECT * FROM cache_logs WHERE link = %s', (url, ))
        link_exists = cursor.fetchone()

        if link_exists:
            print(f'Record {url} already exists')
        else:
            cursor.execute('INSERT INTO cache_logs(id, link, updated_at) VALUES(%s, %s, %s)',
                           (id, url, current_time))
            db.commit()
            print(insert_athlete(url))
            sleep(randint(1, 5))

    db.close_connection()

