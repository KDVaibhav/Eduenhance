from een.db import subjects
from een.web.blueprints.crud_controller import CrudController
from localstorage import getSchool


class SubjectsController(CrudController):
    def __init__(self):
        """Initializes new instance of the SubjectsController class"""
        super().__init__(subjects(getSchool()), namespace="subjects", columns=["name"])

    def _update_model(self, model, data, files):
        model.name = data.get("name", None)
