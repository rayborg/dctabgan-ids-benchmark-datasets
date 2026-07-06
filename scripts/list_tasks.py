#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


def default_release_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_metadata(release_root: Path, metadata_path: str | None) -> dict[str, Any]:
    path = Path(metadata_path or "metadata/datasets.json").expanduser()
    if not path.is_absolute():
        path = release_root / path
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def local_or_public_path(dataset: dict[str, Any]) -> str:
    if dataset.get("public_csv"):
        return str(dataset["public_csv"])
    reproduction = dataset.get("local_reproduction") or {}
    return str(reproduction.get("local_data_path_if_rebuilt") or dataset.get("processed_csv") or "")


def selected_datasets(args: argparse.Namespace, metadata: dict[str, Any]) -> list[dict[str, Any]]:
    datasets = list(metadata["datasets"])
    if args.status == "downloadable":
        datasets = [dataset for dataset in datasets if bool(dataset.get("downloadable"))]
    elif args.status == "omitted":
        datasets = [dataset for dataset in datasets if not bool(dataset.get("downloadable"))]

    if args.corpus:
        wanted_corpora = set(args.corpus)
        datasets = [dataset for dataset in datasets if dataset.get("source_corpus") in wanted_corpora]
    if args.task:
        wanted_tasks = set(args.task)
        known_tasks = {dataset["task_key"] for dataset in metadata["datasets"]}
        unknown = sorted(wanted_tasks - known_tasks)
        if unknown:
            raise SystemExit(f"Unknown task key(s): {', '.join(unknown)}")
        datasets = [dataset for dataset in datasets if dataset["task_key"] in wanted_tasks]
    return datasets


def output_rows(datasets: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for dataset in datasets:
        train_counts = dataset["train_counts"]
        test_counts = dataset["test_counts"]
        rows.append(
            {
                "task_key": str(dataset["task_key"]),
                "title": str(dataset["title"]),
                "source_corpus": str(dataset["source_corpus"]),
                "status": "downloadable" if dataset.get("downloadable") else "omitted_not_redistributed",
                "train_majority": str(train_counts["majority"]),
                "train_minority": str(train_counts["minority"]),
                "test_majority": str(test_counts["majority"]),
                "test_minority": str(test_counts["minority"]),
                "csv_path": local_or_public_path(dataset),
                "redistribution_caveat": str(dataset.get("redistribution_caveat") or ""),
            }
        )
    return rows


def print_table(rows: list[dict[str, str]], show_caveats: bool) -> None:
    columns = [
        ("task_key", 44),
        ("source_corpus", 24),
        ("status", 27),
        ("train", 15),
        ("test", 15),
    ]
    header = "  ".join(name.ljust(width) for name, width in columns) + "  csv_path"
    print(header)
    print("  ".join("-" * width for _name, width in columns) + "  " + "-" * 72)
    for row in rows:
        values = {
            "task_key": row["task_key"],
            "source_corpus": row["source_corpus"],
            "status": row["status"],
            "train": f"{row['train_majority']}/{row['train_minority']}",
            "test": f"{row['test_majority']}/{row['test_minority']}",
        }
        fixed = "  ".join(values[name][:width].ljust(width) for name, width in columns)
        print(f"{fixed}  {row['csv_path']}")
        if show_caveats and row["redistribution_caveat"]:
            print(f"  license: {row['redistribution_caveat']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List DCTABGAN IDS benchmark release tasks.")
    parser.add_argument("--release-root", default=str(default_release_root()))
    parser.add_argument("--metadata", default=None, help="Path to metadata/datasets.json.")
    parser.add_argument(
        "--status",
        choices=["all", "downloadable", "omitted"],
        default="all",
        help="Task availability filter. Default: all.",
    )
    parser.add_argument("--corpus", action="append", help="Restrict to a source corpus; repeatable.")
    parser.add_argument("--task", action="append", help="Restrict to a task key; repeatable.")
    parser.add_argument("--format", choices=["table", "csv", "json"], default="table")
    parser.add_argument("--show-caveats", action="store_true", help="Show redistribution caveats in table output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    release_root = Path(args.release_root).expanduser().resolve()
    metadata = load_metadata(release_root, args.metadata)
    rows = output_rows(selected_datasets(args, metadata))

    if args.format == "json":
        print(json.dumps(rows, indent=2, sort_keys=True))
    elif args.format == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)
    else:
        print_table(rows, show_caveats=bool(args.show_caveats))
        print(f"\nListed {len(rows)} task(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
