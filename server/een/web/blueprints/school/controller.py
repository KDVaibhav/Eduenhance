from een.db import school
from een.web.blueprints.crud_controller import CrudController

class SchoolController(CrudController):
    def __init__(self):
        """Initializes new instance of the ProposalsController class"""
        super().__init__(school(), namespace="school", columns=["name", "address"], script=["app/school.js"])

    def _update_model(self, model, data, files):
        if not model:
            model['dbname'] = data.get("dbname", None)
            model['_id'] = data.get("dbname", None)
        model['name'] = data.get("name", None)
        model['address'] = data.get("address", None)

    @staticmethod
    def __search_view(x):
        return {
            "name": x["name"],
            "dbname": x["dbname"],
            "address": x["address"],
            "_id": x["dbname"]
        }
