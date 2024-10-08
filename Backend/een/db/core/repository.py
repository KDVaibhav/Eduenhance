from bson import ObjectId
from .model import Model
from .cache import Cache


class Repository:
    def __init__(self, collection, cls=Model):
        """Initializes new instance of the Repository class."""
        self._collection = collection
        self._cache = Cache()
        self.__class = cls

    def count(self, *argv):
        """Returns count of object by specified criteria"""
        return self._collection.count(*argv)

    def all(self):
        """Returns all items in collection.
        :return: Array of items."""
        return self.__find({})

    def get(self, oid):
        """Returns object by specified Id"""
        return self.__get(oid)

    def find(self, *argv):
        return self.__map(self.__find(*argv))

    def find_one(self, *argv):
        return self.__map(self.__find_one(*argv))

    def get_list(self, oids):
        criteria = {"_id": {"$in": oids}}
        return self.__map(self.__find(criteria))

    def insert(self, doc):
        return self._collection.insert_one(doc)

    def save(self, doc):
        self._cache.set(doc["_id"], doc)
        return self._collection.replace_one(
            {"_id": doc["_id"]}, doc)

    def delete(self, key):
        return self._collection.find_one_and_delete({
            "_id": ObjectId(key)
        })

    # internal functions

    def __find(self, *argv):
        dbo = list(self._collection.find(*argv))  # fetch database
        objects = self.__map(dbo)  # map to objects
        for obj in objects:            # save objects in cache
            self._cache.set(obj.id, obj)
        return objects

    def __find_one(self, *argv):
        dbo = self._collection.find_one(*argv)  # fetch database
        obj = self.__map(dbo)         # map to object
        if obj:
            self._cache.set(obj.id, obj)  # save object in cache
        return obj

    def __get(self, oid):
        obj = self._cache.get(oid)  # check if object been cached
        if not obj:  # no
            dbo = self._collection.find_one(ObjectId(oid))
            obj = self.__map(dbo)
            if obj:
                self._cache.set(oid, obj)
        return obj

    def __map(self, data):
        if data is None:
            return None
        elif type(data) is list:
            return list(map(lambda x: self.__class(**x), data))
        else:
            return self.__class(**data)
