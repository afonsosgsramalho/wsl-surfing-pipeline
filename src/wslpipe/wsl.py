import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup

first_year = 2010
last_year = datetime.date.today().year

url_rankings = 'https://www.worldsurfleague.com/athletes/tour/mct?year=2023'
page = requests.get(url_rankings)
soup = BeautifulSoup(page.text, 'html.parser')

def get_rows():
    rows = []

    for child in soup.find('table').children:
        row = []
        for td in child:
            try:
                row.append(td.text.replace('\n', ''))
            except:
                continue
        if len(row) > 0:
            rows.append(row)
    
    return rows[1:]


month, day, year = ' '.join(str(soup.find('div', {'class': 'athletes-tour-intro__notes'}).find_all_next('p')[0])
                            .replace('<p>', '').replace('</p>', '').replace(',', '').split()[3:]).split()

print(month)
