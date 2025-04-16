from .core import Repository
from een.db.config import collection

class AttendanceRepository(Repository):
    """Provides interface for Attendance collection of database."""

    def __init__(self, school):
        attendance = collection("attendance", school)
        super().__init__(attendance)

