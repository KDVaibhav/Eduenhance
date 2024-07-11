from pymongo import MongoClient
import json, certifi
# import configparser
# config = configparser.ConfigParser()
# config.read("config.ini")

# host = config.get("db", "host", fallback="127.0.0.1")
# port = config.getint("db", "port", fallback="27017")
# name = config.get("db", "name", fallback="een")

host = "127.0.0.1"
port  = 27017
database = None
school_curr = ""

def connectdb(school=""):
    global host, port
    client = MongoClient("mongodb+srv://Webdatabase:gginaesh@cluster0.bbcqii1.mongodb.net/", tlsCAFile=certifi.where())
    #client = MongoClient(host, port)
    database = client[school]
    return database

def collection(tab, school):
    global database, school_curr
    if school_curr != school:
        print("School changed to " + school)
        database = connectdb(school)
        school_curr = school
    return database[tab]
# users = database["users"]
# sessions = database["sessions"]
# votes = database["votes"]
# comments = database["comments"]
# roles = database["roles"]
# laws = database["laws"]
# articles = database["articles"]
# school = database["school"]
# teacher = database["teacher"]
