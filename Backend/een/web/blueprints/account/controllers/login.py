from flask import flash, redirect, render_template, request, jsonify, make_response
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
            remember = data.get("remember", False) == "on"
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
                flash("Successfully logged in")
                # response = make_response(jsonify({"message": "You have successfully logged in", "user": user, "status code": 201}))
                # response.set_cookie('school', school)
                return redirect("/account")
            else:
                flash("incorrect credentials")
                return jsonify({"error": "User with specified login/password pair not found"}), 401


    def logout(self):
        logout_user()
        flash("You have successfully logged out", category="success")
        return redirect("/")
