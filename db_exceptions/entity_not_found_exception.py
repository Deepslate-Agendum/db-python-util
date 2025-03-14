from .db_exception import DBException


class EntityNotFoundException(DBException):
    def __init__(self, collection, message=None):
        self.collection = collection
        self.message = message
