from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateBoardSchema(BaseModel):
    title: str
    contents: str
    is_free: bool = None
    is_accompany: bool = None

class DeleteBoardSchema(BaseModel):
    b_id: int

class UpdateBoardSchema(BaseModel):
    b_id: int
    contents: str
