from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateBoardSchema(BaseModel):
    title: str
    contents: str
    category: str
    recruitment: str

class DeleteBoardSchema(BaseModel):
    b_id: int

class UpdateBoardSchema(BaseModel):
    b_id: int
    contents: str
