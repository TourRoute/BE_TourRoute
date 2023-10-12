# from haversine import haversine
# from pymongo import MongoClient
# from src.config import settings
# import random
# import re
#
# my_client = MongoClient(settings.MONGODB_URL,
#                         username=settings.MONGODB_USER,
#                         password=settings.MONGODB_PWD,
#                         authSource=settings.MONGODB_AUTHSOURCE,
#                         authMechanism=settings.MONGODB_AUTHMECHANISM)
#
# my_db = my_client["touroute"]
# my_col = my_db["restaurant"]
#
# data_list = my_col.find()
#
#
# for x in data_list:
#     object_id = x["_id"]
#     menu_dict = {}
#     name = list(x['menu'].keys())
#     fee = list(x['menu'].values())
#     for y in range(len(name)):
#         piece_dict = {'name': name[y], 'fee': fee[y]}
#         menu_dict['menu_'+str(y + 1)] = piece_dict
#     my_col.update_one({"_id": object_id},{"$set": {"menu": menu_dict}})

# my_client = MongoClient("127.0.0.1:27017",  username=settings.MONGODB_USER, password=settings.MONGODB_PWD, authSource=settings.MONGODB_AUTHSOURCE,authMechanism=settings.MONGODB_AUTHMECHANISM)
#
# db = my_client["touroute"]
#
#
# a = [x for x in db["restaurant"].find({"store_address": {"$regex":'^'+"대구"}})]
#
# print(len(a))


# a = "대구광역시 달서구 호산동"
# b = "부산광역시 해운대구"

# p = re.compile(r'^대구')

# print(p.search(b))
