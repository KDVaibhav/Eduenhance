from .core import Repository
from een.db.config import collection


class SubjectsRepository(Repository):
    """Provides interface for Subjects collection of database."""

    def __init__(self, school):
        subjects = collection("subjects", school)
        super().__init__(subjects)
