from datetime import datetime

from pydantic import BaseModel, EmailStr

class CreateCommentSchema(BaseModel):
    b_id: int
    contents: str

class UpdateCommentSchema(BaseModel):
    c_id: int
    contents: str

class DeleteCommentSchema(BaseModel):
    c_id: int
