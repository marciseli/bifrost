from abc import abstractmethod
from binascii import unhexlify
from adapters.adapter import Adapter
from config import ENCODING


class MCBTCAdapter(Adapter):

    @staticmethod
    def extract_output(transaction, output_index):
        outputs = transaction['vout']
        return outputs[output_index]

    @staticmethod
    def to_text(data_hex):
        data = unhexlify(data_hex)
        return data.decode(ENCODING)

    @classmethod
    def create_transaction(cls, text):
        input_transaction_hash = cls.get_latest_transaction_from_database()
        inputs = [{'txid': input_transaction_hash, 'vout': 0}]
        data_hex = cls.to_hex(text)
        output = cls.create_transaction_output(data_hex, input_transaction_hash)
        transaction_hex = cls.create_raw_transaction(inputs, output, data_hex)
        return transaction_hex

    @staticmethod
    @abstractmethod
    def get_latest_transaction_from_database():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def to_hex(text):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_transaction_output(data_hex, transaction_hash):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_raw_transaction(inputs, output, data_hex):
        raise NotImplementedError

    @classmethod
    def sign_transaction(cls, transaction_hex):
        parent_outputs = []
        signed = cls.client.signrawtransaction(
            transaction_hex,
            parent_outputs,
            [cls.key]
        )
        assert signed['complete']
        return signed['hex']

    @classmethod
    def send_raw_transaction(cls, transaction_hex):
        transaction_hash = cls.client.sendrawtransaction(transaction_hex)
        return transaction_hash
