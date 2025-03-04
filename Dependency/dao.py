from db_classes import Dependency
from db_helper import ConnectionManager

@ConnectionManager.requires_connection
def get_dependency_by_id(string: id):
    return Dependency.objects.with_id(id)