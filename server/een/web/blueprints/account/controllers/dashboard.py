import itertools
from datetime import date
from flask import render_template, flash
from flask_login import login_required, current_user

from een.db import news, proposals, sessions, users, subjects
from een.web.app.auth import has_permission
from localstorage import getSchool

class DashboardController:
    @login_required
    def index(self):
        # Birthday
        dateNow = date.today()
        all_users = users(getSchool()).all()
        birthday_users = []
        for user in all_users:
            if not ('dob' in user.keys() and user.dob):
                continue
            y, m, d = self._format_date(user.dob)
            dateBirth = date(y, m, d)
            if (dateNow.day != dateBirth.day) or (dateNow.month != dateBirth.month):
                continue
            
            if current_user.id == str(user._id):
                flash("Wishing you a very happy birthday.", category="birthday")
            else:
                birthday_users.append(user.name)
        if len(birthday_users) != 0:
            flash("Birthday(s) today: " + ", ".join(birthday_users), category="info")
            
        sessions_list = self.__upcoming_sessions_for_user(current_user)
        proposals_map = self.__get_proposals_of_sessions(sessions_list)

        # Notifications
        news_specific = news(getSchool()).find({"viewer": current_user.role})
        news_public = news(getSchool()).find({"viewer": 'All'})
        for n in news_public + news_specific:
            flash("<h4>"+n.title+"</h4><p>"+n.content+"</p><br/><i>Last Updated on "+n.date+"</i>", category="info")
        
        return render_template("account_dashboard.html", 
            sessions=sessions_list, 
            proposals=proposals_map, 
            marks_permission=has_permission('marks.comparison'),
            subjects = list(map(lambda x: x.name, subjects(getSchool()).all()))
        )

    @staticmethod
    def __upcoming_sessions_for_user(user):
        upcoming = sessions(getSchool()).upcoming()
        result = filter(lambda x: user.role in x["permissions"]["presence"], upcoming)
        return list(result)

    @staticmethod
    def __get_proposals_of_sessions(sessions_list):
        ids = map(lambda x: x.get("proposals"), sessions_list)
        ids = list(itertools.chain(*ids))
        objs = proposals(getSchool()).find({"_id": {"$in": ids}})
        return {key["_id"]: key for key in objs}

    @staticmethod
    def _format_date(date):
        year = int(date[:4])
        month = int(date[5: 7])
        day = int(date[8: 10])
        return year, month, day

    @staticmethod
    def _get_month(month_number):
        months = [
            "January", "February", "March", 
            "April", "May", "June", 
            "July", "August", "September",
            "October", "November", "December"
        ]
        return months[month_number-1]
