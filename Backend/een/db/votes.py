from bson import ObjectId

from een.db.core.model import Model
from een.db.config import collection
from .core import Repository


class VotesRepository(Repository):
    """Provides interface for Votes collection of database."""

    def __init__(self, school):
        votes = collection("votes", school)
        super().__init__(votes)

    def find_or_create(self, proposal_id, stage):
        doc = self._collection.find_one({"proposal_id": ObjectId(proposal_id), "stage": stage})
        if not doc:
            doc = self.create(proposal_id, stage)
        return Model(**doc)

    def create(self, proposal_id, stage):
        inserted_id = self._collection.insert_one({
            "proposal_id": proposal_id,
            "private": True,
            "stage": stage,
            "votes": {}
        }).inserted_id
        return self.get(inserted_id)
