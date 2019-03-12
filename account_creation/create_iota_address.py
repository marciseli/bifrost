from iota import Iota, Address, ProposedTransaction, Tag, Transaction, TryteString, TransactionHash, Bundle

# Generate a random seed.
# ADDRESS_WITH_CHECKSUM_SECURITY_LEVEL_2 = b"9TPHVCFLAZTZSDUWFBLCJOZICJKKPVDMAASWJZNFFBKRDDTEOUJHR9JVGTJNI9IYNVISZVXARWJFKUZWC"
# "https://github.com/iotaledger/iota.lib.py/blob/master/docs/addresses.rst"
# print(api.get_node_info())
# "https://github.com/iotaledger/iota.lib.py/blob/master/docs/types.rst"
# Generate 1 address, starting with index 42:
# https://medium.com/coinmonks/exploring-iota-2-retrieve-your-transaction-and-create-your-wallet-bc8e8c91fec9
# working_tx = "IMLLFGKXGLFFTTAEBQIVFAWTMJVVKONKRXJBYQJDVWIPUYJOSEHYPGF9JAYJXXEIMZFRYBXTPOQWTW999"


def create_address():
    gna_result = api.get_new_addresses(
        index=42, security_level=2, checksum=True)
    addresses = gna_result['addresses']
    print(addresses)


# from iota import Iota
# from iota import Address, ProposedTransaction, Tag, Transaction, TryteString, TransactionHash
# from iota import Bundle

# # Generate a random seed.
# # ADDRESS_WITH_CHECKSUM_SECURITY_LEVEL_2 = b"9TPHVCFLAZTZSDUWFBLCJOZICJKKPVDMAASWJZNFFBKRDDTEOUJHR9JVGTJNI9IYNVISZVXARWJFKUZWC"
# # "https://github.com/iotaledger/iota.lib.py/blob/master/docs/addresses.rst"
# # print(api.get_node_info())
# # "https://github.com/iotaledger/iota.lib.py/blob/master/docs/types.rst"
# # Generate 1 address, starting with index 42:
# # https://medium.com/coinmonks/exploring-iota-2-retrieve-your-transaction-and-create-your-wallet-bc8e8c91fec9


# api = Iota('https://nodes.devnet.iota.org:443', testnet=True)


# def get_transaction():
#     bundle = api.get_bundles(
#         "AVSOQXUJEFHIMVYZXAILMDVCKRLFKTDLGMHVHUNFNSWZBIZMRWAXZAAWLZJCFHDFIMFQSMPKVPGTXD999")
#     singleBundle = bundle["bundles"][0]
#     json = Bundle.as_json_compatible(singleBundle)
#     data = json[0]["signature_message_fragment"]
#     data = TryteString.decode(data)
#     print(data)


# def create_address():
#     gna_result = api.get_new_addresses(
#         index=42, security_level=2, checksum=True)
#     addresses = gna_result['addresses']
#     print(addresses)


# def transfer():
#     # "https://pyota.readthedocs.io/en/latest/api.html#send-transfer"
#     api.send_transfer(
#         depth=4,
#         transfers=[
#             ProposedTransaction(
#                 # Recipient of the transfer.
#                 address=Address(
#                     'GVMOWHRPLRAQMTMDWKDFNGOCLRYHPHWUSYOTSUUSVVEXLZCHFYANXERRPJPOAVSXEPSTUNEOHIFQYZSEYRNUANOMYA'
#                 ),
#                 value=0,
#                 # Optional tag to attach to the transfer.
#                 tag=Tag(b'ADAPT'),
#                 # Optional message to include with the transfer.
#                 message=TryteString.from_string("Hello!"),
#             ),
#         ],
#     )


# get_transaction()
