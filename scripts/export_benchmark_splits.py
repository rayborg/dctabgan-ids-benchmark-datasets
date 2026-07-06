#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import statistics
import sys
from pathlib import Path
from typing import Any


DEFAULT_DROP_COLUMNS = ["source_row_index"]
MISSING_TOKENS = {"", "nan", "none", "null"}


def default_release_root() -> Path:
    return Path(__file__).resolve().parents[1]


def safe_join(root: Path, relative_path: str) -> Path:
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Refusing unsafe relative path: {relative_path}")
    return root / relative


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def load_metadata(release_root: Path, metadata_path: str | None) -> dict[str, Any]:
    path = Path(metadata_path or "metadata/datasets.json").expanduser()
    if not path.is_absolute():
        path = release_root / path
    return load_json(path)


def task_by_key(metadata: dict[str, Any], task_key: str) -> dict[str, Any]:
    for dataset in metadata["datasets"]:
        if dataset["task_key"] == task_key:
            return dataset
    known = ", ".join(dataset["task_key"] for dataset in metadata["datasets"])
    raise SystemExit(f"Unknown task key {task_key!r}. Known tasks: {known}")


def benchmark_definition_task(
    release_root: Path,
    metadata: dict[str, Any],
    dataset: dict[str, Any],
    definition_path: str | None,
) -> dict[str, Any]:
    path_text = definition_path or metadata.get("inherited_dataset_surface_definition")
    if not path_text:
        return {}
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = release_root / path
    definition = load_json(path)
    for task in definition.get("datasets", []):
        if task.get("key") == dataset["task_key"]:
            try:
                display_path = str(path.relative_to(release_root))
            except ValueError:
                display_path = str(path)
            return {"definition_path": display_path, **task}
    raise SystemExit(f"Task {dataset['task_key']!r} was not found in benchmark definition {path}")


def resolve_input_csv(release_root: Path, dataset: dict[str, Any], csv_path: str | None) -> Path:
    if csv_path:
        path = Path(csv_path).expanduser()
        return path if path.is_absolute() else (release_root / path)
    if dataset.get("public_csv"):
        return safe_join(release_root, dataset["public_csv"])
    reproduction = dataset.get("local_reproduction") or {}
    local_path = reproduction.get("local_data_path_if_rebuilt")
    if local_path:
        return safe_join(release_root, str(local_path))
    raise SystemExit(f"No local CSV path is recorded for task {dataset['task_key']!r}.")


def normalized_label(value: str) -> str:
    text = str(value).strip()
    try:
        numeric = float(text)
    except ValueError:
        return text
    if math.isfinite(numeric) and numeric.is_integer():
        return str(int(numeric))
    return text


def expected_split_counts(dataset: dict[str, Any]) -> dict[str, dict[str, int]]:
    majority = str(dataset.get("majority_label", 0))
    minority = str(dataset.get("minority_label", 1))
    return {
        "train": {
            majority: int(dataset["train_counts"]["majority"]),
            minority: int(dataset["train_counts"]["minority"]),
        },
        "test": {
            majority: int(dataset["test_counts"]["majority"]),
            minority: int(dataset["test_counts"]["minority"]),
        },
        "val": {majority: 0, minority: 0},
    }


