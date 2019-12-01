from web3 import Web3, HTTPProvider
from adapters.adapter import Adapter
from blockchain import Blockchain
from decimal import Decimal
from monero.wallet import Wallet
from monero.address import Address
from monero.seed import Seed
from monero.numbers import PaymentID
from monero.backends.jsonrpc import JSONRPCWallet
from monero.daemon import Daemon
from monero.backends.jsonrpc import JSONRPCDaemon
import db.database as database


class MoneroAdapter(Adapter):
    chain = Blockchain.MONERO
    credentials = database.find_credentials(Blockchain.MONERO)
    wallet = Wallet(JSONRPCWallet(protocol='http', host='127.0.0.1', port=28088))
    # wallet = Wallet(JSONRPCWallet(protocol=’http’, host=’127.0.0.1’, port=18088, path=’/json_rpc’, user=”,password=”, timeout=30, verify_ssl_certs=True))
    daemon = Daemon(JSONRPCDaemon(port=28081))
    address = credentials['address']
    key = credentials['key']


    # ---STORE---
    @classmethod
    def create_transaction(cls, text):
        p1 = PaymentID(cls.to_hex(text))
        if p1.is_short():
            sender = cls.wallet.addresses()[0]
            sender = sender.with_payment_id(p1)
            transaction = cls.wallet.transfer(sender, Decimal('0.000000000001'))
            return transaction

    @classmethod
    def get_transaction_count(cls):
        return len(w.outgoing())

    @staticmethod
    def to_hex(text):
        s = text.encode('utf-8')
        return s.hex()


    @classmethod
    def send_raw_transaction(cls, transaction):
        transaction_hash = daemon.send_transaction(transaction)
        return transaction_hash

    @classmethod
    def sign_transaction(cls, transaction):
        return transaction

    @staticmethod
    def add_transaction_to_database(transaction_hash):
        database.add_transaction(transaction_hash, Blockchain.MONERO)





    # ---RETRIEVE---
    @classmethod
    def get_transaction(cls, transaction_hash):
        for item in cls.wallet.outgoing():
            if transaction_hash in str(item):
                return item

