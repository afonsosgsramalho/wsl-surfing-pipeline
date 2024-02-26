import sys
project_root = '/home/vboxuser/programming/python_projects/wsl_pipeline'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

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
