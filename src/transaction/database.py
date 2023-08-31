from pymongo import MongoClient
from src.config import settings
import random


my_client = MongoClient("127.0.0.1:27017",
                        username=settings.MONGODB_USER,
                        password=settings.MONGODB_PWD,
                        authSource=settings.MONGODB_AUTHSOURCE,
                        authMechanism=settings.MONGODB_AUTHMECHANISM)

def getData(DB: str, Collection: str, field: dict):
    db = my_client["touroute"]
    dest = db[Collection]

    resultList = []

    for i in dest.find(field):
        i['_id'] = str(i['_id'])
        resultList.append(i)

    random.shuffle(resultList)

    return resultList[:5]
