from fastapi import HTTPException


def not_ready(feature: str) -> None:
    raise HTTPException(status_code=501, detail=f"{feature}尚未实现。当前只跑通仓库骨架与健康检查。")
