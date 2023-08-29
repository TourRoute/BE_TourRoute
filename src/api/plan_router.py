from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordBearer
# from fastapi.security import OAuth2PasswordRequestForm # 유저네임으로 로그인할시
from passlib.context import CryptContext
from pymongo import MongoClient
from starlette import status
from src.validation.tokenValidation import checkToken
from src.config import settings
from src.schema.request_response import SignUpRequest, Token, LoginRequest, UpdateUserInfo
from src.transaction import database

router = APIRouter(prefix="/plan")


@router.get("/recommand-plan")
def recommandPlan(city: str, theme: str, token: str = Header(default=None)):
    res = database.getData("touroute", theme, {"도시": city})
    return res
