from fastapi import APIRouter, HTTPException, Header
from pymongo import MongoClient
from fastapi.responses import JSONResponse
from src.config import settings
from src.schema.comment_request_response import CreateCommentSchema, \
    UpdateCommentSchema
from src.validation.tokenValidation import check_token
from datetime import datetime

my_client = MongoClient(settings.MONGODB_URL,
                        username=settings.MONGODB_USER,
                        password=settings.MONGODB_PWD,
                        authSource=settings.MONGODB_AUTHSOURCE,
                        authMechanism=settings.MONGODB_AUTHMECHANISM)

router = APIRouter(prefix="/comment")

async def select_c_id():
    my_db = my_client["comment"]
    my_col = my_db["comments"]
    comment_count = my_col.estimated_document_count()
    if comment_count == 0:
        return 0
    latest_c_id = my_col.find({}, {"_id": 0, "c_id": 1}).sort("created_at", -1).limit(1)
    c_id = latest_c_id[0].get("c_id")
    return int(c_id) + 1

@router.post("/create_comment", status_code=201)
async def create_comment(request_body: CreateCommentSchema, token: str = Header(default=None)):
    my_db = my_client["user"]
    my_col = my_db["users"]
    user_email = check_token(token)
    username = my_col.find_one({"email": user_email}).get("username")
    img_link = my_col.find_one({"email": user_email}).get("img_link")
    response_body = {
        "c_id": await select_c_id(),
        "b_id": request_body.b_id,
        "user_email": user_email,
        "username": username,
        "contents": request_body.contents,
        "created_at": datetime.now(),
        "i_link": img_link
    }
    my_db = my_client["comment"]
    my_col = my_db["comments"]
    my_col.insert_one(response_body)

    raise HTTPException(status_code=201, detail="댓글 작성 성공")

@router.get("/get_comment", status_code=200)
async def get_comment(b_id: int):
    my_db = my_client["comment"]
    my_col = my_db["comments"]
    response_body = my_col.find({"b_id": b_id}, {"_id": 0}).sort("created_at", -1)
    if response_body:
        return [x for x in response_body]
    raise HTTPException(status_code=400, detail="댓글목록이 없습니다.")

@router.put("/update_comment", status_code=201)
async def update_comment(request_body: UpdateCommentSchema, token: str = Header(default=None)):
    user_email = check_token(token)
    my_db = my_client["comment"]
    my_col = my_db["comments"]
    user_email2 = my_col.find_one({"c_id": request_body.c_id}).get("user_email")
    if user_email == user_email2:
        if my_col.find_one({"c_id": request_body.c_id, "user_email": user_email}):
            my_col.update_one({"c_id": request_body.c_id, "user_email": user_email},
                            {"$set": {"contents": request_body.contents}})
            raise HTTPException(status_code=200, detail="댓글 수정 완료")
        else:
            raise HTTPException(status_code=400, detail="댓글 정보 불일치")
    else:
        raise HTTPException(status_code=400, detail="작성자 정보 불일치")

@router.delete("/delete_comment")
async def delete_comment(c_id: int, token: str = Header(default=None)):
    user_email = check_token(token)
    my_db = my_client["comment"]
    my_col = my_db["comments"]
    user_email2 = my_col.find_one({"c_id": c_id}).get("user_email")
    if user_email == user_email2:
        if my_col.find_one({"c_id": c_id, "user_email": user_email}):
            my_col.delete_one({"c_id": c_id, "user_email": user_email})
            raise HTTPException(status_code=200, detail="댓글 삭제 완료")
        else:
            raise HTTPException(status_code=400, detail="댓글 정보 불일치")
    else:
        raise HTTPException(status_code=400, detail="작성자 정보 불일치")
