from functools import wraps
from typing import Optional

from mongoengine import connect, disconnect
from .db_classes import Field, ValueType, AllowedValue


# function that opens a connection to the database
def connectToDatabase():
    host = "mongodb://localhost:27017/agendum"
    connection = connect(host=host)
    if connection is None:
        raise ConnectionError("Failed to connect to the database")
    return connection


class ConnectionManager:
    def __init__(self):
        self._connection = None

    def get_connection(self):
        if self._connection is None:
            self._connection = connectToDatabase()

        return self._connection

    def requires_connection(self, f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            nonlocal self
            self.get_connection()
            return f(*args, **kwargs)
        return wrapped

ConnectionManager = ConnectionManager()


# function that creates tags
@ConnectionManager.requires_connection
def create_tag(name) -> AllowedValue:
    tag_type = ValueType.objects(name = "Tag").first()

    tag = AllowedValue(value=name, value_type=tag_type)
    tag.save()

    return tag

@ConnectionManager.requires_connection
def get_tag(name) -> Optional[AllowedValue]:
    tag_value_type = ValueType.objects(name="Tag").first()
    tag = AllowedValue.objects(value=name, value_type=tag_value_type).first()
    return tag
