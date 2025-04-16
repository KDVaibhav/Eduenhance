from flask import Blueprint, request

from .controller import ExamsController

exams = Blueprint("exams", __name__, template_folder=".")


@exams.route("/")
def index():
    controller = ExamsController()
    return controller.index()


@exams.route("/new", methods=["GET", "POST"])
def create():
    controller = ExamsController()
    return controller.create(request)


@exams.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    controller = ExamsController()
    return controller.update(request, key)
