from flask import Blueprint, request

from .controller import TransactionsController

transactions = Blueprint("transactions", __name__, template_folder=".")


@transactions.route("/")
def index():
    controller = TransactionsController()
    return controller.index()


@transactions.route("/new", methods=["GET", "POST"])
def create():
    controller = TransactionsController()
    return controller.create(request)


@transactions.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    controller = TransactionsController()
    return controller.update(request, key)
