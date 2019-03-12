from web3 import Web3, HTTPProvider
from adapters.adapter import Adapter
from blockchain import Blockchain
import db.database as database


class EthAdapter(Adapter):
    chain = Blockchain.ETHEREUM
    ENDPOINT_URI = 'http://localhost:8545'
    credentials = database.find_credentials(Blockchain.ETHEREUM)
    address = credentials['address']
    key = credentials['key']
    if not Web3.isChecksumAddress(address):
        address = Web3.toChecksumAddress(address)
    web3 = Web3(HTTPProvider(ENDPOINT_URI))
    client = web3.eth

    # ---STORE---
    @classmethod
    def create_transaction(cls, text):
        transaction = {
            'from': cls.address,
            'to': cls.address,
            'gasPrice': cls.client.gasPrice,
            'value': 0,
            'data': bytes(text, 'utf-8'),
            'nonce': cls.get_transaction_count()
        }
        transaction['gas'] = cls.estimate_gas(transaction)
        return transaction

    @classmethod
    def get_transaction_count(cls):
        return cls.client.getTransactionCount(cls.address)

    @classmethod
    def estimate_gas(cls, transaction):
        return cls.client.estimateGas(transaction)

    @classmethod
    def sign_transaction(cls, transaction):
        signed = cls.client.account.signTransaction(transaction, cls.key)
        return signed.rawTransaction

    @classmethod
    def send_raw_transaction(cls, transaction):
        transaction_hash = cls.client.sendRawTransaction(transaction)
        return transaction_hash.hex()

    @staticmethod
    def add_transaction_to_database(transaction_hash):
        database.add_transaction(transaction_hash, Blockchain.ETHEREUM)

    # ---RETRIEVE---
    @classmethod
    def get_transaction(cls, transaction_hash):
        return cls.client.getTransaction(transaction_hash)

    @staticmethod
    def extract_data(transaction):
        # print(transaction)
        # Note that 'input' might be replaced with 'data' in a future release,
        # see here for more detailed information:
        # https://github.com/ethereum/web3.py/issues/901
        return transaction.input

    @staticmethod
    def to_text(data):
        return Web3.toText(data)
