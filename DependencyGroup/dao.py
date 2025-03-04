from db_classes import DependencyGroup
from db_helper import ConnectionManager

@ConnectionManager.requires_connection
def get_dependency_group_by_id(string: id):
    return DependencyGroup.objects.with_id(id)