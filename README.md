# bcio

A project towards blockchain interoperability.

## Dependencies

This project is built with:

- [Python](https://www.python.org/)
- [PyPA](https://pip.pypa.io/en/stable/) tool for installing Python packages
- [Sqlite3](https://www.sqlite.org/index.html) as dbms
- [Web3.py](https://web3py.readthedocs.io/en/stable/) for Ethereum integration
- [mcrpc](https://github.com/coblo/mcrpc) for MultiChain integration
- [python-bitcoinrpc](https://github.com/jgarzik/python-bitcoinrpc) for Bitcoin integration

## Setup

The setup is described in detail [here](SETUP.md).

## Usage

Store a text message on the Ethereum blockchain and retrieve it using the transaction hash:

```python
from bcio import store, retrieve, Blockchain

tx_hash = store('Hello World!', Blockchain.ETHEREUM)
text = retrieve(tx_hash)
```

> Alternatively, the module comes with integration for MultiChain (`Blockchain.MULTICHAIN`) and Bitcoin (`Blockchain.BITCOIN`).
