import psycopg2
from cvs_read import read_csv


class Database:

    def __init__(self,
                 db_name: str,
                 user: str,
                 password: str,
                 host: str,
                 port: str):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def __connection_db(self):
        return psycopg2.connect(database=self.db_name, user=self.user,
                                password=self.password, host=self.host, port=self.port)

    def create_table(self):
        conn = self.__connection_db()
        cur = conn.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS documents (id serial \
            PRIMARY KEY, rubrics varchar(100), text text, created_date timestamp);''')
        conn.commit()
        cur.close()
        conn.close()

    def insert_data(self):
        conn = self.__connection_db()
        cur = conn.cursor()
        file = read_csv('posts.cvs')
        for row in file:
            row[0] = row[0].replace("\'", '\"')
            row[1] = row[1].replace("\'", '\"')
            row[2] = row[2].replace("\'", '\"')
            cur.execute(
                f"INSERT INTO documents (rubrics, text, created_date) VALUES ('{row[2]}', '{row[0]}', '{row[1]}');")
        conn.commit()
        cur.close()
        conn.close()

    def get_all_table_data(self):
        conn = self.__connection_db()
        cur = conn.cursor()
        cur.execute('''SELECT * FROM documents''')
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    def get_dock_by_id(self, id_doc):
        conn = self.__connection_db()
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM documents WHERE id={id_doc}')
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data

    def delete_by_id(self, id_doc):
        conn = self.__connection_db()
        cur = conn.cursor()
        cur.execute(f'DELETE FROM documents WHERE id={id_doc}')
        conn.commit()
        cur.close()
        conn.close()
