import json
from localstorage import getSchool
from een.db import roles, users, subjects, classes
with open("local/config.json", "r") as f:
    sch = json.load(f)

for school in sch.keys():
    with open("data.json", "r") as f:
        data = json.load(f)

    for role in data["roles"]:
        roles(getSchool()).insert(role)
    for user in data["users"]:
        users(getSchool()).insert(user)
    for sub in data['subjects']:
        subjects(school).insert({
            "name": sub
        })
    for class_ in data['classes']:
        classes(school).insert({
            "name": class_,
            "subjects": data["subjects"]
        })