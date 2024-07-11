from flask import Blueprint, request, jsonify

from .controller import LawsController

laws = Blueprint("laws", __name__, template_folder=".")


@laws.route("/")
def index():
    controller = LawsController()
    return controller.index()


@laws.route("/new", methods=["GET", "POST"])
def create():
    controller = LawsController()
    return controller.create(request)


@laws.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    controller = LawsController()
    return controller.update(request, key)
