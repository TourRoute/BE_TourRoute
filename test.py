from pymongo import MongoClient
from src.config import settings
import random


my_client = MongoClient("127.0.0.1:27017",  username=settings.MONGODB_USER, password=settings.MONGODB_PWD, authSource=settings.MONGODB_AUTHSOURCE,authMechanism=settings.MONGODB_AUTHMECHANISM)

db = my_client["touroute"]

a = [x for x in db["festival"].find({}, {"_id": 0})]

print(a)