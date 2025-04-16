from een.db import classes, subjects
from een.web.blueprints.crud_controller import CrudController
from localstorage import getSchool


class ClassesController(CrudController):
    def __init__(self):
        """Initializes new instance of the ClassesController class"""
        super().__init__(classes(getSchool()), namespace="classes", columns=["name"])

    def _update_model(self, model, data, files):
        model.name = data.get("name", None)
        subs = subjects(getSchool()).all()
        sl = map(lambda x: x["name"], subs)
        sl = list(filter(lambda x: data.get(x, False), sl))
        model.subjects = sl

    def _extend(self, model):
        subject_models = subjects(getSchool()).all()
        return {"subjects": list(map(lambda x: x.name, subject_models))}