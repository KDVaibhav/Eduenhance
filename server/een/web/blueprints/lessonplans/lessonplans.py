from flask import Blueprint, request, jsonify

from .controller import LessonplansController

lessonplans = Blueprint("lessonplans", __name__, template_folder=".")


@lessonplans.route("/", methods=['GET', 'POST'])
def index():
    controller = LessonplansController()
    if request.method == "GET": 
        return controller.index()
    if request.method == "POST": 
        return controller.update(request)

@lessonplans.route("/deletefile/", methods=["DELETE"])
def deleteFile():
    controller = LessonplansController()
    return controller.deleteFile(request)


@lessonplans.route("/deletechapter/", methods=["DELETE"])
def deleteChapter():
    controller = LessonplansController()
    return controller.deleteChapter(request)
