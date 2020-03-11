from Db import Db

class Article:
    SCHEMA_NAME = 'data'
    TABLE_NAME = 'article'

    def __init__(self):
        self.db = Db(self.SCHEMA_NAME)
        self.create_table()

    def create_table(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id INTEGER PRIMARY KEY,
                title TEXT,
                raw_text TEXT NOT NULL,
                processed_text TEXT NOT NULL 
            )
        """

        self.db.cur.execute(query)
        self.db.conn.commit()

    def already_exists(self, title: str):
        query = f"""
            SELECT * FROM {self.TABLE_NAME} WHERE title = ? 
        """

        self.db.cur.execute(query, (title,))

        return None != self.db.cur.fetchone()

    def insert(self, title: str, raw_text: str, processed_text: str):
        if self.already_exists(title):
            return

        query = f"""
            INSERT INTO {self.TABLE_NAME} VALUES (?, ?, ?, ?)
        """

        self.db.cur.execute(query, (None, title, raw_text, processed_text))
        self.db.conn.commit()

    def select_all(self):
        query = f"""
            SELECT * FROM {self.TABLE_NAME} 
        """

        self.db.cur.execute(query)

        return self.db.cur.fetchall()

if __name__ == "__main__":
    a = Article()
    
    a.insert('TITLE 1', "LOL RAW", 'lol raw')
    a.insert('TITLE 2', "XD RAW", 'xd raw')

    print(a.select_all())