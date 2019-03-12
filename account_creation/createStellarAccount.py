from stellar_base.keypair import Keypair
import requests


def createAccount():
    kp = Keypair.random()
    url = 'https://friendbot.stellar.org'
    r = requests.get(url, params={'addr': kp.address().decode()})
    print(f"new account created, response: {r}")
    return {
        'public_key': kp.address().decode(),
        'private_key': kp.seed().decode()
    }


    # def getAccountBalance(cls):
    #     address = Address(address=cls.address)  # See signature for additional args
    #     address.get()  # Get the latest information from Horizon
    #     return address.balances

keypair = createAccount()
print(f"private_key: {keypair.get('private_key')}")
print(f"public_key: {keypair.get('public_key')}")