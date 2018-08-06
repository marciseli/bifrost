from binascii import hexlify
from bitcoinrpc.authproxy import AuthServiceProxy
from adapters.mc_btc_adapter import MCBTCAdapter
from config import ENCODING
from blockchain import Blockchain
import database


class BTCAdapter(MCBTCAdapter):

    credentials = database.find_credentials(Blockchain.BITCOIN)
    address = credentials['address']
    key = credentials['key']
    rpcuser = credentials['user']
    rpcpassword = credentials['password']
    endpoint_uri = 'http://%s:%s@127.0.0.1:18332' % (rpcuser, rpcpassword)
    client = AuthServiceProxy(endpoint_uri)

    @classmethod
    def get_transaction(cls, transaction_hash):
        transaction_hex = cls.client.getrawtransaction(transaction_hash)
        return cls.client.decoderawtransaction(transaction_hex)

    @classmethod
    def extract_data(cls, transaction):
        output = cls.extract_output(transaction, output_index=1)
        asm = output['scriptPubKey']['asm']
        _, data = asm.split()
        return data

    @staticmethod
    def get_latest_transaction_from_database():
        return database.find_latest_transaction(Blockchain.BITCOIN)

    @staticmethod
    def to_hex(text):
        data = bytes(text, ENCODING)
        data_hex = hexlify(data)
        return data_hex.decode(ENCODING)

    @classmethod
    def create_transaction_output(cls, data_hex, input_transaction_hash):
        change = cls.get_change(input_transaction_hash)
        return {cls.address: change, 'data': data_hex}

    @classmethod
    def get_change(cls, transaction_hash):
        balance = cls.extract_balance(transaction_hash)
        relay_fee = cls.get_relay_fee()
        return balance - relay_fee

    @classmethod
    def extract_balance(cls, transaction_hash):
        transaction = cls.get_transaction(transaction_hash)
        output = cls.extract_output(transaction, output_index=0)
        return output['value']

    @classmethod
    def get_relay_fee(cls):
        network_info = cls.client.getnetworkinfo()
        return network_info['relayfee']

    @classmethod
    def create_raw_transaction(cls, inputs, output, data_hex):
        transaction_hex = cls.client.createrawtransaction(inputs, output)
        return transaction_hex

    @staticmethod
    def add_transaction_to_database(transaction_hash):
        database.add_transaction(transaction_hash, Blockchain.BITCOIN)
