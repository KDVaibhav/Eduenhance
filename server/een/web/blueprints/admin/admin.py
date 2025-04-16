from flask import Blueprint, request

from .controller import AdminController

admin = Blueprint("admin", __name__, template_folder=".")


@admin.route("/")
def index():
    controller = AdminController()
    return controller.index()


@admin.route("/new", methods=["GET", "POST"])
def create():
    controller = AdminController()
    return controller.create(request)


@admin.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    controller = AdminController()
    return controller.update(request, key)
