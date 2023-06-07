import sqlite3


class Database:

    def __init__(self, db_name: str):
        self.db_name = db_name

    def __connection_db(self):
        self.__connection = sqlite3.connect(self.db_name)

    def create_table(self, table_name: str, field_data: tuple):
        self.__connection_db()
        cursor = self.__connection.cursor()
        cursor.execute(f'CREATE TABLE if not exists {table_name}(id integer PRIMARY KEY, '
                       f'{", ".join([" ".join([field_name, field_type]) for field_name, field_type in field_data])})')
        self.__connection.commit()
        self.__connection.close()

    def drop_table(self, table_name: str):
        self.__connection_db()
        cursor = self.__connection.cursor()
        cursor.execute(f'DROP table if exists {table_name}')
        self.__connection.commit()
        print('Table drop')
        self.__connection.close()

    def show_tables(self):
        self.__connection_db()
        cursor = self.__connection.cursor()
        cursor.execute('SELECT name from sqlite_master where type= "table"')
        print(cursor.fetchall())
        self.__connection.close()

    def insert_data(self, table_name: str, data: tuple):
        self.__connection_db()
        cursor = self.__connection.cursor()
        cursor.execute(f'INSERT INTO {table_name}("Title", "Data") VALUES(?, ?)', data)
        self.__connection.close()

    def get_all_table_data(self, table_name: str):
        self.__connection_db()
        cursor = self.__connection.cursor()
        cursor.execute(f'SELECT * FROM {table_name}')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
