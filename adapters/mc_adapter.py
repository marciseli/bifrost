from binascii import hexlify
from mcrpc import RpcClient
from adapters.mc_btc_adapter import MCBTCAdapter
from config import AMOUNT, ENCODING
from blockchain import Blockchain
import database

HOST = 'localhost'
PORT = '7324'


class MCAdapter(MCBTCAdapter):

    credentials = database.find_credentials(Blockchain.MULTICHAIN)
    address = credentials['address']
    key = credentials['key']
    rpcuser = credentials['user']
    rpcpassword = credentials['password']
    client = RpcClient(HOST, PORT, rpcuser, rpcpassword)

    @classmethod
    def get_transaction(cls, transaction_hash):
        return cls.client.getrawtransaction(transaction_hash, verbose=1)

    @classmethod
    def extract_data(cls, transaction):
        # workaround needed because potentially multiple output addresses in
        # single transaction (and also potentially multiple data items)
        output = cls.extract_output(transaction, output_index=1)
        return output['data'][0]

    @staticmethod
    def get_latest_transaction_from_database():
        return database.find_latest_transaction(Blockchain.MULTICHAIN)

    @staticmethod
    def to_hex(text):
        data = bytes(text, ENCODING)
        return hexlify(data)

    @classmethod
    def create_transaction_output(cls, data_hex, input_transaction_hash):
        return {cls.address: AMOUNT}

    @classmethod
    def create_raw_transaction(cls, inputs, output, data_hex):
        transaction_hex = cls.client.createrawtransaction(
            inputs,
            output,
            [data_hex]
        )
        return transaction_hex

    @staticmethod
    def add_transaction_to_database(transaction_hash):
        database.add_transaction(transaction_hash, Blockchain.MULTICHAIN)
