from flask import Blueprint, request

from .controller import SubjectsController

subjects = Blueprint("subjects", __name__, template_folder=".")


@subjects.route("/")
def index():
    controller = SubjectsController()
    return controller.index()


@subjects.route("/new", methods=["GET", "POST"])
def create():
    controller = SubjectsController()
    return controller.create(request)


@subjects.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    controller = SubjectsController()
    return controller.update(request, key)
