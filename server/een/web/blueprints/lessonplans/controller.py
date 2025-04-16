from flask import render_template, flash, redirect
from flask.json import jsonify
from flask_login.utils import login_required
import json, os, urllib.parse

from een.db import lessonplans, classes, subjects
from een.web.app.auth import access_denied, has_permission
from localstorage import getSchool
from uniqueid import getUniqueId


class LessonplansController():
    def __init__(self):
        """Initializes new instance of the Lessonplans Controller class"""
        self._repository = lessonplans(getSchool())
        self._namespace = "lessonplans"
        self._model_name = "lessonplans"
        self._permission = "lessonplans"
        self._html = "lessonplans_view.html"
        self._url = "lessonplans"

    @login_required
    def index(self):
        if (not has_permission("lessonplans.read")) and (not has_permission("lessonplans.update")):
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
        params = {}
        if has_permission("lessonplans.read"):
            params['models'] = json.dumps(models)
        return render_template("crud/index_special.html", **params, **self.__options(), **self._extend(None))

    @login_required
    def update(self, request):
        """Shows user."""
        if request.method == "POST":
            if has_permission("lessonplans.update"):
                d = self._repository.all()[0]
                subject = request.form.get("subject", "")
                class_ = request.form.get("class", "")
                nq = range(len(request.form.getlist("chapter")))
                def get_attach(name, model):
                    fls = request.files.getlist(name)
                    if not ('attach' in model.keys() and model['attach']):
                        model['attach'] = {}
                    for fl in fls:
                        id = getUniqueId()
                        if not fl.filename:
                            break
                        ext = os.path.splitext(fl.filename)[1]
                        fl.save(os.getcwd() + "/een/web/static/uploads/" + id + ext)
                        viewname = os.path.splitext(fl.filename)[0]
                        model['attach'][id] = {
                            "viewname": viewname,
                            "extension": ext
                        }
                    return model['attach']
                if not class_ in d.keys():
                    d[class_] = {}
                d[class_][subject] = list(map(lambda i: {
                        "chapter": request.form.getlist("chapter")[i],
                        "plan": request.form.getlist("plan")[i],
                        "attach": get_attach("attach-"+str(i)+"[]", d[class_][subject][i] if (subject in d[class_].keys()) and (i < len(d[class_][subject])) else {})
                }, nq))
                
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
            "allow_edit": has_permission("lessonplans.update")
        }

    def deleteFile(self, request):
        if has_permission('lessonplans.update'):
            entity = self._repository.all()[0]
            data = dict(urllib.parse.parse_qsl(request.data.decode("utf-8")))
            class_ = data['class_']
            subject = data['subject']
            key = int(data['key'])
            fileid = data['fileid']
            chapter = entity[class_][subject][key]
            for id in chapter['attach'].keys():
                if id != fileid:
                    continue
                if os.path.exists(os.getcwd() + "/een/web/static/uploads/" + fileid + chapter['attach'][fileid]["extension"]):
                    os.remove(os.getcwd() + "/een/web/static/uploads/" + fileid + chapter['attach'][fileid]["extension"])
                del entity[class_][subject][key]['attach'][fileid]
                self._repository.save(entity)
            return jsonify({"success": True})
                
        return jsonify({"success": False})

    def deleteChapter(self, request):
        if has_permission('lessonplans.update'):
            entity = self._repository.all()[0]
            data = dict(urllib.parse.parse_qsl(request.data.decode("utf-8")))
            class_ = data['class_']
            subject = data['subject']
            key = int(data['key'])
            if (subject in entity[class_].keys()) and (len(entity[class_][subject]) > key):
                chapter = entity[class_][subject][key]
                for id in chapter['attach'].keys():
                    if os.path.exists(os.getcwd() + "/een/web/static/uploads/" + id + chapter['attach'][id]["extension"]):
                        os.remove(os.getcwd() + "/een/web/static/uploads/" + id + chapter['attach'][id]["extension"])
                del entity[class_][subject][key]
                self._repository.save(entity)
            return jsonify({"success": True})
                
        return jsonify({"success": False})