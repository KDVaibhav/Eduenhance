from flask import Blueprint, request

from .controller import AttendanceController

attendance = Blueprint("attendance", __name__, template_folder=".")


@attendance.route("/", methods=["GET", "POST"])
def index():
    controller = AttendanceController()
    if request.method == "GET": 
        return controller.index()
    if request.method == "POST": 
        return controller.update(request)
