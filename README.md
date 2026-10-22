# 历史文化智能问答系统

基于 RAG 与知识图谱的毕设项目。当前是仓库骨架：前端能打开，后端健康检查能通。登录、上传文档和向量问答还没做，图谱放在第二阶段。

语料建议见 [docs/corpus-scope.md](docs/corpus-scope.md)：三国人物与事件，来源用维基文库《三国志》和中文维基百科。

## 目录

- `frontend/`：Vue 3 + TypeScript + Vite + Pinia + Element Plus
- `backend/`：FastAPI。路由按认证、知识库、问答、图谱、反馈、管理拆开
- `docs/`：语料范围，后续补 ER 图和接口说明
- `scripts/`：语料采集脚本，下一步再写

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

## 这一阶段还没有的能力

- 注册登录和 JWT
- 文档上传、切分、向量库
- 流式问答
- 图谱查询

对应接口已经挂上，调用会返回 501，避免看起来像已经可用。
