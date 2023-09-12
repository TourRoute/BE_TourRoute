from pymongo import MongoClient
from src.config import settings
import random


# my_client = MongoClient("127.0.0.1:27017",  username=settings.MONGODB_USER, password=settings.MONGODB_PWD, authSource=settings.MONGODB_AUTHSOURCE,authMechanism=settings.MONGODB_AUTHMECHANISM)

# db = my_client["touroute"]

# a = [x for x in db["festival"].find({}, {"_id": 0})]

# print(a)

data = {"data": 1}

data["log"] = "horse"

print(data)

a = {"city":"대구","theme":"문화","period":["2023-07-10", "2023-70-13"],"accompany":["hgjinkim@gmail.com", "admin@admin.com"],"userEmail":"hgjinkim@gmail.com"}