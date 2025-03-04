from db_classes import Field
from db_helper import ConnectionManager

@ConnectionManager.requires_connection
def get_field_by_id(string: id):
    return Field.objects.with_id(id)