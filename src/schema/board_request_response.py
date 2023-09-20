from datetime import datetime

from pydantic import BaseModel, EmailStr


class create_board_schema(BaseModel):
    title: str
    contents: str
    is_free: bool = None
    is_accompany: bool = None

class delete_board_schema(BaseModel):
    title: str
    created_at: datetime = None

class update_board_schema(BaseModel):
    title: str
    contents: str
    created_at: datetime = None
