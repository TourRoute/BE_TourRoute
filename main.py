from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api import user_router, plan_router, festival_router, board_router

app = FastAPI()

#app.mount("/img", StaticFiles(directory="/app/img"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(plan_router.router)
app.include_router(festival_router.router)
app.include_router(board_router.router)
