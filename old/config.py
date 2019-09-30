from blockchain import Blockchain, blockchain
from credential import credential
from transaction import transaction

AMOUNT = 0
ENCODING = 'utf-8'
DATABASE = 'bcio.db'
BLOCKCHAINS = (
    blockchain(
        blockchain=Blockchain.ETHEREUM,
        name='ETHEREUM'
    ),
    blockchain(
        blockchain=Blockchain.MULTICHAIN,
        name='MULTICHAIN'
    ),
    blockchain(
        blockchain=Blockchain.BITCOIN,
        name='BITCOIN'
    )
)
CREDENTIALS = (
    credential(
        blockchain=Blockchain.ETHEREUM,
        address='',
        key=''
    ),
    credential(
        blockchain=Blockchain.MULTICHAIN,
        address='',
        key='',
        user='',
        password=''
    ),
    credential(
        blockchain=Blockchain.BITCOIN,
        address='',
        key='',
        user='',
        password=''
    )
)
TRANSACTIONS = (
    transaction(
        transaction_hash='',
        blockchain=Blockchain.MULTICHAIN
    ),
    transaction(
        transaction_hash='',
        blockchain=Blockchain.BITCOIN
    )
)

