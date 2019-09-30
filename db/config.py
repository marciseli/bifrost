from blockchain import Blockchain

AMOUNT = 0
ENCODING = 'utf-8'
DATABASE_PATH = 'db/bcio.db'
WAIT_FOR_CONFIRMATION = False

# Set how long to wait until checking if tx arrived
CONFIRMATION_WAITING_TIMES = {
    Blockchain.ETHEREUM.value: max(105, 20),
    Blockchain.MULTICHAIN.value: max(15, 20),
    Blockchain.BITCOIN.value: max(3600, 20),
    Blockchain.POSTGRES.value: max(5, 20),
    Blockchain.STELLAR.value: max(5, 20),
    Blockchain.HYPERLEDGER.value: max(20, 20),
    Blockchain.EOS.value: max(0.5, 20),
    Blockchain.IOTA.value: max(60, 20),
}

CREDENTIALS = [
    {
        "blockchain": Blockchain.ETHEREUM.name,
        "id": Blockchain.ETHEREUM.value,
        "address": '',
        "key": '',
        "user": 'ethereum (not used)',
        "password": 'ethereum (not used)',
    },
    {
        "blockchain": Blockchain.MULTICHAIN,
        "id": Blockchain.MULTICHAIN.value,
        "address": '',
        "key": '',
        "user": 'multichainrpc',
        "password": ''
    },
    {
        "blockchain": Blockchain.BITCOIN,
        "id": Blockchain.BITCOIN.value,
        "address": '',
        "key": '',
        "user": '',
        "password": ''
    },
    {
        "blockchain": Blockchain.POSTGRES,
        "id": Blockchain.POSTGRES.value,
        # database name
        "address": 'test',
        # port number
        "key": '5000',
        "user": 'test',
        "password": '123456'
    },
    {
        "blockchain": Blockchain.STELLAR,
        "id": Blockchain.STELLAR.value,
        "address": '',
        "key": '',
        "user": 'stellar (not used)',
        "password": 'stellar (not used)'
    },
    {
        "blockchain": Blockchain.HYPERLEDGER,
        "id": Blockchain.HYPERLEDGER.value,
        "address": 'will be generated from private key',
        "key": '',
        "user": 'hyperledger (not used)',
        "password": 'hyperledger (not used)'
    },
    {
        "blockchain": Blockchain.EOS,
        "id": Blockchain.EOS.value,
        "address": '',
        "key": '',
        "user": '',
        "password": 'eos (not used)'
    },
    {
        "blockchain": Blockchain.IOTA,
        "id": Blockchain.IOTA.value,
        "address": '',
        "key": 'iota (not used)',
        "user": 'iota (not used)',
        "password": 'iota (not used)',
    }
]
TRANSACTIONS = [
    {
        "blockchain": Blockchain.MULTICHAIN.value,
        "transaction_hash": '',
    },
    {
        "blockchain": Blockchain.BITCOIN.value,
        "transaction_hash": '',
    }
]

