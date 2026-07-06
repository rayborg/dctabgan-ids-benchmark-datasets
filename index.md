---
title: DCTABGAN IDS Benchmark Datasets
---

# DCTABGAN IDS Benchmark Datasets

This GitHub Pages-ready repository is the public-safe subset of the full 30-task no-DoS DCTABGAN IDS benchmark surface.

It directly redistributes 17 cleaned CSVs and documents 13 omitted/not redistributed tasks for local reproduction. The full benchmark remains 30 binary attack-vs-benign/normal tasks.

- Data overview: [`download.html`](download.html)
- Dataset manifest: [`metadata/datasets.json`](metadata/datasets.json)
- CSV manifest: [`metadata/datasets.csv`](metadata/datasets.csv)
- Omitted-task machine manifest: [`metadata/omitted-datasets.json`](metadata/omitted-datasets.json)
- Omitted-task reproduction: [`metadata/omitted-datasets-reproduction.md`](metadata/omitted-datasets-reproduction.md)
- Local recreation scripts: [`scripts/list_tasks.py`](scripts/list_tasks.py) and [`scripts/export_benchmark_splits.py`](scripts/export_benchmark_splits.py)
- Checksums: [`SHA256SUMS.txt`](SHA256SUMS.txt)
- Source manifests: [`metadata/source_manifests/benchmark_definitions/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_NODOS_30D_BENCHMARK_DEFINITION_2026-05-11.json`](metadata/source_manifests/benchmark_definitions/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_NODOS_30D_BENCHMARK_DEFINITION_2026-05-11.json)

## Benchmark-Ready CSV Meaning

The downloadable CSVs are the exact cleaned, selected, preserved-ratio input CSVs used by the benchmark definitions. They already have binary `label` semantics (`0` majority benign/normal, `1` minority attack), no-DoS/no-DDoS scope selection, preserved-ratio row counts, benchmark row order, and recorded task-specific materialization drops.

They are not already train/test files, estimator-specific encodings, scaled matrices, train-imputed matrices, or synthetic DCTABGAN outputs. Provenance columns such as `source_row_index` remain in the full CSVs for auditability and should usually be stripped before ML fitting.

Use `scripts/export_benchmark_splits.py` to reconstruct benchmark-consistent train/test files and drop `source_row_index` by default:

```bash
python3 scripts/list_tasks.py --status downloadable
python3 scripts/export_benchmark_splits.py \
  --task friday_bot \
  --output-dir ml_exports/friday_bot
```

Add `--encoded` for basic dependency-free `X_train.csv`, `y_train.csv`, `X_test.csv`, and `y_test.csv` exports fitted from train rows only.

## Public Bundle Scope

| Source corpus | Full tasks | Downloadable CSVs | Omitted tasks | Status |
|---|---:|---:|---:|---|
| CIC-IDS-2017 | 4 | 4 | 0 | Downloadable with CIC provenance/citation caveat; no project relicensing |
| CSE-CIC-IDS2018 | 4 | 4 | 0 | Downloadable with CIC/UNB provenance/citation caveat; no project relicensing |
| HIKARI-2021 | 2 | 2 | 0 | Downloadable under documented CC BY 4.0 route with attribution |
| 5G-NIDD | 3 | 3 | 0 | Downloadable under Fairdata CC BY 4.0 route; IEEE route remains gated |
| RT-IoT2022 | 4 | 4 | 0 | Downloadable under UCI CC BY 4.0 route with attribution |
| Edge-IIoTset | 6 | 0 | 6 | Omitted/not redistributed; local reproduction only |
| CIC-UNSW-NB15 | 5 | 0 | 5 | Omitted/not redistributed; local reproduction only |
| CICIoMT2024Small mirror | 2 | 0 | 2 | Omitted/not redistributed; local reproduction only |
| Total | 30 | 17 | 13 | Public-safe subset |

Each dataset row includes `downloadable`, `public_bundle_status`, `public_csv`, `source_benchmark_csv`, `omission_reason`, and `redistribution_caveat` fields.

## Reproduce Omitted Tasks Locally

The omitted tasks are not present as downloadable CSVs under `data/`. Their exact processed source paths, local layout targets, expected counts, and expected SHA256 checksums are listed in [`metadata/omitted-datasets.json`](metadata/omitted-datasets.json).

To recreate them locally from a separately obtained benchmark clone:

```bash
python3 scripts/recreate_omitted_datasets.py \
  --benchmark-repo /path/to/dctabgan-benchmark-expansion
python3 scripts/verify_omitted_datasets.py \
  --benchmark-repo /path/to/dctabgan-benchmark-expansion
```

If the benchmark processed CSVs still need to be built and the benchmark clone has the required separately obtained source inputs, add `--run-benchmark-prep` to the recreate command. The scripts copy and verify local/private omitted outputs only; they do not download or redistribute omitted corpora.

Do not redistribute omitted CSVs unless you independently verify upstream rights for your use case.

## Verification

```bash
shasum -a 256 -c SHA256SUMS.txt
```

The checksum manifest covers retained public bundle files, metadata, docs, and scripts. It does not list user-created local omitted CSV outputs.

## Redistribution Status

This release keeps provenance/licensing caveats explicit and conservative. It does not relicense upstream IDS corpora. See [`README.md`](README.md) and [`metadata/source-license-assessment.md`](metadata/source-license-assessment.md).
