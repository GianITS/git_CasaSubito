import pymongo
from pymongo import MongoClient

Cluster = MongoClient("mongodb+srv://luca:L1u2c3a4!@cluster0.u5ont.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = Cluster["Agent"]
cltAgenti =db["Agent"]
cltImmobili = db["immobili"]
