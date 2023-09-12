from pymongo import MongoClient
from src.config import settings
import random


my_client = MongoClient(settings.MONGODB_URL,
                        username=settings.MONGODB_USER,
                        password=settings.MONGODB_PWD,
                        authSource=settings.MONGODB_AUTHSOURCE,
                        authMechanism=settings.MONGODB_AUTHMECHANISM)


def getData(DB: str, Collection: str, field: dict | None):
    db = my_client[DB]
    dest = db[Collection]

    resultList = []

    for i in dest.find(field):
        i['_id'] = str(i['_id'])
        resultList.append(i)

    return resultList


def insertData(DB: str, Collection: str, data: list):
    db = my_client[DB]
    dest = db[Collection]

    return dest.insert_many(data)
