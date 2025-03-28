from db_classes import AllowedValue
from db_helper import ConnectionManager

@ConnectionManager.requires_connection
def get_allowed_value_by_id(id: str):
    return AllowedValue.objects.with_id(id)