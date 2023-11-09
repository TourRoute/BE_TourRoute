import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Header, UploadFile, Form, File, Depends
from fastapi.responses import JSONResponse
from pymongo import MongoClient

from src.config import settings
from src.schema.board_request_response import CreateBoardSchema, DeleteBoardSchema, UpdateBoardSchema
from src.validation.tokenValidation import check_token
from datetime import datetime

my_client = MongoClient(settings.MONGODB_URL,
                        username=settings.MONGODB_USER,
                        password=settings.MONGODB_PWD,
                        authSource=settings.MONGODB_AUTHSOURCE,
                        authMechanism=settings.MONGODB_AUTHMECHANISM)

router = APIRouter(prefix="/board")

async def select_b_id():
    my_db = my_client["board"]
    my_col = my_db["boards"]
    comment_count = my_col.estimated_document_count()
    if comment_count == 0:
        return 0
    latest_b_id = my_col.find({}, {"_id": 0, "b_id": 1}).sort("created_at", -1).limit(1)
    b_id = latest_b_id[0].get("b_id")
    return int(b_id)+1

@router.post("/create_board")
async def create_board(response_schema: CreateBoardSchema = Depends(), file: UploadFile | None = None, token: str = Header(default=None)):
    my_db = my_client["user"]
    my_col = my_db["users"]

    user_email = check_token(token)

    username = my_col.find_one({"email": user_email}).get("username")
    img_link = my_col.find_one({"email": user_email}).get("img_link")

    b_id = await select_b_id()

    if file is not None:
        upload_path = "/app/img/board"
        file_name = f'{str(b_id)}.png'
        file_content = await file.read()

        if not os.path.isdir(upload_path):
            os.mkdir(upload_path)

        with open(os.path.join(upload_path, file_name), "wb") as f:
            f.write(file_content)

        board_img_link = "/board/"+file_name
    else:
        board_img_link = "이미지 파일이 없습니다."

    response_body = {
        "b_id": b_id,
        "user_email": user_email,
        "username": username,
        "title": response_schema.title,
        "contents": response_schema.contents,
        "created_at": datetime.now(),
        "category": response_schema.category,
        "recruitment": response_schema.recruitment,
        "r_link": response_schema.r_link,
        "user_img_link": img_link,
        "board_img_link": board_img_link
    }

    my_db = my_client["board"]
    my_col = my_db["boards"]
    my_col.insert_one(response_body)
    return HTTPException(status_code=201, detail="게시물 작성 성공")

@router.get("/get_board_all", status_code=200)
async def get_board_all():
    my_db = my_client["board"]
    my_col = my_db["boards"]
    response_body = my_col.find({}, {"_id": 0}).sort("created_at", -1)
    return [x for x in response_body]

@router.get("/get_board", status_code=200)
async def get_board(token: str = Header(default=None)):
    user_email = check_token(token)
    my_db = my_client["board"]
    my_col = my_db["boards"]
    response_body = my_col.find({"user_email": user_email}, {"_id": 0}).sort("created_at", -1)
    if response_body:
        return [x for x in response_body]
    raise HTTPException(status_code=400, detail="작성하신 게시물이 없습니다.")

@router.delete("/delete_board")
async def delete_board(b_id: int, token: str = Header(default=None)):
    user_email = check_token(token)

    file = "/app/img/board/" + str(b_id) + ".png"
    if os.path.isfile(file):
        os.remove(file)

    my_db = my_client["board"]
    my_col = my_db["boards"]
    user_email2 = my_col.find_one({"b_id": b_id}).get("user_email")
    if user_email == user_email2:
        if my_col.find_one({"b_id": b_id, "user_email": user_email}):
            my_col.delete_one({"b_id": b_id, "user_email": user_email})
            my_db = my_client["comment"]
            my_col = my_db["comments"]
            my_col.delete_one({"b_id": b_id})
            raise HTTPException(status_code=200, detail="게시물 삭제 완료")
        else:
            raise HTTPException(status_code=400, detail="게시물 정보 없음")
    else:
        raise HTTPException(status_code=400, detail="작성자 정보 불일치")

@router.put("/update_board")
async def update_board(request_body: UpdateBoardSchema = Depends(), file: UploadFile| None = None, token: str = Header(default=None)):
    user_email = check_token(token)
    my_db = my_client["board"]
    my_col = my_db["boards"]
    user_email2 = my_col.find_one({"b_id": request_body.b_id}).get("user_email")

    if user_email == user_email2:

        if file is not None:
            upload_path = "/app/img/board"
            file_name = f'{str(request_body.b_id)}.png'
            file_content = await file.read()

            if not os.path.isdir(upload_path):
                os.mkdir(upload_path)

            with open(os.path.join(upload_path, file_name), "wb") as f:
                f.write(file_content)

            my_col.update_one({"b_id": request_body.b_id, "user_email": user_email},
                            {"$set": {"contents": request_body.contents, "recruitment": request_body.recruitment, "board_img_link": "/board/"+file_name}})
        else:
            my_col.update_one({"b_id": request_body.b_id, "user_email": user_email},
                            {"$set": {"contents": request_body.contents, "recruitment": request_body.recruitment}})

        raise HTTPException(status_code=200, detail="게시물 수정 완료")
    else:
        raise HTTPException(status_code=400, detail="게시물 작성자가 일치하지 않습니다.")

@router.get("/get_latest")
async def get_latest(category: str):
    my_db = my_client["board"]
    my_col = my_db["boards"]
    response_body = my_col.find({"category": category}, {"_id": 0}).sort("created_at", -1)
    return [x for x in response_body]


@router.get("/get_latest_main", status_code=200)
async def get_latest_main():
    my_db = my_client["board"]
    my_col = my_db["boards"]
    response_body = my_col.find({}, {"_id": 0}).sort("created_at", -1).limit(5)
    return [x for x in response_body]
# @router.put("/update_board")
# async def update_board(request_body: update_board_schema, token: str = Header(default=None)):
#     user_email = check_token(token)
#     my_db = my_client["board"]
#     my_col = my_db["boards"]
#
#     if my_col.find_one({"title": request_body.title, "created_at": request_body.created_at, "user_email": user_email}):
#         my_col.update_one({"title": request_body.title, "created_at": request_body.created_at, "user_email": user_email},
#                         {"$set": {"contents": request_body.contents}})
#         raise HTTPException(status_code=200, detail="게시물 수정 완료")
#     else:
#         raise HTTPException(status_code=400, detail="게시물 정보가 없습니다.")
