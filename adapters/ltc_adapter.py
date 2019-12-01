from binascii import hexlify, unhexlify
from bitcoinrpc.authproxy import AuthServiceProxy
from db.config import ENCODING
from blockchain import Blockchain
from adapters.adapter import Adapter
import db.database as database
import collections


class LTCAdapter(Adapter):
    chain = Blockchain.BITCOIN
    credentials = database.find_credentials(Blockchain.LITECOIN)
    address = credentials['address']
    key = credentials['key']
    rpcuser = credentials['user']
    rpcpassword = credentials['password']
    endpoint_uri = f"http://{rpcuser}:{rpcpassword}@localhost:18332/"
    client = AuthServiceProxy(endpoint_uri)

    # ---Store---
    @classmethod
    def create_transaction(cls, text):
        input_transaction_hash = database.find_latest_transaction(Blockchain.LITECOIN)
        inputs = [{'txid': input_transaction_hash, 'vout': 0}]
        data_hex = cls.to_hex(text)
        output = cls.create_transaction_output(data_hex, input_transaction_hash)
        # Necessary so that the address is the first output of the TX
        output = collections.OrderedDict(sorted(output.items()))
        transaction_hex = cls.client.createrawtransaction(inputs, output)
        return transaction_hex

    @classmethod
    def create_transaction_output(cls, data_hex, input_transaction_hash):
        balance = cls.extract_balance(input_transaction_hash)
        relay_fee = cls.client.getnetworkinfo()['relayfee']
        change = balance - relay_fee
        return {cls.address: change, 'data': data_hex}

    @classmethod
    def extract_balance(cls, transaction_hash):
        transaction = cls.get_transaction(transaction_hash)
        output = transaction['vout'][0]['value']
        return output

    @staticmethod
    def to_hex(text):
        data = bytes(text, ENCODING)
        data_hex = hexlify(data)
        return data_hex.decode(ENCODING)

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
        database.add_transaction(transaction_hash, Blockchain.BITCOIN)


    # ---Receive---
    @classmethod
    def get_transaction(cls, transaction_hash):
        transaction_hex = cls.client.getrawtransaction(transaction_hash)
        return cls.client.decoderawtransaction(transaction_hex)

    @classmethod
    def extract_data(cls, transaction):
        output = transaction['vout'][1]
        asm = output['scriptPubKey']['asm']
        _, data = asm.split()
        return data

    @staticmethod
    def to_text(data_hex):
        data = unhexlify(data_hex)
        return data.decode(ENCODING)
