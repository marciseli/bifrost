from enum import Enum, auto


class Blockchain(Enum):
    ETHEREUM = auto()
    MULTICHAIN = auto()
    BITCOIN = auto()


def blockchain(blockchain, name):
    return {
        'blockchain': blockchain,
        'name': name
    }
