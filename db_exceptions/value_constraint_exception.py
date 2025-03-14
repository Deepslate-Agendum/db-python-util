from .db_exception import DBException


class ValueConstraintViolation(DBException):
    def __init__(self, collection, field, message=None):
        self.collection = collection
        self.field = field
        self.message = message
