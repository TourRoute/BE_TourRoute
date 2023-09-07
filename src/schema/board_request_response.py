from datetime import datetime

from pydantic import BaseModel, EmailStr


class create_board_schema(BaseModel):
    user_email: EmailStr = None
    username: str = None
    title: str
    contents: str
    created_at: datetime = None
