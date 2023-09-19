from pymongo import MongoClient
from src.config import settings

my_client = MongoClient("127.0.0.1",
                        username=settings.MONGODB_USER,
                        password=settings.MONGODB_PWD,
                        authSource=settings.MONGODB_AUTHSOURCE,
                        authMechanism=settings.MONGODB_AUTHMECHANISM)

my_db = my_client["touroute"]
my_col = my_db["festival"]

trash = "http://13.209.56.221/home/tour/img/"

imageList = list()

for i in my_col.find({}):
    i["i_link"] = i["i_link"][len(trash):]
    imageList.append(i["i_link"])

print(imageList)

for i in imageList:
    my_col.update_one({"i_link": {"$regex": i}}, {"$set":{"i_link": i}})