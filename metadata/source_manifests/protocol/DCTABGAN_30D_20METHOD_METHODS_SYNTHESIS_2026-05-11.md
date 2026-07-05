# DCTABGAN 30D 20-Method Methods Synthesis

Date: 2026-05-11

## Purpose

This document defines the corrected primary no-DoS 30D paper-facing methodology for the preserved-ratio IDS benchmark. It supersedes the earlier 30D interpretation that treated the completed `faircw` 11-method output as the primary final surface. The corrected primary no-DoS outputs are now complete and validated.

The corrected primary surface is a 20-condition treatment-method benchmark on a no-DoS/no-DDoS/no-flood dataset surface. The frozen retained 23D surface and completed 11-method `faircw` 30D artifact remain useful only as historical/sensitivity references.

## Corrected Scientific Estimand

The primary estimand is the downstream IDS classification utility of imbalance-treatment conditions on preserved-ratio binary attack-vs-benign tasks.

The estimand is not a pure synthetic-generator leaderboard. It compares the utility consequences of no treatment, classifier-side class weighting, data-level resampling, generative augmentation, hybrid cleaning/resampling, and each data-level treatment combined with classifier-side class weighting.

The key correction is that class weighting is a treatment factor, not a universal fairness wrapper applied to every condition before ranking. The primary analysis must therefore separate treatment-only effects from treatment-plus-class-weighting effects.

Paper-facing wording should distinguish these claims:

- `DCTABGAN` treatment-only estimates the utility of DCTABGAN augmentation without downstream class weighting.
- `DCTABGAN + CW` estimates the combined pipeline effect of DCTABGAN augmentation plus downstream class-weighted fitting.
- A `DCTABGAN + CW` result is a pipeline-treatment claim, not a generator-only claim.

## Primary 20 Treatment Conditions

The corrected condition set contains 20 treatment conditions:

| Group | Condition |
|---|---|
| Control | No treatment |
| Classifier-side only | Class-weighted only |
| Treatment-only | SMOTE |
| Treatment-only | CTGAN |
| Treatment-only | CopulaGAN |
| Treatment-only | TVAE |
| Treatment-only | DCTABGAN |
| Treatment-only | RandomOverSampler |
| Treatment-only | RandomUnderSampler |
| Treatment-only | BorderlineSMOTE |
| Treatment-only | SMOTEENN |
| Treatment + CW | SMOTE + class-weighted fitting |
| Treatment + CW | CTGAN + class-weighted fitting |
| Treatment + CW | CopulaGAN + class-weighted fitting |
| Treatment + CW | TVAE + class-weighted fitting |
| Treatment + CW | DCTABGAN + class-weighted fitting |
| Treatment + CW | RandomOverSampler + class-weighted fitting |
| Treatment + CW | RandomUnderSampler + class-weighted fitting |
| Treatment + CW | BorderlineSMOTE + class-weighted fitting |
| Treatment + CW | SMOTEENN + class-weighted fitting |

The 9 treatment families are `SMOTE`, `CTGAN`, `CopulaGAN`, `TVAE`, `DCTABGAN`, `RandomOverSampler`, `RandomUnderSampler`, `BorderlineSMOTE`, and `SMOTEENN`.

`No treatment` and `Class-weighted only` are single controls, not members of the 9 treatment-family cross. This avoids duplicating the no-treatment control under a second name.

## Primary No-DoS Dataset Surface

The primary study surface is the new no-DoS 30D definition:

- `research/docs/dctabgan_iteration_map/planning_docs/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_NODOS_30D_BENCHMARK_DEFINITION_2026-05-11.json`

It contains `30` datasets: `13` retained non-DoS tasks kept from the frozen retained 23D definition, the `7` prepared modern7 tasks, and the `10` replacement additional10 tasks.

Primary surface composition summary:

| Source slice | Dataset count |
|---|---:|
| Retained non-DoS | 13 |
| Modern7 | 7 |
| Additional10 | 10 |

Primary surface composition by dataset:

