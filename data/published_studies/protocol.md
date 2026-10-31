# Applying the claim-indexed evidence checks to published external validations of surgical AI: protocol

Version 1.0, fixed on 30 October 2026, before any published study was rated. Changes after this date will be listed at the end with their reasons.

## Objective

To estimate, for published external validations of surgical scene-understanding models, how often each of the eight claim-indexed evidence checks (D1–D8) can be confirmed from the published report and its supplements, and how reliably two independent raters apply the checks.

## Sample

**Eligibility.** All studies classified as external validation ("external retrospective: validation using data from other centres or data sources") in the systematic review by Carstens et al. (npj Digit Med 2026; 9: 59), identified from its supplementary extraction tables. The review reports 19 such studies.

The sample is fixed by an independent, published classification rather than by us. This avoids selection by the authors.

**Exclusions.** A study is excluded only if its full text cannot be obtained. Exclusions are reported with their reason.

## Unit of analysis

The unit is the primary external validation claim of each study. This is the claim stated in the abstract or conclusion that the model performs at another centre or on another data source. When a study reports several external claims, the one in the abstract is rated; if there are several, the first is rated.

## Recording the claim

For each study, raters record the four claim elements:

- the behaviour, meaning the task and metric named in the claim;
- the unit of generalisation (patient, procedure, video, centre or dataset);
- the setting (the external centre or data source);
- the contrast (internal versus external), when the claim compares settings.

## Rating rules for published reports

Each check is rated using the published article, its supplements and any linked code or data repository.

Six ratings are available:

- **met**: the report gives the evidence named below;
- **partly met**: the evidence is given for part of the data, or is asserted without the record needed to check it;
- **not met**: the report shows that the requirement fails;
- **not reported**: the report is silent;
- **not assessable**: the report says the evidence existed but is not available;
- **not applicable**: for D7–D8, when the study does not compare settings.

| Check | Met when the report… | Not met when the report… |
|---|---|---|
| D1 Clinical-unit identity | states the unit of the external set and shows that no unit of the claimed kind occurs in both development and external data (for example, external data from another centre with patient identifiers or a statement of disjointness at the claimed unit) | shows overlap at the claimed unit, or splits at a lower unit than the claim names |
| D2 Content identity | describes a duplicate check (hash, near-duplicate or source-level control) between development and external data, or uses data from a centre that contributed nothing to development | reports duplicated content across sets |
| D3 Provenance and traceability | provides code and either the evaluated data or a manifest (case list, video identifiers or split file) from which the external evaluation can be replayed | states that the data or split cannot be shared and gives no manifest (rate partly met if code only, or manifest only) |
| D4 Endpoint estimability | reports the number of external cases or instances for every class or endpoint that is reported | reports an endpoint with zero external support, or omits classes without explanation |
| D5 Endpoint–claim alignment | uses a metric that measures the behaviour named in the claim (for example, detection claims with a localisation-based metric; recognition claims with per-class or balanced metrics when classes are imbalanced) | uses a proxy that does not measure the claimed behaviour (for example, output frequency for detection; accuracy alone for a rare-event claim) |
| D6 Reference sufficiency | describes how the external reference was produced (annotators, protocol) and states that it covers every case or frame evaluated | uses a reference that covers only part of the evaluated data while reporting metrics that need complete coverage |
| D7 Source adequacy | reports internal (source) performance with the same metric before interpreting the external result | interprets an external difference without internal performance on the same metric |
| D8 Fixed model and operating rule | states that the same trained model and thresholds were applied externally without re-training or tuning on external data | tunes, re-trains or re-thresholds on external data without separating that from the external estimate |

Decision rules for borderline cases are recorded in a log during the pilot and applied to all studies.

## Procedure

1. **Pilot.** Both raters rate three studies chosen at random, discuss the results and refine the decision log. The pilot studies are then re-rated independently.
2. **Independent rating.** Two raters rate every study independently, recording a verbatim quotation and its location for every rating that is not "not reported". If draft extractions are prepared with AI assistance, each rater verifies every rating against the quoted text in the original article, and the use of AI assistance is disclosed in the manuscript.
3. **Consensus.** Disagreements are resolved by discussion. A third author decides if no agreement is reached.
4. **Supportable claim.** From the consensus ratings, raters state the strongest claim the report supports and whether it equals the claimed one.

## Analysis

- **Agreement.** Raw agreement and Cohen's κ for each check, computed on the six-category ratings, with 95% CIs by bootstrap over studies. Agreement is also reported on a collapsed scale (met versus not met).
- **Prevalence.** For each check, the number and percentage of studies with each consensus rating, with Wilson 95% CIs.
- **Complete profiles.** The number of studies whose report allows every required check to be confirmed as met.
- **Claim match.** The number of studies whose supportable claim matches the stated claim.
- **No hypothesis tests.** The analysis is descriptive.

## Reporting

Ratings, quotations and the decision log are published with the manuscript.

## Changes after fixing the protocol

1. **No pilot.** The pilot on three studies was not run. Decision rules added independently by each extraction were reconciled after rating into one decision log (decision_log.md). The adjudicator then applied that log to every study, including cells on which the two extractions agreed. Six such agreed cells were changed.
2. **D8 rated for every study.** D8 was rated for every study, because a model or threshold can be changed on external data even when the claim does not compare settings. Read literally, the protocol would have rated D8 as not applicable in 12 studies.
3. **Independent extraction.** The two extractions were prepared with AI assistance under this protocol, blind to each other, and adjudicated against the source text. Two authors verified every consensus rating and quotation against the source articles.
4. **Source of quotations.** For 11 studies, quotations were taken from publisher or repository web pages rather than from the PDFs. For the other eight, they were taken from PDFs supplied by the authors.
