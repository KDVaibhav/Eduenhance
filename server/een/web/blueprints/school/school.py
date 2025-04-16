import json
from flask import Blueprint, request, jsonify
from .controller import SchoolController
school = Blueprint("school", __name__, template_folder=".")


@school.route("/")
def index():
    controller = SchoolController()
    return controller.index()


@school.route("/new", methods=["GET", "POST"])
def create():
    controller = SchoolController()
    return controller.create(request)


@school.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    controller = SchoolController()
    return controller.update(request, key)

# New endpoint to fetch schools for login
@school.route("/getSchools", methods=["GET"])
def get_schools():
    try:
        with open("local/config.json", "r") as f:
            sch = json.load(f)
        schools = [{'id': k, 'name': v['name']} for k, v in sch.items()]
        return jsonify(success=True, schools=schools), 200
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500