# DCTABGAN IDS Benchmark Datasets

This repository is a GitHub Pages-ready, public-safe subset of the full 30-task no-DoS DCTABGAN IDS benchmark dataset surface.

The full benchmark remains 30 binary attack-vs-benign/normal tasks. This public bundle directly redistributes 17 cleaned CSVs and documents 13 additional tasks as omitted/not redistributed for local reproduction only.

These are real, cleaned, preserved-ratio, benchmark-ready IDS classification inputs for ML use. They are not synthetic DCTABGAN outputs. Each task uses `label` as the target, where `0` is the majority benign/normal class and `1` is the minority attack class.

## What Is Included

- 17 processed CSV datasets under `data/`, grouped by source corpus and task key.
- Metadata for all 30 benchmark tasks in `metadata/datasets.json` and `metadata/datasets.csv`.
- A machine-readable omitted-dataset copy manifest in `metadata/omitted-datasets.json`.
- Machine-readable availability fields that distinguish downloadable CSVs from omitted/not redistributed tasks.
- Source benchmark definitions and materialization/task manifests under `metadata/source_manifests/`.
- Reproduction instructions for omitted tasks in `metadata/omitted-datasets-reproduction.md`.
- Local recreation and verification scripts under `scripts/`.
- `SHA256SUMS.txt` and `metadata/checksums.json` for the retained public bundle files.

## Public Bundle Scope

Directly downloadable CSVs are kept only for CIC-IDS-2017, CSE-CIC-IDS2018, HIKARI-2021, 5G-NIDD, and RT-IoT2022. Edge-IIoTset, CIC-UNSW-NB15, and the CICIoMT2024Small mirror tasks are metadata-only omissions in this public release.

| Source corpus | Full benchmark tasks | Downloadable CSVs under `data/` | Omitted/not redistributed tasks | Public release status |
|---|---:|---:|---:|---|
| CIC-IDS-2017 | 4 | 4 | 0 | Downloadable with CIC provenance caveats |
| CSE-CIC-IDS2018 | 4 | 4 | 0 | Downloadable with CIC provenance caveats |
| HIKARI-2021 | 2 | 2 | 0 | Downloadable with CC BY 4.0 attribution caveat |
| 5G-NIDD | 3 | 3 | 0 | Downloadable with Fairdata CC BY 4.0 attribution caveat |
| RT-IoT2022 | 4 | 4 | 0 | Downloadable with UCI CC BY 4.0 attribution caveat |
| Edge-IIoTset | 6 | 0 | 6 | Omitted; documented for local reproduction |
| CIC-UNSW-NB15 | 5 | 0 | 5 | Omitted; documented for local reproduction |
| CICIoMT2024Small mirror | 2 | 0 | 2 | Omitted; documented for local reproduction |
| Total | 30 | 17 | 13 | Public-safe subset of the full benchmark |

## Availability Metadata

Every row in `metadata/datasets.json` and `metadata/datasets.csv` includes availability fields:

- `downloadable`: `true` when a CSV is included under `data/`, `false` when the task is omitted from the public CSV bundle.
- `public_bundle_status`: `downloadable_csv_included` or `omitted_not_redistributed`.
- `public_csv`: the directly downloadable CSV path for included tasks; `null` or empty for omitted tasks.
- `source_benchmark_csv`: the exact processed CSV path inside the benchmark repo for rebuilding or local copying.
- `local_reproduction`: benchmark definition paths, mirrored manifest paths, rebuild script, and local layout path if the user rebuilds privately.
- `metadata/omitted-datasets.json`: the dedicated omitted-task manifest with source paths, local output paths, expected counts, and expected SHA256 checksums.
- `omission_reason` and `omission_caveat`: populated for omitted tasks.
- `redistribution_caveat`: conservative provenance/licensing note for every corpus.

## Split And Count Semantics

The downloadable CSV files are full cleaned selected-row datasets, not separate train/test files. The benchmark definitions specify `split_mode: classwise_temporal`, `test_size: 0.5`, and `val_size: 0.0`. Downstream benchmark code reconstructs train/test partitions from the definition and row order.

Every task in the 30-task benchmark has exactly 500 minority attack rows for train and 500 minority attack rows for test. Majority train/test counts preserve the source-ratio floor for each task and are recorded in `metadata/datasets.json`, including the omitted tasks.

## Omitted Dataset Reproduction

The source-of-truth dataset surface is inherited from the May 11 definition, and the active operational equal-dose definition inherits that surface:

