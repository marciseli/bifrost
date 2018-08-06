from web3 import Web3, HTTPProvider
from adapters.adapter import Adapter
from config import AMOUNT, ENCODING
from blockchain import Blockchain
import database

ENDPOINT_URI = 'http://localhost:8545'


class EthAdapter(Adapter):

    credentials = database.find_credentials(Blockchain.ETHEREUM)
    address = credentials['address']
    if not Web3.isChecksumAddress(address):
        address = Web3.toChecksumAddress(address)
    key = credentials['key']
    web3 = Web3(HTTPProvider(ENDPOINT_URI))
    client = web3.eth

    @classmethod
    def get_transaction(cls, transaction_hash):
        return cls.client.getTransaction(transaction_hash)

    @staticmethod
    def extract_data(transaction):
        # Note that 'input' might be replaced with 'data' in a future release,
        # see here for more detailed information:
        # https://github.com/ethereum/web3.py/issues/901
        return transaction.input

    @staticmethod
    def to_text(data):
        return Web3.toText(data)

    @classmethod
    def create_transaction(cls, text):
        transaction = {
            'from': cls.address,
            'to': cls.address,
            'gasPrice': cls.client.gasPrice,
            'value': AMOUNT,
            'data': bytes(text, ENCODING),
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
