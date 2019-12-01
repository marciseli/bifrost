from blockchain import Blockchain
from binascii import hexlify, unhexlify
import db.database as database
from db.config import ENCODING
import json
from adapters.adapter import Adapter
from ripple_api import RippleRPCClient

class RippleAdapter(Adapter):
    chain = Blockchain.RIPPLE
    credentials = database.find_credentials(Blockchain.RIPPLE)
    address = credentials['address']
    key = credentials['key']
    #Test
    rpc = RippleRPCClient('https://s.altnet.rippletest.net:51234/')
    #Prod with Fully History
    #rpc = RippleRPCClient('https://s2.ripple.com:51234/')

    # ---Store---
    @staticmethod
    def create_transaction(cls, text):
        memoData = cls.to_hex(text)
        query = {
            "TransactionType": "Payment",
            "Account": cls.address,
            "Destination": cls.address,
            "Amount": 0,
            "LastLedgerSequence": None,
            "Fee": 12,
            "Memos": [
                {
                    "Memo": {
                        "MemoType": "42696672c3b67374",
                        "MemoData": memoData
                    }
                }
            ]
        }
        return query

    @staticmethod
    def sign_transaction(cls, transaction):
        tx_object = cls.rpc._call('sign', transaction)
        return tx_object

    @classmethod
    def send_raw_transaction(cls, transaction):
        tx = transaction['results']['tx_blob']
        tx_hash = cls.rpc.submit(tx_blob=tx)
        return tx_hash

    @staticmethod
    def add_transaction_to_database(transaction_hash):
        database.add_transaction(transaction_hash, Blockchain.RIPPLE)

    @staticmethod
    def to_hex(text):
        data = bytes(json.dumps(text), ENCODING)
        data_hex = hexlify(data)
        return data_hex.decode(ENCODING)

    # ---Retrieve---

    @classmethod
    def get_transaction(cls, transaction_hash):
        tx = cls.rpc._call('tx',{"transaction": transaction_hash,"binary": False})

    @staticmethod
    def extract_data(transaction):
        # Not required in case of DB
        return transaction

    @staticmethod
    def to_text(data_hex):
        data = unhexlify(data_hex)
        return data.decode(ENCODING)
