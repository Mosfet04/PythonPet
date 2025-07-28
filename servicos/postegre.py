from peewee import PostgresqlDatabase
from config import DATABASE

class Postgre:
    _db_instance = None

    @classmethod
    def get_database(cls):
        if cls._db_instance is None:
            if DATABASE['ssl']:
                cls._db_instance = PostgresqlDatabase(
                    DATABASE['name'],
                    user=DATABASE['user'],
                    password=DATABASE['password'],
                    host=DATABASE['host'],
                    port=int(DATABASE['port']),
                    sslmode='require'
                )
            else:
                cls._db_instance = PostgresqlDatabase(
                    DATABASE['name'],
                    user=DATABASE['user'],
                    password=DATABASE['password'],
                    host=DATABASE['host'],
                    port=int(DATABASE['port'])
                )
        return cls._db_instance