import sqlite3 as sql


class Database(object):

    def __init__(self, database='database.db'):
        self.database = database
        self.connected = None
        self.connect()
        self.create_users_table()

    def connect(self):
        self.connection = None
        try:
            self.connection = sql.connect(self.database)
            self.connected = True
            self.cursor = self.connection.cursor()
            print('Connection success')

        except sql.Error as e:
            self.connected = False
            print(f'the error {e} occurred')

    def disconnect(self):
        self.connection.commit()
        self.connection.close()
        self.connected = False
        print('dc')

    def create_users_table(self):
        create_users_table_query = """ 
        CREATE TABLE IF NOT EXISTS users (
        user TEXT,
        hash TEXT,
        mail TEXT
        );
        """

        try:
            self.cursor.execute(create_users_table_query)
            self.connection.commit()
            print('query executed users create')
        except sql.Error as e:
            print(f'error {e} occurred')

    def add_hash(self, user, hash):
        add_hash_query = """
        INSERT INTO 
        users (user, hash)
        VALUES 
        (?, ?); 
        """

        try:
            self.cursor.execute(add_hash_query, (user, hash))
            self.connection.commit()
            print('hash added')
        except sql.Error as e:
            print(f'error {e} occurred')

    def get_hash(self, user):
        get_hash_query = f"""
        SELECT hash
        FROM users
        WHERE user = '{user}'
        """

        results = None
        try:
            self.cursor.execute(get_hash_query)
            results = self.cursor.fetchall()
            self.connection.commit()
            print('got hashs')
            return results
        except sql.Error as e:
            print(f'error {e} occurred')

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print('query executed')
        except sql.Error as e:
            print(f'error {e} occurred')

    def execute_read_query(self, query):
        result = None
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall() # returns a list of query results
            self.connection.commit()
            return result
        except sql.Error as e:
            print(f'error {e} occurred')