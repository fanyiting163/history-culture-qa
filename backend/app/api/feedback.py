from fastapi import APIRouter

from app.api.errors import not_ready

router = APIRouter(tags=["feedback"])


@router.post("/feedback")
def create_feedback() -> None:
    not_ready("反馈")
