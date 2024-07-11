import json
from .core.cache import Cache
from pymongo import MongoClient

class SchoolRepository():
    """Provides interface for Schools collection of database."""

    def __init__(self):
        self._host = "127.0.0.1"
        self._port = 27017
        with open("local/config.json", "r") as f:
            self._school = json.load(f)
            self._cache = Cache()

    def insert(self, model):
        name = model['name']
        dbname = model['dbname']
        address = model['address']
        if dbname in self._school.keys():
            return False
        else:
            self._school[dbname] = {
                'name': name, 
                'address': address
            }
            with open("local/config.json", "w") as f:
                json.dump(self._school, f, indent=2)

            from een.db import roles, users, subjects, classes
            with open("data.json", "r") as f:
                data = json.load(f)

            for role in data["roles"]:
                roles(dbname).insert(role)
            for user in data["users"]:
                users(dbname).insert(user)
            for sub in data['subjects']:
                subjects(dbname).insert({
                    "name": sub
                })
            for class_ in data['classes']:
                classes(dbname).insert({
                    "name": class_,
                    "subjects": data["subjects"]
                })
            return True
    def get(self, oid):
        return {
            'dbname': oid, 
            'name': self._school[oid]['name'], 
            'address': self._school[oid]['address'],
            '_id': oid
        }

    def all(self):
        """Returns all items in collection.
        :return: Array of items."""
        return list(map(lambda x: {
            'dbname': x, 
            'name': self._school[x]['name'],
            'address': self._school[x]['address'], 
            '_id': x
        }, self._school.keys()))

    def save(self, model):
        self._school[model['_id']] = {
                'name': model['name'], 
                'address': model['address']
            }
        with open("local/config.json", "w") as f:
            json.dump(self._school, f, indent=2)

    def delete(self, key):
        if not key in self._school.keys():
            return False
        else:
            #host = "mongodb+srv://moulindu:1LfdJciKEWaU83cr@cluster0.toj7q.mongodb.net/"+key+"?retryWrites=true&w=majority"
            MongoClient(self._host, self._port).drop_database(key)
            self._school.pop(key)
            with open("local/config.json", "w") as f:
                json.dump(self._school, f, indent=2)