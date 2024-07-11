from .core import Repository
from een.db.config import collection


class ClassesRepository(Repository):
    """Provides interface for Classes collection of database."""

    def __init__(self, school):
        classes = collection("classes", school)
        super().__init__(classes)
