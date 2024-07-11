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
