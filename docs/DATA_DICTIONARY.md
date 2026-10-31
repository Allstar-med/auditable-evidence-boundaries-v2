# Data dictionary
- sample_id: identifier for one sample
- clinical_unit_id: patient, procedure, or video used to separate splits
- sha256: SHA-256 hash of the source file
- split: train, validation, val, or test
- label_*: labels for the planned endpoints
- source_position: timestamp or frame number
- source_prefix: source folder or group label; not treated as a patient ID
- audit_version: version of the checker or study method
- manifest_checksum: hash of the manifest used for an audit
- cross_split_hash_groups: hashes found in more than one split

## Published-study audit (`data/published_studies/`)
- study_id: S01–S19, in the order of the review's extraction table (see `sample.csv`)
- D1–D8: rating of each check; m met, p partly met, n not met, r not reported, a not assessable, x not applicable
- D*_quote: verbatim quotation (at most 40 words) and its location supporting the rating
- claim_verbatim, behaviour, unit, setting, contrast: the primary external claim and its four elements
- supportable_claim: the strongest claim the report's evidence supports
- claim_supported: yes if the supportable claim equals the stated claim
- agreement.csv: raw agreement, κ with 95% CI, and κ for met versus any other rating, per check
- prevalence.csv: count, percentage and Wilson 95% CI of each consensus rating, per check

## Public near-duplicate analysis (`data/public/`)
- distance_histograms.json: `hash_bits` is 256; `adjacent_counts[d]` is the number of consecutive-keyframe pairs at distance d; `cross_counts[d]` is the number of random cross-operation pairs at distance d (20 000 pairs, seed 1). Each count vector has 257 entries, for distances 0 through 256. Original pair order and frame/video identifiers are not retained.
- The local image-analysis script additionally writes endoscapes_files.csv, endoscapes_adjacent.csv and cross.npy. These local outputs are not included in the public archive.
