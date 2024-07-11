from .core import Repository
from een.db.config import collection


class TransactionsRepository(Repository):
    """Provides interface for Transactions collection of database."""

    def __init__(self, school):
        transactions = collection("transactions", school)
        super().__init__(transactions)
