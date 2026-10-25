"""把 chinese-poetry 全唐诗整理成 work / poet / chunk 三份 JSONL，并输出清洗统计。

用法：python scripts/ingest_tang.py [--raw DIR] [--out DIR] [--no-check]
来源与版本见 docs/SOURCE.md。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

from opencc import OpenCC

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RAW = ROOT / "data" / "raw" / "chinese-poetry"
DEFAULT_OUT = ROOT / "data" / "processed"

EXPECTED_COMMIT = "b8594f81"
EXPECTED_FILES = 58
EXPECTED_WORKS = 57_607
EXPECTED_POETS = 3_675

FULLWIDTH_SPACE = "\u3000"
DUPLICATE_SAMPLES = 20


def load_json(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def raw_commit(raw: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(raw), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return out.stdout.strip()


def clean_text(text: str | None, stats: Counter) -> str:
    """去掉 BOM、零宽字符和控制字符，全角空格换成普通空格；不动标点。"""
    kept = []
    for ch in text or "":
        if ch in "\t\r\n":
            kept.append(" ")
        elif unicodedata.category(ch) in ("Cc", "Cf"):
            stats["removed_chars"] += 1
        else:
            kept.append(ch)
    cleaned = "".join(kept)
    stats["fullwidth_spaces_replaced"] += cleaned.count(FULLWIDTH_SPACE)
    return cleaned.replace(FULLWIDTH_SPACE, " ").strip()


def changed_chars(trad: str, simp: str) -> int:
    return sum(a != b for a, b in zip(trad, simp)) + abs(len(trad) - len(simp))


def build_poets(
    raw_authors: list[dict], converter: OpenCC, stats: Counter
) -> tuple[list[dict], list[dict]]:
    poets, chunks = [], []
    for a in raw_authors:
        name_trad = clean_text(a.get("name"), stats)
        desc_trad = clean_text(a.get("desc"), stats)
        name = converter.convert(name_trad)
        desc = converter.convert(desc_trad)
        diff = changed_chars(name_trad, name) + changed_chars(desc_trad, desc)
        if diff:
            stats["poets_converted"] += 1
            stats["poet_chars_converted"] += diff
        poet = {
            "id": a["id"],
            "name": name,
            "name_trad": name_trad,
            "desc": desc,
            "desc_trad": desc_trad,
        }
        poets.append(poet)
        if desc_trad:
            chunks.append(
                {
                    "chunk_id": f"poet:{poet['id']}",
                    "kind": "poet_bio",
                    "poet_id": poet["id"],
                    "text": f"{name}\n{desc}",
                }
            )
    return poets, chunks


def clean_poem(source_file: str, p: dict, stats: Counter) -> dict:
    lines = []
    for raw_line in p.get("paragraphs") or []:
        line = clean_text(raw_line, stats)
        if line:
            lines.append(line)
        else:
            stats["empty_lines_removed"] += 1
    poem = {
        "id": p["id"],
        "title_trad": clean_text(p.get("title"), stats),
        "author_trad": clean_text(p.get("author"), stats),
        "paragraphs_trad": lines,
        "source_file": source_file,
    }
    if not poem["title_trad"]:
        stats["works_without_title"] += 1
    if not lines:
        stats["works_without_body"] += 1
    return poem


def drop_duplicates(poems: list[dict]) -> tuple[list[dict], list[dict]]:
    """作者、标题、正文（清洗后的繁体）完全相同才算重复，只留第一条。"""
    first_by_key: dict[tuple, dict] = {}
    kept, dropped = [], []
    for poem in poems:
        key = (poem["author_trad"], poem["title_trad"], tuple(poem["paragraphs_trad"]))
        first = first_by_key.setdefault(key, poem)
        if first is poem:
            kept.append(poem)
        else:
            dropped.append(
                {
                    "id": poem["id"],
                    "source_file": poem["source_file"],
                    "kept_id": first["id"],
                    "kept_source_file": first["source_file"],
                    "author_trad": poem["author_trad"],
                    "title_trad": poem["title_trad"],
                }
            )
    return kept, dropped


def build_works(
    poems: list[dict],
    poet_ids_by_name: dict[str, list[str]],
    converter: OpenCC,
    stats: Counter,
) -> tuple[list[dict], list[dict]]:
    works, chunks = [], []
    for poem in poems:
        title_trad = poem["title_trad"]
        author_trad = poem["author_trad"]
        lines_trad = poem["paragraphs_trad"]
        title = converter.convert(title_trad)
        author = converter.convert(author_trad)
        lines = [converter.convert(line) for line in lines_trad]
        diff = (
            changed_chars(title_trad, title)
            + changed_chars(author_trad, author)
            + sum(changed_chars(t, s) for t, s in zip(lines_trad, lines))
        )
        if diff:
            stats["works_converted"] += 1
            stats["work_chars_converted"] += diff

        ids = poet_ids_by_name.get(author_trad, [])
        if len(ids) == 1:
            stats["works_linked"] += 1
        elif ids:
            stats["works_author_ambiguous"] += 1
        else:
            stats["works_author_unknown"] += 1

        work = {
            "id": poem["id"],
            "title": title,
            "title_trad": title_trad,
            "author": author,
            "author_trad": author_trad,
            # 同名作者不止一位时不猜，留给人工或图谱阶段处理
            "poet_id": ids[0] if len(ids) == 1 else None,
            "paragraphs": lines,
            "paragraphs_trad": lines_trad,
            "source_file": poem["source_file"],
        }
        works.append(work)
        if not lines:
            continue
        chunks.append(
            {
                "chunk_id": f"work:{work['id']}",
                "kind": "work",
                "work_id": work["id"],
                "poet_id": work["poet_id"],
                "text": "\n".join([f"{title}（{author}）", *lines]),
            }
        )
    return works, chunks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--raw", type=Path, default=DEFAULT_RAW, help="chinese-poetry 仓库根目录")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="输出目录")
    parser.add_argument("--no-check", action="store_true", help="跳过 commit 和数量核对")
    args = parser.parse_args()

    tang_dir = args.raw / "全唐诗"
    poem_files = sorted(tang_dir.glob("poet.tang.*.json"), key=lambda f: int(f.stem.rsplit(".", 1)[-1]))
    authors_file = tang_dir / "authors.tang.json"
    if not poem_files or not authors_file.exists():
        print(f"找不到全唐诗数据：{tang_dir}，拉取方式见 docs/SOURCE.md", file=sys.stderr)
        return 1

    raw_poems = [(f.name, p) for f in poem_files for p in load_json(f)]
    raw_authors = load_json(authors_file)
    commit = raw_commit(args.raw)

    problems = []
    if not args.no_check:
        if commit is None or not commit.startswith(EXPECTED_COMMIT):
            problems.append(f"commit 应为 {EXPECTED_COMMIT}，实际 {commit or '未知'}")
        for label, got, want in [
            ("JSON 文件数", len(poem_files), EXPECTED_FILES),
            ("诗数", len(raw_poems), EXPECTED_WORKS),
            ("作者数", len(raw_authors), EXPECTED_POETS),
        ]:
            if got != want:
                problems.append(f"{label}应为 {want}，实际 {got}")
    if problems:
        print("与 docs/SOURCE.md 不一致：\n  " + "\n  ".join(problems), file=sys.stderr)
        return 1

    stats: Counter = Counter()
    converter = OpenCC("t2s")
    poets, bio_chunks = build_poets(raw_authors, converter, stats)
    poet_ids_by_name: dict[str, list[str]] = defaultdict(list)
    for poet in poets:
        poet_ids_by_name[poet["name_trad"]].append(poet["id"])

    cleaned = [clean_poem(source_file, p, stats) for source_file, p in raw_poems]
    kept, dropped = drop_duplicates(cleaned)
    works, work_chunks = build_works(kept, poet_ids_by_name, converter, stats)

    report = {
        "source": {
            "commit": commit,
            "files": len(poem_files),
            "works": len(raw_poems),
            "poets": len(raw_authors),
        },
        "cleaning": {
            "removed_chars": stats["removed_chars"],
            "fullwidth_spaces_replaced": stats["fullwidth_spaces_replaced"],
            "empty_lines_removed": stats["empty_lines_removed"],
            "works_without_title": stats["works_without_title"],
            "works_without_body": stats["works_without_body"],
        },
        "dedup": {
            "key": "author_trad + title_trad + paragraphs_trad",
            "dropped": len(dropped),
            "works_after": len(works),
            "dropped_samples": dropped[:DUPLICATE_SAMPLES],
        },
        "conversion": {
            "converter": "opencc t2s",
            "works_converted": stats["works_converted"],
            "work_chars_converted": stats["work_chars_converted"],
            "poets_converted": stats["poets_converted"],
            "poet_chars_converted": stats["poet_chars_converted"],
        },
        "linking": {
            "linked": stats["works_linked"],
            "author_unknown": stats["works_author_unknown"],
            "author_ambiguous": stats["works_author_ambiguous"],
        },
        "output": {
            "works": len(works),
            "poets": len(poets),
            "work_chunks": len(work_chunks),
            "bio_chunks": len(bio_chunks),
        },
    }

    args.out.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.out / "poets.jsonl", poets)
    write_jsonl(args.out / "works.jsonl", works)
    write_jsonl(args.out / "chunks.jsonl", work_chunks + bio_chunks)
    stats_path = args.out / "ingest_stats.json"
    stats_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"work {len(works)}（去掉重复 {len(dropped)}，关联到作者 {stats['works_linked']}），poet {len(poets)}")
    print(f"chunk {len(work_chunks) + len(bio_chunks)}（诗 {len(work_chunks)} + 作者简介 {len(bio_chunks)}）")
    print(f"输出：{args.out}")
    print(f"统计：{stats_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
