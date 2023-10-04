from fastapi import APIRouter, HTTPException, Header
from pymongo import MongoClient

from src.config import settings
from src.validation.tokenValidation import check_token

my_client = MongoClient(settings.MONGODB_URL,
                        username=settings.MONGODB_USER,
                        password=settings.MONGODB_PWD,
                        authSource=settings.MONGODB_AUTHSOURCE,
                        authMechanism=settings.MONGODB_AUTHMECHANISM)

router = APIRouter(prefix="/festival")

@router.get("/get_info")
async def get_festival_info(token: str = Header(default=None)):
    if token is None:
        my_db = my_client["touroute"]
        my_col = my_db["festival"]

        response = [x for x in my_col.find({}, {"_id": 0})]

        if response:
            return response
        else:
            raise HTTPException(status_code=400, detail="컬렉션 정보가 없습니다.")
    else:
        user_email = check_token(token)
        my_db = my_client["user"]
        my_col = my_db["festival"]
        return [x for x in my_col.find({"user_email": user_email}, {"_id": 0})]

@router.get("/get_city_info")
async def get_city_info(city_name: str, token: str = Header(default=None)):
    if token is None:
        my_db = my_client["touroute"]
        my_col = my_db["festival"]

        response = [x for x in my_col.find({"city": city_name}, {"_id": 0})]

        if response:
            return response
        else:
            raise HTTPException(status_code=400, detail="컬렉션 정보가 없습니다.")
    else:
        user_email = check_token(token)
        my_db = my_client["user"]
        my_col = my_db["festival"]
        return [x for x in my_col.find({"user_email": user_email, "city": city_name}, {"_id": 0})]

@router.post("/bookmark")
async def bookmark(festival_name: str, token: str = Header(default=None)):
    user_email = check_token(token)
    my_db = my_client["user"]
    my_col = my_db["festival"]
    is_bookmark = my_col.find_one({"f_name": festival_name, "user_email": user_email}).get("is_bookmark")
    if is_bookmark is True:
        my_col.update_one({"f_name": festival_name, "user_email": user_email}, {"$set": {"is_bookmark": False}})
    else:
        my_col.update_one({"f_name": festival_name, "user_email": user_email}, {"$set": {"is_bookmark": True}})

    raise HTTPException(status_code=200, detail="즐겨찾기 변경 성공")

# @router.post("/bookmark")
# async def add_bookmark(festival_name: str, token: str = Header(default=None)):
#     user_email = check_token(token)
#     my_db = my_client["touroute"]
#     my_col = my_db["festival"]
#     festival_info = my_col.find_one({"f_name": festival_name}, {"_id": 0})
#     if festival_info:
#         my_col = my_db["bookmark"]
#         check_info = my_col.find_one({"f_name": festival_name, "user_email": user_email}, {"_id": 0})
#         if check_info:
#             raise HTTPException(status_code=400, detail="이미 즐겨찾기가 되어 있습니다.")
#         keys = [key for key in festival_info.keys()]
#         keys.append("user_email")
#         values = [value for value in festival_info.values()]
#         values.append(user_email)
#         res_body = dict(zip(keys, values))
#         my_db = my_client["touroute"]
#         my_col = my_db["bookmark"]
#         my_col.insert_one(res_body)
#         raise HTTPException(status_code=200, detail="즐겨찾기 완료")
#     else:
#         raise HTTPException(status_code=400, detail="축제 정보가 없습니다.")

# @router.get("/get_bookmark", status_code=200)
# async def get_bookmark(token: str = Header(default=None)):
#     user_email = check_token(token)
#     my_db = my_client["touroute"]
#     my_col = my_db["bookmark"]
#     bookmark_info = my_col.find({"user_email": user_email}, {"_id": 0})
#     if bookmark_info:
#         return [x for x in bookmark_info]
#     else:
#         raise HTTPException(status_code=400, detail="즐겨찾기 정보가 없습니다.")
#
# @router.delete("/delete_bookmark")
# async def delete_bookmark(festival_name: str, token: str = Header(default=None)):
#     user_email = check_token(token)
#     my_db = my_client["touroute"]
#     my_col = my_db["bookmark"]
#     bookmark = my_col.find_one({"user_email": user_email, "f_name": festival_name}, {"_id: 0"})
#     print(bookmark)
#     if bookmark:
#         my_col.delete_one({"user_email": user_email, "f_name": festival_name})
#         raise HTTPException(status_code=200, detail="즐겨찾기 삭제 완료")
#     else:
#         raise HTTPException(status_code=400, detail="삭제하려는 즐겨찾기 정보가 없습니다")
