from fastapi import FastAPI

from src.api import user_router, plan_router

app = FastAPI()
app.include_router(user_router.router)
app.include_router(plan_router.router)
