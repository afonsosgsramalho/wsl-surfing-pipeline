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
 
    def get_athlete(self, html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            name = soup.find('div', {'class': 'avatar-text-primary'}).text
            country = soup.find('div', {'class': 'country-name'}).text
            bio = soup.find('div', {'class': 'new-athlete-bio-stats'})
            value = bio.find_all('div', {'class': 'value'})

            values = []

            for v in value:
                values.append(v.text.strip())

            _, _, age, height, weight, hometown = values

            return [name, country, int(age[:2]), height[-6:], weight[-5:], hometown]
        
        except:
            return f'Athlete {name} could not be processed'
        
    def get_competition(self, html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            event = soup.find('h1', {'class': 'event-information__title'}).text
            data_range = soup.find('span', {'class': 'event-information__meta-item event-information__meta-item--date-range'}).text
            start_date = data_range.split('-')[0] + data_range[-4:].strip()
            start_date_object = datetime.strptime(
                start_date, '%b %d %Y').date()
            end_date = data_range.split('-')[1].replace(',', '').strip()
            end_date_object = datetime.strptime(
                end_date, '%b %d %Y').date()
            state = soup.find('span', {'class': 'status-module__status'}).text

            return [event, start_date_object, end_date_object, state]

        except:
            return f'Event {event} could not be processed'

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
# html = wsl.fetch_page('/athletes/tour/mct?year=2023')
# print(wsl.get_last_update_ranking(html))
# html2 = wsl.fetch_page('/athletes/10192/lucas-vicente')
html3 = wsl.fetch_page('/events/2024/ct/196/lexus-pipe-pro/main')
print(wsl.get_competition(html3))

