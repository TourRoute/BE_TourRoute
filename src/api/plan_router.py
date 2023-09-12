from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pymongo import MongoClient
from starlette import status
from src.validation.tokenValidation import check_token
from src.config import settings
from src.schema.user_request_response import SignUpRequest, Token, LoginRequest, UpdateUserInfo
from src.transaction import database
import random

router = APIRouter(prefix="/plan")


@router.post("/recommand-plan")
def recommandPlan(city: str, theme: str, data: dict, token: str = Header(default=None)):
    database.insertData("touroute", "plan", list(data))

    response = database.getData("touroute", theme, {"도시": city})
    random.shuffle(response)

    return response[:5]


@router.get("/get-plan")
def getPlan(email: str):
    response = database.getData("touroute", "plan", {"email": email})

    resultList = [x for x in response]
