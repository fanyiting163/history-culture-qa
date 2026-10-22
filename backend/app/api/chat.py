from fastapi import APIRouter

from app.api.errors import not_ready

router = APIRouter(tags=["chat"])


@router.post("/chat/completions")
def chat_completions() -> None:
    not_ready("流式问答")


@router.get("/conversations")
def list_conversations() -> None:
    not_ready("会话历史")