| Source slice | Dataset key | Family label |
|---|---|---|
| Retained non-DoS | `friday_bot` | CIC-IDS-2017 botnet |
| Retained non-DoS | `thursday_web_attack_bruteforce` | CIC-IDS-2017 web brute force |
| Retained non-DoS | `tuesday_ftp_patator` | CIC-IDS-2017 FTP brute force |
| Retained non-DoS | `tuesday_ssh_patator` | CIC-IDS-2017 SSH brute force |
| Retained non-DoS | `cse_cic_ids2018_bot` | CSE-CIC-IDS2018 botnet |
| Retained non-DoS | `cse_cic_ids2018_ftp_bruteforce` | CSE-CIC-IDS2018 FTP brute force |
| Retained non-DoS | `cse_cic_ids2018_infilteration` | CSE-CIC-IDS2018 infiltration |
| Retained non-DoS | `cse_cic_ids2018_ssh_bruteforce` | CSE-CIC-IDS2018 SSH brute force |
| Retained non-DoS | `cic_unsw_nb15_exploits` | CIC-UNSW-NB15 exploits |
| Retained non-DoS | `cic_unsw_nb15_fuzzers` | CIC-UNSW-NB15 fuzzing |
| Retained non-DoS | `cic_unsw_nb15_generic` | CIC-UNSW-NB15 generic |
| Retained non-DoS | `cic_unsw_nb15_reconnaissance` | CIC-UNSW-NB15 reconnaissance |
| Retained non-DoS | `cic_unsw_nb15_shellcode` | CIC-UNSW-NB15 shellcode |
| Modern7 | `hikari_bruteforce_vs_benign` | HIKARI-2021 brute force |
| Modern7 | `hikari_probing_vs_benign` | HIKARI-2021 probing |
| Modern7 | `ciciomt2024_arp_spoofing_vs_benign` | CICIoMT2024 ARP spoofing |
| Modern7 | `ciciomt2024_mqtt_malformed_data_vs_benign` | CICIoMT2024 MQTT malformed data |
| Modern7 | `edge_iiotset_sql_injection_vs_normal` | Edge-IIoTset SQL injection |
| Modern7 | `edge_iiotset_password_vs_normal` | Edge-IIoTset password attack |
| Modern7 | `edge_iiotset_uploading_vs_normal` | Edge-IIoTset uploading |
| Additional10 | `5g_nidd_tcp_connect_scan_vs_benign` | 5G-NIDD TCP connect scan |
| Additional10 | `5g_nidd_syn_scan_vs_benign` | 5G-NIDD SYN scan |
| Additional10 | `5g_nidd_udp_scan_vs_benign` | 5G-NIDD UDP scan |
| Additional10 | `edge_iiotset_vulnerability_scanner_vs_normal` | Edge-IIoTset vulnerability scanner |
| Additional10 | `edge_iiotset_backdoor_vs_normal` | Edge-IIoTset backdoor |
| Additional10 | `edge_iiotset_port_scanning_vs_normal` | Edge-IIoTset port scanning |
| Additional10 | `rt_iot2022_nmap_udp_scan_vs_benign` | RT-IoT2022 NMAP UDP scan |
| Additional10 | `rt_iot2022_nmap_xmas_tree_scan_vs_benign` | RT-IoT2022 NMAP Xmas scan |
| Additional10 | `rt_iot2022_nmap_os_detection_vs_benign` | RT-IoT2022 NMAP OS detection |
| Additional10 | `rt_iot2022_nmap_tcp_scan_vs_benign` | RT-IoT2022 NMAP TCP scan |

This study intentionally excludes DoS, DDoS, and flood-like detection tasks. These cases are often identifiable through simple traffic-volume, rate, or protocol heuristics without requiring machine learning, and including them would risk distorting the primary study toward high-signal, operationally obvious scenarios. The scope therefore focuses on harder benchmark settings where model behavior, synthetic-data fidelity, and downstream utility are more meaningfully evaluated.

- The no-DoS/no-DDoS/no-flood rule applies to the whole primary surface.
- This is a scope-control decision, not a claim that DoS/DDoS attacks are unimportant.

## Learner Panel

The corrected primary learner panel remains a six-classifier panel, but `LinearSVM` replaces `kNN`:

| Slot | Learner | Family rationale |
|---|---|---|
| 1 | LightGBM | Boosted-tree tabular learner; strong nonlinear mixed-feature baseline. |
| 2 | LogisticRegression | Linear probabilistic baseline aligned with multinomial/logistic regression use in IDS generator papers. |
| 3 | QDA | Generative quadratic discriminant baseline; useful family diversity with a class-prior caveat for CW. |
| 4 | RandomForest | Bagged-tree ensemble aligned with repeated RF use in CTAB-GAN and CTAB-GAN+ IDS validation. |
| 5 | LinearSVM | Large-margin linear classifier aligned with CTAB-GAN and CTAB-GAN+ learner panels. |
| 6 | DeepMLP | Neural downstream classifier family aligned with MLP use in CTGAN, CTAB-GAN, CTAB-GAN+, and related IDS utility panels. |

