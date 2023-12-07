from fastapi import APIRouter

from src.routers.auth import router as authRouter
from src.routers.users import router as usersRouter

apis = APIRouter()
apis.include_router(authRouter)
apis.include_router(usersRouter)

__all__ = ["apis"]
