# Source License And Redistribution Assessment

This note summarizes what was verifiable from the documented source routes for the eight corpora represented in the full 30-task benchmark. It is not legal advice.

The current public repository directly redistributes only the 17 CSV tasks from CIC-IDS-2017, CSE-CIC-IDS2018, HIKARI-2021, 5G-NIDD, and RT-IoT2022. The 13 tasks from Edge-IIoTset, CIC-UNSW-NB15, and the CICIoMT2024Small mirror are omitted from the downloadable CSV bundle and retained only as metadata/reproduction instructions.

## Corpus Summary

| Corpus | Verified source route | Explicit license / permission found | Redistribution of source data | Derivative / adapted redistribution | Practical release reading |
|---|---|---|---|---|---|
| CIC-IDS-2017 | UNB/CIC dataset page | No standard license named; CIC FAQ says CIC datasets may be redistributed, republished, and mirrored with citation | Yes, based on CIC FAQ | Not explicitly stated | Likely acceptable with strong citation and provenance retention, but derivative rights are not spelled out in standard-license form |
| CSE-CIC-IDS2018 | UNB/CIC dataset page and AWS registry | No standard license named; UNB page says dataset may be redistributed, republished, and mirrored in any form with citation | Yes | Broadly implied by “in any form,” but not expressed as a standard derivative-data license | Likely acceptable with citation and provenance retention |
| CIC-UNSW-NB15 | UNSW project page | Free use for academic research; citation required; commercial use requires author agreement | Not explicitly granted | Not explicitly granted | Omitted from public CSV bundle; metadata retained for local reproduction |
| HIKARI-2021 | Zenodo | CC BY 4.0 | Yes | Yes | Strong documented basis for redistribution with attribution |
| CICIoMT2024Small mirror | Official UNB/CIC page for full dataset plus public Hugging Face mirror for the “Small” artifact | No official “Small” release license found; CIC FAQ supports redistribution for CIC datasets; mirror metadata did not expose a license | Full CIC family likely redistributable via CIC policy; mirror-specific status unclear | Not explicitly stated for the mirror-derived “Small” artifact | Omitted from public CSV bundle; metadata retained for local reproduction |
| Edge-IIoTset | IEEE DataPort page and public Kaggle mirror | Kaggle mirror reports CC BY-NC-SA 4.0; IEEE page emphasizes academic use | Yes for noncommercial redistribution under the mirror license | Yes for noncommercial derivatives under share-alike terms | Omitted from public CSV bundle to avoid overclaiming rights for a general public release |
| 5G-NIDD | IEEE DataPort page plus open Fairdata route | Fairdata metadata states CC BY 4.0 | Yes | Yes | Strong documented basis for redistribution with attribution |
| RT-IoT2022 | UCI Machine Learning Repository | CC BY 4.0 | Yes | Yes | Strong documented basis for redistribution with attribution |

## Mirror Caveat

The fact that a dataset is publicly mirrored does not by itself prove that every downstream redistribution is authorized. A public mirror is strongest when it also exposes an explicit license or when the upstream dataset family separately grants redistribution rights.

In this benchmark, that distinction matters most for:

- `CICIoMT2024Small mirror`, where the release used a public mirror of a smaller artifact rather than an official open release.
- `Edge-IIoTset`, where the mirror is public and licensed for noncommercial reuse, but the official route is gated.
- `5G-NIDD`, where the open Fairdata route is the strongest licensing basis, not the gated IEEE route.

## Current Release Posture

The current public-positioning is:

- preserve all upstream citations and provenance notes;
- avoid relicensing the bundled datasets under a more permissive project-wide license;
- state clearly that upstream terms still govern each corpus;
- directly redistribute only the 17 lower-risk CSVs selected for the public-safe subset;
- omit `Edge-IIoTset`, `CIC-UNSW-NB15`, and `CICIoMT2024Small mirror` CSVs from the public bundle;
- keep omitted tasks documented in machine-readable metadata with exact local reproduction paths.
