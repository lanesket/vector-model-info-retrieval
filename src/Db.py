import sqlite3


class Db:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
