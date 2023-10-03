from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pymongo import MongoClient
from starlette import status
from src.validation.tokenValidation import check_token
from src.config import settings
from src.schema.user_request_response import SignUpRequest, Token, LoginRequest, UpdateUserInfo
from typing import Annotated
from src.schema.plan_request_response import plan_schema
from src.transaction import database
import random


router = APIRouter(prefix="/plan")


### 맛집이 너무 애매한 위치에 있어서 최대한 디비 트렌잭션 적게 하는 방법으로 해서 코드가 좀 복잡합니다
### 모든 일정마다 식당이 꼭 들어가야 하는데 맛집이랑 식당이 겹치면 안되니까...
@router.get("/recommand-plan")
def recommandPlan(city: str, theme: str, period: int, token: str = Header(default=None)):
    
    tourPair = {"restaurant":"park", "mountain":"restaurant", "museum":"tourspot", "park":"restaurant", "tourspot":"restaurant"}
    dbField = {"mountain":"name", "park":"소재지지번주소","restaurant":"store_address","museum":"소재지도로명주소","tourspot":"소재지지번주소"}
    check_token(token)
    
    resultList = list()
    
    restaurant = [x for x in database.getData("touroute", "restaurant", {dbField["restaurant"]: {"$regex": '^'+city}})]
    random.shuffle(restaurant)
    
    
    if theme == "restaurant":
        pairTheme = [x for x in database.getData("touroute", tourPair[theme], {dbField[tourPair[theme]]: {"$regex": '^'+city}})]
        random.shuffle(pairTheme)

        for i in range(period):
            temp = []
            temp.append(restaurant.pop(0))
            temp.append(restaurant.pop(0))
            temp.append(pairTheme.pop(0))

            resultList.append(temp)

        
        return resultList

    elif tourPair[theme] == "restaurant":
        mainTheme = [x for x in database.getData("touroute", theme, {dbField[theme]: {"$regex": '^'+city}})]
        random.shuffle(mainTheme)

        for i in range(period):
            temp = []
            temp.append(restaurant.pop(0))
            temp.append(restaurant.pop(0))
            temp.append(mainTheme.pop(0))

            resultList.append(temp)

        return resultList
        
    
    else:
        mainTheme = [x for x in database.getData("touroute", theme, {dbField[theme]: {"$regex": '^'+city}})]
        random.shuffle(mainTheme)

        subTheme = [x for x in database.getData("touroute", tourPair[theme], {dbField[tourPair[theme]]: {"$regex": '^'+city}})]
        random.shuffle(subTheme)

        for i in range(period):
            temp = []
            temp.append(mainTheme.pop(0))
            temp.append(restaurant.pop(0))
            temp.append(subTheme.pop(0))

            resultList.append(temp)

        return resultList


@router.post("/save-plan")
def savePlan(request: plan_schema, token: str = Header(default=None)):
    res = check_token(token)
    data = list()
    data.append(request.__dict__)
    database.insertData("touroute", "plan", data)

    raise HTTPException(status_code=200, detail="여행 계획이 저장 되었습니다.")


@router.get("/get-plan/{email}")
def getPlan(email: str, token: str = Header(default=None),):
    res = check_token(token)

    response = database.getData("touroute", "plan", {"email": email})

    resultList = [x for x in response]

    return resultList