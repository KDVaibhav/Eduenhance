from een.db.config import collection
from .core import Repository


class ArticlesRepository(Repository):
    """Provides interface for Articles collection of database."""

    def __init__(self, school):
        articles = collection("articles", school)
        super().__init__(articles)
