from pymongo import MongoClient
from src.config import settings
import random


my_client = MongoClient(settings.MONGODB_URL, 27017)
# my_db = my_client["user"]
# my_col = my_db["users"]


def getData(DB: str, Collection: str, field: dict):
    db = my_client["touroute"]
    dest = db[Collection]

    resultList = []

    for i in dest.find(field):
        i['_id'] = str(i['_id'])
        resultList.append(i)

    random.shuffle(resultList)

    return resultList[:5]
