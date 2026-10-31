# What can be checked from this repository

## Recomputed from files in this repository

- **Published-study audit.** `code/published_study_agreement.py` recomputes Cohen's κ (with 95% CIs from 5000 bootstrap resamples of studies, seed 20261030) and the prevalence of each consensus rating (Wilson 95% CIs) from the two extractions and the consensus ratings in `data/published_studies/`. `tests/test_published_study_agreement.py` checks that a rerun reproduces the archived tables.
- **Public near-duplicate result.** `data/public/distance_histograms.json` holds the counts at each hash distance computed from the Endoscapes2023 test keyframes, without frame names, pair indices or video identifiers. The test suite checks that 382 of 1623 consecutive pairs fall below the 0·1th percentile of 20 000 random pairs from different operations. Recomputing the distances themselves needs local images (`code/endoscapes_near_duplicates.py`). The histogram conversion preserves the complete distance distributions, including the percentile and plotted bins.
- **Figures.** `code/figures/make_figures.py` redraws every figure. The image panels need `ENDOSCAPES_ROOT` (the public dataset) and `CLINICAL_FRAME` (a clinical frame stem; not distributed); without them those panels are left blank.

## Transcribed from the study record

`data/frozen_results.json` (case 1 and the case 2 manifest) and `data/case2/case2_results.json` (case 2 reconstruction) are transcribed from the project records. They are not recalculated here, because the clinical images, videos and model weights cannot be shared. `code/clip_classifier_checks.py` and `code/detector_transfer_checks.py` are the checks to run on those records where access is approved.

## Analytic references

The provenance table gives an arithmetic reference. If a required field is retained in a fraction `r` of records, the single-field reference is `r`. Checking both members of a duplicate pair requires two retained hashes, so the pair reference is `r²`. These values concern available provenance, not changes in model accuracy. The controlled-corruption and threshold tables list test settings and theoretical outcomes, not measured detection rates.
