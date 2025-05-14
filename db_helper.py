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

@ConnectionManager.requires_connection
def create_enum(enum_name, value_names):
    value_type = ValueType(
        name=enum_name,
        allowed_values=[],
    )
    value_type.save()

    values_map = {}
    for value_name in value_names:
        value = AllowedValue(
            value=value_name,
            value_type=value_type,
        )
        value.save()
        values_map[value_name] = value

    value_type.update(allowed_values=values_map.values())
    value_type.save()

    return value_type, values_map

@ConnectionManager.requires_connection
def get_enum(name):
    value_type = ValueType.objects(name=name).first()
    values = AllowedValue.objects(value_type=value_type)
    value_map = {value.value: value for value in values}

    return value_type, value_map
