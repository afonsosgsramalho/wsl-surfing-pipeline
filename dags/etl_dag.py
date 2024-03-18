import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    
from wslpipe.etl import WSLDataManager
from wslpipe.wsl import Wsl
from config_db import *

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


def my_etl():
    try:
        db_credentials = {
            'dbname': POSTGRES_DB,
            'user': POSTGRES_USER,
            'password': POSTGRES_PASSWORD,
            'host': POSTGRES_HOST,
        }

        wsl_instance = Wsl()
        data_manager = WSLDataManager(db_credentials, wsl_instance)

        current_year = datetime.now().year
        data_manager.update_rankings_if_needed(current_year)
        data_manager.build_historic_athletes()
    
    except Exception as e:
        print("An error occurred:", e)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    "wsl_etl",
    default_args=default_args,
    description='wsl etl dag',
    schedule='30 11 * * 0',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:
    insert_info = PythonOperator(
        task_id='insert_info',
        python_callable=my_etl,
    )
