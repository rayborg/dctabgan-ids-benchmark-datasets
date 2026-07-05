# Omitted Dataset Reproduction

This file documents the 13 full-benchmark tasks that are intentionally omitted from the public downloadable CSV bundle. They remain part of the 30-task benchmark metadata, but their processed CSVs are not redistributed in this repository.

Use these instructions only for local/private reproduction unless you independently verify upstream redistribution rights for your use case. This repository does not relicense upstream IDS corpora.

## Benchmark Definitions

The active operational definition and inherited dataset-surface definition in the benchmark repo are:

```text
research/docs/dctabgan_iteration_map/planning_docs/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_NODOS_30D_CLEAN_DCT_AND_GAN_DOSE_MATCHED_OPERATIONAL_BENCHMARK_DEFINITION_2026-05-20.json
research/docs/dctabgan_iteration_map/planning_docs/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_NODOS_30D_BENCHMARK_DEFINITION_2026-05-11.json
```

Mirrored copies are retained in this public repository for provenance:

```text
metadata/source_manifests/benchmark_definitions/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_NODOS_30D_CLEAN_DCT_AND_GAN_DOSE_MATCHED_OPERATIONAL_BENCHMARK_DEFINITION_2026-05-20.json
metadata/source_manifests/benchmark_definitions/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_NODOS_30D_BENCHMARK_DEFINITION_2026-05-11.json
```

## Machine-Readable Manifest

The dedicated omitted-task manifest is:

```text
metadata/omitted-datasets.json
```

It lists each omitted task's exact `source_benchmark_csv`, local `target_local_csv`, benchmark rebuild script, expected SHA256 checksum, byte size, row count, column count, and label counts.

## Local Copy Workflow

Use this from the release repository root after separately obtaining or cloning the benchmark repo:

```bash
python3 scripts/recreate_omitted_datasets.py \
  --benchmark-repo /path/to/dctabgan-benchmark-expansion
```

The script copies only the 13 omitted processed benchmark CSVs into this repository's local-only omitted layout. It verifies each source CSV against the expected path, counts, and checksum before copying. The target directories are ignored by git and are not part of the public downloadable bundle.

If the benchmark repo has the required separately obtained upstream/source inputs but the processed CSVs are missing, the wrapper can run the benchmark materializers first:

```bash
python3 scripts/recreate_omitted_datasets.py \
  --benchmark-repo /path/to/dctabgan-benchmark-expansion \
  --run-benchmark-prep
```

This is a wrapper/copy workflow. It does not download upstream corpora, does not reimplement the benchmark preparation logic, and does not grant redistribution rights for the omitted corpora.

Verify recreated local outputs with:

```bash
python3 scripts/verify_omitted_datasets.py \
  --benchmark-repo /path/to/dctabgan-benchmark-expansion
```

With `--benchmark-repo` or an auto-detected sibling benchmark clone, verification checks the expected benchmark source paths and local target paths, then confirms source/target SHA256 identity. Without a benchmark path, it checks local target paths against the expected counts and checksums in `metadata/omitted-datasets.json`.

## Rebuild Commands

Run the relevant script from the benchmark repo root after satisfying the upstream raw/source access requirements recorded in the source manifests:

```bash
python3 repo/scripts/prepare_preserved_ratio_train500_test500_single_label_benchmark.py
python3 repo/scripts/prepare_modern_ids_preserved_ratio_train500_test500_benchmark.py
python3 repo/scripts/prepare_additional_modern_ids_preserved_ratio_train500_test500_benchmark.py
```

The exact processed CSV path for each omitted task is also stored in `metadata/datasets.json` as `source_benchmark_csv` and in `metadata/datasets.csv` as `source_benchmark_csv`. The local layout target, if you rebuild privately, is stored as `local_reproduction.local_data_path_if_rebuilt` in JSON and `local_data_path_if_rebuilt` in CSV.

## Exact Omitted Task Paths

