from flask import flash, redirect, render_template, request
from flask_login import logout_user, login_user
import json

from een.db import users
from een.web.app.auth import User
from localstorage import setSchool


class LoginController:
    def login(self):
        if request.method == "GET":
            with open("local/config.json", "r") as f:
                sch = json.load(f)
            return render_template("login.html", schools=list(map(lambda x: (x, sch[x]['name']), sch.keys())))

        elif request.method == "POST":
            with open("local/config.json", "r") as f:
                sch = json.load(f)
            data = request.form
            lgn = data.get("login", None)
            password = data.get("password", None)
            remember = data.get("remember-me", False) == "on"
            school = data.get("school", "")
            if not school:
                flash("Please select a school.", category="danger")
                return render_template("login.html", schools=list(map(lambda x: (x, sch[x]['name']), sch.keys())))

            user = users(school).find_one(
                {"$and": [{"password": password}, {"$or": [{"login": lgn}, {"name": lgn}]}]})

            if user:
                setSchool(school)
                u = User(user)
                login_user(u, remember=remember)
                flash("You have successfully logged in", category="success")
                return redirect("/account")
            else:
                flash("User with specified login/password pair not found", category="danger")
                return render_template("login.html", schools=list(map(lambda x: (x, sch[x]['name']), sch.keys())))

    def logout(self):
        logout_user()
        flash("You have successfully logged out", category="success")
        return redirect("/")
