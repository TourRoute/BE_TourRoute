from fastapi import APIRouter, HTTPException, Depends, Header, Request
from src.validation.tokenValidation import check_token
from src.schema.plan_request_response import plan_schema
from src.transaction import database
from typing import Annotated
import random

router = APIRouter(prefix="/plan")


@router.get("/recommand-plan/{city}/{theme}")
def recommandPlan(city: str, theme: str, token: str = Header(default=None), origin: Annotated[str | None, Header()] = None):
    res = check_token(token)
    print(token)

    response = database.getData("touroute", theme, {"도시": city})
    random.shuffle(response)

    return response[:5]


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