def read_and_split(
    csv_path: Path,
    dataset: dict[str, Any],
    benchmark_task: dict[str, Any],
    drop_columns: set[str],
) -> tuple[list[str], dict[str, list[dict[str, str]]], dict[str, Any]]:
    split_mode = str(benchmark_task.get("split_mode") or dataset.get("split_mode"))
    if split_mode != "classwise_temporal":
        raise SystemExit(f"Unsupported split_mode for this helper: {split_mode!r}")

    label_column = str(dataset.get("label_column") or "label")
    if not csv_path.exists():
        message = f"Input CSV does not exist: {csv_path}"
        if not dataset.get("downloadable"):
            message += "\nFor omitted tasks, run scripts/recreate_omitted_datasets.py first."
        raise SystemExit(message)

    expected = expected_split_counts(dataset)
    seen_by_label = {label: 0 for label in expected["train"]}
    split_rows: dict[str, list[dict[str, str]]] = {"train": [], "val": [], "test": []}
    split_label_counts: dict[str, dict[str, int]] = {"train": {}, "val": {}, "test": {}}

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise SystemExit(f"CSV has no header: {csv_path}")
        if label_column not in reader.fieldnames:
            raise SystemExit(f"CSV missing label column {label_column!r}: {csv_path}")
        if label_column in drop_columns:
            raise SystemExit(f"Refusing to drop label column {label_column!r}")

        output_fieldnames = [column for column in reader.fieldnames if column not in drop_columns]
        for row in reader:
            label = normalized_label(row[label_column])
            if label not in seen_by_label:
                raise SystemExit(f"Unexpected label {label!r} in {csv_path}; expected {sorted(seen_by_label)}")

            offset = seen_by_label[label]
            train_limit = expected["train"][label]
            val_limit = train_limit + expected["val"][label]
            test_limit = val_limit + expected["test"][label]
            if offset < train_limit:
                split_name = "train"
            elif offset < val_limit:
                split_name = "val"
            elif offset < test_limit:
                split_name = "test"
            else:
                raise SystemExit(f"Too many rows for label {label!r} in {csv_path}")

            seen_by_label[label] += 1
            split_rows[split_name].append({column: row[column] for column in output_fieldnames})
            split_label_counts[split_name][label] = split_label_counts[split_name].get(label, 0) + 1

    for split_name in ("train", "val", "test"):
        for label, count in expected[split_name].items():
            actual = split_label_counts[split_name].get(label, 0)
            if actual != count:
                raise SystemExit(
                    f"{split_name} label {label} count mismatch for {dataset['task_key']}: "
                    f"expected {count}, got {actual}"
                )
    return output_fieldnames, split_rows, {"expected": expected, "actual": split_label_counts}


def planned_outputs(output_dir: Path, include_val: bool, encoded: bool) -> list[Path]:
    paths = [output_dir / "train.csv", output_dir / "test.csv", output_dir / "split_metadata.json"]
    if include_val:
        paths.append(output_dir / "val.csv")
    if encoded:
        paths.extend(
            [
                output_dir / "X_train.csv",
                output_dir / "y_train.csv",
                output_dir / "X_test.csv",
                output_dir / "y_test.csv",
                output_dir / "encoded_metadata.json",
            ]
        )
        if include_val:
            paths.extend([output_dir / "X_val.csv", output_dir / "y_val.csv"])
    return paths


def ensure_outputs_available(paths: list[Path], overwrite: bool) -> None:
    existing = [path for path in paths if path.exists()]
    if existing and not overwrite:
        formatted = "\n".join(str(path) for path in existing)
        raise SystemExit(f"Output file(s) already exist. Use --overwrite to replace them:\n{formatted}")


def write_split_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_missing(value: str) -> bool:
    return str(value).strip().lower() in MISSING_TOKENS


def parse_float(value: str) -> float | None:
    if is_missing(value):
        return None
    try:
        numeric = float(str(value).strip())
    except ValueError:
        return None
    if not math.isfinite(numeric):
        return None
    return numeric


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", str(value).strip()).strip("_").lower()
    return slug or "missing"


def unique_name(base: str, used: set[str]) -> str:
    candidate = base
    index = 2
    while candidate in used:
        candidate = f"{base}_{index}"
        index += 1
    used.add(candidate)
    return candidate


