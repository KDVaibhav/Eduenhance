from een.db import roles
from een.web.blueprints.crud_controller import CrudController
from localstorage import getSchool

class RolesController(CrudController):
    def __init__(self):
        repo = roles(getSchool())
        super().__init__(repo, namespace="roles", columns=["name"])
        rolesName = list(map(lambda x: x.name.lower(), repo.all()))
        self._permissions = [
            {"name": "roles.create", "desc": "Create new role"},
            {"name": "roles.read", "desc": "Read role data"},
            {"name": "roles.update", "desc": "Update existing role"},
            {"name": "roles.delete", "desc": "Delete role"},  # 4
            {"name": "school.create", "desc": "Create new school"},
            {"name": "school.read", "desc": "Read school"},
            {"name": "school.update", "desc": "Update existing school"},
            {"name": "school.delete", "desc": "Delete school"},  # 8
            {"name": "timetable.read_all", "desc": "Read all timetable"},
            {"name": "timetable.read_own", "desc": "Read only own timetable"},
            {"name": "timetable.update", "desc": "Update existing timetable"},  # 11
            {"name": "attendance.read_all", "desc": "Read everyone's attendance"},
            {"name": "attendance.read_own", "desc": "Read only own attendance"},
            {"name": "attendance.update", "desc": "Take attendance"},  # 14
            {"name": "exams.create", "desc": "Create new exams"},
            {"name": "exams.read", "desc": "Read exams"},
            {"name": "exams.update", "desc": "Update existing exams"},
            {"name": "exams.delete", "desc": "Delete exams"},  # 18
            {"name": "marks.read_all", "desc": "Read everyone's marks"},
            {"name": "marks.read_own", "desc": "Read only own marks"},
            {"name": "marks.update", "desc": "Update marks"},  # 21
            {"name": "lessonplans.read", "desc": "Read lesson plans"},
            {"name": "lessonplans.update", "desc": "Update existing lesson plans"},  # 23
            {"name": "subjects.create", "desc": "Create new subjects"},
            {"name": "subjects.read", "desc": "Read subjects"},
            {"name": "subjects.update", "desc": "Update existing subjects"},
            {"name": "subjects.delete", "desc": "Delete subjects"},  # 27
            {"name": "classes.create", "desc": "Create new classes"},
            {"name": "classes.read", "desc": "Read classes"},
            {"name": "classes.update", "desc": "Update existing classes"},
            {"name": "classes.delete", "desc": "Delete classes"},  # 31
            {"name": "transactions.create", "desc": "Create new transactions"},
            {"name": "transactions.read", "desc": "Read transactions"},
            {"name": "transactions.delete", "desc": "Delete transactions"},  # 34
            {"name": "balances.read_all", "desc": "Read all balances"},
            {"name": "balances.read_own", "desc": "Read only own balance"},  # 36
            {"name": "periods.create", "desc": "Create new periods"},
            {"name": "periods.read", "desc": "Read periods"},
            {"name": "periods.update", "desc": "Update existing periods"},
            {"name": "periods.delete", "desc": "Delete periods"},  # 40
            {"name": "leave.create", "desc": "Apply for leave"},
            {"name": "leave.read_all", "desc": "Read all leave"},
            {"name": "leave.read_own", "desc": "Read own leave"},
            {"name": "leave.approve", "desc": "Approve leave"},
            {"name": "leave.update", "desc": "Update existing leave"},
            {"name": "leave.delete", "desc": "Delete leave"},  # 46
            {"name": "payment.create", "desc": "Create new payment"},
            {"name": "payment.read_all", "desc": "Read all payment"},
            {"name": "payment.read_own", "desc": "Read own payment"},
            {"name": "payment.update", "desc": "Update existing payment"},
            {"name": "payment.delete", "desc": "Delete payment"},  # 51
            {"name": "news.create", "desc": "Create new news"},
            {"name": "news.read", "desc": "Read news"},
            {"name": "news.update", "desc": "Update existing news"},
            {"name": "news.delete", "desc": "Delete news"},  # 55
            {"name": "users.create", "desc": "Create new user", "click": "activate('create')", "id": "user-create"},
            {"name": "users.read", "desc": "Read user data", "click": "activate('read')", "id": "user-read"},
            {"name": "users.update", "desc": "Update existing user", "click": "activate('update')", "id": "user-update"},
            {"name": "users.delete", "desc": "Delete user", "click": "activate('delete')", "id": "user-delete"},
        ]
        for role in rolesName:
            self._permissions.append({"name": role+".create", "desc": "Create new "+role, "class": "type-create"})
            self._permissions.append({"name": role+".read", "desc": "Read "+role, "class": "type-read"})
            self._permissions.append({"name": role+".update", "desc": "Update existing "+role, "class": "type-update"})
            self._permissions.append({"name": role+".delete", "desc": "Delete "+role, "class": "type-delete"})

    def _update_model(self, model, data, files):
        pl = map(lambda x: x["name"], self._permissions)
        pl = list(filter(lambda x: data.get(x, False), pl))

        model.name = data.get("name", None)
        model.permissions = pl

    def _extend(self, model):
        return {
            "role_groups": [
                {"name": "Roles", "roles": self._permissions[0:4]},
                {"name": "School", "roles": self._permissions[4:8]},
                {"name": "Timetable", "roles": self._permissions[8:11]},
                {"name": "Attendance", "roles": self._permissions[11:14]},
                {"name": "Exams", "roles": self._permissions[14:18]},
                {"name": "Marks", "roles": self._permissions[18:21]},
                {"name": "Lesson Plans", "roles": self._permissions[21:23]},
                {"name": "Subjects", "roles": self._permissions[23:27]},
                {"name": "Classes", "roles": self._permissions[27:31]},
                {"name": "Transactions", "roles": self._permissions[31:34]},
                {"name": "Balances", "roles": self._permissions[34:36]},
                {"name": "Periods", "roles": self._permissions[36:40]},
                {"name": "Leave", "roles": self._permissions[40:46]},
                {"name": "Payment", "roles": self._permissions[46:51]},
                {"name": "News", "roles": self._permissions[51:55]},
                {"name": "Users", "roles": self._permissions[55:]}
            ]
        }
