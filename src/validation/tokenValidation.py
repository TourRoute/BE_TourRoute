import jwt
from src.config import settings
from fastapi import HTTPException
from starlette import status

def check_token(token: str):
    if token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="토큰이 없거나 올바르지 않습니다.")

    else:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email: str = payload.get("sub")

        if user_email is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="토큰에 해당하는 유저의 정보가 없습니다.")
        
        return user_email