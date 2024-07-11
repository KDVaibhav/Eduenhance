from een.db import exams
from een.web.blueprints.crud_controller import CrudController
from localstorage import getSchool


class ExamsController(CrudController):
    def __init__(self):
        """Initializes new instance of the ProposalsController class"""
        super().__init__(exams(getSchool()), namespace="exams", columns=["name", "type", "date"])

    def _update_model(self, model, data, files):
        model.key = data.get("key", None)
        model.name = data.get("name", None)
        model.type = data.get("type", None)
        if model.type == "Weekly":
            model.date = data.get("date", None)
        else:
            model.date = [data.get("datefrom", None), data.get("dateto", None)]
        model.details = data.get("details", None)
    
    def _extend(self, model):
        return {"types": ['Weekly', 'Cumulative']}
        