from .core import Repository
from een.db.config import collection


class UsersRepository(Repository):
    """Provides interface for Users collection of database."""

    def __init__(self, school):
        users = collection("users", school)
        super().__init__(users)

    def with_permission(self, permission):
        # todo not effective
        from een.db import roles

        result = []
        for user in self.all():
            role = roles.find_one({"name": user.role})
            if permission in role.permissions:
                result.append(user)
        return result
