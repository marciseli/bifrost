from abc import ABC, abstractmethod


class Adapter(ABC):

    @property
    @abstractmethod
    def credentials(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def address(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def key(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def client(self):
        raise NotImplementedError

    @classmethod
    def retrieve(cls, transaction_hash):
        transaction = cls.get_transaction(transaction_hash)
        data = cls.extract_data(transaction)
        return cls.to_text(data)

    @staticmethod
    @abstractmethod
    def get_transaction(transaction_hash):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def extract_data(transaction):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def to_text(data):
        raise NotImplementedError

    @classmethod
    def store(cls, text):
        transaction = cls.create_transaction(text)
        signed_transaction = cls.sign_transaction(transaction)
        transaction_hash = cls.send_raw_transaction(signed_transaction)
        cls.add_transaction_to_database(transaction_hash)
        return transaction_hash

    @staticmethod
    @abstractmethod
    def create_transaction(text):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def sign_transaction(transaction):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def send_raw_transaction(transaction):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def add_transaction_to_database(transaction_hash):
        raise NotImplementedError
