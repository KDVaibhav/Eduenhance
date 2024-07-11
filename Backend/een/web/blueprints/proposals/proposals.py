from flask import Blueprint, request, jsonify

from .controller import ProposalsController

proposals = Blueprint("proposals", __name__, template_folder=".")


@proposals.route("/")
def index():
    controller = ProposalsController()
    return controller.index()


@proposals.route("/new", methods=["GET", "POST"])
def create():
    controller = ProposalsController()
    return controller.create(request)


@proposals.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    controller = ProposalsController()
    return controller.update(request, key)


@proposals.route("/search")
def search():
    controller = ProposalsController()
    return jsonify(controller.search(request))
