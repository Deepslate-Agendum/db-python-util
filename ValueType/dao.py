from db_classes import ValueType
from db_helper import ConnectionManager

@ConnectionManager.requires_connection
def get_value_type_by_id(id: str):
    return ValueType.objects.with_id(id)

@ConnectionManager.requires_connection
def create_value_type(name: str) -> str:
    allowed_values = []

    value_type = ValueType(name=name, allowed_values=allowed_values)
    value_type.save()
    return value_type.id.binary.hex()