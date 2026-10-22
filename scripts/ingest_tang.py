"""把 chinese-poetry 全唐诗整理成 work / poet / chunk 三份 JSONL。

用法：python scripts/ingest_tang.py [--raw DIR] [--out DIR] [--no-check]
来源与版本见 docs/SOURCE.md。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RAW = ROOT / "data" / "raw" / "chinese-poetry"
DEFAULT_OUT = ROOT / "data" / "processed"

EXPECTED_COMMIT = "b8594f81"
EXPECTED_FILES = 58
EXPECTED_WORKS = 57_607
EXPECTED_POETS = 3_675


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


def build_poets(raw_authors: list[dict]) -> tuple[list[dict], list[dict]]:
    poets, chunks = [], []
    for a in raw_authors:
        poet = {"id": a["id"], "name": a["name"].strip(), "desc": (a.get("desc") or "").strip()}
        poets.append(poet)
        if poet["desc"]:
            chunks.append(
                {
                    "chunk_id": f"poet:{poet['id']}",
                    "kind": "poet_bio",
                    "poet_id": poet["id"],
                    "text": f"{poet['name']}\n{poet['desc']}",
                }
            )
    return poets, chunks


def build_works(
    raw_poems: list[tuple[str, dict]], poet_ids_by_name: dict[str, list[str]]
) -> tuple[list[dict], list[dict]]:
    works, chunks = [], []
    for source_file, p in raw_poems:
        author = (p.get("author") or "").strip()
        ids = poet_ids_by_name.get(author, [])
        lines = [line.strip() for line in p.get("paragraphs") or [] if line.strip()]
        work = {
            "id": p["id"],
            "title": (p.get("title") or "").strip(),
            "author": author,
            # 同名作者不止一位时不猜，留给人工或图谱阶段处理
            "poet_id": ids[0] if len(ids) == 1 else None,
            "paragraphs": lines,
            "source_file": source_file,
        }
        works.append(work)
        chunks.append(
            {
                "chunk_id": f"work:{work['id']}",
                "kind": "work",
                "work_id": work["id"],
                "poet_id": work["poet_id"],
                "text": "\n".join([f"{work['title']}（{author}）", *lines]),
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

    problems = []
    if not args.no_check:
        commit = raw_commit(args.raw)
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

    poets, bio_chunks = build_poets(raw_authors)
    poet_ids_by_name: dict[str, list[str]] = defaultdict(list)
    for poet in poets:
        poet_ids_by_name[poet["name"]].append(poet["id"])
    works, work_chunks = build_works(raw_poems, poet_ids_by_name)

    args.out.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.out / "poets.jsonl", poets)
    write_jsonl(args.out / "works.jsonl", works)
    write_jsonl(args.out / "chunks.jsonl", work_chunks + bio_chunks)

    linked = sum(1 for w in works if w["poet_id"])
    print(f"work {len(works)}（关联到作者 {linked}），poet {len(poets)}")
    print(f"chunk {len(work_chunks) + len(bio_chunks)}（诗 {len(work_chunks)} + 作者简介 {len(bio_chunks)}）")
    print(f"输出：{args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
