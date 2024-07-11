from flask import request, render_template, flash, redirect
from flask_login import current_user

from een.db import users
from localstorage import getSchool


class AccountController():
    def edit(self, **kwargs):
        if request.method == "GET":
            return render_template("account_edit.html", **kwargs)

        elif request.method == "POST":
            data = request.form
            d = users(getSchool()).get(current_user.get_id())
            d.password = data.get("password", None) or d.password
            # is_unique = self.__is_user_unique(d)
            # is_all_filled = d.password

            # if is_all_filled and is_unique:
            users(getSchool()).save(d)
            flash("Your account was successfully updated", category="success")
            return redirect("/account")
            # else:
            #     error = \
            #         "User with same login or name already exist" if not is_unique else \
            #         "Not all required fields are filled in" if not is_all_filled else \
            #         "God does not deign"
            #     flash("Your account was not updated: {}".format(error), category="danger")
            #     return redirect("/account")

    @staticmethod
    def __is_user_unique(user):
        return users(getSchool()).count({
            "$or": [
                {"login": user.login},
                {"name": user.name}
            ],
            "_id": {
                "$ne": user["_id"]
            }
        }) == 0
