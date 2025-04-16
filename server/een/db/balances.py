from .core import Repository
from een.db.config import collection


class BalancesRepository(Repository):
    """Provides interface for Balances collection of database."""

    def __init__(self, school):
        balances = collection("balances", school)
        super().__init__(balances)
