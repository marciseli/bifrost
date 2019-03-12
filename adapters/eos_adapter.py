from blockchain import Blockchain
from adapters.adapter import Adapter
from eosjs_python import Eos
import db.database as database
import requests
import json


class EosAdapter(Adapter):
    chain = Blockchain.EOS
    credentials = database.find_credentials(Blockchain.EOS)
    address = credentials['address']
    key = credentials['key']
    user = credentials['user']
    node_url = "http://jungle2.cryptolions.io:80"

    eos = Eos({
        'http_address': node_url,
        'key_provider': key,
    })

    # ---Store---
    @classmethod
    def create_transaction(cls, text):
        tx_data = {
            "from": cls.user,
            "to": "lioninjungle",
            "quantity": "0.0001 EOS",
            "memo": text
        }
        return tx_data

    @staticmethod
    def sign_transaction(tx):
        # will be signed in next step
        return tx

    @classmethod
    def send_raw_transaction(cls, tx_data):
        response = cls.eos.push_transaction(
            'eosio.token', 'transfer', 'jungletimohe', 'active', tx_data
        )
        transaction_hash = f"{response['transaction_id']};{response['processed']['block_num']}"
        return transaction_hash

    @staticmethod
    def add_transaction_to_database(transaction_hash):
        database.add_transaction(transaction_hash, Blockchain.EOS)

    # ---Retrieve---
    @classmethod
    def get_transaction(cls, transaction_hash):
        data = {
            "id": transaction_hash.strip(";").split(";")[0],
            "block_num_hint": int(transaction_hash.strip(";").split(";")[1])
        }
        r = requests.post(
            f'{cls.node_url}/v1/history/get_transaction', json=data)
        response = json.loads(r.text)
        return response

    @staticmethod
    def extract_data(transaction):
        memo = transaction["trx"]["trx"]["actions"][0]["data"]["memo"]
        return memo

    @staticmethod
    def to_text(data):
        return str(data)
