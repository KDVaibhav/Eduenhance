from attr import has
from flask import jsonify, render_template, flash, redirect
from flask_login.utils import login_required, current_user
import json
from datetime import date, datetime
from pytz import timezone
import numpy as np
import pandas as pd

from een.db import marks, users, exams, classes, subjects
from een.web.app.auth import access_denied, has_permission
from localstorage import getSchool


class MarksController():
    def __init__(self):
        """Initializes new instance of the Marks Controller class"""
        self._repository = marks(getSchool())
        self._namespace = "marks"
        self._model_name = "Marks"
        self._permission = "marks"
        self._html = "marks_view.html"
        self._url = "marks"

    @login_required
    def index(self):
        if (not has_permission("marks.read_all")) and (not has_permission("marks.read_own")) and (not has_permission("marks.update")):
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
        exams_models = exams(getSchool()).all()
        exams_models_js = {}
        students = list(map(lambda x: {"name": x.name, "login": x.login, "class": x["class"]}, users(getSchool()).find({"role": "Student", "suspend.value": False})))
        for i in range(len(exams_models)):
            exams_models[i]['_id'] = str(exams_models[i]['_id'])
            exams_models_js[exams_models[i]['_id']] = exams_models[i]['name']
        params = {}
        if has_permission("marks.read_all") or has_permission("marks.update"):
            params['students'] = json.dumps(students)
            params['exams'] = exams_models
            params['exams_js'] = json.dumps(exams_models_js)
            params['models'] = json.dumps(models)
        if has_permission("marks.read_own"):
            params['model_class'] = models[current_user.class_] if current_user.class_ in models.keys() else None
            params['model_class_js'] = json.dumps(params['model_class'])
            params['mysubjects'] = classes(getSchool()).find_one({'name': current_user.class_}).subjects
            params['exams'] = exams_models
            params['roll'] = current_user.login
        return render_template("crud/index_special.html", **params, **self.__options(), **self._extend(None))

    @login_required
    def update(self, request):
        """Shows user."""
        if request.method == "POST":
            if has_permission("marks.update"):
                d = self._repository.all()[0]
                subject = request.form.get("subject", "")
                class_ = request.form.get("class", "")
                examid = request.form.get("examid", "")
                if not class_ in d.keys():
                    d[class_] = {}
                if not subject in d[class_].keys():
                    d[class_][subject] = {}
                students = users(getSchool()).find({'role': 'Student', 'class': class_})
                now = datetime.now(timezone('Asia/Kolkata'))
                sl = {
                    "total": request.form.get("total"),
                    "uploaded_at": [
                        now.year,
                        now.month,
                        now.day,
                        now.hour,
                        now.minute
                    ]
                }
                for s in students:
                    sl[s["login"]] = request.form.get(s["login"], 0)
                d[class_][subject][examid] = sl
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
            "allow_edit": has_permission("marks.update"),
            "allow_view": has_permission("marks.read_all")
        }

    @login_required
    def comparison(self, request, subject):
        if not has_permission('marks.comparison'):
            return "Access denied"
        students = users(getSchool()).find({'role': "Student", "suspend.value": False}, {'_id': 0, "name": 1, 'login': 1, 'class': 1})
        marks_all = self._repository.find_one({}, {"_id": 0})
        
        # Internal functions
        def students_of_class(c):
            return list(filter(lambda e: e['class'] == str(c), students))
        
        def get_marks_of_students(class_, subject):
            marks_object = {"Total": [], "Type": []}
            s_list = students_of_class(class_)
            for s in s_list:
                marks_object[s.login] = []
            for t in marks_all[str(class_)][subject].values():
                e = t.copy()
                fm = int(e['total'])
                del e['total']
                del e['uploaded_at']
                marks_object["Total"].append(fm)
                marks_object["Type"].append("Weekly" if fm == 10 else "Unit")
                for s in s_list:
                    try:
                        marks_object[s.login].append(float(e[s.login]))
                    except:
                        marks_object[s.login].append(None)
            
            df = pd.DataFrame(marks_object)
            #return df
            del marks_object['Total']
            del marks_object['Type']
            ret = []
            for s in s_list:
                #print(s.login)
                m = df.loc[df[s.login].notnull(), ['Total', 'Type', s.login]].groupby('Type').sum()
                if m['Total'].empty:
                    del marks_object[s.login]
                else:
                    try:
                        x = (m[s.login]['Weekly'] / m['Total']['Weekly'] * 10 + m[s.login]['Unit'] / m['Total']['Unit'] * 20) / 0.3
                    except:
                        try:
                            x = m[s.login]['Weekly'] / m['Total']['Weekly'] * 100
                        except:
                            x = m[s.login]['Unit'] / m['Total']['Unit'] * 100
                    marks_object[s.login] = x
                    ret.append(x)
            return sum(ret)/len(ret)
        cs = self._extend(None)['classes']
        return_object = {}
        for cl in cs:
            c = int(cl)
            try:
                current = get_marks_of_students(c, subject)
                last = pd.read_csv('een/web/blueprints/marks/lastyear.csv', index_col='Class').loc[c][subject]
                if np.isnan(last):
                    continue
                return_object[cl] = {"current": current, "last": last}
            except:
                continue

        return jsonify(return_object)