from flask import render_template, flash, redirect, jsonify
from flask_login import login_required
from inflection import singularize

from een.db.core.model import Model
from een.web.app.auth import has_permission, access_denied
from localstorage import getSchool
import json
import os

class CrudController:
    def __init__(self, repository, namespace=None, columns=None, row_class=None, script=None, permission=None):
        self._repository = repository
        self._columns = columns or []
        self._namespace = namespace
        self._model_name = singularize(self._namespace).capitalize()
        self._actions = []
        self._row_class = row_class or self.__row_class
        self._js = script or []
        self.__override_permission = permission

        if namespace:
            self._permission = namespace
            self._form = "{}_form.html".format(namespace)
            self._url = namespace

    def add_script(self, name):
        self._js.append(name)

    def add_action(self, css_class, icon, permission=None):
        self._actions.append({"css_class": css_class, "icon": icon, "permission": permission})

    @login_required
    def index(self):
        """Shows list of models."""
        if not self._has_permission("read"):
            return access_denied()
        if self._namespace == "users":
            models = []
            temp = self._repository.all()
            for model in temp:
                if has_permission("{}.read".format(model.role.lower())):
                    if has_permission("{}.delete".format(model.role.lower())):
                        model.show_delete = True
                    models.append(model)
        else:
            models = self._repository.all()
        with open("local/config.json", "r") as f:
            schoolsData = json.load(f)
        return render_template("crud/index.html", models=models, school=schoolsData[getSchool()]['name'], fields=self._columns, **self.__options())

    @login_required
    def create(self, request):
        """Creates new user."""
        if not self._has_permission("create"):
            return access_denied()

        if request.method == "GET":
            with open("local/config.json", "r") as f:
                schoolsData = json.load(f)
            return render_template("crud/new.html", school=schoolsData[getSchool()]['name'], **self.__options(), **self._extend(None))

        elif request.method == "POST":
            model = Model()
            self._update_model(model, request.form, request.files)
            if not self._repository.insert(model):
                flash("Database name already exists", category="danger")
            else:
                flash("{} was successfully created".format(self._model_name), category="success")
            return redirect("/" + self._url)

    @login_required
    def update(self, request, key):
        """Shows user."""
        if request.method == "GET":
            if self._has_permission("read"):
                entity = self._repository.get(key)
                if self._namespace == "users" and has_permission("{}.update".format(entity.role.lower())):
                    entity.allow_edit = True
                with open("local/config.json", "r") as f:
                    schoolsData = json.load(f)
                return render_template("crud/view.html", model=entity, school=schoolsData[getSchool()]['name'], **self.__options(), **self._extend(entity))
            else:
                return access_denied()

        elif request.method == "POST":
            if self._has_permission("update"):
                d = self._repository.get(key)
                self._update_model(d, request.form, request.files)
                self._repository.save(d)

                flash("{} was successfully updated".format(self._model_name), category="success")
                return redirect("/" + self._url)
            else:
                return access_denied()

        if request.method == "DELETE":
            if self._has_permission("delete"):
                if self._namespace == "users":
                    d = self._repository.get(key)
                    if 'photo' in d.keys():
                        if os.path.exists('een/web/static/uploads/' + d.photo):
                            os.remove('een/web/static/uploads/' + d.photo)
                    if 'sign' in d.keys():
                        if os.path.exists('een/web/static/uploads/' + d.sign):
                            os.remove('een/web/static/uploads/' + d.sign)
                    if 'files' in d.keys():
                        for file in d.files.keys():
                            if os.path.exists('een/web/static/uploads/' + file + d.files[file]["extension"]):
                                os.remove('een/web/static/uploads/' + file + d.files[file]["extension"])
                self._repository.delete(key)
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})

    def _update_model(self, model, data):
        pass

    def _has_permission(self, kind):
        # No permission specified, so everything is allowed
        if self.__override_permission and self.__override_permission in self._permission:
            return True

        if not self._permission:
            return True
        else:
            return has_permission("{}.{}".format(self._permission, kind))

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
            "allow_edit": self._has_permission("update"),
            "row_class": self._row_class
        }

    @staticmethod
    def __row_class(model):
        return ""

    def _extend(self, model):
        return {}
