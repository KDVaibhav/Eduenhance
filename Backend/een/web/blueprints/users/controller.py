from flask import jsonify, flash
from localstorage import getSchool
import os
import json

from een.db import roles, users, lastids, classes, subjects
from een.web.blueprints.crud_controller import CrudController
from een.web.app.auth import has_permission
from uniqueid import getUniqueId

class UsersController(CrudController):
    def __init__(self):
        super().__init__(users(getSchool()), namespace="users", columns=["name", "role"], row_class=self.__row_class)

    def _update_model(self, model, data, files):
        
        role = model.role if model else data.get("role", None)
        if (role != "Superadmin") and ((not model) or (model.role != role)):
            model.role = role
            lastidsRepo = lastids(getSchool())
            lidmodel = lastidsRepo.find_one({"role": model.role})
            if lidmodel:
                id = lidmodel.lid
                lidmodel.lid += 1
                lastidsRepo.save(lidmodel)
            else:
                id = 0
                lastidsRepo.insert({"role": model.role, "lid": 1})
            if model.role == "Teacher":
                model.login = "TE-{0:05d}".format(id+1)
            elif model.role == "Student":
                model.login = "ST-{0:06d}".format(id+1)
            elif model.role == "Principal":
                model.login = "PR-{0:02d}".format(id+1)
            elif model.role == "Accountant":
                model.login = "AC-{0:02d}".format(id+1)
            elif model.role == "Supervisor":
                model.login = "SV-{0:02d}".format(id+1)
            else:
                model.login = "OT-{0:03d}".format(id+1)
            
        model.name = data.get("name", None)
        model.password = data.get("password", "")
        model.dob = data.get("dob", None)
        model.gender = data.get("gender", None)
        model.blgroup = data.get("blgroup", None)
        model.mobile = data.get("mobile", None)
        model.email = data.get("email", None)
        model.category = data.get("category", None)
        model.address = data.get("address", None)
        model.address_current = data.get("address_current", None)
        
        if model.role == "Teacher":
            model.aadhar = data.get("aadhar", None)
            model.pan = data.get("pan", None)
            model.voterid = data.get("voterid", None)
            model.doj = data.get("doj", None)
            nq = range(len(data.getlist("q_year[]")))
            model.qualifications = list(map(lambda i: {
                "q": data.getlist("q[]")[i],
                "q_university": data.getlist("q_university[]")[i],
                "q_degree": data.getlist("q_degree[]")[i],
                "q_year": data.getlist("q_year[]")[i],
                "q_percentage": data.getlist("q_percentage[]")[i],
                "q_subject": data.getlist("q_subject[]")[i]
            }, nq))
            model.emergency = {
                "name": data.get("emergency_name", ""),
                "phone": data.get("emergency_phone", ""),
                "address": data.get("emergency_address", "")
            }
            model.bank = {
                "number": data.get("bank_number", ""),
                "ifsc": data.get("bank_ifsc", ""),
                "name": data.get("bank_name", "")
            }
            model.guardian = {
                "name": data.get("guardian_name", ""),
                "phone": data.get("guardian_phone", ""),
                "email": data.get("guardian_email", ""),
                "address": data.get("guardian_address", "")
            }
        
        if model.role == "Student":
            model['class'] = data.get("class", None)
            model.aadhar = data.get("aadhar", None)
            model.doj = data.get("doj", None)
            nq = range(len(data.getlist("q_year[]")))
            model.emergency = {
                "name": data.get("emergency_name", ""),
                "phone": data.get("emergency_phone", ""),
                "address": data.get("emergency_address", "")
            }
            model.guardian = {
                "name": data.get("guardian_name", ""),
                "phone": data.get("guardian_phone", ""),
                "email": data.get("guardian_email", ""),
                "address": data.get("guardian_address", "")
            }
        
        if 'photo' in files:
            photo = files.get('photo')
            id = getUniqueId()
            if photo.filename:
                extension = os.path.splitext(photo.filename)[1]
                if extension in ['.jpeg', '.jpg', '.png']:
                    idname = id + extension
                    photo.save(os.getcwd() + "/een/web/static/uploads/" + idname)
                    model.photo = idname
                else:
                    flash("Image type is not supported. Only upload jpg or png image.", category="danger")

        if 'sign' in files:
            sign = files.get('sign')
            id = getUniqueId()
            if sign.filename:
                extension = os.path.splitext(sign.filename)[1]
                if extension in ['.jpeg', '.jpg', '.png']:
                    idname = id + extension
                    sign.save(os.getcwd() + "/een/web/static/uploads/" + idname)
                    model.sign = idname
                else:
                    flash("Image type is not supported. Only upload jpg or png image.", category="danger")
        if 'files[]' in files:
            fls = files.getlist('files[]')
            for fl in fls:
                id = getUniqueId()
                if not fl.filename:
                    break
                ext = os.path.splitext(fl.filename)[1]
                fl.save(os.getcwd() + "/een/web/static/uploads/" + id + ext)
                viewname = os.path.splitext(fl.filename)[0]
                if not 'files' in model.keys():
                    model.files = {}
                model.files[id] = {
                    "viewname": viewname,
                    "extension": ext
                }

        model.suspend = {
            "value": False if data.get("enrolled", False) else True,
            "reason": data.get("suspend-reason", None)
        }

    def _extend(self, model):
        role_docs = roles(getSchool()).all()
        role_view = [] #list(map(lambda x: x.name, role_docs))
        if model:
            for x in role_docs:
                if has_permission("{}.update".format(x.name.lower())) and (has_permission("{}.create".format(x.name.lower())) or (x.name == model.role)):
                    role_view.append(x.name)
        else:
            for x in role_docs:
                if has_permission("{}.create".format(x.name.lower())):
                    role_view.append(x.name)
        with open("data.json") as f:
            data = json.load(f)
        class_view = sorted(classes(getSchool()).all(), key = lambda x: x.name)
        subject_view = subjects(getSchool()).all()
        category_view = data["categories"]
        blgroup_view = data["blood_groups"]
        return {
            "roles": role_view, 
            "classes": list(map(lambda x: x.name, class_view)), 
            "subjects": list(map(lambda x: x.name, subject_view)),
            "blgroups": blgroup_view,
            "categories": category_view
        }

    def deleteFile(self, request, key, fileid):
        if self._has_permission('update'):
            entity = self._repository.get(key)
            if entity:
                for id in entity.files.keys():
                    if id != fileid:
                        continue
                    if os.path.exists(os.getcwd() + "/een/web/static/uploads/" + fileid + entity.files[fileid]["extension"]):
                        os.remove(os.getcwd() + "/een/web/static/uploads/" + fileid + entity.files[fileid]["extension"])
                    del entity.files[fileid]
                    self._repository.save(entity)
                    return jsonify({"success": True})
                
        return jsonify({"success": False})

    @staticmethod
    def __row_class(model):
        is_suspended = model.get("suspend", {}).get("value", False) is True
        return "danger" if is_suspended else None
