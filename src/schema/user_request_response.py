from pydantic import BaseModel, validator, EmailStr


class SignUpRequest(BaseModel):
    username: str
    email: EmailStr
    password1: str
    password2: str

    @validator('username', 'email', 'password1', 'password2')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @validator('password2')
    def passwords_math(cls, v, values):
        if 'password1' in values and v != values['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다.')
        return v

class Token(BaseModel):
    access_token: str
    token_type: str
    email: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UpdateUserInfo(BaseModel):
    username: str
