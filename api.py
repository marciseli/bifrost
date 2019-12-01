# append the root project path to the pythonpath so that blockchain.py can be accessed by every adapter
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from adapters.btc_adapter import BTCAdapter
from adapters.mc_adapter import MCAdapter
from adapters.eth_adapter import EthAdapter
from adapters.postgres_adapter import PostgresAdapter
from adapters.stellar_adapter import StellarAdapter
from adapters.eos_adapter import EosAdapter
from adapters.iota_adapter import IotaAdapter
#from adapters.hyperledger_adapter import HyperledgerAdapter
from adapters.monero_adapter import MoneroAdapter
from adapters.ltc_adapter import LTCAdapter
from adapters.ripple_adapter import RippleAdapter

from blockchain import Blockchain
import db.database as database
import sys
import os
import string
import random


Adapter = {
    Blockchain.BITCOIN: BTCAdapter,
    Blockchain.MULTICHAIN: MCAdapter,
    Blockchain.ETHEREUM: EthAdapter,
    Blockchain.POSTGRES: PostgresAdapter,
    Blockchain.STELLAR: StellarAdapter,
    Blockchain.EOS: EosAdapter,
    Blockchain.IOTA: IotaAdapter,
    #Blockchain.HYPERLEDGER: HyperledgerAdapter

    Blockchain.MONERO: MoneroAdapter,
    Blockchain.LITECOIN: LTCAdapter,
    Blockchain.RIPPLE: RippleAdapter
}


def store(text, blockchain):
    """Store a text in a specific Blockchain:
        Args:
            Blockchain to use, e.g. Ethereum.
        Returns:
            string: The transaction hash.
    """
    adapter = Adapter[blockchain]
    transaction_hash = adapter.store(text)
    print(transaction_hash)
    return transaction_hash


def retrieve(transaction_hash):
    """Get the text stored on the Blockchain:
        Args:
            Transaction hash
        Returns:
            string: The text belonging to the transactiont.
    """
    blockchain = database.find_blockchain(transaction_hash)
    adapter = Adapter[blockchain]
    text = adapter.retrieve(transaction_hash)
    print(text)
    return text


def migrate(transaction_hash, blockchain):
    """Copy a value from a transaction to another Blockchain:
        Args:
            Transaction hash
        Returns:
            string: The transaction hash from the new transaction.
    """
    value = retrieve(transaction_hash)
    new_hash = store(value, blockchain)
    return new_hash


# print(store("timoishere", Blockchain.STELLAR))


# print(
#     retrieve(
#         "e229c47f66d3ed3b9076e86a37862738a2e5770009654e8a3cc75458924851da"
#     ))
# print(migrate("f12cc0275e47d8040c04d0ea0d26bf8117f25e0628697da338f73e1eb3d39cad;25316099",
#         Blockchain.STELLAR))
