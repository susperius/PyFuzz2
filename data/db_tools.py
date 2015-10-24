__author__ = 'susperius'


import sqlite3 as sql


class DBTools:
    def __init__(self, path_to_db):
        self._db_conn = sql.connect(path_to_db)
        self._cursor = self._db_conn.cursor()

    def clear_tables(self):
        self._cursor.execute("DELETE FROM crashes")
        self._cursor.execute("DELETE FROM nodes")
        self._db_conn.commit()

    def close(self):
        self._cursor.close()
        self._db_conn.close()

if __name__ == "__main__":
    db_tools = DBTools("server.db")
    db_tools.clear_tables()
    db_tools.close()
