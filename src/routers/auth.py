import datetime
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from prisma.models import User
from src.models.scalar import Gender
from src.prisma import prisma
from src.utils.auth import encrypt_password, sign_jwt, validate_password

router = APIRouter()


class SignIn(BaseModel):
    email: str
    password: str


class SignInOut(BaseModel):
    token: str
    user: User


@router.post("/auth/sign-in", tags=["auth"])
async def sign_in(sign_in: SignIn):
    user = await prisma.user.find_first(
        where={
            "email": sign_in.email,
        }
    )

    validated = validate_password(sign_in.password, user.password)
    del user.password

    if validated:
        token = sign_jwt(user.id)
        return SignInOut(token=token, user=user)

    return None


class SignUp(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    nickname: Optional[str] = None
    birthday: Optional[datetime.date] = None
    gender: Optional[Gender] = None
    phone: Optional[str] = None


@router.post("/auth/sign-up", tags=["auth"])
async def sign_up(user: SignUp):
    try:
        password = encrypt_password(user.password)
        created = await prisma.user.create(
            {
                "email": user.email,
                "password": password,
                "name": user.name,
                "nickname": user.nickname,
                "birthDay": datetime.datetime(
                    user.birthday.year, user.birthday.month, user.birthday.day
                ),
                "gender": user.gender.value,
                "phone": user.phone,
            }
        )

        return created
    except Exception as e:
        return {"message": str(e)}


@router.get("/auth/", tags=["auth"])
async def auth():
    users = await prisma.user.find_many()

    for user in users:
        del user.password

    return users