def fit_basic_encoder(
    train_rows: list[dict[str, str]],
    feature_columns: list[str],
) -> tuple[list[str], dict[str, Any]]:
    used_output_names: set[str] = set()
    encoded_columns: list[str] = []
    features: dict[str, Any] = {}

    for column in feature_columns:
        raw_values = [row.get(column, "") for row in train_rows]
        nonmissing = [value for value in raw_values if not is_missing(value)]
        parsed = [parse_float(value) for value in nonmissing]
        if len(nonmissing) == 0 or all(value is not None for value in parsed):
            numbers = [float(value) for value in parsed if value is not None]
            fill_value = float(statistics.median(numbers)) if numbers else 0.0
            output_name = unique_name(column, used_output_names)
            encoded_columns.append(output_name)
            features[column] = {
                "kind": "numeric",
                "output_column": output_name,
                "fill_value": fill_value,
            }
            continue

        categories = sorted({value if not is_missing(value) else "__MISSING__" for value in raw_values})
        output_columns = []
        for category in categories:
            output_name = unique_name(f"{column}__{slugify(category)}", used_output_names)
            output_columns.append(output_name)
            encoded_columns.append(output_name)
        features[column] = {
            "kind": "categorical",
            "categories": categories,
            "output_columns": output_columns,
        }

    return encoded_columns, {"features": features, "output_columns": encoded_columns}


def transform_basic_encoder(
    rows: list[dict[str, str]],
    feature_columns: list[str],
    encoder: dict[str, Any],
) -> tuple[list[dict[str, str]], dict[str, int]]:
    transformed: list[dict[str, str]] = []
    unknown_counts: dict[str, int] = {}
    features = encoder["features"]
    for row in rows:
        output: dict[str, str] = {}
        for column in feature_columns:
            spec = features[column]
            raw_value = row.get(column, "")
            if spec["kind"] == "numeric":
                numeric = parse_float(raw_value)
                if numeric is None:
                    numeric = float(spec["fill_value"])
                output[spec["output_column"]] = repr(float(numeric))
            else:
                value = raw_value if not is_missing(raw_value) else "__MISSING__"
                categories = spec["categories"]
                if value not in categories:
                    unknown_counts[column] = unknown_counts.get(column, 0) + 1
                for category, output_column in zip(categories, spec["output_columns"]):
                    output[output_column] = "1" if value == category else "0"
        transformed.append(output)
    return transformed, unknown_counts


