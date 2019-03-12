from adapters.adapter import Adapter
from binascii import hexlify, unhexlify
from mcrpc import RpcClient
from db.config import AMOUNT, ENCODING
from blockchain import Blockchain
import db.database as database
import collections


HOST = 'localhost'
PORT = '8000'


class MCAdapter(Adapter):
    chain = Blockchain.MULTICHAIN
    credentials = database.find_credentials(Blockchain.MULTICHAIN)
    address = credentials['address']
    key = credentials['key']
    rpcuser = credentials['user']
    rpcpassword = credentials['password']
    client = RpcClient(HOST, PORT, rpcuser, rpcpassword)

    # ---Store---

    @classmethod
    def create_transaction(cls, text):
        input_transaction_hash = database.find_latest_transaction(
            Blockchain.MULTICHAIN)
        inputs = [{'txid': input_transaction_hash, 'vout': 0}]
        data_hex = cls.to_hex(text)
        output = {cls.address: AMOUNT}
        # Necessary so that the address is the first output of the TX
        output = collections.OrderedDict(sorted(output.items()))
        transaction_hex = cls.client.createrawtransaction(
            inputs,
            output,
            [data_hex]
        )
        return transaction_hex

    @staticmethod
    def to_hex(text):
        data = bytes(text, ENCODING)
        return hexlify(data)

    @classmethod
    def sign_transaction(cls, transaction_hex):
        parent_outputs = []
        signed = cls.client.signrawtransaction(
            transaction_hex,
            parent_outputs,
            [cls.key]
        )
        assert signed['complete']
        return signed['hex']

    @classmethod
    def send_raw_transaction(cls, transaction_hex):
        transaction_hash = cls.client.sendrawtransaction(transaction_hex)
        return transaction_hash

    @staticmethod
    def add_transaction_to_database(transaction_hash):
        database.add_transaction(transaction_hash, Blockchain.MULTICHAIN)

    # ---Retrieve---
    @classmethod
    def get_transaction(cls, transaction_hash):
        return cls.client.getrawtransaction(transaction_hash, verbose=1)

    @classmethod
    def extract_data(cls, transaction):
        # workaround needed because potentially multiple output addresses in single tx        
        output = transaction['vout'][1]
        # for version 2.0+ use
        # return output['data'][0]
        return output['scriptPubKey']['hex']

    @staticmethod
    def to_text(data_hex):
        data = unhexlify(data_hex)
        # for version 2.0+ use
        # return data.decode(ENCODING)
        return data.decode(ENCODING)[2:]
