from pydantic import BaseModel, EmailStr


class plan_schema(BaseModel):
    city: str = None
    theme: str = None
    period: list = None
    accompany: list = None
    tourList: list = None
