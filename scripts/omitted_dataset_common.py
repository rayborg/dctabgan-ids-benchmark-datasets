from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
from typing import Any


DEFAULT_MANIFEST_PATH = "metadata/omitted-datasets.json"
BENCHMARK_REPO_ENV = "DCTABGAN_BENCHMARK_REPO"


def default_release_root() -> Path:
    return Path(__file__).resolve().parents[1]


def join_relative(root: Path, relative_path: str) -> Path:
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Refusing unsafe relative path: {relative_path}")
    return root / relative


def load_manifest(release_root: Path, manifest_path: str | None = None) -> tuple[Path, dict[str, Any]]:
    path_text = manifest_path or DEFAULT_MANIFEST_PATH
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = release_root / path
    with path.open("r", encoding="utf-8") as handle:
        return path, json.load(handle)


def resolve_benchmark_repo(release_root: Path, supplied_path: str | None) -> Path | None:
    if supplied_path:
        return Path(supplied_path).expanduser().resolve()
    env_path = os.environ.get(BENCHMARK_REPO_ENV)
    if env_path:
        return Path(env_path).expanduser().resolve()
    sibling = release_root.parent / "dctabgan-benchmark-expansion"
    if sibling.exists():
        return sibling.resolve()
    return None


def selected_datasets(manifest: dict[str, Any], task_keys: list[str] | None) -> list[dict[str, Any]]:
    datasets = list(manifest["datasets"])
    if not task_keys:
        return datasets
    wanted = set(task_keys)
    known = {dataset["task_key"] for dataset in datasets}
    unknown = sorted(wanted - known)
    if unknown:
        raise ValueError(f"Unknown omitted task key(s): {', '.join(unknown)}")
    return [dataset for dataset in datasets if dataset["task_key"] in wanted]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def csv_profile(path: Path, label_column: str) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        if label_column not in fieldnames:
            raise ValueError(f"Missing label column {label_column!r}")
        label_counts: dict[str, int] = {}
        row_count = 0
        for row in reader:
            row_count += 1
            label = row[label_column]
            label_counts[label] = label_counts.get(label, 0) + 1
    return {
        "row_count": row_count,
        "column_count": len(fieldnames),
        "label_counts": dict(sorted(label_counts.items())),
    }


def verify_csv_file(path: Path, dataset: dict[str, Any]) -> tuple[list[str], dict[str, Any] | None]:
    expected = dataset["expected_source_csv"]
    label_column = expected["label_column"]
    errors: list[str] = []
    if not path.exists():
        return [f"missing file: {path}"], None
    if not path.is_file():
        return [f"not a regular file: {path}"], None

    actual: dict[str, Any] = {
        "path": str(path),
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }
    try:
        actual.update(csv_profile(path, label_column))
    except Exception as exc:  # noqa: BLE001 - report CSV parse failures as validation errors.
        errors.append(f"CSV profile failed for {path}: {exc}")
        return errors, actual

    for key in ("bytes", "sha256", "row_count", "column_count"):
        if actual[key] != expected[key]:
            errors.append(
                f"{key} mismatch for {path}: expected {expected[key]!r}, got {actual[key]!r}"
            )
    expected_labels = {str(k): int(v) for k, v in expected["label_counts"].items()}
    actual_labels = {str(k): int(v) for k, v in actual["label_counts"].items()}
    if actual_labels != expected_labels:
        errors.append(
            f"label_counts mismatch for {path}: expected {expected_labels!r}, got {actual_labels!r}"
        )
    return errors, actual


def source_path(benchmark_repo: Path, dataset: dict[str, Any]) -> Path:
    return join_relative(benchmark_repo, dataset["source_benchmark_csv"])


def target_path(output_root: Path, dataset: dict[str, Any]) -> Path:
    return join_relative(output_root, dataset["target_local_csv"])
