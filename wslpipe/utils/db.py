import psycopg2


class DB:
    def __init__(self, user, dbname, password, host):
        self.connection = None
        try:
            self.connection = psycopg2.connect(
                user=user,
                dbname=dbname,
                password=password,
                host=host,
                port='5432'
            )

        except Exception as e:
            print(f"The connection was not established: {e}")

    def get_connection(self):
        if self.connection is not None:
            return self.connection
        else:
            raise Exception("Database connection is not established.")

    def connect_cursor(self):
        try:
            return self.get_connection().cursor()
        except Exception as e:
            print(f"Failed to create a cursor: {e}")
            raise e

    def commit(self):
        if self.connection is not None:
            self.connection.commit()
        else:
            raise Exception("Database connection is not established.")

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None