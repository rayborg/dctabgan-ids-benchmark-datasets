# Modern IDS 30D Pipeline Integration Plan

Date: 2026-05-11

## Objective

Integrate the seven staged modern IDS preserved-ratio tasks into the real benchmark pipeline, then recompute treatment-method utility metrics, rankings, guardrails, and statistical validation on a new 30-dataset benchmark surface.

This expands the current retained benchmark from `23 datasets x 6 learners x 11 methods = 138` learner blocks to `30 datasets x 6 learners x 11 methods = 180` learner blocks. The frozen 23D benchmark definition remains unchanged.

## Manager Decisions Applied

- Treat the seven modern tasks as provisional real-pipeline inputs using the staged public mirrors already documented in `data/staging/modern_ids_pipeline_candidates/`.
- Keep the existing six-learner panel: `LightGBM`, `LogisticRegression`, `QDA`, `RandomForest`, `kNN`, and `DeepMLP`.
- Keep the existing eleven treatment conditions: control, classical resampling, synthetic generators, algorithmic class weighting, and DCTABGAN.
- Use the current preserved-ratio rule: train/test each receive `500` attack rows and `ratio_floor * 500` majority rows.
- Use conservative Edge-IIoTset feature filtering before pipeline registration to remove obvious identifiers, payload/free-text fields, timestamps, and raw sequence/checksum artifacts.
- Keep similarity/fidelity metrics as diagnostics and guardrails; downstream IDS classification utility remains the primary treatment-method objective.

## Integrated Datasets

The modern7 benchmark definition will include:

- `hikari_bruteforce_vs_benign`
- `hikari_probing_vs_benign`
- `ciciomt2024_arp_spoofing_vs_benign`
- `ciciomt2024_mqtt_malformed_data_vs_benign`
- `edge_iiotset_sql_injection_vs_normal`
- `edge_iiotset_password_vs_normal`
- `edge_iiotset_uploading_vs_normal`

The final 30D definition will append those seven datasets to the current retained 23D definition at:

`research/docs/dctabgan_iteration_map/planning_docs/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_23D_BENCHMARK_DEFINITION_2026-04-18.json`

## Files To Create

- `repo/scripts/prepare_modern_ids_preserved_ratio_train500_test500_benchmark.py`
- `research/docs/dctabgan_iteration_map/planning_docs/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_MODERN7_BENCHMARK_DEFINITION_2026-05-11.json`
- `research/docs/dctabgan_iteration_map/planning_docs/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_30D_BENCHMARK_DEFINITION_2026-05-11.json`
- `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_7d/<candidate>/...csv`
- `data/preserved_ratio_experiments/processed/train500_test500_modern_ids_7d/<candidate>/split_metadata.json`
- `data/preserved_ratio_experiments/manifests/train500_test500_modern_ids_7d/modern7_materialization_manifest.json`
- `research/docs/PRESERVED_RATIO_TRAIN500_TEST500_MODERN_IDS_7D_PIPELINE_PREPARATION_2026-05-11.md`

## Split Handling

Current DCTABGAN, SMOTE, and imbalanced-learn baselines use `DataPreparation.preprocess_data()`. In that implementation, `source_row_index` ordering is only passed for `chronological`, not `classwise_temporal`. Therefore the pipeline-ready modern CSVs must place intended train rows before intended test rows.

The SDV baselines (`CTGAN`, `CopulaGAN`, `TVAE`) can replay explicit split metadata when `split_metadata.json` contains `train_source_row_index`, `val_source_row_index`, and `test_source_row_index`. Each modern candidate receives its own input folder so that split replay metadata cannot collide across candidates.

## Edge-IIoTset Feature Policy

Drop these Edge-IIoTset columns during pipeline materialization when present:

`Attack_label`, `Attack_type`, `frame.time`, `ip.src_host`, `ip.dst_host`, `arp.dst.proto_ipv4`, `arp.src.proto_ipv4`, `http.file_data`, `http.request.uri.query`, `http.referer`, `http.request.full_uri`, `tcp.ack`, `tcp.ack_raw`, `tcp.checksum`, `tcp.options`, `tcp.payload`, `tcp.seq`, `tcp.srcport`, `udp.stream`, `mqtt.msg`, `mqtt.topic`, `mbtcp.trans_id`.

