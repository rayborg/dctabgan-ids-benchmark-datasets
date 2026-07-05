---
title: DCTABGAN IDS Benchmark Datasets
---

# DCTABGAN IDS Benchmark Datasets

This GitHub Pages-ready repository is the public-safe subset of the full 30-task no-DoS DCTABGAN IDS benchmark surface.

It directly redistributes 17 cleaned CSVs and documents 13 omitted/not redistributed tasks for local reproduction. The full benchmark remains 30 binary attack-vs-benign/normal tasks.

- Data: [`data/`](data/)
- Dataset manifest: [`metadata/datasets.json`](metadata/datasets.json)
- CSV manifest: [`metadata/datasets.csv`](metadata/datasets.csv)
- Omitted-task machine manifest: [`metadata/omitted-datasets.json`](metadata/omitted-datasets.json)
- Omitted-task reproduction: [`metadata/omitted-datasets-reproduction.md`](metadata/omitted-datasets-reproduction.md)
- Local recreation scripts: [`scripts/`](scripts/)
- Checksums: [`SHA256SUMS.txt`](SHA256SUMS.txt)
- Source manifests: [`metadata/source_manifests/`](metadata/source_manifests/)

## Public Bundle Scope

| Source corpus | Full tasks | Downloadable CSVs | Omitted tasks | Status |
|---|---:|---:|---:|---|
| CIC-IDS-2017 | 4 | 4 | 0 | Downloadable with provenance caveats |
| CSE-CIC-IDS2018 | 4 | 4 | 0 | Downloadable with provenance caveats |
| HIKARI-2021 | 2 | 2 | 0 | Downloadable with attribution caveat |
| 5G-NIDD | 3 | 3 | 0 | Downloadable with attribution caveat |
| RT-IoT2022 | 4 | 4 | 0 | Downloadable with attribution caveat |
| Edge-IIoTset | 6 | 0 | 6 | Omitted/not redistributed |
| CIC-UNSW-NB15 | 5 | 0 | 5 | Omitted/not redistributed |
| CICIoMT2024Small mirror | 2 | 0 | 2 | Omitted/not redistributed |
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
