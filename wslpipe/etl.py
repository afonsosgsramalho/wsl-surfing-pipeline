import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .utils.db import DB
from psycopg2.extras import execute_values

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from random import randint
from time import sleep


class WSLDataManager:
    def __init__(self, db_credentials, wsl_instance):
        print('ola')
        self.db = DB(**db_credentials)
        self.wsl = wsl_instance
        print('adeus')

    @staticmethod
    def _get_current_time():
        """Returns the current date."""
        return datetime.now().date()

    def get_athletes_url(self, xml_url):
        """Fetches athlete URLs from a provided XML sitemap URL."""
        response = requests.get(xml_url)
        xml_data = response.text
        root = ET.fromstring(xml_data)
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        athletes_urls = [elem.text for elem in root.findall(
            './/ns:loc', namespaces)]
        return athletes_urls

    def insert_athlete(self, athlete_page):
        """Inserts athlete data into the database."""
        try:
            html = self.wsl.fetch_page(athlete_page)
            athlete_data = self.wsl.get_athlete(html)
            athlete_data.append(self._get_current_time())
            with self.db.connect_cursor() as cursor:
                cursor.execute(
                    'INSERT INTO athletes(name, country, name_country, stance, age, height, weight, hometown, created_at) \
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)', athlete_data)
                self.db.commit()
            return f'{athlete_data[0]} inserted'
        except Exception as e:
            return 'This athlete doesnt have the full attributes to be processed'

    def insert_ranking(self, year):
        """Inserts ranking data for a specific year into the database."""
        try:
            ranking_df = self.wsl.get_ranking(year)
            ranking_df['Year'] = year
            with self.db.connect_cursor() as cursor:
                tuples = [tuple(x) for x in ranking_df.to_numpy()]
                query = "INSERT INTO rankings (ranking, athlete, event, score, created_at, year) VALUES %s;"
                execute_values(cursor, query, tuples)
                self.db.commit()
            return f'Ranking of year {year} inserted'
        except Exception as e:
            return f"An error occurred: {e}"
        
    def delete_ranking(self, year):
        """Deletes ranking data for a specific year into the database."""
        try:
            ranking_df = self.wsl.get_ranking(year)
            ranking_df['Year'] = year
            with self.db.connect_cursor() as cursor:
                cursor.execute(f"DELETE FROM rankings WHERE year = {year};")
                self.db.commit()
            return f'Ranking of year {year} deleted'
        except Exception as e:
            return f"An error occurred: {e}"
        
    def build_historic_data(self):
        """Rebuilds the database with historical rankings and athlete data."""
        self.build_historic_rankings()
        self.build_historic_athletes()

    def build_historic_rankings(self):
        """Inserts historical ranking data into the database."""
        start_year = 2010
        end_year = self._get_current_time().year
        for year in range(start_year, end_year + 1):
            print(self.insert_ranking(year))
            sleep(randint(1, 5))

    def build_historic_athletes(self, xml_athletes='https://www.worldsurfleague.com/rss/sitemap_athletes.xml'):
        """Inserts historical athlete data into the database."""
        urls = self.get_athletes_url(xml_athletes)
        for url in urls:
            with self.db.connect_cursor() as cursor:
                cursor.execute(
                    'SELECT * FROM cache_logs WHERE link = %s', (url,))
                if cursor.fetchone():
                    print(f'Record {url} already exists')
                else:
                    cursor.execute(
                        'INSERT INTO cache_logs(link, created_at) VALUES(%s, %s)', (url, self._get_current_time()))
                    self.db.commit()
                    print(self.insert_athlete(url))
                    sleep(randint(1, 5))

    def get_last_db_update(self):
        """Fetches the last update date for rankings from the database."""
        with self.db.connect_cursor() as cursor:
            cursor.execute("SELECT MAX(created_at) FROM rankings;")
            max_date = cursor.fetchone()[0]
            return max_date if max_date else datetime.min.date()
        
    def update_rankings_if_needed(self, year):
        """Updates the rankings for a given year if the last update is older than the current WSL update."""
        print('rankings 1')
        last_db_update = self.get_last_db_update()
        print('rankings 2')
        last_wsl_update = self.wsl.get_last_update_ranking()
        print('rankings 3')

        print(last_wsl_update)
        print(last_db_update)
        if last_wsl_update.date() > last_db_update:
            if last_wsl_update.year == last_db_update.year:
                self.delete_ranking(year)
            self.insert_ranking(year)
            print(f"Ranking for {year} updated.")
        else:
            print("No update needed for rankings.")
