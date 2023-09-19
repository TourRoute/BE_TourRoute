from datetime import timedelta, datetime
import jwt
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Header, Request
from fastapi.security import OAuth2PasswordBearer
# from fastapi.security import OAuth2PasswordRequestForm # 유저네임으로 로그인할시
from passlib.context import CryptContext
from pymongo import MongoClient
from starlette import status
from src.validation.tokenValidation import check_token
from src.schema.user_request_response import SignUpRequest, Token, LoginRequest, UpdateUserInfo
from src.config import settings
from src.transaction import database

my_client = MongoClient(settings.MONGODB_URL,
                        username=settings.MONGODB_USER,
                        password=settings.MONGODB_PWD,
                        authSource=settings.MONGODB_AUTHSOURCE,
                        authMechanism=settings.MONGODB_AUTHMECHANISM)

my_db = my_client["user"]
my_col = my_db["users"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/users")

# 회원가입


@router.post("/signup", status_code=201)
async def signup(user: SignUpRequest):

    if my_col.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="가입되어있는 이메일입니다.")

    insert_user = {
        "username": user.username,
        "email": user.email,
        "password": pwd_context.hash(user.password1),
    }

    my_col.insert_one(insert_user)

    return {"message": "회원가입이 완료되었습니다."}


@router.post("/login", response_model=Token)
async def login(form_data: LoginRequest = Depends(),):
    request_query = {"email": form_data.email}
    db_user = my_col.find_one(request_query)

    if not db_user or not pwd_context.verify(form_data.password, db_user["password"]):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    data = {
        "sub": form_data.email,
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    access_token = jwt.encode(data, settings.SECRET_KEY,
                              algorithm=settings.ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": form_data.email
    }


@router.get("/mypage")
async def read_mypage(token: str = Header(default=None)):
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="토큰이 없거나 올바르지 않습니다.")
    else:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail="토큰에 해당하는 유저의 정보가 없습니다.")
    user_info = my_col.find_one({"email": user_email})
    response_query = {
        "username": user_info["username"],
        "email": user_email,
    }
    return response_query


@router.put("/update_mypage")
async def update_mypage(request_data: UpdateUserInfo, token: str = Header(default=None)):

    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="토큰이 없거나 올바르지 않습니다.")
    else:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail="토큰에 해당하는 유저의 정보가 없습니다.")

    if my_col.find_one({"email": user_email}):
        my_col.update_one({"email": user_email},
                          {"$set": {"username": request_data.username}})
        raise HTTPException(status_code=200, detail="수정이 완료되었습니다.")
    else:
        raise HTTPException(status_code=400, detail="이메일 정보가 없습니다.")


@router.get("/get-user/{email}")
async def get_user(email, token: str = Header(default=None),):
    res = check_token(token)

    response = database.getData("user", "users", {"email":email})

    del response[0]["password"]

    return response