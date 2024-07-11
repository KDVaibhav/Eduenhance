from .core import Repository
from een.db.config import collection


class MarksRepository(Repository):
    """Provides interface for Marks collection of database."""

    def __init__(self, school):
        marks = collection("marks", school)
        super().__init__(marks)
