from utils.db import DB
from configparser import ConfigParser
from wsl import Wsl
from datetime import datetime


# Only use when rebuilding all DBs
def building_historic():
    pass

def _get_current_time():
    return datetime.now().date()

def insert_athlete():
    try:
        wsl = Wsl()
        html2 = wsl.fetch_page('/athletes/3962/barron-mamiya')
        athlete = wsl.get_athlete(html2)
        athlete.append(_get_current_time())

        db = DB('postgres', 'wsl', 'changeme', 'localhost')
        cursor = db.connect_cursor()
        cursor.execute(
            'INSERT INTO athletes(name, country, stance, age, height, weight, hometown, created_at) \
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', athlete)

        db.commit()
        db.close_connection()

    except Exception as e:
        print(f"An error occurred: {e}")

        return None


if __name__ == '__main__':
    print(insert_athlete())

