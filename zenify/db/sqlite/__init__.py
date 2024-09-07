from zenify.db import DB
import sqlite3


class SqliteDB(DB):
    # Path to DB file
    __path = None

    # Class attribute for DB connection
    __connections = []

    def __init__(self, db_path: str | None = None):
        super().__init__()
        SqliteDB.__path = db_path

        if len(SqliteDB.__connections) < 1:
            self.__connections.append(sqlite3.connect(db_path))

        # print("Class instantiated", SqliteDB.__connections,
        #       len(SqliteDB.__connections))

    def create(self):
        pass

    def retrieve(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def execute(self):
        pass

    def get_conn(self):
        return self.__connections[0]