| Task key | Corpus | Rebuild script | Exact processed source path in benchmark repo | Local layout target if rebuilt privately | Manifest pointers |
|---|---|---|---|---|---|
| `cic_unsw_nb15_exploits` | CIC-UNSW-NB15 | `python3 repo/scripts/prepare_preserved_ratio_train500_test500_single_label_benchmark.py` | `data/preserved_ratio_experiments/processed/train500_test500_single_label_25d/tuning_fixed/cic_unsw_nb15_exploits_vs_benign_preservedratio_train500minority_5500benign_test500minority_5500benign_fixed.csv` | `data/cic-unsw-nb15/cic_unsw_nb15_exploits/cic_unsw_nb15_exploits_vs_benign_preservedratio_train500minority_5500benign_test500minority_5500benign_fixed.csv` | `metadata/source_manifests/retained_single_label_25d/cic_unsw_nb15_exploits_vs_benign.json` |
| `cic_unsw_nb15_fuzzers` | CIC-UNSW-NB15 | `python3 repo/scripts/prepare_preserved_ratio_train500_test500_single_label_benchmark.py` | `data/preserved_ratio_experiments/processed/train500_test500_single_label_25d/tuning_fixed/cic_unsw_nb15_fuzzers_vs_benign_preservedratio_train500minority_6000benign_test500minority_6000benign_fixed.csv` | `data/cic-unsw-nb15/cic_unsw_nb15_fuzzers/cic_unsw_nb15_fuzzers_vs_benign_preservedratio_train500minority_6000benign_test500minority_6000benign_fixed.csv` | `metadata/source_manifests/retained_single_label_25d/cic_unsw_nb15_fuzzers_vs_benign.json` |
| `cic_unsw_nb15_generic` | CIC-UNSW-NB15 | `python3 repo/scripts/prepare_preserved_ratio_train500_test500_single_label_benchmark.py` | `data/preserved_ratio_experiments/processed/train500_test500_single_label_25d/tuning_fixed/cic_unsw_nb15_generic_vs_benign_preservedratio_train500minority_38500benign_test500minority_38500benign_fixed.csv` | `data/cic-unsw-nb15/cic_unsw_nb15_generic/cic_unsw_nb15_generic_vs_benign_preservedratio_train500minority_38500benign_test500minority_38500benign_fixed.csv` | `metadata/source_manifests/retained_single_label_25d/cic_unsw_nb15_generic_vs_benign.json` |
| `cic_unsw_nb15_reconnaissance` | CIC-UNSW-NB15 | `python3 repo/scripts/prepare_preserved_ratio_train500_test500_single_label_benchmark.py` | `data/preserved_ratio_experiments/processed/train500_test500_single_label_25d/tuning_fixed/cic_unsw_nb15_reconnaissance_vs_benign_preservedratio_train500minority_10500benign_test500minority_10500benign_fixed.csv` | `data/cic-unsw-nb15/cic_unsw_nb15_reconnaissance/cic_unsw_nb15_reconnaissance_vs_benign_preservedratio_train500minority_10500benign_test500minority_10500benign_fixed.csv` | `metadata/source_manifests/retained_single_label_25d/cic_unsw_nb15_reconnaissance_vs_benign.json` |
| `cic_unsw_nb15_shellcode` | CIC-UNSW-NB15 | `python3 repo/scripts/prepare_preserved_ratio_train500_test500_single_label_benchmark.py` | `data/preserved_ratio_experiments/processed/train500_test500_single_label_25d/tuning_fixed/cic_unsw_nb15_shellcode_vs_benign_preservedratio_train500minority_85000benign_test500minority_85000benign_fixed.csv` | `data/cic-unsw-nb15/cic_unsw_nb15_shellcode/cic_unsw_nb15_shellcode_vs_benign_preservedratio_train500minority_85000benign_test500minority_85000benign_fixed.csv` | `metadata/source_manifests/retained_single_label_25d/cic_unsw_nb15_shellcode_vs_benign.json` |
| `ciciomt2024_arp_spoofing_vs_benign` | CICIoMT2024Small mirror | `python3 repo/scripts/prepare_modern_ids_preserved_ratio_train500_test500_benchmark.py` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_7d/ciciomt2024_arp_spoofing_vs_benign/ciciomt2024_arp_spoofing_vs_benign_preservedratio_train500minority_12500majority_test500minority_12500majority_modern7.csv` | `data/ciciomt2024small-mirror/ciciomt2024_arp_spoofing_vs_benign/ciciomt2024_arp_spoofing_vs_benign_preservedratio_train500minority_12500majority_test500minority_12500majority_modern7.csv` | `metadata/source_manifests/materialization/modern7_materialization_manifest.json`; `metadata/source_manifests/modern_ids/ciciomt2024_arp_spoofing_vs_benign/candidate_manifest.json`; `metadata/source_manifests/modern_ids/ciciomt2024_arp_spoofing_vs_benign/split_metadata.json`; `metadata/source_manifests/modern_ids/ciciomt2024_arp_spoofing_vs_benign/access_status.md` |
| `ciciomt2024_mqtt_malformed_data_vs_benign` | CICIoMT2024Small mirror | `python3 repo/scripts/prepare_modern_ids_preserved_ratio_train500_test500_benchmark.py` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_7d/ciciomt2024_mqtt_malformed_data_vs_benign/ciciomt2024_mqtt_malformed_data_vs_benign_preservedratio_train500minority_8500majority_test500minority_8500majority_modern7.csv` | `data/ciciomt2024small-mirror/ciciomt2024_mqtt_malformed_data_vs_benign/ciciomt2024_mqtt_malformed_data_vs_benign_preservedratio_train500minority_8500majority_test500minority_8500majority_modern7.csv` | `metadata/source_manifests/materialization/modern7_materialization_manifest.json`; `metadata/source_manifests/modern_ids/ciciomt2024_mqtt_malformed_data_vs_benign/candidate_manifest.json`; `metadata/source_manifests/modern_ids/ciciomt2024_mqtt_malformed_data_vs_benign/split_metadata.json`; `metadata/source_manifests/modern_ids/ciciomt2024_mqtt_malformed_data_vs_benign/access_status.md` |
| `edge_iiotset_sql_injection_vs_normal` | Edge-IIoTset | `python3 repo/scripts/prepare_modern_ids_preserved_ratio_train500_test500_benchmark.py` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_7d/edge_iiotset_sql_injection_vs_normal/edge_iiotset_sql_injection_vs_normal_preservedratio_train500minority_15500majority_test500minority_15500majority_modern7.csv` | `data/edge-iiotset/edge_iiotset_sql_injection_vs_normal/edge_iiotset_sql_injection_vs_normal_preservedratio_train500minority_15500majority_test500minority_15500majority_modern7.csv` | `metadata/source_manifests/materialization/modern7_materialization_manifest.json`; `metadata/source_manifests/modern_ids/edge_iiotset_sql_injection_vs_normal/candidate_manifest.json`; `metadata/source_manifests/modern_ids/edge_iiotset_sql_injection_vs_normal/split_metadata.json` |
| `edge_iiotset_password_vs_normal` | Edge-IIoTset | `python3 repo/scripts/prepare_modern_ids_preserved_ratio_train500_test500_benchmark.py` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_7d/edge_iiotset_password_vs_normal/edge_iiotset_password_vs_normal_preservedratio_train500minority_16000majority_test500minority_16000majority_modern7.csv` | `data/edge-iiotset/edge_iiotset_password_vs_normal/edge_iiotset_password_vs_normal_preservedratio_train500minority_16000majority_test500minority_16000majority_modern7.csv` | `metadata/source_manifests/materialization/modern7_materialization_manifest.json`; `metadata/source_manifests/modern_ids/edge_iiotset_password_vs_normal/candidate_manifest.json`; `metadata/source_manifests/modern_ids/edge_iiotset_password_vs_normal/split_metadata.json` |
| `edge_iiotset_uploading_vs_normal` | Edge-IIoTset | `python3 repo/scripts/prepare_modern_ids_preserved_ratio_train500_test500_benchmark.py` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_7d/edge_iiotset_uploading_vs_normal/edge_iiotset_uploading_vs_normal_preservedratio_train500minority_21000majority_test500minority_21000majority_modern7.csv` | `data/edge-iiotset/edge_iiotset_uploading_vs_normal/edge_iiotset_uploading_vs_normal_preservedratio_train500minority_21000majority_test500minority_21000majority_modern7.csv` | `metadata/source_manifests/materialization/modern7_materialization_manifest.json`; `metadata/source_manifests/modern_ids/edge_iiotset_uploading_vs_normal/candidate_manifest.json`; `metadata/source_manifests/modern_ids/edge_iiotset_uploading_vs_normal/split_metadata.json` |
| `edge_iiotset_vulnerability_scanner_vs_normal` | Edge-IIoTset | `python3 repo/scripts/prepare_additional_modern_ids_preserved_ratio_train500_test500_benchmark.py` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_additional10/edge_iiotset_vulnerability_scanner_vs_normal/edge_iiotset_vulnerability_scanner_vs_normal_preservedratio_train500minority_16000majority_test500minority_16000majority_additional10.csv` | `data/edge-iiotset/edge_iiotset_vulnerability_scanner_vs_normal/edge_iiotset_vulnerability_scanner_vs_normal_preservedratio_train500minority_16000majority_test500minority_16000majority_additional10.csv` | `metadata/source_manifests/materialization/additional10_materialization_manifest.json`; `metadata/source_manifests/modern_ids/edge_iiotset_vulnerability_scanner_vs_normal/candidate_manifest.json`; `metadata/source_manifests/modern_ids/edge_iiotset_vulnerability_scanner_vs_normal/split_metadata.json` |
| `edge_iiotset_backdoor_vs_normal` | Edge-IIoTset | `python3 repo/scripts/prepare_additional_modern_ids_preserved_ratio_train500_test500_benchmark.py` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_additional10/edge_iiotset_backdoor_vs_normal/edge_iiotset_backdoor_vs_normal_preservedratio_train500minority_32000majority_test500minority_32000majority_additional10.csv` | `data/edge-iiotset/edge_iiotset_backdoor_vs_normal/edge_iiotset_backdoor_vs_normal_preservedratio_train500minority_32000majority_test500minority_32000majority_additional10.csv` | `metadata/source_manifests/materialization/additional10_materialization_manifest.json`; `metadata/source_manifests/modern_ids/edge_iiotset_backdoor_vs_normal/candidate_manifest.json`; `metadata/source_manifests/modern_ids/edge_iiotset_backdoor_vs_normal/split_metadata.json` |
| `edge_iiotset_port_scanning_vs_normal` | Edge-IIoTset | `python3 repo/scripts/prepare_additional_modern_ids_preserved_ratio_train500_test500_benchmark.py` | `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_additional10/edge_iiotset_port_scanning_vs_normal/edge_iiotset_port_scanning_vs_normal_preservedratio_train500minority_35500majority_test500minority_35500majority_additional10.csv` | `data/edge-iiotset/edge_iiotset_port_scanning_vs_normal/edge_iiotset_port_scanning_vs_normal_preservedratio_train500minority_35500majority_test500minority_35500majority_additional10.csv` | `metadata/source_manifests/materialization/additional10_materialization_manifest.json`; `metadata/source_manifests/modern_ids/edge_iiotset_port_scanning_vs_normal/candidate_manifest.json`; `metadata/source_manifests/modern_ids/edge_iiotset_port_scanning_vs_normal/split_metadata.json` |

## Omission Caveats

| Corpus | Omission reason |
|---|---|
| CIC-UNSW-NB15 | Academic use and citation requirements are clear, but redistribution of repackaged or derived benchmark subsets was not explicitly verified from the documented source route. |
| CICIoMT2024Small mirror | The benchmark used a public small-artifact mirror rather than an official open Small release; mirror-specific license terms were not clearly exposed and labels were assigned from filenames. |
| Edge-IIoTset | The official IEEE DataPort route is gated and public mirror terms carry noncommercial/share-alike obligations that should not be overclaimed for a general public bundle. |
