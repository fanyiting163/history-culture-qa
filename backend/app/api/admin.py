from fastapi import APIRouter

from app.api.errors import not_ready

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
def stats() -> None:
    not_ready("运营统计")
