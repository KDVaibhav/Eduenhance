from .core import Repository
from een.db.config import collection


class LastidsRepository(Repository):
    """Provides interface for Lastids collection of database."""

    def __init__(self, school):
        lastids = collection("lastids", school)
        super().__init__(lastids)
