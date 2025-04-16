from flask import Blueprint, request

from .controller import NewsController

news = Blueprint("news", __name__, template_folder=".")


@news.route("/")
def index():
    controller = NewsController()
    return controller.index()


@news.route("/new", methods=["GET", "POST"])
def create():
    controller = NewsController()
    return controller.create(request)


@news.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    controller = NewsController()
    return controller.update(request, key)
