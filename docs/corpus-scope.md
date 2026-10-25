# 语料范围（已定）

垂直子域：**唐诗**。RAG 主库用 chinese-poetry 的全唐诗，来源、版本和许可见 [SOURCE.md](SOURCE.md)。

## RAG 主库

| 数据 | 文件 | 规模 | 入库方式 |
| --- | --- | --- | --- |
| 全唐诗 | `全唐诗/poet.tang.*.json`，共 58 个 | 57,607 首 | 每首诗一条 `work`，一首一个 chunk |
| 唐代作者 | `全唐诗/authors.tang.json` | 3,675 人 | 每位作者一条 `poet`，简介单独成一个 bio chunk |

原始数据是繁体。入库时先清洗、去重，再用 OpenCC 转简体，步骤和统计见 [SOURCE.md](SOURCE.md#处理)。

字段映射：

- 诗：`title` / `author` / `paragraphs` / `id` → `work`。`title`、`author`、`paragraphs` 存简体，`title_trad`、`author_trad`、`paragraphs_trad` 存清洗后的繁体原文。`paragraphs` 按行拼成正文；按繁体作者名关联 `poet`，同名多人时 `poet_id` 留空
- 作者：`name` / `desc` / `id` → `poet`。`name`、`desc` 存简体，`name_trad`、`desc_trad` 存繁体。`desc` 为空的作者只建 `poet` 记录，不产出 bio chunk
- chunk 的 `text` 用简体；正文为空的诗只保留 `work` 记录，不产出 chunk

一首一个 chunk 是因为唐诗普遍很短，再切会把一联拆散；检索命中后能直接引用整首诗和作者。

## 知识图谱

第二周做，不进第一周主路径。从主库里挑 50–150 位名家建轻量子集，实体先限定「诗人 / 作品」，关系从作者字段直接得到，其余关系（交游、师承、地点）按需人工补。

## 不纳入

- 宋词、元曲及 chinese-poetry 里的其他子集，不写进主路径
- 现代注释、赏析、专著等有版权的文本

## 许可

诗文本身属于公有领域；chinese-poetry 的 JSON 整理按 MIT 许可使用。本项目仅用于非商业的教学和毕业设计，论文与系统界面里注明数据来源。
