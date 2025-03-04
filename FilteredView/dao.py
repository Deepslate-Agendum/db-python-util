from db_classes import FilteredView
from db_helper import ConnectionManager

@ConnectionManager.requires_connection
def get_filtered_view_by_id(string: id):
    return FilteredView.objects.with_id(id)