import sqlite3

from hometask.db.settings import DBNAME


class Database:
    db = None

    def __init__(self):
        self.conn = sqlite3.connect(DBNAME)
        self.cursor = self.conn.cursor()

    @staticmethod
    def get_database():
        if not Database.db:
            Database.db = Database()
        return Database.db

    @staticmethod
    def execute(sql, params=None, unescape=None):
        self = Database.get_database()
        sql = sql.format(unescape) if unescape else sql
        try:
            if params:
                return self.cursor.execute(sql, params)
            else:
                return self.cursor.execute(sql)
        finally:
            self.conn.commit()
