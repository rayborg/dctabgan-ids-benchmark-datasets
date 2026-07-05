# Access Status: ciciomt2024_arp_spoofing_vs_benign

Status: `materialized_from_public_huggingface_mirror`

Raw class-separated flow CSVs were found in the public Hugging Face mirror `somnath0100/CICIoMT2024Small` and staged under `data/staging/modern_ids_audit/CICIoMT2024/data`. The official UNB/CIC endpoint remains registration-gated for unauthenticated access.

## Downloaded Raw Inputs

- `data/staging/modern_ids_audit/CICIoMT2024/data/Benign_train.pcap_Flow.csv`: 35810 rows, 23215387 bytes.
- `data/staging/modern_ids_audit/CICIoMT2024/data/ARP_Spoofing_train.pcap_Flow.csv`: 1387 rows, 849503 bytes.

## Materialized Split

- Ratio floor: `25` for `Benign`:`ARP Spoofing`.
- Train total: `13000`, with `12500` Benign and `500` ARP Spoofing.
- Test total: `13000`, with `12500` Benign and `500` ARP Spoofing.
- Train/test overlap by `source_row_index`: `0`.

## Notes

- Raw `Label` values in these class-separated files are `NeedManualLabel`; labels were assigned from filenames.
- Mirror counts are sufficient for this candidate but do not match prior full-dataset public counts.
