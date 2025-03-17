from db_python_util.db_classes import User

from .value_constraint_exception import ValueConstraintViolation


class UsernameTakenException(ValueConstraintViolation):
    def __init__(self, username):
        super().__init__(User, 'username', f"The username '{username}' is already taken")
