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

脚本会核对文件数、诗数和作者数是否与上表一致，结果写到 `data/processed/`。换版本时先更新本页的 commit 和数量，再改脚本里的期望值。上表数量是原始数据的数量，不是去重后的数量。

核对通过后依次做三步：

1. 清洗：删掉 BOM、零宽字符和其他控制字符，制表符和换行换成空格，全角空格换成普通空格，去掉首尾空白和空诗句；标点不改
2. 去重：作者、标题、正文（清洗后的繁体）完全相同的诗只留第一条
3. 繁转简：用 OpenCC `t2s` 生成简体字段，供检索和展示；繁体原文另存在 `*_trad` 字段。作者关联用繁体原名，避免异体字把不同的人合成一个

按 `b8594f81` 跑出的结果：

| 项 | 数量 |
| --- | --- |
| 去重后诗数 | 57,603（去掉 4 首完全重复） |
| 全角空格替换 | 31 处 |
| 删掉的异常字符 | 0 |
| 无标题 / 无正文的诗 | 168 / 4 |
| 发生繁转简的诗 / 作者 | 57,544 / 3,265 |
| 关联到唯一作者的诗 | 56,657；作者同名无法判断 946 |
| chunk | 60,172（诗 57,599 + 作者简介 2,573） |

每次运行的完整统计写在 `data/processed/ingest_stats.json`，重复诗的样本也在里面。

OpenCC 按常用简体转换，一个繁体字对应多个简体字时（如「乾」「後」「發」）不看上下文，个别字可能转错，所以引用原文时以繁体字段为准。