## Literature-Review Grounding

The local literature-review brief `research/docs/briefs/GAN_Imbalanced_Data_Utility_Learner_Dataset_Survey_2026-04-08.md` identifies conventional tabular classifiers as the dominant downstream utility evaluators in IDS-oriented GAN/TVAE papers.

The strongest directly reusable learner-panel evidence comes from CTAB-GAN and CTAB-GAN+, which evaluate IDS utility with Decision Tree, Linear SVM, Random Forest, Multinomial Logistic Regression, and MLP on `Intrusion`.

The same brief notes that CTGAN's original IDS evidence uses Decision Tree and MLP, Bourou et al. use Decision Tree, AdaBoost, Logistic Regression, and MLP on `NSL-KDD`, and Ammara et al. emphasize TSTR/TRTR utility reporting on `CIC-IDS2017` without a clearly recoverable fixed learner panel.

The corrected six-learner panel is therefore literature-grounded by family coverage rather than by exact one-to-one duplication:

- Tree ensembles are represented by `RandomForest` and `LightGBM`.
- Linear models are represented by `LogisticRegression` and `LinearSVM`.
- Neural utility evaluation is represented by `DeepMLP`.
- A generative discriminant family is retained through `QDA` for diversity, with the caveat below.

## LinearSVM Replaces kNN

`LinearSVM` replaces `kNN` in the primary corrected 30D learner panel.

The reason is methodological, not performance tuning. `LinearSVM` is repeatedly present in the CTAB-GAN and CTAB-GAN+ IDS validation panels, while `kNN` is not a recurring primary learner in the local IDS GAN/TVAE survey. The corrected paper-facing panel should therefore privilege the more literature-grounded classifier family.

`kNN` remains useful as a support-placement diagnostic learner because it is sensitive to local neighborhood geometry. However, that makes it better suited to exploratory or sensitivity analysis than to the primary corrected +CW panel.

## QDA Balanced-Prior Caveat

QDA does not provide the same class-weighting semantics as learners with direct `class_weight` or equivalent sample-weight support. For the corrected +CW panel, QDA must be documented as a balanced-prior or prior-adjusted analogue rather than as a strict implementation of the same class-weight mechanism used by the other classifiers.

Paper-facing tables and methods text should mark QDA + CW with this caveat. QDA results can remain in the primary family-diverse panel, but claims about the class-weighted factor should not overstate QDA as identical to direct class-weighted fitting.

## kNN Status

`kNN` is not used in the primary corrected +CW learner panel.

If `kNN` is retained in any output, it should be labeled sensitivity-only. It should not be mixed into the primary 20-condition corrected leaderboard because the corrected learner panel is `LightGBM`, `LogisticRegression`, `QDA`, `RandomForest`, `LinearSVM`, and `DeepMLP`.

## Historical/Sensitivity Output Status

The frozen retained 23D definition is historical/sensitivity-only under the no-DoS methodology. It remains unchanged for provenance and prior-result continuity, but it is not the primary study surface.

The old completed 30D `faircw` output is historical/sensitivity-only under this corrected protocol.

Existing completed run IDs:

- Reference methods: `benchmark_singlelabel30_faircw_reference_20260511_01`
- DCTABGAN: `benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01`

Existing completed artifacts:

- Ledger: `research/docs/benchmark_runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01/BENCHMARK_FULL_METRIC_LEDGER.md`
- Tables: `research/outputs/benchmark_tables/runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01/`
- Dashboards: `research/docs/dashboards/runs/benchmark_singlelabel30_faircw_dct_ckpt0009_20260511_01/`

Why sensitivity-only:

- It evaluates 11 nominal methods, not the corrected 20 treatment conditions.
- It applies the downstream class-weighted utility treatment broadly instead of treating class weighting as an explicit condition factor.
- It uses the older six-learner panel containing `kNN`, not the corrected primary panel containing `LinearSVM`.
- It can answer the conditional question: what happens when the previous 11-method surface is evaluated under the shared fair class-weighted utility treatment?
- It cannot serve as the primary paper-facing estimate for the corrected 20-condition estimand.

## Statistical Interpretation

Primary confirmatory statistics must use datasets as the paired inference unit.

For the 30D surface, the primary statistic should first average matched learner-block scores within each dataset for each treatment condition, then run the omnibus and paired post-hoc tests over the 30 dataset-level units.

Learner-block inference over `30 datasets x 6 learners = 180` blocks is sensitivity-only because learners share the same dataset splits and are correlated repeated measures, not independent datasets.

Recommended reporting:

