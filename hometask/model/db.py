import sqlite3

from hometask.example_db.settings import DBNAME


class DataWrapper:
    def __init__(self):
        conn = Database.get_database().conn
        self.conn = conn
        self.cursor = conn.cursor()

    def execute(self, sql, params=None, unescape=None):
        sql = sql.format(unescape) if unescape else sql
        try:
            if params:
                return self.cursor.execute(sql, params)
            else:
                return self.cursor.execute(sql)
        finally:
            self.conn.commit()

    def __iter__(self):
        return self

    def __next__(self):
        data = self.cursor.fetchone()
        if data is None:
            raise StopIteration
        return str(data)  # Здесь генерировать объекты нужного типа


class Database:
    db = None

    def __init__(self):
        self.conn = sqlite3.connect(DBNAME)

    @staticmethod
    def get_database():
        if not Database.db:
            Database.db = Database()
        return Database.db

