from flask import Blueprint, request

from .controller import LeaveController

leave = Blueprint("leave", __name__, template_folder=".")


@leave.route("/", methods=["GET", "POST"])
def index():
    controller = LeaveController()
    if request.method == "GET": 
        return controller.index()
    if request.method == "POST": 
        return controller.update(request)

@leave.route("/new", methods=["GET", "POST"])
def apply():
    controller = LeaveController()
    return controller.apply(request)

@leave.route("/<string:key>", methods=["GET", "POST", "DELETE", "PUT"])
def update(key):
    controller = LeaveController()
    return controller.update(request, key)