from een.db import laws
from een.web.blueprints.crud_controller import CrudController
from localstorage import getSchool


class LawsController(CrudController):
    def __init__(self):
        """Initializes new instance of the ProposalsController class"""
        super().__init__(laws(getSchool()), namespace="laws", columns=["key", "title"], script=["app/laws.js"])

    def _update_model(self, model, data):
        model.key = data.get("key", None)
        model.title = data.get("title", None)
        model.content = data.get("content", None)

    @staticmethod
    def __search_view(x):
        return {
            "title": x.title,
            "key": str(x["_id"])
        }
