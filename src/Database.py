from config import POSTGRES_HOST, POSTGRES_DB, POSTGRES_PORT, POSTGRES_PASSWORD, POSTGRES_USER
from database_ddl import APIUSER_DDL
import psycopg2


class Database:
    def __init__(self, logger):
        self.logger = logger

    def get_connection(self, database_name='postgres'):
        self.logger.info(f'[POSTGRES] Openning connection to database {database_name}')
        conn = psycopg2.connect(f"user={POSTGRES_USER} dbname={database_name} password={POSTGRES_PASSWORD} host={POSTGRES_HOST} port={POSTGRES_PORT}")
        conn.autocommit = True
        return conn

    def close_connection(self, connection, database_name='postgres'):
        self.logger.info(f"[POSTGRES] Closing connection to database {database_name}")
        connection.close()

    def check_if_database_exists(self, connection, database_name='fastapi'):
        cursor = connection.cursor()

        self.logger.info(f'[POSTGRES] Checking if database {database_name} exists')
        cursor.execute("SELECT datname FROM pg_database;")
        records = cursor.fetchall()
        return bool([record for record in records if record[0] == database_name])

    def create_database(self, connection, database_name="fastapi"):
        cursor = connection.cursor()

        self.logger.info(f'[POSTGRES] Creating database {database_name}')
        cursor.execute(f"CREATE DATABASE {database_name} ;")
        self.logger.info(f'[POSTGRES] Database {database_name} created')

    def create_database_if_not_exists(self, connection, database_name='fastapi'):
        if not self.check_if_database_exists(connection):
            self.create_database(connection)
        else:
            self.logger.info(f'[POSTGRES] Database {database_name} already exists')

    def create_table_if_not_exists(self, connection, table_name, query):
        cursor = connection.cursor()

        self.logger.info(f'[POSTGRES] Creating table {table_name}')
        cursor.execute(query)
        self.logger.info(f'[POSTGRES] Table {table_name} created')

    def execute_migrates(self):
        postgres_conn = self.get_connection()
        self.create_database_if_not_exists(postgres_conn)
        self.close_connection(postgres_conn)

        fastapidb_conn = self.get_connection('fastapi')
        self.create_table_if_not_exists(fastapidb_conn, 'apiuser', APIUSER_DDL)
        self.close_connection(fastapidb_conn, 'fastapi')


# # psql -U postgres -d postgres -p 5432 -h 127.0.0.1
# if __name__ == '__main__':

