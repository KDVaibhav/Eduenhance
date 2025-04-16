from een.db import periods
from een.web.blueprints.crud_controller import CrudController
from localstorage import getSchool


class PeriodsController(CrudController):
    def __init__(self):
        """Initializes new instance of the PeriodsController class"""
        super().__init__(periods(getSchool()), namespace="periods", columns=["no", "timefrom", "timeto"])

    def _update_model(self, model, data, files):
        model.no = data.get("no", "")
        model.timefrom = data.get("timefrom", "")
        model.timeto = data.get("timeto", "")
