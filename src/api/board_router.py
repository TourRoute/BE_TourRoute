from fastapi import APIRouter, HTTPException, Header
from pymongo import MongoClient

from src.config import settings
from src.schema.board_request_response import create_board_schema
from src.validation.tokenValidation import check_token
from datetime import datetime

my_client = MongoClient(settings.MONGODB_URL,
                        username=settings.MONGODB_USER,
                        password=settings.MONGODB_PWD,
                        authSource=settings.MONGODB_AUTHSOURCE,
                        authMechanism=settings.MONGODB_AUTHMECHANISM)

router = APIRouter(prefix="/board")

@router.post("/create_board", status_code=201)
async def create_board(response_schema: create_board_schema, token: str = Header(default=None)):
    my_db = my_client["board"]
    my_col = my_db["boards"]
    user_email = check_token(token)
    username = my_col.find_one({"user_email": user_email}, {"username": 1}).values()
    response_body = {
        "user_email": user_email,
        "username": username,
        "title": response_schema.title,
        "contents": response_schema.contents,
        "created_at": datetime.now()
    }
    my_col.insert_one(response_body)
