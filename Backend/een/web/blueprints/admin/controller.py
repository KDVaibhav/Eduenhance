from localstorage import getSchool
from een.db import articles
from een.web.blueprints.crud_controller import CrudController


class AdminController(CrudController):
    def __init__(self):
        super().__init__(articles(getSchool()), namespace="admin", columns=["name"], permission="admin",
                         script=["app/admin.js"])

    def _update_model(self, model, data, files):
        model.name = data.get("name", None)
        model.value = data.get("value", None)
