from fastapi import APIRouter

from app.api import admin, auth, chat, documents, feedback, health, kg

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(documents.router)
api_router.include_router(chat.router)
api_router.include_router(kg.router)
api_router.include_router(feedback.router)
api_router.include_router(admin.router)


@api_router.get("/me", tags=["auth"])
def me() -> None:
    from app.api.errors import not_ready

    not_ready("当前用户")
