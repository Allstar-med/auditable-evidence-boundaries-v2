# Auditable evidence boundaries in surgical model validation

Code, protocol and reference data for the reconstruction of two clinical pipelines and an evidence
audit of published external validations (version 2.0).

This is the separate [version 2 repository](https://github.com/Allstar-med/auditable-evidence-boundaries-v2).

The study defines eight claim-indexed evidence checks (D1–D8). It applies them to two clinical development
pipelines and to all 19 studies classified as external validations in a systematic review of surgical
scene understanding. It also measures near-duplicate keyframes in a public benchmark.

## What is recomputed and what is transcribed

| Result | Status | Location |
|---|---|---|
| Case 1 split counts and accuracies | Transcribed from project records; the original analysis files were not available | `data/frozen_results.json` |
| Case 2 reconstruction and archive audit | Transcribed from the reconstruction records | `data/case2/case2_results.json` |
| Ratings of the 19 published studies, agreement and prevalence | Recomputed by `code/published_study_agreement.py` from the ratings in `data/published_studies/` | `data/published_studies/` |
| Endoscapes near-duplicate summary | Recomputed from the included distance histograms; deriving the distances from images requires local Endoscapes data | `data/public/distance_histograms.json` |
| Figures | Recomputed by `code/figures/make_figures.py` | — |

Clinical images, videos, patient identifiers and model weights are not distributed. Endoscapes images are
available from the dataset's own repository under its CC BY-NC-SA 4.0 licence, and are not copied here.
The public archive also omits the Endoscapes per-frame file list and pair-to-frame linkage. It retains
only counts at each hash distance, sufficient to reproduce the distribution plot and threshold result.

## Contents

- **`code/validation_integrity_auditor.py`**: checks clinical-unit overlap, exact (SHA-256) duplicates across splits and endpoint support for a split manifest.
- **`code/public_duplicate_audit.py`**: audits a public dataset for exact and near-duplicate images across its official splits.
- **`code/endoscapes_near_duplicates.py`**: computes 256-bit difference-hash distances between consecutive Endoscapes test keyframes and between random pairs from different operations.
- **`code/distance_summary.py`**: converts locally computed distances into public histograms without frame or video identifiers.
- **`code/detector_transfer_checks.py`**: runs the case 2 detector checks, comprising:
  - per-class AP50 on the training, validation and test splits, with training AP50 as a positive control;
  - checks of box-convention errors;
  - output rates per site;
  - recall on annotated external polygons;
  - overlays of references and predictions.
- **`code/clip_classifier_checks.py`**: computes accuracy and balanced accuracy with patient-clustered bootstrap intervals, per-class recall and per-patient accuracy.
- **`code/published_study_agreement.py`**: computes Cohen's κ (bootstrap 95% CI) between the two extractions and the prevalence of each consensus rating (Wilson 95% CI).
- **`code/run_provenance_stress.py`**: computes the analytic reference for the loss of auditability when provenance fields are missing.
- **`code/figures/`**: the figures of the manuscript.
- **`data/published_studies/`**:
  - the protocol and the decision log;
  - the study list;
  - the two independent extractions, each with its verbatim quotations and their locations;
  - the consensus ratings;
  - the agreement and prevalence tables.
- **`tests/`**: unit tests.

## Reproduce

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v

# agreement and prevalence of the published-study ratings
python code/published_study_agreement.py data/published_studies/extraction_1.csv \
    data/published_studies/extraction_2.csv data/published_studies/consensus.csv results/

# Endoscapes near-duplicate analysis (needs the public Endoscapes2023 test images)
python code/endoscapes_near_duplicates.py /path/to/endoscapes/test results/

# figures from the included tables and histograms; unavailable image panels show notices
python code/figures/make_figures.py figures/

# optional image panels, with locally available source data
ENDOSCAPES_ROOT=/path/to/endoscapes CLINICAL_FRAME=/path/to/frame_stem python code/figures/make_figures.py figures/
```

On Windows, use Python's UTF-8 mode (`python -X utf8 ...`). The environment-variable assignment on the
last line uses Bash syntax; in PowerShell, set `$env:ENDOSCAPES_ROOT` and `$env:CLINICAL_FRAME` first.
The clinical checks require local predictions, references and images; the transcribed clinical
performance values cannot be independently reproduced from this public archive alone.

The published-study protocol records assisted extraction and subsequent author verification. These
statements are part of the supplied study record; the software tests check calculations and table
consistency, not the accuracy of quotations against all source articles.

## Licence

Code: MIT. Data tables: CC BY 4.0.