Retain protocol, count, length, flag, and type fields such as `tcp.dstport`, `udp.port`, `tcp.len`, `mqtt.len`, `mqtt.msgtype`, DNS query/retransmission fields, and ARP opcode/size fields.

## Execution Run IDs

Modern7 smoke:

- Reference/control source run: `benchmark_modern7_smoke_reference_20260511_01`
- DCT smoke run: `benchmark_modern7_smoke_dct_20260511_01`
- Fair reference smoke run: `benchmark_modern7_smoke_faircw_reference_20260511_01`
- Fair DCT smoke run: `benchmark_modern7_smoke_faircw_dct_20260511_01`

Full 30D:

- Source reference run: `benchmark_singlelabel30_train500_test500_full_20260511_01`
- DCT checkpoint-source run: `benchmark_singlelabel30_dct_mult1_ckpts_20260511_01`
- DCT checkpoint replay run: `benchmark_singlelabel30_dct_mult1_ckpt0009_20260511_01`
- Fair reference run: `benchmark_singlelabel30_faircw_reference_20260511_01`
- Fair DCT run: `benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01`

## Execution Phases

1. Materialize modern7 processed inputs and benchmark definitions.
2. Validate all generated CSVs, manifests, split metadata, and benchmark definitions.
3. Run a modern7 smoke with `no_resampling` and a one-epoch DCT pass if runtime allows.
4. Run all non-DCT methods on modern7 or the full 30D definition.
5. Run DCT checkpoint-source training for the same benchmark definition.
6. Replay DCT epoch `0009` for the same benchmark definition.
7. Run fair utility treatment over all methods with `augmented_plus_class_weighted`.
8. Rebuild dashboards, full metric ledger, rankings, guardrail tables, and statistical tests with the 30D definition.

## Rebuild Commands

After complete final artifacts exist under the final run IDs:

```bash
PYTHONPATH=repo:repo/scripts repo/.venv/bin/python repo/scripts/build_benchmark_full_metric_ledger.py \
  --benchmark-definition research/docs/dctabgan_iteration_map/planning_docs/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_30D_BENCHMARK_DEFINITION_2026-05-11.json \
  --reference-run-id benchmark_singlelabel30_faircw_reference_20260511_01 \
  --dct-run-id benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01 \
  --ledger-path research/docs/benchmark_runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01/BENCHMARK_FULL_METRIC_LEDGER.md \
  --tables-dir research/outputs/benchmark_tables/runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01 \
  --benchmark-label "30D preserved-ratio fair utility treatment benchmark"
```

```bash
PYTHONPATH=repo:repo/scripts repo/.venv/bin/python repo/scripts/build_tuning_dataset_dashboards.py \
  --benchmark-definition research/docs/dctabgan_iteration_map/planning_docs/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_30D_BENCHMARK_DEFINITION_2026-05-11.json \
  --reference-run-id benchmark_singlelabel30_faircw_reference_20260511_01 \
  --dct-run-id benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01 \
  --role-label "Final 30D benchmark" \
  --dashboards-dir research/docs/dashboards/runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01 \
  --summary-path research/docs/dashboards/runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01/tuning_summary.html \
  --index-path research/docs/dashboards/runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01/tuning_index.html \
  --final-summary-path research/docs/dashboards/runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01/final_summary.html \
  --iteration-dashboard-path research/docs/dashboards/runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01/iteration_metrics_dashboard.html
```

## Completion Criteria

- Modern7 processed inputs exist in real pipeline data layout.
- Modern7 and 30D benchmark definitions load through current runner code.
- Generated split metadata reports `500` attack rows per train/test split for every modern candidate.
- Final 30D ledger sees `30` active datasets, `6` learners, `11` methods, and `180` matched learner blocks after full benchmark artifacts exist.
- Statistical validation is regenerated from the 30D run outputs, not copied from the retained 23D run.

## Risks

- Full 30D execution is expensive and may require resumed tranche runs.
- This worktree currently contains the generated modern7 processed inputs, but not the retained 23D processed input folder referenced by the frozen 23D definition; full 30D execution requires restoring or rematerializing those 23D inputs/artifacts.
- Public mirror provenance for CICIoMT2024 and Edge-IIoTset must be stated in paper-facing claims.
- Edge-IIoTset feature filtering changes staged feature count and must be documented as a pipeline-integration policy.
- Missing utility metrics for any method/dataset/learner will make overall scores incomplete under the current strict ranking code.
