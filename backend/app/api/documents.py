from fastapi import APIRouter

from app.api.errors import not_ready

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("")
def list_documents() -> None:
    not_ready("知识库列表")


@router.post("")
def upload_document() -> None:
    not_ready("文档上传")


@router.post("/{document_id}/ingest")
def ingest_document(document_id: str) -> None:
    not_ready(f"文档 {document_id} 的切分入库")
