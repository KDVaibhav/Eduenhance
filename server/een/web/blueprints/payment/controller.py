from flask import render_template, flash, redirect, jsonify
from flask_login.utils import login_required, current_user
from een.db.core.model import Model
import json, datetime

from een.db import payment, leave, users
from een.web.app.auth import access_denied, has_permission
from localstorage import getSchool


class PaymentController():
    def __init__(self):
        """Initializes new instance of the Payment Controller class"""
        self._repository = payment(getSchool())
        self._namespace = "payment"
        self._model_name = "Payment"
        self._permission = "payment"
        self._html = "payment_view.html"
        self._url = "payment"

    @login_required
    def index(self):
        if (not has_permission("payment.read_all")) and (not has_permission("payment.read_own")) and (not has_permission("payment.update")):
            return access_denied()
        params = {}
        if has_permission("payment.read_all"):
            params['models'] = self._repository.all()
            for i in range(len(params['models'])):
                name = users(getSchool()).find_one({'login': params['models'][i].teacher}).name
                params['models'][i].login = params['models'][i].teacher
                params['models'][i].teacher = name

        if has_permission("payment.read_own"):
            params['models'] = self._repository.find({'teacher': current_user.login})
            for i in range(len(params['models'])):
                params['models'][i].login = current_user.login
                params['models'][i].teacher = current_user.name
        return render_template("crud/index_special.html", **params, **self.__options(), **self._extend(None))

    @login_required
    def create(self, request):
        """Create for Payment"""
        if request.method == "GET":
            if has_permission("payment.create"):
                return render_template("crud/new.html", **self.__options(), **self._extend(None))
            else:
                return access_denied()
        elif request.method == "POST":
            if has_permission("payment.create"):
                model = Model()
                model.teacher = request.form.get('teacher')
                model.month = request.form.get('month')
                model.net = request.form.get('net')
                model.basic = request.form.get('basic')
                model.dul = request.form.get('dul')
                model.deduc = request.form.get('deduc')
                today = datetime.date.today()
                model.paid_on = "{0:04d}".format(today.year) + "-" + "{0:02d}".format(today.month) + "-" + "{0:02d}".format(today.day)
                if not self._repository.insert(model):
                    flash("Database name already exists", category="danger")
                else:
                    flash("{} was successfully created".format(self._model_name), category="success")
                return redirect("/" + self._url)
            else:
                return access_denied()

    @login_required
    def update(self, request, key):
        """Shows payment."""
        if request.method == "POST":
            if has_permission("payment.update"):
                d = self._repository.get(key)
                d.month = request.form.get('month')
                d.net = request.form.get('net')
                d.basic = request.form.get('basic')
                d.deduc = request.form.get('deduc')
                self._repository.save(d)
                flash("{} was successfully updated".format(self._model_name), category="success")
                return redirect("/" + self._url)
            else:
                return access_denied()
        elif request.method == "GET":
            if has_permission("payment.read_all") or has_permission("payment.read_own"):
                entity = self._repository.get(key)
                return render_template("crud/view.html", model=entity, **self.__options(), **self._extend(entity))
            else:
                return access_denied()

        elif request.method == "DELETE":
            if has_permission("payment.delete"):
                self._repository.delete(key)
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})

    @login_required
    def dul(self, request):
        """Calculates due unpaid leave."""
        if has_permission("payment.create") or has_permission("payment.update"):
            teacher = request.form.get('teacher')
            n_leaves = leave(getSchool()).count({'teacher': teacher})
            payments = self._repository.find({'teacher': teacher})
            n_ul_deducted = 0
            for p in payments:
                n_ul_deducted += int(p.dul)
            dul = (n_leaves - 10 - n_ul_deducted) if n_leaves > 10 else 0
            return jsonify({"success": True, "dul": dul})
        else:
            return jsonify({"success": False})

    def _extend(self, model):
        with open("data.json") as f:
            data = json.load(f)
        teachers = users(getSchool()).find({'role': 'Teacher'}, {'name': 1, 'login': 1, '_id': 0})
        #print(teachers)
        return {
            "teachers": teachers,
            "months": data['months']
        }

    def __options(self):
        return {
            "index": self._html,
            "form": "payment_form.html",
            "active_page": self._namespace,
            "url": self._url,
            "model_name": self._model_name,
            "namespace": self._namespace,
            "allow_edit": has_permission("payment.update"),
            "allow_view_own": has_permission("payment.read_own"),
            "allow_view_all": has_permission("payment.read_all"),
            "allow_delete": has_permission("payment.delete"),
            "allow_create": has_permission("payment.create")
        }
