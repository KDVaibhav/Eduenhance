from bson import ObjectId
from flask import Blueprint, request
from flask_login import login_required, current_user

from een.channel.channel import get
from een.web.app.printer.comments import print_comments
from .controller import SessionController

session = Blueprint("session", __name__, template_folder=".")
channel = get()


@session.route("/<string:session_id>")
@login_required
def index(session_id):
    controller = SessionController()
    return controller.index(session_id, current_user)


# Messages -------------------------------------------------------------------------------------------------------------

@channel.on("join")
@login_required
def on_join_message(data):
    controller = SessionController()
    return controller.join(request.sid, current_user.id, data)


@channel.on("chat")
@login_required
def on_chat_message(data):
    controller = SessionController()
    return controller.chat(request.sid, data)


@channel.on("change_stage")
@login_required
def on_change_stage_message(data):
    controller = SessionController()
    return controller.change_stage(request.sid, data)


@channel.on("close")
@login_required
def on_close_message():
    controller = SessionController()
    return controller.close(request.sid)


@channel.on("vote")
@login_required
def on_vote_message(data):
    controller = SessionController()
    return controller.vote(request.sid, data)


@channel.on("comment")
@login_required
def on_comment_message(data):
    controller = SessionController()
    return controller.comment(request.sid, data)


@channel.on("disconnect")
@login_required
def on_disconnect():
    controller = SessionController()
    return controller.disconnect(request.sid)


@channel.on("timer")
@login_required
def on_timer(data):
    controller = SessionController()
    return controller.set_timer(request.sid, data)


@channel.on("manage")
@login_required
def on_manage(data):
    controller = SessionController()
    return controller.manage(request.sid, data)


@channel.on("manage_session")
@login_required
def on_manage_session(data):
    controller = SessionController()
    return controller.manage_session(request.sid, data)


@channel.on("kick")
@login_required
def on_kick(data):
    controller = SessionController()
    return controller.kick(request.sid, data)


@channel.on("print")
@login_required
def on_print(data):
    crt = data["criteria"]
    if "proposal_id" in crt:
        crt["proposal_id"] = ObjectId(crt["proposal_id"])
    return print_comments(current_user, crt)
