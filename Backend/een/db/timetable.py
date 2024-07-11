from .core import Repository
from een.db.config import collection

class TimetableRepository(Repository):
    """Provides interface for Timetable collection of database."""

    def __init__(self, school):
        timetable = collection("timetable", school)
        super().__init__(timetable)


    def create(self, class_, table):
        return self._collection.insert_one({
            "class": class_,
            "table": table
        })
