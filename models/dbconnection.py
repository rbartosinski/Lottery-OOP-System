from mysql.connector import connect

class DBconnection:

    def __init__(self, user, password, database, host="127.0.0.1"):
        self.cnx = connect(user=user, password=password,
                      host=host, database=database)
        self.cursor = self.cnx.cursor()

