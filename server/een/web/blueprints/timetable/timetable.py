from flask import Blueprint, request

from .controller import TimetableController

timetable = Blueprint("timetable", __name__, template_folder=".")


@timetable.route("/", methods=["GET", "POST"])
def index():
    controller = TimetableController()
    if request.method == "GET": 
        return controller.index()
    if request.method == "POST": 
        return controller.update(request)
