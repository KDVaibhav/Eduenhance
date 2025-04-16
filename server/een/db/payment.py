from .core import Repository
from een.db.config import collection


class PaymentRepository(Repository):
    """Provides interface for Payment collection of database."""

    def __init__(self, school):
        payment = collection("payment", school)
        super().__init__(payment)
