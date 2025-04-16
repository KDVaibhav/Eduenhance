from flask import Blueprint, request

from .controller import MarksController

marks = Blueprint("marks", __name__, template_folder=".")


@marks.route("/", methods=["GET", "POST"])
def index():
    controller = MarksController()
    if request.method == "GET": 
        return controller.index()
    if request.method == "POST": 
        return controller.update(request)

@marks.route("/comparison/<string:s>", methods=["GET"])
def comparison(s):
    controller = MarksController()
    return controller.comparison(request, s)