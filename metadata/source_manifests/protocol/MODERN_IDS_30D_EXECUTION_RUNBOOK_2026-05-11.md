# Modern IDS 30D Execution Runbook

Date: 2026-05-11

## Corrected Methodology Addendum

Use `research/docs/protocol/DCTABGAN_30D_20METHOD_METHODS_SYNTHESIS_2026-05-11.md` as the corrected primary no-DoS 30D methods specification.

The primary no-DoS 20-condition outputs are now complete and validated. The commands below also document the older completed 11-method `faircw` pathway, which remains historical/sensitivity-only along with the frozen retained 23D definition.

The corrected primary run must use the no-DoS 30D definition: 13 retained non-DoS tasks, 7 prepared modern7 tasks, and 10 replacement additional10 tasks. No DoS/DDoS/flood-like task is part of the primary surface.

The corrected primary run must use 20 treatment conditions: no treatment, class-weighted only, 9 treatment-only conditions, and the same 9 treatment families with downstream class-weighted fitting. It must also use the corrected six-learner panel with `LinearSVM` replacing `kNN`; `QDA + CW` must be labeled with the balanced-prior caveat, and `kNN` must not be used in the primary +CW panel.

Primary statistical reporting for the corrected run is dataset-level over 30 datasets. Learner-block reporting over `30 x 6 = 180` blocks is sensitivity-only.

Reporting convention: paper composite remains rank-based over AP/PR-AUC, Recall, MCC, and Balanced Accuracy; the headline MCC leaderboard now uses mean raw MCC.

## Environment Status

This worktree currently has no `repo/.venv/bin/python`. The available `python3` can run the stdlib-only materialization script and runner dry-runs, but it cannot execute benchmark training, utility evaluation, dashboards, or statistical ledger generation because these imports are missing:

- `pandas`
- `numpy`
- `sklearn`
- `scipy`
- `sdv`
- `imblearn`
- `torch`

Restore/install the benchmark environment before running the non-dry-run commands below.

The generated modern7 and additional10 processed inputs are present in this worktree. A no-DoS 30D rerun also requires the 13 retained non-DoS processed inputs referenced by the frozen 23D definition and any final run artifacts chosen for reuse.

## Definitions

```bash
MODERN7_DEF="research/docs/dctabgan_iteration_map/planning_docs/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_MODERN7_BENCHMARK_DEFINITION_2026-05-11.json"
FAIRCW30D_SENSITIVITY_DEF="research/docs/dctabgan_iteration_map/planning_docs/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_30D_BENCHMARK_DEFINITION_2026-05-11.json"
NODOS30D_PRIMARY_DEF="research/docs/dctabgan_iteration_map/planning_docs/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_NODOS_30D_BENCHMARK_DEFINITION_2026-05-11.json"
CORRECTED20_DEF="$NODOS30D_PRIMARY_DEF"
```

Use `repo/.venv/bin/python` if restored; otherwise use the configured benchmark Python for the environment.

```bash
PY="repo/.venv/bin/python"
```

## Rebuild Prepared Inputs

```bash
python3 repo/scripts/prepare_modern_ids_preserved_ratio_train500_test500_benchmark.py
python3 repo/scripts/prepare_additional_modern_ids_preserved_ratio_train500_test500_benchmark.py
```

## Modern7 Smoke

Run one low-cost dataset first:

```bash
"$PY" repo/scripts/run_baseline_method_tranche.py \
  --method no_resampling \
  --run-id benchmark_modern7_smoke_reference_20260511_01 \
  --benchmark-definition "$MODERN7_DEF" \
  --datasets hikari_probing_vs_benign \
  --skip-complete-stages \
  --allow-existing-run-id
```

```bash
"$PY" repo/scripts/run_dctabgan_experiment_cycle.py \
  --run-id benchmark_modern7_smoke_dct_20260511_01 \
  --benchmark-definition "$MODERN7_DEF" \
  --datasets hikari_probing_vs_benign \
  --skip-checks \
  --num-epochs 1 \
  --generation-max-iterations 20 \
  --utility-seeds 42 \
  --extra-models qda \
  --skip-complete-stages \
  --allow-existing-run-id
```

If that passes, run the same smoke over all modern7 datasets by removing `--datasets hikari_probing_vs_benign`.

## Modern7 Full Method Tranches

```bash
for METHOD in no_resampling smote ctgan copulagan tvae random_over_sampler random_under_sampler borderline_smote smoteenn class_weighted; do
  "$PY" repo/scripts/run_baseline_method_tranche.py \
    --method "$METHOD" \
    --run-id benchmark_singlelabel30_train500_test500_full_20260511_01 \
    --benchmark-definition "$MODERN7_DEF" \
    --skip-complete-stages \
    --allow-existing-run-id
done
```

## Modern7 DCT Checkpoint Source And Replay

```bash
"$PY" repo/scripts/run_dctabgan_experiment_cycle.py \
  --run-id benchmark_singlelabel30_dct_mult1_ckpts_20260511_01 \
  --benchmark-definition "$MODERN7_DEF" \
  --synthetic-sample-multiplier 1.0 \
  --save-checkpoints-every 3 \
  --skip-complete-stages \
  --allow-existing-run-id
```

```bash
"$PY" repo/scripts/run_dctabgan_experiment_cycle.py \
  --run-id benchmark_singlelabel30_dct_mult1_ckpt0009_20260511_01 \
  --benchmark-definition "$MODERN7_DEF" \
  --synthetic-sample-multiplier 1.0 \
  --checkpoint-source-run-id benchmark_singlelabel30_dct_mult1_ckpts_20260511_01 \
  --checkpoint-epoch 9 \
  --skip-complete-stages \
  --allow-existing-run-id
```

## Fair Utility Treatment Sensitivity Path

