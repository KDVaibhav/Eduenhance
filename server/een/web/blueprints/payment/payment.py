from flask import Blueprint, request

from .controller import PaymentController

payment = Blueprint("payment", __name__, template_folder=".")


@payment.route("/", methods=["GET", "POST"])
def index():
    controller = PaymentController()
    if request.method == "GET": 
        return controller.index()
    if request.method == "POST": 
        return controller.update(request)

@payment.route("/new", methods=["GET", "POST"])
def create():
    controller = PaymentController()
    return controller.create(request)

@payment.route("/<string:key>", methods=["GET", "POST", "DELETE"])
def update(key):
    controller = PaymentController()
    return controller.update(request, key)

@payment.route("/dul", methods=["POST"])
def dul():
    controller = PaymentController()
    return controller.dul(request)