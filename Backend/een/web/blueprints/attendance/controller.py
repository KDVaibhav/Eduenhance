from flask import render_template, flash, redirect
from flask_login.utils import login_required, current_user
import json
from datetime import date, datetime
from pytz import timezone

from een.db import attendance, users, classes, subjects
from een.web.app.auth import access_denied, has_permission
from .get_dates import get_dates
from localstorage import getSchool


class AttendanceController():
    def __init__(self):
        """Initializes new instance of the Attendance Controller class"""
        self._repository = attendance(getSchool())
        self._namespace = "attendance"
        self._model_name = "Attendance"
        self._permission = "attendance"
        self._html = "attendance_view.html"
        self._url = "attendance"
        today = date.today()
        self._today = "{0:04d}".format(today.year) + "-" + "{0:02d}".format(today.month) + "-" + "{0:02d}".format(today.day)

    @login_required
    def index(self):
        if (not has_permission("attendance.read_all")) and (not has_permission("attendance.read_own")) and (not has_permission("attendance.update")):
            return access_denied()
        models = self._repository.all()
        if models:
            models = models[0]
            del models['_id']
        else:
            models = {}
            for class_ in list(map(lambda x: x.name, sorted(classes(getSchool()).all(), key = lambda x: x.name))):
                models[class_] = {}
            self._repository.insert(models)
            del models['_id']
        students = list(map(lambda x: {"name": x.name, "login": x.login, "class": x["class"]}, users(getSchool()).find({"role": "Student", "suspend.value": False})))
        params = {}
        if has_permission("attendance.read_all") or has_permission("attendance.update"):
            params['models'] = json.dumps(models)
            params['students'] = json.dumps(students)
        if has_permission("attendance.read_own"):
            params['model_class'] = models[current_user.class_] if current_user.class_ in models.keys() else None
            params['model_class_js'] = json.dumps(params['model_class'])
            params['roll'] = current_user.login
            params['mysubjects'] = classes(getSchool()).find_one({'name': current_user.class_}).subjects
            params['dates'] = get_dates()
            params['dates_js'] = json.dumps(params['dates'])
            params['month_now'] = list(params['dates'].keys())[0]
        return render_template("crud/index_special.html", **params, **self.__options(), **self._extend(None))

    @login_required
    def update(self, request):
        """Shows user."""
        if request.method == "POST":
            if has_permission("attendance.update"):
                d = self._repository.all()[0]
                subject = request.form.get("subject", "")
                class_ = request.form.get("class", "")
                date = request.form.get("date", "")
                if not class_ in d.keys():
                    d[class_] = {}
                if not subject in d[class_].keys():
                    d[class_][subject] = {}
                students = users(getSchool()).find({'role': 'Student', 'class': class_})
                sl = map(lambda x: x["login"], students)
                sl = list(filter(lambda x: request.form.get(x, False), sl))
                now = datetime.now(timezone('Asia/Kolkata'))
                d[class_][subject][date] = {
                    "taken_at": [now.hour, now.minute, now.second],
                    "attendance": sl
                }
                self._repository.save(d)

                flash("{} was successfully updated".format(self._model_name), category="success")
                return redirect("/" + self._url)
            else:
                return access_denied()

    def _extend(self, model):
        return {
            "classes": list(map(lambda x: x.name, sorted(classes(getSchool()).all(), key = lambda x: x.name))), 
            "subjects": list(map(lambda x: x.name, subjects(getSchool()).all())),
            "subjects_js": json.dumps(dict(map(lambda x: (x['name'], x['subjects']), sorted(classes(getSchool()).all(), key = lambda x: x.name))))
        }

    def __options(self):
        return {
            "index": self._html,
            "active_page": self._namespace,
            "url": self._url,
            "model_name": self._model_name,
            "namespace": self._namespace,
            "today": self._today,
            "allow_edit": has_permission("attendance.update"),
            "allow_view": has_permission("attendance.read_all")
        }