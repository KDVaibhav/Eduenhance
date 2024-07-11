from flask import render_template, flash, redirect, jsonify
from flask_login.utils import login_required, current_user
from een.db.core.model import Model
import json

from een.db import leave, classes, users
from een.web.app.auth import access_denied, has_permission
from localstorage import getSchool


class LeaveController():
    def __init__(self):
        """Initializes new instance of the Leave Controller class"""
        self._repository = leave(getSchool())
        self._namespace = "leave"
        self._model_name = "leave"
        self._permission = "leave"
        self._html = "leave_view.html"
        self._url = "leave"

    @login_required
    def index(self):
        if (not has_permission("leave.read_all")) and (not has_permission("leave.read_own")) and (not has_permission("leave.update")):
            return access_denied()
        params = {}
        if has_permission("leave.read_all"):
            params['models'] = self._repository.all()
            for i in range(len(params['models'])):
                name = users(getSchool()).find_one({'login': params['models'][i].teacher}).name
                params['models'][i].login = params['models'][i].teacher
                params['models'][i].teacher = name

        if has_permission("leave.read_own"):
            params['models'] = self._repository.find({'teacher': current_user.login})
        return render_template("crud/index_special.html", **params, **self.__options(), **self._extend(None))

    @login_required
    def apply(self, request):
        """Apply for Leave"""
        if request.method == "GET":
            if has_permission("leave.create"):
                return render_template("crud/new.html", **self.__options(), **self._extend(None))
            else:
                return access_denied()
        elif request.method == "POST":
            if has_permission("leave.create"):
                model = Model()
                model.teacher = current_user.login
                model.date = request.form.get('date')
                model.reason = request.form.get('reason')
                model.approved = False
                if not self._repository.insert(model):
                    flash("Database name already exists", category="danger")
                else:
                    flash("{} was successfully created".format(self._model_name), category="success")
                return redirect("/" + self._url)
            else:
                return access_denied()

    @login_required
    def update(self, request, key):
        """Shows leave."""
        if request.method == "POST":
            if has_permission("leave.update"):
                d = self._repository.get(key)
                if not d.approved:
                    d.teacher = current_user.login
                    d.date = request.form.get('date')
                    d.reason = request.form.get('reason')
                    self._repository.save(d)
                    flash("{} was successfully updated".format(self._model_name), category="success")
                    return redirect("/" + self._url)
                else:
                    flash("Cannot update", category="error")
                    return redirect("/" + self._url)
            else:
                return access_denied()
        elif request.method == "GET":
            if has_permission("leave.read_all") or has_permission("leave.read_own"):
                entity = self._repository.get(key)
                o = self.__options()
                if entity.approved:
                    o["allow_edit"] = False
                return render_template("crud/view.html", model=entity, **o, **self._extend(entity))
            else:
                return access_denied()

        elif request.method == "DELETE":
            if has_permission("leave.delete"):
                entity = self._repository.get(key)
                if not entity.approved:
                    self._repository.delete(key)
                    return jsonify({"success": True})
                else:
                    return jsonify({"success": False})
            else:
                return jsonify({"success": False})

        elif request.method == "PUT":
            if has_permission("leave.approve"):
                d = self._repository.get(key)
                d.approved = True
                self._repository.save(d)
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})

    def _extend(self, model):
        return {}

    def __options(self):
        return {
            "index": self._html,
            "form": "leave_form.html",
            "active_page": self._namespace,
            "url": self._url,
            "model_name": self._model_name,
            "namespace": self._namespace,
            "allow_edit": has_permission("leave.update"),
            "allow_view_own": has_permission("leave.read_own"),
            "allow_view_all": has_permission("leave.read_all"),
            "allow_delete": has_permission("leave.delete"),
            "allow_approve": has_permission("leave.approve"),
            "allow_apply": has_permission("leave.create")
        }
