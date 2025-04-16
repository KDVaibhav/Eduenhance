from .core import Repository
from een.db.config import collection


class ExamsRepository(Repository):
    """Provides interface for Exams collection of database."""

    def __init__(self, school):
        exams = collection("exams", school)
        super().__init__(exams)
