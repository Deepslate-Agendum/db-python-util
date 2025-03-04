from db_classes import TaskType
from db_helper import ConnectionManager

@ConnectionManager.requires_connection
def get_task_type_by_id(id: str):
    return TaskType.objects.with_id(id)