- Primary: dataset-level omnibus test and DCTABGAN-relevant paired tests over 30 datasets.
- Sensitivity: learner-block Friedman/Wilcoxon/Nemenyi over 180 dataset x learner blocks.
- Descriptive: paper composite leaderboard, headline mean raw MCC leaderboard, operational guardrails, and learner/dataset blocker diagnostics.
- Caveat: any `faircw` 11-method tables should be labeled sensitivity-only beside the corrected 20-condition primary tables.

## Artifact And Run-ID Status

The corrected primary no-DoS 30D 20-condition surface is complete and validated.

Primary execution definition:

- `research/docs/dctabgan_iteration_map/planning_docs/PRESERVED_RATIO_TRAIN500_TEST500_SINGLE_LABEL_NODOS_30D_BENCHMARK_DEFINITION_2026-05-11.json`

Completed primary run IDs:

- Primary source/control and treatment-only reference run: `benchmark_singlelabel30_nodos_20method_reference_20260511_01`
- Primary DCT checkpoint replay run: `benchmark_singlelabel30_nodos_20method_dct_ckpt0009_20260511_01`
- Primary treatment + CW reference run: `benchmark_singlelabel30_nodos_20method_cw_reference_20260511_01`
- Primary treatment + CW DCT run: `benchmark_singlelabel30_nodos_20method_cw_dct_ckpt0009_20260511_01`

Final primary no-DoS artifacts:

- Ledger: `research/docs/benchmark_runs/benchmark_singlelabel30_nodos_20method_cw_dct_ckpt0009_20260511_01/BENCHMARK_FULL_METRIC_LEDGER.md`
- Tables: `research/outputs/benchmark_tables/runs/benchmark_singlelabel30_nodos_20method_cw_dct_ckpt0009_20260511_01/`
- Dashboards: `research/docs/dashboards/runs/benchmark_singlelabel30_nodos_20method_cw_dct_ckpt0009_20260511_01/`
- Publication/statistical dashboard: `research/docs/dashboards/runs/benchmark_singlelabel30_nodos_20method_cw_dct_ckpt0009_20260511_01/statistical_metrics_dashboard.html`
- Publication/statistical dashboard (scaled): `research/docs/dashboards/runs/benchmark_singlelabel30_nodos_20method_cw_dct_ckpt0009_20260511_01/statistical_metrics_dashboard_scaled.html`
- Publication/statistical assets: `research/docs/dashboards/runs/benchmark_singlelabel30_nodos_20method_cw_dct_ckpt0009_20260511_01/statistical_metrics_assets/`
- Publication/statistical assets (scaled): `research/docs/dashboards/runs/benchmark_singlelabel30_nodos_20method_cw_dct_ckpt0009_20260511_01/statistical_metrics_assets_scaled/`
- Run-scoped analysis: `research/outputs/benchmark_tables/runs/benchmark_singlelabel30_nodos_20method_cw_dct_ckpt0009_20260511_01/current_dct_paper_analysis.json`

The run-scoped analysis records all four primary source run groups, `30` datasets, `20` conditions, and dataset-level statistics over `30` paired dataset units. Validation artifacts include `paper_ids_dataset_statistical_validation.csv` and `paper_ids_statistical_validation.csv` in the primary tables directory. The frozen retained `23D` surface and old completed `30D` `faircw` surface remain historical/sensitivity-only.

Reporting convention: the paper composite remains rank-based over AP/PR-AUC, Recall, MCC, and Balanced Accuracy; the headline MCC leaderboard is sorted by mean raw MCC, not by the legacy MCC-only rank-score aggregate.

## Primary Ranking Highlights

- Paper composite, rank-based over AP/PR-AUC, Recall, MCC, and Balanced Accuracy: SMOTE rank `1`, score `9.1778`; RandomOverSampler rank `2`, score `9.1896`; SMOTEENN rank `3`, score `9.4111`; DCTABGAN + CW rank `5`, score `10.0111`; DCTABGAN rank `9`, score `10.3500`.
- IDS operational: RandomUnderSampler + CW rank `1`, score `8.9417`; SMOTEENN rank `2`, score `8.9583`; SMOTE + CW rank `3`, score `9.0139`; DCTABGAN + CW rank `13`, score `10.7806`; DCTABGAN rank `20`, score `13.2389`.
- Headline MCC, mean raw MCC: DCTABGAN rank `1`, mean `0.839200`; No treatment rank `2`, mean `0.836143`; CTGAN rank `3`, mean `0.824774`; DCTABGAN + CW rank `10`, mean `0.807903`.
