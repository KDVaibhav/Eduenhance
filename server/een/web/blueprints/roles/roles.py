from flask import Blueprint, request

from .controller import RolesController

roles = Blueprint("roles", __name__, template_folder=".")


@roles.route("/")
def index():
    controller = RolesController()
    return controller.index()


@roles.route("/new", methods=["GET", "POST"])
def create():
    controller = RolesController()
    return controller.create(request)


@roles.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    controller = RolesController()
    return controller.update(request, key)
