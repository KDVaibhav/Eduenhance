from een.db import news, roles
from een.web.blueprints.crud_controller import CrudController
from localstorage import getSchool

import datetime

class NewsController(CrudController):
    def __init__(self):
        """Initializes new instance of the NewsController class"""
        super().__init__(news(getSchool()), namespace="news", columns=["title", "viewer", "date"])

    def _update_model(self, model, data, files):
        model.title = data.get("title", None)
        model.content = data.get("content", None)
        model.viewer = data.get("viewer", None)
        today = datetime.date.today()
        model.date = "{0:04d}".format(today.year) + "-" + "{0:02d}".format(today.month) + "-" + "{0:02d}".format(today.day)

    def _extend(self, model):
        return {
            "roles": roles(getSchool()).find({}, {"name": 1, "_id": 0})
        }
