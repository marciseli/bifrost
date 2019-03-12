import psycopg2
from blockchain import Blockchain
import db.database as database
from adapters.adapter import Adapter


class PostgresAdapter(Adapter):
    chain = Blockchain.POSTGRES
    credentials = database.find_credentials(Blockchain.POSTGRES)
    address = "not necessary for psql"
    key = "not necessary for psql"

    # ---Store---
    @staticmethod
    def create_transaction(text):
        query = f'''INSERT INTO test (id, value) VALUES (DEFAULT, '{text}') RETURNING id'''
        return query

    @staticmethod
    def sign_transaction(transaction):
        # Not required in case of DB
        return transaction

    @classmethod
    def send_raw_transaction(cls, transaction):
        cls.connect()
        try:
            cls.cursor.execute(transaction)
            cls.connection.commit()
            return cls.cursor.fetchone()[0]

        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error while sending transaction: {error}")

    @staticmethod
    def add_transaction_to_database(transaction_hash):
        database.add_transaction(transaction_hash, Blockchain.POSTGRES)

    @classmethod
    def connect(cls):
        try:
            # connect and print version or error
            cls.connection = psycopg2.connect(
                user=cls.credentials['user'],
                password=cls.credentials['password'],
                host="localhost",
                port=cls.credentials['key'],
                database=cls.credentials['address'])
            cls.cursor = cls.connection.cursor()
            cls.cursor.execute("SELECT version();")
            version = cls.cursor.fetchone()
            # print(f"Connected to {version}")
            # create table if not exists
            cls.cursor.execute(
                '''CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, value text)'''
            )
            cls.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL", error)

    # ---Retrieve---

    @classmethod
    def get_transaction(cls, transaction_hash):
        cls.connect()
        try:
            query = f"select value from test WHERE id = {transaction_hash}"
            cls.cursor.execute(query)
            return cls.cursor.fetchone()[0]

        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error while sending transaction: {error}")

        # finally:
        #     if (cls.connection):
        #         cls.cursor.close()
        #         cls.connection.close()
        #         print("PostgreSQL connection was closed")

    @staticmethod
    def extract_data(transaction):
        # Not required in case of DB
        return transaction

    @staticmethod
    def to_text(data):
        return str(data)
