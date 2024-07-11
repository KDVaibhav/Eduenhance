from flask_login import current_user
import json
from een.db import sessions, articles
from localstorage import getSchool
from flask import Blueprint, render_template

index = Blueprint("index", __name__, template_folder=".")

@index.route("/", methods=["GET", "POST"])
def index_index():
    with open("local/config.json", "r") as f:
        sch = json.load(f)
    welcome1 = articles(getSchool()).find_one({"name": "welcome1"})
    welcome2 = articles(getSchool()).find_one({"name": "welcome2"})
    welcome3 = articles(getSchool()).find_one({"name": "welcome3"})
    return render_template("index_index.html",
                            schools=list(map(lambda x: (x, sch[x]['name']), sch.keys())),
                           upcoming_sessions=__upcoming_sessions_for_user(current_user),
                           active_sessions=__active_sessions_for_user(current_user),
                           welcome1=welcome1, welcome2=welcome2, welcome3=welcome3)


def __upcoming_sessions_for_user(user):
    if user and hasattr(user, "role"):
        upcoming = sessions(getSchool()).upcoming()
        result = filter(lambda x: x.get("status", None) != "run", upcoming)
        return list(result)[:5]
    return []

def __active_sessions_for_user(user):
    if user and hasattr(user, "role"):
        upcoming = sessions(getSchool()).active()
        return list(upcoming)[:3]
    return []