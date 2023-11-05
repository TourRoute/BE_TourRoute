import os
from datetime import timedelta, datetime
import jwt
from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile
from fastapi.security import OAuth2PasswordBearer
# from fastapi.security import OAuth2PasswordRequestForm # 유저네임으로 로그인할시
from passlib.context import CryptContext
from pymongo import MongoClient
from starlette import status
from src.validation.tokenValidation import check_token
from src.transaction import database
from src.schema.user_request_response import SignUpRequest, Token, LoginRequest, AddFriend
from src.config import settings

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
        "latest": datetime.now(),
        "img_link": ""
    }

    my_col.insert_one(insert_user)

    my_db2 = my_client["touroute"]
    my_col2 = my_db2["festival"]
    f_list = my_col2.find({}, {"_id": 0})
    f_list = [x for x in f_list]
    my_db3 = my_client["user"]
    my_col3 = my_db3["festival"]
    for x in f_list:
        x["is_bookmark"] = False
        x["user_email"] = user.email
        my_col3.insert_one(x)

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

    access_token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {
        "access_token": access_token
    }


@router.get("/mypage")
async def read_mypage(token: str = Header(default=None)):
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="토큰이 없거나 올바르지 않습니다.")
    else:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail="토큰에 해당하는 유저의 정보가 없습니다.")
    user_info = my_col.find_one({"email": user_email})
    response_query = {
        "username": user_info["username"],
        "email": user_email,
        "latest": user_info["latest"],
        "img_link": user_info["img_link"]
    }
    return response_query


@router.put("/update_mypage")
async def update_mypage(username: str = None, file: UploadFile | None = None, token: str = Header(default=None)):

    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="토큰이 없거나 올바르지 않습니다.")
    else:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail="토큰에 해당하는 유저의 정보가 없습니다.")

    if file is not None:
        upload_path = "/app/img/userinfo"
        file_name = f'{user_email.split("@")[0]}.png'
        file_content = await file.read()
        my_col.update_one({"email": user_email}, {"$set": {"img_link": "http://13.209.56.221:8000/img/userinfo/" + file_name}})

        if not os.path.isdir(upload_path):
            os.mkdir(upload_path)

        with open(os.path.join(upload_path, file_name), "wb") as f:
            f.write(file_content)

    if my_col.find_one({"email": user_email}):
        if username is None:
            my_col.update_one({"email": user_email},
                            {"$set": {"latest": datetime.now()}})
        else:
            my_col.update_one({"email": user_email},
                            {"$set": {"username": username, "latest": datetime.now()}})
        raise HTTPException(status_code=200, detail="수정이 완료되었습니다.")
    else:
        raise HTTPException(status_code=400, detail="이메일 정보가 없습니다.")


@router.get("/get-user/{email}")
async def get_user(email: str, token: str = Header(default=None)):
    user_email = check_token(token)

    response = my_col.find_one({"email": email}, {"_id": 0, "password": 0})
    if response:
        response["status_code"] = 200
        return response
    else:
        return HTTPException(status_code=400, detail="이메일이 없습니다.")

@router.put("/add_friend/{email}")
async def get_user(request_body: AddFriend, token: str = Header(default=None)):
    user_email = check_token(token)

    my_db = my_client["user"]
    my_col = my_db["users"]

    check_email = my_col.find_one({"email": request_body.email})
    if check_email:
        pass
    else:
        return HTTPException(status_code=400, detail="추가하려는 이메일이 없습니다.")

    my_db = my_client["touroute"]
    my_col = my_db["plan"]

    res_body = my_col.find_one({"email": user_email, "p_id": request_body.p_id}, {"_id": 0, "accompany": 1})
    if res_body:
        accompany_list = res_body["accompany"]
        accompany_list.append(request_body.email)
        my_col.update_one({"email": user_email, "p_id": request_body.p_id}, {"$set": {"accompany": accompany_list}})
        return HTTPException(status_code=200, detail="동행 이메일이 추가되었습니다.")
    else:
        return HTTPException(status_code=400, detail="추가하려는 계획이 없습니다.")

