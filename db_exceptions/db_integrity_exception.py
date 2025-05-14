from .db_exception import DBException


class DBIntegrityException(DBException):
    def __init__(self, collection, message=None):
        self.collection = collection
        self.message = message
