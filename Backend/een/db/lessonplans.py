from .core import Repository
from een.db.config import collection


class LessonplansRepository(Repository):
    """Provides interface for Lessonplans collection of database."""

    def __init__(self, school):
        lessonplans = collection("lessonplans", school)
        super().__init__(lessonplans)