def write_xy(
    output_dir: Path,
    split_name: str,
    encoded_columns: list[str],
    encoded_rows: list[dict[str, str]],
    labels: list[str],
) -> None:
    with (output_dir / f"X_{split_name}.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=encoded_columns)
        writer.writeheader()
        writer.writerows(encoded_rows)
    with (output_dir / f"y_{split_name}.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["label"])
        for label in labels:
            writer.writerow([label])


def write_encoded_exports(
    output_dir: Path,
    fieldnames: list[str],
    split_rows: dict[str, list[dict[str, str]]],
    label_column: str,
) -> dict[str, Any]:
    feature_columns = [column for column in fieldnames if column != label_column]
    encoded_columns, encoder = fit_basic_encoder(split_rows["train"], feature_columns)
    unknown_by_split: dict[str, dict[str, int]] = {}

    for split_name in ("train", "val", "test"):
        rows = split_rows[split_name]
        if not rows and split_name == "val":
            continue
        encoded_rows, unknown_counts = transform_basic_encoder(rows, feature_columns, encoder)
        labels = [normalized_label(row[label_column]) for row in rows]
        write_xy(output_dir, split_name, encoded_columns, encoded_rows, labels)
        unknown_by_split[split_name] = unknown_counts

    metadata = {
        "fit_semantics": "Basic encoder fitted on train rows only, then applied to val/test.",
        "numeric_policy": "Columns numeric in train are exported as floats; missing or non-finite values use the train median, or 0.0 if the train column is empty.",
        "categorical_policy": "Columns non-numeric in train are one-hot encoded using train categories only; unseen val/test categories are all-zero for that source column and counted below.",
        "feature_columns_before_encoding": feature_columns,
        "encoded_feature_columns": encoded_columns,
        "encoder": encoder["features"],
        "unknown_category_counts": unknown_by_split,
    }
    write_json(output_dir / "encoded_metadata.json", metadata)
    return metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Export benchmark-consistent train/test splits for one DCTABGAN IDS task. "
            "The helper reads metadata/datasets.json and the mirrored benchmark definition."
        )
    )
    parser.add_argument("--task", required=True, help="Task key, e.g. friday_bot.")
    parser.add_argument("--release-root", default=str(default_release_root()))
    parser.add_argument("--metadata", default=None, help="Path to metadata/datasets.json.")
    parser.add_argument("--benchmark-definition", default=None, help="Override the mirrored benchmark definition path.")
    parser.add_argument("--csv-path", default=None, help="Override the input CSV path for this task.")
    parser.add_argument("--output-dir", default=None, help="Default: ml_exports/<task> under the release root.")
    parser.add_argument("--drop-column", action="append", default=[], help="Additional non-feature column to drop; repeatable.")
    parser.add_argument(
        "--keep-provenance-columns",
        action="store_true",
        help="Keep default provenance columns such as source_row_index instead of dropping them.",
    )
    parser.add_argument("--encoded", action="store_true", help="Also write basic numeric X/y CSVs fitted on train only.")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing exported files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    release_root = Path(args.release_root).expanduser().resolve()
    metadata = load_metadata(release_root, args.metadata)
    dataset = task_by_key(metadata, args.task)
    benchmark_task = benchmark_definition_task(release_root, metadata, dataset, args.benchmark_definition)
    input_csv = resolve_input_csv(release_root, dataset, args.csv_path).resolve()

    output_dir = Path(args.output_dir or (release_root / "ml_exports" / args.task)).expanduser()
    if not output_dir.is_absolute():
        output_dir = release_root / output_dir
    output_dir = output_dir.resolve()

    drop_columns = set(args.drop_column)
    if not args.keep_provenance_columns:
        drop_columns.update(DEFAULT_DROP_COLUMNS)

    fieldnames, split_rows, count_metadata = read_and_split(input_csv, dataset, benchmark_task, drop_columns)
    include_val = bool(split_rows["val"])
    ensure_outputs_available(planned_outputs(output_dir, include_val, bool(args.encoded)), bool(args.overwrite))
    output_dir.mkdir(parents=True, exist_ok=True)

    write_split_csv(output_dir / "train.csv", fieldnames, split_rows["train"])
    if include_val:
        write_split_csv(output_dir / "val.csv", fieldnames, split_rows["val"])
    write_split_csv(output_dir / "test.csv", fieldnames, split_rows["test"])

    encoded_metadata = None
    if args.encoded:
        encoded_metadata = write_encoded_exports(output_dir, fieldnames, split_rows, str(dataset.get("label_column") or "label"))

    split_metadata = {
        "task_key": dataset["task_key"],
        "title": dataset["title"],
        "source_corpus": dataset["source_corpus"],
        "public_bundle_status": dataset["public_bundle_status"],
        "downloadable": bool(dataset.get("downloadable")),
        "input_csv": str(input_csv),
        "benchmark_definition_task": benchmark_task,
        "split_mode": benchmark_task.get("split_mode") or dataset.get("split_mode"),
        "test_size": benchmark_task.get("test_size") or dataset.get("test_size"),
        "val_size": benchmark_task.get("val_size") or dataset.get("val_size"),
        "label_column": dataset.get("label_column") or "label",
        "dropped_columns_from_export": sorted(column for column in drop_columns if column),
        "row_order_semantics": "CSV rows are split classwise in existing row order: first train count per class, then val count, then test count; rows within each output split keep original CSV order.",
        "split_counts": count_metadata,
        "output_files": {
            "train_csv": str(output_dir / "train.csv"),
            "val_csv": str(output_dir / "val.csv") if include_val else None,
            "test_csv": str(output_dir / "test.csv"),
            "encoded_metadata_json": str(output_dir / "encoded_metadata.json") if encoded_metadata else None,
        },
        "redistribution_caveat": dataset.get("redistribution_caveat"),
    }
    write_json(output_dir / "split_metadata.json", split_metadata)

    print(f"Wrote benchmark split exports for {dataset['task_key']} to {output_dir}")
    print(f"  train rows: {len(split_rows['train'])}")
    print(f"  test rows:  {len(split_rows['test'])}")
    if args.encoded:
        print("  encoded X/y CSVs: yes, fitted on train rows only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
