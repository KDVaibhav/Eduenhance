from flask import Blueprint, request
import os
from flask import json

from flask.json import jsonify

from een.web.app.auth import has_permission
from een.web.blueprints.users.controller import UsersController

users = Blueprint("users", __name__, template_folder=".")



@users.route("/")
def index():
    controller = UsersController()
    return controller.index()


@users.route("/new", methods=["GET", "POST"])
def create():
    controller = UsersController()
    return controller.create(request)


@users.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    controller = UsersController()
    return controller.update(request, key)

@users.route("/<string:key>/<string:fileid>", methods=["DELETE"])
def deleteFile(key, fileid):
    controller = UsersController()
    return controller.deleteFile(request, key, fileid)

@users.route("/get_files", methods=['GET'])
def get_files():
    pastIds = os.listdir(os.getcwd() + "/een/web/static/uploads/")
    school_details = json.load(open(os.getcwd() + "/local/config.json"))
    return jsonify({"files": pastIds, "school": school_details}) 
    
    