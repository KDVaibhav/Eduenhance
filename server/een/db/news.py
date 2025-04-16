from .core import Repository
from een.db.config import collection


class NewsRepository(Repository):
    """Provides interface for News collection of database."""

    def __init__(self, school):
        news = collection("news", school)
        super().__init__(news)
