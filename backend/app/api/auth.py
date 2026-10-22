from fastapi import APIRouter

from app.api.errors import not_ready

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register() -> None:
    not_ready("注册")


@router.post("/login")
def login() -> None:
    not_ready("登录")
