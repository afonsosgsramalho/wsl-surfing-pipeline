<<<<<<< HEAD
FROM apache/airflow:slim-2.8.3-python3.11
=======
FROM apache/airflow:slim-latest-python3.11
>>>>>>> 04c558c3548d50ce222b6ab79060a8ba497277c6

COPY requirements.txt /opt/airflow/

USER root
RUN apt-get update && apt-get install -y gcc python3-dev

USER airflow

<<<<<<< HEAD
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt
=======
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt
>>>>>>> 04c558c3548d50ce222b6ab79060a8ba497277c6