```text
research/docs/dctabgan_iteration_map/planning_docs/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_NODOS_30D_CLEAN_DCT_AND_GAN_DOSE_MATCHED_OPERATIONAL_BENCHMARK_DEFINITION_2026-05-20.json
research/docs/dctabgan_iteration_map/planning_docs/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_NODOS_30D_BENCHMARK_DEFINITION_2026-05-11.json
```

Mirrored copies are included in this repository:

```text
metadata/source_manifests/benchmark_definitions/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_NODOS_30D_CLEAN_DCT_AND_GAN_DOSE_MATCHED_OPERATIONAL_BENCHMARK_DEFINITION_2026-05-20.json
metadata/source_manifests/benchmark_definitions/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_NODOS_30D_BENCHMARK_DEFINITION_2026-05-11.json
```

The runnable clone/copy manifest for the omitted tasks is:

```text
metadata/omitted-datasets.json
```

The practical recreation path is to use a separately obtained or separately cloned benchmark worktree, then copy the exact processed benchmark CSVs into this repository's local-only omitted layout:

```bash
python3 scripts/recreate_omitted_datasets.py \
  --benchmark-repo /path/to/dctabgan-benchmark-expansion
```

The script validates each benchmark source CSV against the expected path, row count, column count, label counts, byte size, and SHA256 checksum before copying. It writes only the 13 omitted CSVs to the local target paths listed in `metadata/omitted-datasets.json`; the omitted target directories are ignored by git and are not part of the public release bundle.

If the benchmark clone has the required separately obtained upstream inputs but the processed CSVs have not been materialized yet, the wrapper can invoke the benchmark repo's own materialization scripts before copying:

```bash
python3 scripts/recreate_omitted_datasets.py \
  --benchmark-repo /path/to/dctabgan-benchmark-expansion \
  --run-benchmark-prep
```

This wrapper does not download upstream corpora and does not relicense or redistribute omitted data. It delegates any rebuild to the benchmark repo scripts, then verifies that the resulting processed CSVs match the benchmark files used for this release.

You can also run the underlying benchmark materialization scripts yourself from the benchmark worktree:

```bash
python3 repo/scripts/prepare_preserved_ratio_train500_test500_single_label_benchmark.py
python3 repo/scripts/prepare_modern_ids_preserved_ratio_train500_test500_benchmark.py
python3 repo/scripts/prepare_additional_modern_ids_preserved_ratio_train500_test500_benchmark.py
```

Verify local recreated omitted outputs with:

```bash
python3 scripts/verify_omitted_datasets.py \
  --benchmark-repo /path/to/dctabgan-benchmark-expansion
```

When the benchmark path is supplied or auto-detected, the verifier checks both the expected source files and local target files, and confirms source/target SHA256 identity. Without a benchmark path, it verifies local targets against the expected counts and checksums recorded in `metadata/omitted-datasets.json`.

For omitted tasks, copy or use the exact processed source paths below only in a local/private environment unless you have independently verified redistribution rights.

