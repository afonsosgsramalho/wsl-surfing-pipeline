import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wslpipe.utils.db import DB
from dags.config_db import *

import streamlit as st
import pandas.io.sql as sqlio


def ahtletes_to_df(connection):
    df = sqlio.read_sql_query("SELECT name, country, stance, age, height, weight, hometown FROM athletes", connection)
    
    return df


if __name__ == '__main__':
    db_credentials = {
        'dbname': POSTGRES_DB,
        'user': POSTGRES_USER,
        'password': POSTGRES_PASSWORD,
        'host': POSTGRES_HOST,
    }
    db = DB(**db_credentials)
    connection = db.get_connection()

    athlets_df = ahtletes_to_df(connection)

    st.title('Athletes page')
    st.table(athlets_df)
    st.sidebar.success("You are currently viewing Athletes page")
