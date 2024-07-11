import uuid
import os

def getUniqueId():
    pastIds = list(map(lambda filename: os.path.splitext(filename)[0], os.listdir(os.getcwd() + "/een/web/static/uploads/")))
    while True:
        id = str(uuid.uuid4())
        if id not in pastIds:
            return id
        else:
            print("Id repeated")