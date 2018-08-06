from adapters.eth_adapter import EthAdapter
from adapters.mc_adapter import MCAdapter
from adapters.btc_adapter import BTCAdapter
from blockchain import Blockchain
import database

Adapter = {
    Blockchain.ETHEREUM: EthAdapter,
    Blockchain.MULTICHAIN: MCAdapter,
    Blockchain.BITCOIN: BTCAdapter
}


def store(text, blockchain):
    adapter = Adapter[blockchain]
    transaction_hash = adapter.store(text)
    return transaction_hash


def retrieve(transaction_hash):
    blockchain = database.find_blockchain(transaction_hash)
    adapter = Adapter[blockchain]
    text = adapter.retrieve(transaction_hash)
    return text
