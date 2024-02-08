import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup

first_year = 2010
last_year = datetime.date.today().year

url_rankings = 'https://www.worldsurfleague.com/athletes/tour/mct?year=2023'
page = requests.get(url_rankings)
soup = BeautifulSoup(page.text, 'html.parser')

def get_ranking(year):
    url = f'https://www.worldsurfleague.com/athletes/tour/mct?year={year}'
    df = pd.read_html(url)[0]

    number_columns = len(df.columns)
    df.columns = ['Ranking'] + ['erase1'] + ['erase2'] + \
        ['Athlete'] + [str(i) for i in range(1, number_columns - 5 + 1)] + ['erase3']

    df = df.drop(columns=['erase1', 'erase2', 'erase3'], axis=1)

    df_melted = df.melt(id_vars=['Ranking', 'Athlete'],
                        var_name='Number', value_name='Score')

    return df_melted


def get_last_update():
    month, day, year = ' '.join(str(soup.find('div', {'class': 'athletes-tour-intro__notes'}).find_all_next('p')[0])
                                .replace('<p>', '').replace('</p>', '').replace(',', '').split()[3:]).split()
    

print(get_ranking(2021))
