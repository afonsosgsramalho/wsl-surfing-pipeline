from wslpipe.utils.db import DB
from dags.config_db import *

import streamlit as st
import pandas as pd
import pandas.io.sql as sqlio


def ahtletes_to_df():
    db_credentials = {
        'dbname': POSTGRES_DB,
        'user': POSTGRES_USER,
        'password': POSTGRES_PASSWORD,
        'host': POSTGRES_HOST,
    }
    db = DB(**db_credentials)
    connection = db.get_connection()
    df = sqlio.read_sql_query(
        "SELECT name, country, stance, age, height, weight, hometown FROM athletes", connection)
    
    return df


if __name__ == '__main__':
    athlets_df = ahtletes_to_df()

    st.table(athlets_df)
