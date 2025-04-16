from flask import Blueprint, request

from een.web.blueprints.sessions.controller import SessionsController

sessions = Blueprint("sessions", __name__, template_folder=".")


@sessions.route("/")
def index():
    controller = SessionsController()
    return controller.index()


@sessions.route("/new", methods=["GET", "POST"])
def create():
    controller = SessionsController()
    return controller.create(request)


@sessions.route("/<string:key>", methods=["GET", "POST", "DELETE", "PUT"])
def update(key):
    controller = SessionsController()
    if request.method == "PUT":
        return controller.run(request, key)
    else:
        return controller.update(request, key)
