import sqlite3
import logging
logging.basicConfig(level=logging.INFO)

class DataBase:
    def __init__(self, name):

        self.db = sqlite3.connect(f"{name}")
        sql = self.db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS AATree (key integer, data TEXT)""")
        self.db.commit()
        sql.close()

    def get_from_db(self):
        sql = self.db.cursor()
        data = [value for value in sql.execute(f"SELECT * FROM AATree")]
        if not data:
            logging.log(logging.INFO, ' база данных пуста')
        sql.close()
        return data

    def del_all(self):
        cur = self.db.cursor()
        cur.execute("DELETE from AATree")
        self.db.commit()

    def db_insert(self, val):
        cur = self.db.cursor()
        cur.execute("INSERT INTO AATree VALUES (?)", (val))
        self.db.commit()
        cur.close()

    def save_all(self, path):
        self.del_all()
        for val in path:
            if val[1] is not None:
                self.db_insert(val[0], val[1])
