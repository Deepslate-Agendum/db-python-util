from mongoengine import Document, ListField, StringField, IntField, LazyReferenceField

class ValueType(Document):
    name = StringField(required=True)

    # static_fields # a value type is the type of 0+ static fields
    # fields # a value type is the type of 0+ fields
    allowed_values = ListField(LazyReferenceField('AllowedValue', passthrough=True))


class AllowedValue(Document):
    value = StringField(required=True)

    # dependency_group # an allowed value specifies the manner of 0+ dependency groups
    # field_value # an allowed value provides the value for 0+ field values
    # field # an allowed value provides the default value for 0+ fields
    value_type = LazyReferenceField('ValueType', required=True, passthrough=True) # an allowed value is of 1 type


class Field(Document):
    name = StringField(required=True)
    min_values = IntField(required=True)
    max_values = IntField()

    # field_value # a field has 0+ values
    # static_task_types # a field belongs statically to 0+ task types
    # dynamic_task_types # a field belongs dynamically to 0+ task types
    default_allowed_value = LazyReferenceField('AllowedValue', passthrough=True) # a field has 0/1 default values
    value_type = LazyReferenceField('ValueType', required=True, passthrough=True) # a field has 1 value type


class FieldValue(Document):
    value = StringField() # (non-null iff allowed_value is null)

    # task # a field value belongs to 0/1 tasks (non-null iff task type is null)
    # task_type # a field value belongs to 0/1 task types (non-null iff task is null)
    field = LazyReferenceField('Field', required=True, passthrough=True) # a field value belongs to 1 field
    allowed_value = LazyReferenceField('AllowedValue', passthrough=True) # a field value is provided by 0/1 allowed values (non-null iff value is null)


class User(Document):
    username = StringField(required=True, unique=True)
    display_name = StringField(required=True)
    password_hash = StringField(required=True)
    password_salt = StringField(required=True, unique=True) # !TODO: check with backend, do we enforce uniqueness?

    workspaces = ListField(LazyReferenceField('Workspace', passthrough=True)) # a user belongs to 0+ workspaces
    tasks = ListField(LazyReferenceField('Task', passthrough=True)) # a user is assigned 0+ tasks
    owned_filtered_views = ListField(LazyReferenceField('FilteredView', passthrough=True)) # a user owns 0+ filtered views
    shared_filtered_views = ListField(LazyReferenceField('FilteredView', passthrough=True)) # a user has shared with them 0+ filtered views


class Workspace(Document):
    name = StringField(required=True)

    users = ListField(LazyReferenceField('User', passthrough=True)) # a workspace has 1+ members
    task_types = ListField(LazyReferenceField('TaskType', passthrough=True)) # a workspace has 1+ task types (default when created)
    tasks = ListField(LazyReferenceField('Task', passthrough=True)) # a workspace has 0+ tasks
    # filtered_views # a workspace is the domain of 0+ filtered views


class TaskType(Document):
    name = StringField(required=True)

    static_fields = ListField(LazyReferenceField('Field', passthrough=True)) # a task type has 0+ static fields
    nonstatic_fields = ListField(LazyReferenceField('Field', passthrough=True)) # a task type has 0+ non-static fields
    static_field_values = ListField(LazyReferenceField('FieldValue', passthrough=True)) # a task type has 0+ static field values
    # tasks # a task type is the type of 0+ tasks
    workspaces = ListField(LazyReferenceField('Workspace', passthrough=True)) # a task type belongs to 0+ workspaces
    dependency_groups = ListField(LazyReferenceField('DependencyGroup', passthrough=True)) # a task type groups its dependencies through 0+ dependency groups



class Task(Document):
    # no intrinsic attributes

    nonstatic_field_values = ListField(LazyReferenceField('FieldValue', passthrough=True)) # a task has 0+ non-static field values
    dependencies = ListField(LazyReferenceField('Dependency', passthrough=True)) # a task depends on (0+) tasks via 0+ dependencies
    # workspaces = ListField(LazyReferenceField('Workspace')) # a task belongs to 1+ workspaces # TODO: are we doing same task in multiple workspaces?
    task_type = LazyReferenceField('TaskType', required=True, passthrough=True) # a task is of 1 task type
    dependency_groups = ListField(LazyReferenceField('DependencyGroup', passthrough=True)) # a task groups its dependencies through 0+ dependency groups


class DependencyGroup(Document):
    name = StringField(required=True)
    minTasks = IntField()
    maxTasks = IntField()

    # task_type # a dependency type groups the dependencies of 1 task type
    # dependency # a dependency type groups 0+ dependencies
    manner = LazyReferenceField('AllowedValue', required=True, passthrough=True) # a dependency group's manner (subtask / blocker) is specified by 1 allowed value


class Dependency(Document):
    # no intrinsic attributes

    depended_on_task = LazyReferenceField('Task', required=True, passthrough=True) # a dependency expresses a task's dependence on 1 task
    dependent_task = LazyReferenceField('Task', required=True, passthrough=True) # a dependency expresses the dependence of 1 task
    dependency_group = LazyReferenceField('DependencyGroup', passthrough=True) # a dependency is of 0 or 1 dependency type
    manner = LazyReferenceField('AllowedValue', required=True, passthrough=True) # a(n ungrouped) dependency's manner (subtask / blocker) is specified by 1 allowed value


class FilteredView(Document):
    name = StringField(required=True)
    query = StringField(required=True)

    owner_user = LazyReferenceField('User', passthrough=True) # a filtered view is owned by 1 user
    shared_with_users = ListField(LazyReferenceField('User', passthrough=True)) # a filtered view is shared with 0+ (non-owning) users
    workspaces = ListField(LazyReferenceField('Workspace', required=True, passthrough=True)) # a filtered view belongs to 1+ workspaces
