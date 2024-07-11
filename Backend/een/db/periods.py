from .core import Repository
from een.db.config import collection


class PeriodsRepository(Repository):
    """Provides interface for Periods collection of database."""

    def __init__(self, school):
        periods = collection("periods", school)
        super().__init__(periods)
