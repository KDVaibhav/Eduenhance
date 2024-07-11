from bson import ObjectId
from flask.json import JSONEncoder


class EenJsonEncoder(JSONEncoder):
    def default(self,obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return JSONEncoder.default(self, obj)
