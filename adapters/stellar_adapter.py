from adapters.adapter import Adapter
from blockchain import Blockchain
import db.database as database
from stellar_base.builder import Builder
from stellar_base.horizon import horizon_testnet, horizon_livenet


class StellarAdapter(Adapter):
    chain = Blockchain.STELLAR
    credentials = database.find_credentials(Blockchain.STELLAR)
    address = credentials['address']
    key = credentials['key']

    # ---Store---
    @classmethod
    def create_transaction(cls, text):
        builder = Builder(secret=cls.key)
        # use this to use local node e.g with docker instead of public node
        # builder = Builder(secret=cls.key, horizon_uri="http://localhost:8000/")
        builder.append_payment_op(cls.address, '100', 'XLM')
        builder.add_text_memo(text)  # string length <= 28 bytes
        return builder

    @staticmethod
    def sign_transaction(tx_builder):
        tx_builder.sign()
        return tx_builder

    @staticmethod
    def send_raw_transaction(tx_builder):
        # Uses an internal horizon instance to submit over the network
        hash = tx_builder.submit().get('hash')
        return hash

    @staticmethod
    def add_transaction_to_database(transaction_hash):
        database.add_transaction(transaction_hash, Blockchain.STELLAR)

    # ---Retrieve---
    @classmethod
    def get_transaction(cls, transaction_hash):
        # horizon = horizon_livenet() for LIVENET
        horizon = horizon_testnet()
        return horizon.transaction(transaction_hash)

    @staticmethod
    def extract_data(transaction):
        return transaction.get('memo')

    @staticmethod
    def to_text(data):
        return str(data)
