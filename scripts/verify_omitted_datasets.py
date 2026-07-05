#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from omitted_dataset_common import (
    BENCHMARK_REPO_ENV,
    default_release_root,
    load_manifest,
    resolve_benchmark_repo,
    selected_datasets,
    source_path,
    target_path,
    verify_csv_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify locally recreated omitted datasets against expected counts and SHA256 checksums."
    )
    parser.add_argument(
        "--benchmark-repo",
        help=f"Optional path to dctabgan-benchmark-expansion. Defaults to ${BENCHMARK_REPO_ENV} or a sibling clone if present.",
    )
    parser.add_argument("--release-root", default=str(default_release_root()))
    parser.add_argument("--manifest", default=None, help="Path to metadata/omitted-datasets.json.")
    parser.add_argument("--task", action="append", dest="tasks", help="Task key to verify; repeatable.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable verification results.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    release_root = Path(args.release_root).expanduser().resolve()
    benchmark_repo = resolve_benchmark_repo(release_root, args.benchmark_repo)
    _, manifest = load_manifest(release_root, args.manifest)
    datasets = selected_datasets(manifest, args.tasks)

    results = []
    for dataset in datasets:
        task_key = dataset["task_key"]
        target = target_path(release_root, dataset)
        target_errors, target_actual = verify_csv_file(target, dataset)
        errors = [f"target: {error}" for error in target_errors]
        source_actual = None

        if benchmark_repo is not None:
            source = source_path(benchmark_repo, dataset)
            source_errors, source_actual = verify_csv_file(source, dataset)
            errors.extend(f"source: {error}" for error in source_errors)
            if target_actual and source_actual and target_actual["sha256"] != source_actual["sha256"]:
                errors.append(
                    "target/source SHA256 mismatch: "
                    f"target {target_actual['sha256']} vs source {source_actual['sha256']}"
                )

        results.append(
            {
                "task_key": task_key,
                "ok": not errors,
                "target_local_csv": str(target),
                "source_benchmark_csv": str(source_path(benchmark_repo, dataset)) if benchmark_repo else None,
                "errors": errors,
                "target_actual": target_actual,
                "source_actual": source_actual,
            }
        )

    ok = all(result["ok"] for result in results)
    if args.json:
        print(json.dumps({"ok": ok, "results": results}, indent=2, sort_keys=True))
    else:
        if benchmark_repo is None:
            print(
                f"No benchmark repo supplied or found; checked local targets against {len(datasets)} expected checksums only."
            )
        else:
            print(f"Checked source benchmark repo: {benchmark_repo}")
        for result in results:
            if result["ok"]:
                print(f"OK {result['task_key']}: {result['target_local_csv']}")
            else:
                print(f"FAIL {result['task_key']}: {result['target_local_csv']}", file=sys.stderr)
                for error in result["errors"]:
                    print(f"  {error}", file=sys.stderr)

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
