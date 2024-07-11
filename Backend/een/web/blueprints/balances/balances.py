from flask import Blueprint, request

from .controller import BalancesController

balances = Blueprint("balances", __name__, template_folder=".")


@balances.route("/", methods=["GET", "POST"])
def index():
    controller = BalancesController()
    if request.method == "GET": 
        return controller.index()
