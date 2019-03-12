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
        "address": '0xf717e2d05037d13d6bfd0d783d6f4ebd68dd5b46',
        "key": '0xec7a5eb646075cc16dd842381489614a49eda87e1f600d8780bbb3012288a98f',
        "user": 'ethereum (not used)',
        "password": 'ethereum (not used)',
    },
    {
        "blockchain": Blockchain.MULTICHAIN,
        "id": Blockchain.MULTICHAIN.value,
        "address": '1Gw2SBr1VcFCpTQ8XnEeyAvoo9hmGmq39DfRw3',
        "key": 'VBvmxHaJ41cfYuaaJYLzR2yCcVYyJX5spJFZwJpRGgK4z1KSMi96ub5w',
        "user": 'multichainrpc',
        "password": '79pgKQusiH3VDVpyzsM6e3kRz6gWNctAwgJvymG3iiuz'
    },
    {
        "blockchain": Blockchain.BITCOIN,
        "id": Blockchain.BITCOIN.value,
        "address": '2NGMq7iBuJTeDMQPxSaEQVqMtdt3VQxuN7B',
        "key": 'cS6kdk7zxTCij8HpXHE8Kdnh1uAM46PU5LNtQxpBZ6YjP3t3zgWL',
        "user": 'bc4cc',
        "password": 'bc4cc112358'
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
        "address": 'GCCAETWXN5VYPOU4MYTUGTFPTSWWNFYMDZWHWS566PUXR5GCQ7SY7QHQ',
        "key": 'SBJF56A62FP7OEATJIDFYUTXORNJXWGXD5GBWW7TDVN2QMHDJMOXBLPK',
        "user": 'stellar (not used)',
        "password": 'stellar (not used)'
    },
    {
        "blockchain": Blockchain.HYPERLEDGER,
        "id": Blockchain.HYPERLEDGER.value,
        "address": 'will be generated from private key',
        "key": 'c2d0a398c3c3074e066b953b3bb15ae7053fd8aba1c2279b2f3ff058ab7e7661',
        "user": 'hyperledger (not used)',
        "password": 'hyperledger (not used)'
    },
    {
        "blockchain": Blockchain.EOS,
        "id": Blockchain.EOS.value,
        "address": 'EOS8Vfg6ssQxj66wX9LrFq3EZY8z4EEkiyiQiDc7bwyn65K4YFVwW',
        "key": '5KazRYnXDCNougrvuVtZFDMAiB3kr7M2tjGYNJtQQ2Wn3JFRdTM',
        "user": 'jungletimohe',
        "password": 'eos (not used)'
    },
    {
        "blockchain": Blockchain.IOTA,
        "id": Blockchain.IOTA.value,
        "address": 'GVMOWHRPLRAQMTMDWKDFNGOCLRYHPHWUSYOTSUUSVVEXLZCHFYANXERRPJPOAVSXEPSTUNEOHIFQYZSEYRNUANOMYA',
        "key": 'iota (not used)',
        "user": 'iota (not used)',
        "password": 'iota (not used)',
    }
]
TRANSACTIONS = [
    {
        "blockchain": Blockchain.MULTICHAIN.value,
        "transaction_hash": '9946b1c99fd316807f55812a0c133be828d1908345f08bb9d708262b701dd504',
    },
    {
        "blockchain": Blockchain.BITCOIN.value,
        "transaction_hash": 'fd712ad8f279574b3a0cbe706a03f6d39b2a31c63420a42bf49c2d7035036a7f',
    }
]

