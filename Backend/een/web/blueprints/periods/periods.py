from flask import Blueprint, request

from .controller import PeriodsController

periods = Blueprint("periods", __name__, template_folder=".")


@periods.route("/")
def index():
    controller = PeriodsController()
    return controller.index()


@periods.route("/new", methods=["GET", "POST"])
def create():
    controller = PeriodsController()
    return controller.create(request)


@periods.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    controller = PeriodsController()
    return controller.update(request, key)
