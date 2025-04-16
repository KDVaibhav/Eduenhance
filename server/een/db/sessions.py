import datetime

import pymongo

from een.db.config import collection
from .core import Repository


class SessionsRepository(Repository):
    """Provides interface for Users collection of database."""

    def __init__(self, school):
        sessions = collection("sessions", school)
        super().__init__(sessions)

    def active(self):
        return self._collection.find({"status": "run"})

    def upcoming(self):
        today = datetime.datetime.today()
        return self._collection.find({
            "date": {
                "$gte": today.strftime('%Y/%m/%d')
            },
            "status": {
                "$ne": "closed"
            }
        }).sort([("date", pymongo.ASCENDING)])
