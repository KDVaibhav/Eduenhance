from een.channel.channel import get
from flask import render_template, flash, redirect
from flask_login.utils import login_required, current_user
import json

from een.db import timetable, classes, users, periods
from een.db.core.model import Model
from een.web.app.auth import access_denied, has_permission
from localstorage import getSchool


class TimetableController():
    def __init__(self):
        """Initializes new instance of the Attendance Controller class"""
        self._repository = timetable(getSchool())
        self._namespace = "timetable"
        self._model_name = "timetable"
        self._permission = "timetable"
        self._html = "timetable_view.html"
        self._url = "timetable"

    @login_required
    def index(self):
        if (not has_permission("timetable.read_all")) and (not has_permission("timetable.read_own")) and (not has_permission("timetable.update")):
            return access_denied()
        models = self._repository.all()
        for i in range(len(models)):
            del models[i]['_id']
        models = dict(map(lambda x: (x['class_'], x.get('timetable', "")), models))
        params = {}
        teachers = list(map(lambda x: {"name": x.name, "login": x.login}, users(getSchool()).find({"role": "Teacher"})))
        params['teachers'] = teachers
        params['teachers_js'] = json.dumps(teachers)
        if has_permission("timetable.read_all"):
            params['models'] = models
        if has_permission("timetable.read_own"):
            params['model_class'] = models[current_user.class_] if current_user.class_ in models.keys() else None
            params['class_'] = current_user.class_
        return render_template("crud/index_special.html", **params, **self.__options(), **self._extend(None))

    @login_required
    def update(self, request):
        """Shows user."""
        if request.method == "POST":
            if has_permission("timetable.update"):
                ds = self._repository.all()
                if not ds:
                    for class_ in self._extend(None)['classes']:
                        d = Model()
                        d.class_ = class_
                        self._update_model(request.form, d)
                        self._repository.insert(d)
                else:
                    for d in ds:
                        self._update_model(request.form, d)
                        self._repository.save(d)

                flash("{} was successfully updated".format(self._model_name), category="success")
                return redirect("/" + self._url)
            else:
                return access_denied()

    def _update_model(self, data, model):
        model.timetable = {}
        for day in self._extend(None)['days']:
            model.timetable[day] = []
            teachers = data.getlist("teacher-"+model.class_+"-"+day)
            subjects = data.getlist("subject-"+model.class_+"-"+day)
            for i in range(len(teachers)):
                model.timetable[day].append({
                    "teacher": teachers[i],
                    "subject": subjects[i]
                })

    def _extend(self, model):
        c = sorted(classes(getSchool()).all(), key = lambda x: x.name)
        return {
            "classes": list(map(lambda x: x.name, c)),
            "subjects": dict(map(lambda x: (x['name'], x['subjects']), c)),
            "subjects_js": json.dumps(dict(map(lambda x: (x['name'], x['subjects']), c))),
            "days": ['Mon', "Tue", "Wed", "Thu", "Fri", "Sat"],
            "periods": periods(getSchool()).all(),
            "n": len(periods(getSchool()).all())
        }

    def __options(self):
        return {
            "index": self._html,
            "active_page": self._namespace,
            "url": self._url,
            "model_name": self._model_name,
            "namespace": self._namespace,
            "allow_edit": has_permission("timetable.update"),
            "allow_view": has_permission("timetable.read_all")
        }