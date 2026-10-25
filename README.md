# 历史文化智能问答系统

基于 RAG 与知识图谱的毕设项目。当前是仓库骨架：前端能打开，后端健康检查能通。登录、上传文档和向量问答还没做，图谱放在第二阶段。

## 语料

垂直子域是**唐诗**，详见 [docs/corpus-scope.md](docs/corpus-scope.md)，来源与许可见 [docs/SOURCE.md](docs/SOURCE.md)。

- RAG 主库：[chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) commit `b8594f81`。只读 `全唐诗/poet.tang.*.json`（58 个，57,607 首）和 `全唐诗/authors.tang.json`（3,675 人）。同目录里的宋诗，以及仓库里的宋词、元曲等其他子集不入库
- 入库：先清洗，再按繁体的作者、标题、正文去掉完全重复，最后用 OpenCC 转成简体。`title`、`author`、`paragraphs`、`name`、`desc` 是简体，对应的 `*_trad` 保留繁体原文。按 `b8594f81` 处理后是 57,603 首；正文为空的诗不产生 chunk。字段和统计见 [docs/SOURCE.md](docs/SOURCE.md)
- 图谱：后续再做，取约 50–150 位名家的轻量子集
- 许可：诗文公有领域，JSON 整理 MIT，非商业教学使用

## 目录

- `frontend/`：Vue 3 + TypeScript + Vite + Pinia + Element Plus
- `backend/`：FastAPI。路由按认证、知识库、问答、图谱、反馈、管理拆开
- `docs/`：语料范围和数据来源，后续补 ER 图和接口说明
- `scripts/`：`ingest_tang.py` 把全唐诗整理成 `data/processed/` 下的 `works.jsonl`、`poets.jsonl`、`chunks.jsonl`，并写出 `ingest_stats.json`。转换依赖见 `scripts/requirements.txt`
- `data/`：本地数据目录，`raw/` 和 `processed/` 不进仓库

## 本地启动

后端：

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

健康检查：<http://127.0.0.1:8000/api/health>

前端另开一个终端：

```powershell
cd frontend
npm install
npm run dev
```

打开 <http://localhost:5173>。开发服务器把 `/api` 代理到 `8000`。

语料按 [docs/SOURCE.md](docs/SOURCE.md) 拉到 `data/raw/chinese-poetry` 后，在仓库根目录执行。OpenCC 不在后端依赖里，要单独装：

```powershell
.\backend\.venv\Scripts\python.exe -m pip install -r scripts/requirements.txt
.\backend\.venv\Scripts\python.exe scripts/ingest_tang.py
```

## 这一阶段还没有的能力

- 注册登录和 JWT
- 文档上传、切分、向量库
- 流式问答
- 图谱查询

对应接口已经挂上，调用会返回 501，避免看起来像已经可用。
