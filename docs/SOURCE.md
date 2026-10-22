# 数据来源

| 项 | 值 |
| --- | --- |
| 仓库 | <https://github.com/chinese-poetry/chinese-poetry> |
| 版本 | commit `b8594f81` |
| 核对日期 | 2026-10-22 |
| 使用范围 | `全唐诗/poet.tang.*.json`（58 个，57,607 首）、`全唐诗/authors.tang.json`（3,675 人） |
| 许可 | 诗文公有领域；JSON 整理 MIT；本项目非商业教学使用 |

## 拉取

原始 JSON 不进本仓库，放在 `data/raw/`（已在 `.gitignore` 中）：

```powershell
git clone https://github.com/chinese-poetry/chinese-poetry.git data/raw/chinese-poetry
git -C data/raw/chinese-poetry checkout b8594f81
```

## 处理

```powershell
python scripts/ingest_tang.py
```

脚本会核对文件数、诗数和作者数是否与上表一致，结果写到 `data/processed/`。换版本时先更新本页的 commit 和数量，再改脚本里的期望值。