| Task key | Exact benchmark repo processed source path |
|---|---|
| `cic_unsw_nb15_exploits` | `data/preserved_ratio_experiments/processed/train500_test500_single_label_25d/tuning_fixed/cic_unsw_nb15_exploits_vs_benign_preservedratio_train500minority_5500benign_test500minority_5500benign_fixed.csv` |
| `cic_unsw_nb15_fuzzers` | `data/preserved_ratio_experiments/processed/train500_test500_single_label_25d/tuning_fixed/cic_unsw_nb15_fuzzers_vs_benign_preservedratio_train500minority_6000benign_test500minority_6000benign_fixed.csv` |
| `cic_unsw_nb15_generic` | `data/preserved_ratio_experiments/processed/train500_test500_single_label_25d/tuning_fixed/cic_unsw_nb15_generic_vs_benign_preservedratio_train500minority_38500benign_test500minority_38500benign_fixed.csv` |
| `cic_unsw_nb15_reconnaissance` | `data/preserved_ratio_experiments/processed/train500_test500_single_label_25d/tuning_fixed/cic_unsw_nb15_reconnaissance_vs_benign_preservedratio_train500minority_10500benign_test500minority_10500benign_fixed.csv` |
| `cic_unsw_nb15_shellcode` | `data/preserved_ratio_experiments/processed/train500_test500_single_label_25d/tuning_fixed/cic_unsw_nb15_shellcode_vs_benign_preservedratio_train500minority_85000benign_test500minority_85000benign_fixed.csv` |
| `ciciomt2024_arp_spoofing_vs_benign` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_7d/ciciomt2024_arp_spoofing_vs_benign/ciciomt2024_arp_spoofing_vs_benign_preservedratio_train500minority_12500majority_test500minority_12500majority_modern7.csv` |
| `ciciomt2024_mqtt_malformed_data_vs_benign` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_7d/ciciomt2024_mqtt_malformed_data_vs_benign/ciciomt2024_mqtt_malformed_data_vs_benign_preservedratio_train500minority_8500majority_test500minority_8500majority_modern7.csv` |
| `edge_iiotset_sql_injection_vs_normal` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_7d/edge_iiotset_sql_injection_vs_normal/edge_iiotset_sql_injection_vs_normal_preservedratio_train500minority_15500majority_test500minority_15500majority_modern7.csv` |
| `edge_iiotset_password_vs_normal` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_7d/edge_iiotset_password_vs_normal/edge_iiotset_password_vs_normal_preservedratio_train500minority_16000majority_test500minority_16000majority_modern7.csv` |
| `edge_iiotset_uploading_vs_normal` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_7d/edge_iiotset_uploading_vs_normal/edge_iiotset_uploading_vs_normal_preservedratio_train500minority_21000majority_test500minority_21000majority_modern7.csv` |
| `edge_iiotset_vulnerability_scanner_vs_normal` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_additional10/edge_iiotset_vulnerability_scanner_vs_normal/edge_iiotset_vulnerability_scanner_vs_normal_preservedratio_train500minority_16000majority_test500minority_16000majority_additional10.csv` |
| `edge_iiotset_backdoor_vs_normal` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_additional10/edge_iiotset_backdoor_vs_normal/edge_iiotset_backdoor_vs_normal_preservedratio_train500minority_32000majority_test500minority_32000majority_additional10.csv` |
| `edge_iiotset_port_scanning_vs_normal` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_additional10/edge_iiotset_port_scanning_vs_normal/edge_iiotset_port_scanning_vs_normal_preservedratio_train500minority_35500majority_test500minority_35500majority_additional10.csv` |

See `metadata/omitted-datasets-reproduction.md` for the same omitted tasks with local layout targets and manifest pointers.

## Provenance Caveats

- This repository does not relicense upstream IDS corpora. Upstream terms still govern the data.
- CIC-IDS-2017 and CSE-CIC-IDS2018 are included with conservative CIC provenance and citation caveats; derivative-subset rights are not expressed as a standard open-data license.
- HIKARI-2021, 5G-NIDD, and RT-IoT2022 have the strongest documented redistribution posture here because explicit CC BY 4.0 routes were recorded, but attribution and upstream terms still apply.
- Edge-IIoTset tasks were materialized from a public Kaggle mirror while the official IEEE DataPort route was gated; the public CSVs are omitted from this release.
- CIC-UNSW-NB15 tasks are omitted because academic use is clear but redistribution of repackaged benchmark subsets was not explicitly verified.
- CICIoMT2024Small mirror tasks are omitted because the benchmark used a public small-artifact mirror rather than a clearly licensed official Small release, and labels were assigned from filenames.
- 5G-NIDD tasks were sourced from the open Fairdata route because the official IEEE DataPort route was gated. `Offset`, `SrcTCPBase`, and `DstTCPBase` were dropped during materialization.
- RT-IoT2022 tasks are small clean scan tasks; some have small train sizes relative to feature count, as noted in the manifests.
- The release follows the benchmark's no-DoS/no-DDoS/no-flood scope-control rule. This is a benchmark design decision, not a claim that DoS/DDoS attacks are unimportant.

## Verify The Release

Run this from the repository root:

```bash
shasum -a 256 -c SHA256SUMS.txt
```

The checksum file covers retained public bundle files, including metadata/docs/manifests, scripts, and the 17 downloadable CSVs. It excludes `SHA256SUMS.txt`, `metadata/checksums.json`, `.git` internals, and user-created local omitted CSV outputs. Use `scripts/verify_omitted_datasets.py` for recreated omitted CSVs.

## License And Upstream Terms

This repository packages a public-safe subset of cleaned benchmark-ready CSVs for reproducible ML benchmarking and documents the remaining full-benchmark tasks for local reproduction. It does not relicense upstream IDS corpora. Check original corpus licenses and access terms before redistributing or using the data outside benchmark reproduction.

See also: `metadata/source-license-assessment.md`.
