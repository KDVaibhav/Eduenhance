from flask import Blueprint, request

from .controller import ClassesController

classes = Blueprint("classes", __name__, template_folder=".")


@classes.route("/")
def index():
    controller = ClassesController()
    return controller.index()


@classes.route("/new", methods=["GET", "POST"])
def create():
    controller = ClassesController()
    return controller.create(request)


@classes.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    controller = ClassesController()
    return controller.update(request, key)
