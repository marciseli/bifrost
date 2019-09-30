# Setup

## General Remarks
There are credentials provided in the database which can be used for testing, meaning that there is no real value attached to the cryptocurrencies. Additionally, there is code to help you create an account in the `account_creation` folder.

## Bitcoin

Install the following packages using your favourite package manager:

```console
# pacman -S bitcoind bitcoin-cli
```

### Connecting to the Public Testnet

To connect to the public testnet of Bitcoin (`testnet3`), the following settings are required in the `~/.bitcoin/bitcoin.conf` file:

```
testnet = 1
rpcuser = 'bitcoinrpc'
rpcpassword = 'password'
```

> An example configuration file is available [here](https://github.com/bitcoin/bitcoin/blob/master/contrib/debian/examples/bitcoin.conf).

> In `bitcoind` rpc connections are allowed by default, in `bitcoin-qt` `server = 1` is required in the configuration file to allow rpc connections.

To sync the node with the public testnet:

```console
$ bitcoind
```

The progress of the syncing process can be monitored with:

```console
$ tail -f ~/.bitcoin/testnet3/debug.log
```

To stop the blockchain:

```console
$ bitcoin-cli stop
```

## Ethereum
This command will start a docker node with a preconfigured account which holds 100 eth
`docker-compose -f  docker/docker_compose_eth.yaml up` (on Linux, sudo may be required)

### Dependencies
Docker image used from here:    
https://hub.docker.com/r/trufflesuite/ganache-cli/

## Postgres
This will start a postgres server on docker with the following configuration:
```
User = test
Password = 123456
Port 5432
```
The DB structure will be automatically build when using the adapter.
`docker-compose -f docker/docker_compose_postgres.yaml up`  (on Linux, sudo may be required)

#### More information:    
Psycopg: http://initd.org/psycopg/docs/install.html#binary-install-from-pypi    
https://pynative.com/python-postgresql-tutorial/


## Stellar
Uses public node, no local node is needed

### To run with local node instead of public node
Run a docker container and map port 8000 for REST requests.    
`docker run --rm -it -p "8000:8000" --name stellar stellar/quickstart --testnet`  (on Linux, sudo may be required)   
In stellar_adapter.py, enable the following line:   
builder = Builder(secret=cls.key, horizon_uri="http://localhost:8000/")

### Account creation
An account on the testnet can be created by running account_creation/createStellarAccount

### More Information:     
Horizon server on docker: https://hub.docker.com/r/stellar/quickstart/    
Python SDK to interact with horizon: https://github.com/StellarCN/py-stellar-base          
API documentation: https://stellar-base.readthedocs.io/en/latest/api.html    

Maximum size to save on stellar is 28 bytes.    
https://www.stellar.org/developers/guides/concepts/transactions.html#memo    

files
cd in the folder and run `python setup.py install`


## EOS
Uses public node, no local node is needed.
The EOS library uses NodeJS in the background. Therefore install NodeJS:    
Mac: https://nodejs.org/en/download/     
Linux:`apt-get -y install nodejs`
Install eosjs with node:    
`sudo npm install -g eosjs`    
If you got a message saying "module not found", follow this:    
https://github.com/EvaCoop/eosjs_python/issues/4#issuecomment-433742701

### Account creation
Info about creating the account and using the faucet can be found here: https://jungletestnet.io/

## IOTA
Uses public node, no local node is needed.    
IOTA does not need a sender for zero-value transactions. This means there is no need to create an account and private key to sign the transaction.

## Hyperledger Sawtooth
As the Hyperledger libary tends to cause issues when installing, it is commented out by default in api.py.     
Please follow the setup instructions below to install and enable it.


### Setup
(Linux)`sudo apt-get install python3-pip build-essential autoconf  libtool automake pkg-config libtool libffi-dev libgmp-dev python-dev libsecp256k1-dev`      
(Mac)`brew install autoconf automake libtool`     

`sudo pip3 install sawtooth-sdk` (only works with sudo pip, install if needed)      
`pip install sawtooth-sdk`    


### Start
Enable commented out imports in api.py.

Start the node:    
`sudo docker-compose -f docker/docker-compose_hyperledger.yaml up`  (on Linux, sudo may be required)    


### More information
To test if local node is running: `curl http://localhost:8008/blocks`
https://sawtooth.hyperledger.org/docs/core/releases/1.0/app_developers_guide/docker.html
   
## Multichain
Build and start the docker container:    
`docker-compose -f docker/docker_multichain/docker-compose.yml up` (on Linux, sudo may be required)    
Look up the name of the running container (column NAMES):    
`sudo docker container ls`    
Enter container:     
`docker exec -it docker_multichain_masternode_1_5454208681af sh`, replace with name of container

Start CLI tool with preconfigured blockchain dockerchain:         
`multichain-cli dockerchain`    

Create keys:        
`>createkeypairs` will return something like this:    
```
[
    {
        "address" : "1LKfR5yQVKx3YJ27enyKDNske7XFHzkN6bm43Y",
        "pubkey" : "0323187cd83c9dde13f223b5df1fb2899e645e8b0cd1fa73ae61c41b07ce9cd7a6",
        "privkey" : "VHrFLuvdBeb1oVTmKD48Sdm1ovoc8mS5pbrk2gpKhCUWh72LavvAF8jx"
    }
]
```
Save the address and privkey in the SQLite DB under `address` resp. `key`. (e.g. using "DB Browser for SQLite", available in Ubuntu Store and as dmg for Mac)    

Grant the new address send and receive rights:     
`grant [address from beforesend,receive`     
e.g. `grant 1LKfR5yQVKx3YJ27enyKDNske7XFHzkN6bm43Y send,receive`    
Save the resulting transaction hash in de database as transaction (will be used as input).
