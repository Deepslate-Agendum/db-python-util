from db_classes import ValueType
from db_helper import ConnectionManager

@ConnectionManager.requires_connection
def get_value_type_by_id(string: id):
    return ValueType.objects.with_id(id)