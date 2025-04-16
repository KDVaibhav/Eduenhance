from .core import Repository
from een.db.config import collection


class LeaveRepository(Repository):
    """Provides interface for Leave collection of database."""

    def __init__(self, school):
        leave = collection("leave", school)
        super().__init__(leave)
