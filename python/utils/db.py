import psycopg2

class Connection:
    def __init__(self, user, dbname, password, host):
        self.user = user
        self.dbname = dbname
        self.password = password
        self.host = host
        self.cursor = None


    def connect_cursor(self):
        try:
            connection = psycopg2.connect(
                user=self.user,
                dbname=self.dbname,
                password=self.password,
                host=self.host
            )
            self.cursor = connection.cursor()

        except Exception as e:
            print(f"The connection was not established: {e}")
        

    def close_connection(self):
        return self.cursor.close()


