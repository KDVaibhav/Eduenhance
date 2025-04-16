from .core import Repository
from een.db.config import collection


class RolesRepository(Repository):
    """Provides interface for Roles collection of database."""

    def __init__(self, school):
        roles = collection("roles", school)
        super().__init__(roles)
