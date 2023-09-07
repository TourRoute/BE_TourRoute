from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api import user_router, plan_router, festival_router, board_router

app = FastAPI()
app.include_router(user_router.router)
app.include_router(plan_router.router)
app.include_router(festival_router.router)
app.include_router(board_router.router)
