from adapters.adapter import Adapter
from blockchain import Blockchain
import db.database as database
from iota import Iota, Address, ProposedTransaction, TryteString, Bundle, Tag, TransactionHash


class IotaAdapter(Adapter):
    chain = Blockchain.IOTA
    client = Iota('https://nodes.devnet.thetangle.org:443', testnet=True)
    credentials = database.find_credentials(Blockchain.IOTA)
    address = credentials['address']
    # There needs to be no key because zero-value transfers do not have a sender
    # https://iota.stackexchange.com/questions/1266/can-one-send-a-zero-value-transaction-from-any-address-to-any-address
    key = credentials['key']

    # ---Store---
    @classmethod
    def create_transaction(cls, text):
        tx = [
            ProposedTransaction(
                # Recipient
                address=Address(cls.address
                                ),
                value=0,
                tag=Tag(b'TAG'),
                message=TryteString.from_string(text),
            ),
        ]
        return tx

    @staticmethod
    def sign_transaction(tx):
        # tx will be signed and sent in send_raw_transaction
        return tx

    @classmethod
    def send_raw_transaction(cls, tx):
        # "https://pyota.readthedocs.io/en/latest/api.html#send-transfer"
        bundle = cls.client.send_transfer(
            depth=4,
            transfers=tx
        )
        bundle = bundle["bundle"]
        bundle = Bundle.as_json_compatible(bundle)
        bundle = bundle[0]
        tx_hash = bundle["hash_"]
        tx_hash = str(tx_hash)
        return tx_hash

    @staticmethod
    def add_transaction_to_database(transaction_hash):
        database.add_transaction(transaction_hash, Blockchain.IOTA)

    # ---Retrieve---
    @classmethod
    def get_transaction(cls, transaction_hash):
        bundle = cls.client.get_bundles(transaction_hash)
        return bundle["bundles"][0]

    @staticmethod
    def extract_data(bundle):
        json = Bundle.as_json_compatible(bundle)
        data = json[0]["signature_message_fragment"]
        return data

    @staticmethod
    def to_text(data):
        data = TryteString.decode(data)
        return str(data)
