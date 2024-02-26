import sys
project_root = '/home/vboxuser/programming/python_projects/wsl_pipeline'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from wslpipe.utils.db import DB
from dags.config_db import *

import streamlit as st
import pandas.io.sql as sqlio


def rankings_to_df(connection):
    df = sqlio.read_sql_query("SELECT ranking, athlete, event, score, year FROM rankings", connection)
    
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

    rankings_df = rankings_to_df(connection)

    st.title('Rankings page')
    st.table(rankings_df)
    st.sidebar.success("You are currently viewing Rankings page")