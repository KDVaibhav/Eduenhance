from flask import render_template
from flask_login.utils import login_required, current_user
import json

from een.db import balances, classes, subjects, users, transactions
from een.web.app.auth import access_denied, has_permission
from localstorage import getSchool


class BalancesController():
    def __init__(self):
        """Initializes new instance of the Balances Controller class"""
        self._repository = balances(getSchool())
        self._namespace = "balances"
        self._model_name = "balances"
        self._permission = "balances"
        self._html = "balances_view.html"
        self._url = "balances"

    @login_required
    def index(self):
        if (not has_permission("balances.read_all")) and (not has_permission("balances.read_own")):
            return access_denied()
        models = self._repository.all()
        trans = transactions(getSchool()).all()
        for i in range(len(models)):
            del models[i]['_id']
        for i in range(len(trans)):
            del trans[i]['_id']
        params = {}
        students = list(map(lambda x: {"name": x.name, "login": x.login, "class": x["class"]}, users(getSchool()).find({"role": "Student", "suspend.value": False})))
        if has_permission("balances.read_all"):
            params['models'] = json.dumps(models)
            params['students'] = json.dumps(students)
            params['trans'] = json.dumps(trans)
        if has_permission("balances.read_own"):
            params['model_ind'] = self._repository.find_one({"student": current_user.login})
            params['tran_ind'] = transactions(getSchool()).find({"student": current_user.login})
        return render_template("crud/index_special.html", **params, **self.__options(), **self._extend(None))

    def _extend(self, model):
        with open("data.json") as f:
            data = json.load(f)
        return {
            "classes": list(map(lambda x: x.name, sorted(classes(getSchool()).all(), key = lambda x: x.name))),
            "btypes": data['btypes']
        }

    def __options(self):
        return {
            "index": self._html,
            "active_page": self._namespace,
            "url": self._url,
            "model_name": self._model_name,
            "namespace": self._namespace,
            "allow_edit": has_permission("balances.update"),
            "allow_view": has_permission("balances.read_all")
        }