import sqlite3


class SingletonDB:
    __db_connection = None

    def __init__(self, path):
        """ Virtually private constructor. """
        if SingletonDB.__db_connection is None:
            SingletonDB.__db_connection = sqlite3.connect(path)
        create_main_table = 'CREATE TABLE IF NOT EXISTS main ( id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT, duration REAL )'
        self.execute_query(create_main_table)

    def execute_query(self, query):
        cursor = SingletonDB.__db_connection.cursor()
        try:
            cursor.execute(query)
            SingletonDB.__db_connection.commit()
        except Exception as e:
            print(f'The error "{e}" occurred @1')

    def execute_read_query(self, query):
        cursor = SingletonDB.__db_connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"The error '{e}' occurred @2")

    def execute_write_query(self, file_name, duration):
        query_string = f'INSERT INTO main ( filename, duration ) VALUES ( "{file_name}", {duration} )'
        self.execute_query(query_string)

    def get_duration(self, ids):
        query_string = 'SELECT duration FROM main WHERE id = {}'
        result = [
            self.execute_read_query(query_string.format(i + 1))[0][0]
            for i in ids
        ]
        return sum(result)