This section produces the older 11-method `faircw` output. Keep it for continuity and sensitivity analysis only.

```bash
"$PY" repo/scripts/run_fair_utility_treatment_tranche.py \
  --benchmark-definition "$MODERN7_DEF" \
  --source-reference-run-id benchmark_singlelabel30_train500_test500_full_20260511_01 \
  --source-dct-run-id benchmark_singlelabel30_dct_mult1_ckpt0009_20260511_01 \
  --target-reference-run-id benchmark_singlelabel30_faircw_reference_20260511_01 \
  --target-dct-run-id benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01 \
  --skip-complete-stages \
  --allow-existing-run-id
```

## Sensitivity 30D Artifact Requirement

The ledger/dashboard builders accept one reference run ID and one DCT run ID for the whole benchmark definition. Before building the sensitivity-only 11-method faircw outputs, all 30 datasets must have artifacts under:

- `benchmark_singlelabel30_faircw_reference_20260511_01`
- `benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01`

If the retained 23D artifacts are reused rather than rerun, materialize or symlink the retained 23D benchmark and utility roots into those 30D run IDs before rebuilding the sensitivity outputs.

## Sensitivity 30D Metrics, Rankings, And Statistical Tests

```bash
PYTHONPATH=repo:repo/scripts "$PY" repo/scripts/build_benchmark_full_metric_ledger.py \
  --benchmark-definition "$FAIRCW30D_SENSITIVITY_DEF" \
  --reference-run-id benchmark_singlelabel30_faircw_reference_20260511_01 \
  --dct-run-id benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01 \
  --ledger-path research/docs/benchmark_runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01/BENCHMARK_FULL_METRIC_LEDGER.md \
  --tables-dir research/outputs/benchmark_tables/runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01 \
  --benchmark-label "30D preserved-ratio fair utility treatment sensitivity benchmark"
```

```bash
PYTHONPATH=repo:repo/scripts "$PY" repo/scripts/build_tuning_dataset_dashboards.py \
  --benchmark-definition "$FAIRCW30D_SENSITIVITY_DEF" \
  --reference-run-id benchmark_singlelabel30_faircw_reference_20260511_01 \
  --dct-run-id benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01 \
  --role-label "Sensitivity 30D faircw benchmark" \
  --dashboards-dir research/docs/dashboards/runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01 \
  --summary-path research/docs/dashboards/runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01/tuning_summary.html \
  --index-path research/docs/dashboards/runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01/tuning_index.html \
  --final-summary-path research/docs/dashboards/runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01/final_summary.html \
  --iteration-dashboard-path research/docs/dashboards/runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01/iteration_metrics_dashboard.html
```

The 11-method faircw ledger emits both dataset-level confirmatory statistics and learner-block sensitivity statistics, but this path is not the corrected primary 20-condition result.

## Completed Primary 20-Condition Outputs

The completed corrected definition is:

- `research/docs/dctabgan_iteration_map/planning_docs/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_NODOS_30D_BENCHMARK_DEFINITION_2026-05-11.json`

It maps each of the 20 conditions to four completed primary run groups:

- `standard_reference`: `benchmark_singlelabel30_nodos_20method_reference_20260511_01`
- `standard_dct`: `benchmark_singlelabel30_nodos_20method_dct_ckpt0009_20260511_01`
- `cw_reference`: `benchmark_singlelabel30_nodos_20method_cw_reference_20260511_01`
- `cw_dct`: `benchmark_singlelabel30_nodos_20method_cw_dct_ckpt0009_20260511_01`

Final primary no-DoS artifacts:

- Ledger: `research/docs/benchmark_runs/benchmark_singlelabel30_nodos_20method_cw_dct_ckpt0009_20260511_01/BENCHMARK_FULL_METRIC_LEDGER.md`
- Tables: `research/outputs/benchmark_tables/runs/benchmark_singlelabel30_nodos_20method_cw_dct_ckpt0009_20260511_01/`
- Dashboards: `research/docs/dashboards/runs/benchmark_singlelabel30_nodos_20method_cw_dct_ckpt0009_20260511_01/`
- Run-scoped analysis: `research/outputs/benchmark_tables/runs/benchmark_singlelabel30_nodos_20method_cw_dct_ckpt0009_20260511_01/current_dct_paper_analysis.json`

Primary outputs cover `30` datasets, `6` learners, `20` treatment conditions, and `180` matched dataset x learner blocks. Validation artifacts include `paper_ids_dataset_statistical_validation.csv` and `paper_ids_statistical_validation.csv` in the primary tables directory. Dataset-level statistics over `30` datasets are primary; learner-block statistics remain sensitivity-only. The old retained `23D` and old `30D` `faircw` outputs remain historical/sensitivity-only and must not be promoted over these no-DoS outputs.

Primary ranking highlights:

- Paper composite, rank-based over AP/PR-AUC, Recall, MCC, and Balanced Accuracy: SMOTE rank `1`, score `9.1778`; RandomOverSampler rank `2`, score `9.1896`; SMOTEENN rank `3`, score `9.4111`; DCTABGAN + CW rank `5`, score `10.0111`; DCTABGAN rank `9`, score `10.3500`.
- IDS operational: RandomUnderSampler + CW rank `1`, score `8.9417`; SMOTEENN rank `2`, score `8.9583`; SMOTE + CW rank `3`, score `9.0139`; DCTABGAN + CW rank `13`, score `10.7806`; DCTABGAN rank `20`, score `13.2389`.
- Headline MCC, mean raw MCC: DCTABGAN rank `1`, mean `0.839200`; No treatment rank `2`, mean `0.836143`; CTGAN rank `3`, mean `0.824774`; DCTABGAN + CW rank `10`, mean `0.807903`.
