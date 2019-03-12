from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import Secp256k1Context
import _pickle as cPickle
import codecs
import base64

#Create and log new private key as hex
context = create_context('secp256k1')
p_key = context.new_random_private_key()
print(p_key.as_hex())

#Import a private key from hex
# priv_hex = "4ae268d2848de006edadf08cc7cd26123bb79c69c25339e2155fe5a20b61a4ce"
# context = create_context('secp256k1')
# signer = CryptoFactory(context).new_signer(
#     context.new_random_private_key().from_hex(priv_hex))

