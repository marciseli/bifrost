import sawtooth_sdk
import cbor
from hashlib import sha512
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
import urllib.request
from urllib.error import HTTPError
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import Batch
from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from adapters.adapter import Adapter
import requests
import json
import base64
import db.database as database
from blockchain import Blockchain
from random import randint


class HyperledgerAdapter(Adapter):
    chain = Blockchain.HYPERLEDGER
    context = create_context('secp256k1')
    credentials = database.find_credentials(Blockchain.HYPERLEDGER)
    # address = credentials['address']
    key = credentials['key']
    signer = CryptoFactory(context).new_signer(
        context.new_random_private_key().from_hex(key))
    # ---Store---

    @classmethod
    def create_transaction(cls, text):
        # encode the payload
        # Value needs to be random, because else it would be the exact same tx and same hash every time
        payload = {'Verb': 'set', 'Name': text, 'Value': randint(0, 999999999)}
        payload_bytes = cbor.dumps(payload)

        # create the transaction header:
        txn_header_bytes = TransactionHeader(
            family_name='intkey',
            family_version='1.0',
            inputs=[''],
            outputs=[''],
            signer_public_key=cls.signer.get_public_key().as_hex(),
            batcher_public_key=cls.signer.get_public_key().as_hex(),
            # More infos about dependencies here:
            # https://sawtooth.hyperledger.org/docs/core/releases/1.0/architecture/transactions_and_batches.html#dependencies-and-input-output-addresses
            dependencies=[],
            payload_sha512=sha512(payload_bytes).
            hexdigest()).SerializeToString()

        return {
            'txn_header_bytes': txn_header_bytes,
            'payload_bytes': payload_bytes,
        }

    @classmethod
    def sign_transaction(cls, tx_dict):
        signature = cls.signer.sign(tx_dict.get('txn_header_bytes'))
        txn = Transaction(
            header=tx_dict.get('txn_header_bytes'),
            header_signature=signature,
            payload=tx_dict.get('payload_bytes'))
        return txn

    @classmethod
    def send_raw_transaction(cls, txn):
        # create batch header
        txns = [txn]
        batch_header_bytes = BatchHeader(
            signer_public_key=cls.signer.get_public_key().as_hex(),
            transaction_ids=[txn.header_signature for txn in txns],
        ).SerializeToString()
        # create the batch
        # !!!Change here to header_signature
        header_signature = cls.signer.sign(batch_header_bytes)
        batch = Batch(
            header=batch_header_bytes,
            header_signature=header_signature,
            transactions=txns)
        # encode the batch in a batchlist
        batch_list_bytes = BatchList(batches=[batch]).SerializeToString()

        # Submitting Batches to the Validator
        try:
            r = requests.post(
                'http://localhost:8008/batches',
                batch_list_bytes,
                headers={'Content-Type': 'application/octet-stream'})
            # response is not needed, because the tx hash is created locally
            response = json.loads(r.text)
            return [txn.header_signature for txn in txns][0]

        except HTTPError as e:
            response = e.file

    @staticmethod
    def add_transaction_to_database(transaction_hash):
        database.add_transaction(transaction_hash, Blockchain.HYPERLEDGER)
        return ""


# ---Retrieve---


    @classmethod
    def get_transaction(cls, transaction_id):
        r = requests.get(
            f"http://localhost:8008/transactions/{transaction_id}")
        result = json.loads(r.text)
        return result

    @staticmethod
    def extract_data(transaction):
        return transaction["data"]["payload"]

    @staticmethod
    def to_text(data):
        txt_cbor = base64.b64decode(data)
        txt_dict = cbor.loads(txt_cbor)
        return str(txt_dict.get('Name'))
