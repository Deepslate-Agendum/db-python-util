from db_classes import FieldValue
from db_helper import ConnectionManager

@ConnectionManager.requires_connection
def get_field_value_by_id(string: id):
    return FieldValue.objects.with_id(id)