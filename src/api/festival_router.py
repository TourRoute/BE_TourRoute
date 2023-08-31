from fastapi import APIRouter, HTTPException
from pymongo import MongoClient

from src.config import settings

my_client = MongoClient("127.0.0.1:27017",
                        username=settings.MONGODB_USER,
                        password=settings.MONGODB_PWD,
                        authSource=settings.MONGODB_AUTHSOURCE,
                        authMechanism=settings.MONGODB_AUTHMECHANISM)

my_db = my_client["touroute"]
my_col = my_db["festival"]

router = APIRouter(prefix="/festival")

@router.get("/get_info")
async def get_festival_info():
    response_query = my_col.find({}, {"_id": 0})
    if response_query:
        return response_query
    else:
        raise HTTPException(status_code=400, detail="컬렉션 정보가 없습니다.")
