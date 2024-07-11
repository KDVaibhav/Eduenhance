from flask import redirect, render_template, jsonify, flash
from flask_login import login_required
import json

from een.db import transactions, users, balances
from een.web.blueprints.crud_controller import CrudController
from localstorage import getSchool
from een.db.core.model import Model
from een.web.app.auth import access_denied


class TransactionsController(CrudController):
    def __init__(self):
        """Initializes new instance of the TransactionsController class"""
        super().__init__(transactions(getSchool()), namespace="transactions", columns=["student", "ttype", "btype", "amount"])

    @login_required
    def create(self, request):
        """Creates new transaction."""
        if not self._has_permission("create"):
            return access_denied()

        if request.method == "GET":
            with open("local/config.json", "r") as f:
                schoolsData = json.load(f)
            return render_template("crud/new.html", school=schoolsData[getSchool()]['name'], **self.__options(), **self._extend(None))

        elif request.method == "POST":
            model = Model()
            balance_model = balances(getSchool()).find_one({'student': request.form.get("student")})
            if not balance_model:
                balance_model = Model()
                balance_model.student = request.form.get("student")
                balances(getSchool()).insert(balance_model)
            self._update_model(model, request.form, balance_model)
            self._repository.insert(model)
            balances(getSchool()).save(balance_model)
            flash("{} was successfully created".format(self._model_name), category="success")
            return redirect("/" + self._url)

    @login_required
    def update(self, request, key):
        """Shows Transactions."""
        if request.method == "GET":
            if self._has_permission("read"):
                entity = self._repository.get(key)
                with open("local/config.json", "r") as f:
                    schoolsData = json.load(f)
                return render_template("crud/view.html", model=entity, school=schoolsData[getSchool()]['name'], **self.__options(), **self._extend(entity))
            else:
                return access_denied()

        if request.method == "DELETE":
            if self._has_permission("delete"):
                d = self._repository.get(key)
                self._repository.delete(key)
                balance_model = balances(getSchool()).find_one({'student': d.student})
                if balance_model:
                    if d.ttype == 'Credit':
                        balance_model[d.btype] -= int(d.amount)
                    elif d.ttype == 'Debit':
                        balance_model[d.btype] += int(d.amount)
                    balances(getSchool()).save(balance_model)
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})

    def _update_model(self, model, data, balance_model):
        model.student = data.get("student", None)
        model.ttype = data.get("ttype", None)
        model.btype = data.get("btype", None)
        model.amount = data.get("amount", None)
        if not model.btype in balance_model.keys():
            balance_model[model.btype] = 0
        if model.ttype == 'Credit':
            balance_model[model.btype] += int(model.amount)
        elif model.ttype == 'Debit':
            balance_model[model.btype] -= int(model.amount)
        model.remarks = data.get("remarks", None)
        model.date = data.get("date", None)

    def _extend(self, model):
        with open("data.json") as f:
            data = json.load(f)
        return {
            "students": list(map(lambda x: {"name": x.name, "login": x.login, "class": x["class"]}, users(getSchool()).find({"role": "Student", "suspend.value": False}))),
            "btypes": data['btypes']
        }

    def __options(self):
        return {
            "form": self._form,
            "active_page": self._namespace,
            "url": self._url,
            "model_name": self._model_name,
            "namespace": self._namespace,
            "actions": self._actions,
            "js": self._js,
            "show_actions": self._has_permission("delete"),
            "show_delete": self._has_permission("delete"),
            "show_create": self._has_permission("create"),
            "row_class": self._row_class
        }