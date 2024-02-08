import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup


class Wsl:
    def __init__(self):
        self.base_url = 'https://www.worldsurfleague.com'

    def fetch_page(self, page):
        response = requests.get(self.base_url + page)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception('Failed to fetch the page')

    def get_athletes(self, html):
        soup = BeautifulSoup(html, 'html.parser')

    def get_competitions(self, html):
        soup = BeautifulSoup(html, 'html.parser')

    def get_ranking(self, year):
        url = f'https://www.worldsurfleague.com/athletes/tour/mct?year={year}'
        df = pd.read_html(url)[0]

        number_columns = len(df.columns)
        df.columns = ['Ranking'] + ['erase1'] + ['erase2'] + \
            ['Athlete'] + [str(i) for i in range(1, number_columns - 5 + 1)] + ['erase3']

        df = df.drop(columns=['erase1', 'erase2', 'erase3'], axis=1)

        df_melted = df.melt(id_vars=['Ranking', 'Athlete'],
                            var_name='Number', value_name='Score')

        return df_melted

    def get_last_update_ranking(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        month, day, year = ' '.join(str(soup.find('div', {'class': 'athletes-tour-intro__notes'}).find_all_next('p')[0])
                                    .replace('<p>', '').replace('</p>', '').replace(',', '').split()[3:]).split()

        date_string = f'{day}/{month}/{year}'
        date_object = datetime.strptime(date_string, "%d/%B/%Y").date()

        return date_object
    

wsl = Wsl()
html = wsl.fetch_page('/athletes/tour/mct?year=2023')
print(wsl.get_last_update_ranking(html))
