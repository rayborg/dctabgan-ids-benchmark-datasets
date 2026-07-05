#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from omitted_dataset_common import (
    BENCHMARK_REPO_ENV,
    default_release_root,
    join_relative,
    load_manifest,
    resolve_benchmark_repo,
    selected_datasets,
    source_path,
    target_path,
    verify_csv_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Recreate omitted local-only datasets by copying exact processed CSVs "
            "from a separately obtained dctabgan-benchmark-expansion clone."
        )
    )
    parser.add_argument(
        "--benchmark-repo",
        help=f"Path to dctabgan-benchmark-expansion. Defaults to ${BENCHMARK_REPO_ENV} or a sibling clone.",
    )
    parser.add_argument("--release-root", default=str(default_release_root()))
    parser.add_argument("--manifest", default=None, help="Path to metadata/omitted-datasets.json.")
    parser.add_argument("--task", action="append", dest="tasks", help="Task key to recreate; repeatable.")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing local omitted CSVs.")
    parser.add_argument("--dry-run", action="store_true", help="Show planned actions without copying files.")
    parser.add_argument(
        "--run-benchmark-prep",
        action="store_true",
        help="Run the benchmark repo materialization scripts needed by the selected omitted tasks before copying.",
    )
    parser.add_argument(
        "--python",
        default="python3",
        help="Python executable used with --run-benchmark-prep. Default: python3.",
    )
    return parser.parse_args()


def print_errors(task_key: str, label: str, errors: list[str]) -> None:
    print(f"FAIL {task_key} {label}", file=sys.stderr)
    for error in errors:
        print(f"  {error}", file=sys.stderr)


def run_benchmark_prep(benchmark_repo: Path, datasets: list[dict], python_executable: str, dry_run: bool) -> int:
    scripts: list[str] = []
    for dataset in datasets:
        script = dataset["benchmark_rebuild_script"]
        if script not in scripts:
            scripts.append(script)

    for script in scripts:
        script_path = join_relative(benchmark_repo, script)
        if not script_path.exists():
            print(f"Missing benchmark materialization script: {script_path}", file=sys.stderr)
            return 1
        command = [python_executable, script]
        print(f"Running benchmark materializer: {' '.join(command)}")
        if dry_run:
            continue
        completed = subprocess.run(command, cwd=benchmark_repo)
        if completed.returncode != 0:
            return completed.returncode
    return 0


def main() -> int:
    args = parse_args()
    release_root = Path(args.release_root).expanduser().resolve()
    benchmark_repo = resolve_benchmark_repo(release_root, args.benchmark_repo)
    if benchmark_repo is None:
        print(
            f"No benchmark repo supplied. Use --benchmark-repo or set {BENCHMARK_REPO_ENV}.",
            file=sys.stderr,
        )
        return 2
    if not benchmark_repo.exists():
        print(f"Benchmark repo does not exist: {benchmark_repo}", file=sys.stderr)
        return 2

    _, manifest = load_manifest(release_root, args.manifest)
    datasets = selected_datasets(manifest, args.tasks)
    if args.run_benchmark_prep:
        status = run_benchmark_prep(benchmark_repo, datasets, args.python, args.dry_run)
        if status != 0:
            return status

    print("Recreating omitted datasets from local benchmark outputs only.")
    print("This script does not download, redistribute, or relicense omitted upstream corpora.")

    failures = 0
    for dataset in datasets:
        task_key = dataset["task_key"]
        source = source_path(benchmark_repo, dataset)
        target = target_path(release_root, dataset)

        source_errors, _ = verify_csv_file(source, dataset)
        if source_errors:
            print_errors(task_key, "source", source_errors)
            print(f"  Rebuild script: {dataset['benchmark_rebuild_script']}", file=sys.stderr)
            failures += 1
            continue

        if target.exists():
            target_errors, _ = verify_csv_file(target, dataset)
            if not target_errors and not args.overwrite:
                print(f"OK existing {task_key}: {target}")
                continue
            if target_errors and not args.overwrite:
                print_errors(task_key, "existing target", target_errors)
                print("  Use --overwrite to replace it from the verified benchmark source.", file=sys.stderr)
                failures += 1
                continue

        print(f"COPY {task_key}: {source} -> {target}")
        if args.dry_run:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

        target_errors, _ = verify_csv_file(target, dataset)
        if target_errors:
            print_errors(task_key, "copied target", target_errors)
            failures += 1
        else:
            print(f"OK copied {task_key}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
