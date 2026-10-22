from fastapi import APIRouter

from app.api.errors import not_ready

router = APIRouter(prefix="/kg", tags=["kg"])


@router.get("/entities/{entity_id}")
def get_entity(entity_id: str) -> None:
    not_ready(f"实体 {entity_id} 查询")


@router.get("/subgraph")
def get_subgraph() -> None:
    not_ready("图谱子图")
