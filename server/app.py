import os
from flask import Flask, redirect, request, current_app, send_from_directory
from flask_login import LoginManager, current_user
from flask_cors import CORS

from een.channel import init
from een.db import users as users_db
from een.web.app.auth import User, has_permission, access_denied
from een.web.app.json_encoder import EenJsonEncoder
from een.web.blueprints.admin import admin
from een.web.blueprints.proposals import proposals
from een.web.blueprints.sessions import sessions
from een.web.blueprints.users import users
from een.web.blueprints.roles import roles
from een.web.blueprints.index import index
from een.web.blueprints.laws import laws
from een.web.blueprints.school import school
from een.web.blueprints.timetable import timetable
from een.web.blueprints.periods import periods
from een.web.blueprints.attendance import attendance
from een.web.blueprints.exams import exams
from een.web.blueprints.subjects import subjects
from een.web.blueprints.classes import classes
from een.web.blueprints.marks import marks
from een.web.blueprints.lessonplans import lessonplans
from een.web.blueprints.transactions import transactions
from een.web.blueprints.balances import balances
from een.web.blueprints.leave import leave
from een.web.blueprints.payment import payment
from een.web.blueprints.news import news
from een.web.blueprints.search import search
from localstorage import getSchool


app = Flask(__name__,
            template_folder="een/web/templates",
            static_folder="een/web/static")
app.secret_key = 'some_secret'
app.debug = True
app.json_encoder = EenJsonEncoder
channel = init(app)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

from een.web.blueprints.account import account
from een.web.blueprints.session import session

login_manager = LoginManager()

app.register_blueprint(index)
app.register_blueprint(proposals, url_prefix="/proposals")
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(roles, url_prefix="/roles")
app.register_blueprint(sessions, url_prefix="/sessions")
app.register_blueprint(account, url_prefix="/account")
app.register_blueprint(session, url_prefix="/session")
app.register_blueprint(laws, url_prefix="/laws")
app.register_blueprint(school, url_prefix="/school")
app.register_blueprint(timetable, url_prefix="/timetable")
app.register_blueprint(periods, url_prefix="/periods")
app.register_blueprint(attendance, url_prefix="/attendance")
app.register_blueprint(exams, url_prefix="/exams")
app.register_blueprint(subjects, url_prefix="/subjects")
app.register_blueprint(classes, url_prefix="/classes")
app.register_blueprint(marks, url_prefix="/marks")
app.register_blueprint(lessonplans, url_prefix="/lessonplans")
app.register_blueprint(transactions, url_prefix="/transactions")
app.register_blueprint(balances, url_prefix="/balances")
app.register_blueprint(leave, url_prefix="/leave")
app.register_blueprint(payment, url_prefix="/payment")
app.register_blueprint(news, url_prefix="/news")
app.register_blueprint(search, url_prefix="/search")
app.register_blueprint(admin, url_prefix="/admin")

login_manager.init_app(app)
login_manager.login_view = "account.login"
login_manager.login_message_category = "info"

if __name__ == "__main__":
    channel.run(app)

@app.route('/files/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, "files")
    return send_from_directory(directory=uploads, filename=filename, as_attachment=True)


@app.before_request
def before_request():
    if not current_user:
        return

    if not hasattr(current_user, "suspended"):
        return

    if current_user.suspended and request.path not in ["/account/logout"]:
        return access_denied("Your account has been suspended. Reason: " + current_user.suspend_reason)

    if not current_user.password and request.path not in ["/account/setup", "/account/logout"]:
        return redirect("/account/setup")


@app.add_template_global
def user_has_permission(permission):
    return has_permission(permission)


@login_manager.user_loader
def load_user(user_id):
    sch = getSchool()
    user = users_db(sch).get(user_id)
    if user:
        u = User(user)
        return u
    return None
