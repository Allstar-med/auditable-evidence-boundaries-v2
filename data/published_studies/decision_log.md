# Decision log: harmonised rules and adjudication

Adjudication rules fixed 30 October 2026, after both independent extractions were complete. A and B denote extractions 1 and 2. The rules below replace rater A's rules (A1 to A4) and rater B's rules (R1 to R4), along with every other ad hoc rule in the rater notes. Section 3 shows how each rater rule was handled. Codes: m met, p partly met, n not met, r not reported, a not assessable, x not applicable.

## 1. General rules

- **G1 Claim.** Rate the external claim in the abstract. If the abstract has none, rate the first external claim in the conclusions, and if there is none there, the first in the body. If the report makes no external claim at all, rate the main performance claim in the abstract. In that case, the data that Carstens et al. classified as external count as the "external set" for every check.
- **G2 Several settings in one claim.** When one claim names several datasets or scenarios, rate each one, then combine the ratings. If all are m, the result is m. If any is n, the result is n. Otherwise, if any is m or p, the result is p. Failing that, the result is a if any is a, or r if not. A setting that has no quantitative result counts as r for D4 to D6.
- **G3 Unit.** Use the unit that the claim names. If the claim names none, use the unit that makes the data "external": dataset or centre.
- **G4 Evidence base.** Use only the article, its supplements and any linked code or data. Outside knowledge may be used for two things only: to identify known derivative datasets (from the rater instructions), and to judge `external_as_defined` from the documentation of a cited dataset. It is never used to raise a rating.
- **G5 Task as defined.** Rate D5 against the task as the methods define it, not against the word used in the claim. For example, "triplet detection" scored by presence mAP is rated as recognition.

## 2. Check-specific rules

### D1 Clinical-unit identity
- **D1.1 m:** the report shows that no unit of the claimed kind occurs in both development and external data. Any of these is enough: an explicit statement of disjointness at the claimed unit; a description of the external source that separates it from every development source (another named centre, another species or procedure, a new collection); or procedures performed prospectively with the deployed, frozen system.
- **D1.2 Different public dataset, at the dataset unit:** rate m if the report's description separates the dataset from all development sources. Rate p if the report only names it or calls it "a different source/dataset". Rate r if the report says nothing.
- **D1.3 n:** any of the following. Overlap at the claimed unit is shown. The external set is a known derivative of a development dataset. The data are split below the claimed unit: a frame, image or sequence split for a dataset or centre claim, which includes fine-tuning on the external source's own training split (rule F1). Images are assigned at random from a single pool.
- **D1.4 p:** disjointness is shown only at a lower unit, or development data of unknown origin make it impossible to verify disjointness at the centre level.

### D2 Content identity
- **D2.1 m:** the report describes a duplicate, near-duplicate or source-level control between all development data (pretraining, training and fine-tuning) and the evaluated data. A split at the video, patient or sequence level, or prospective procedures as in D1.1, count as source-level controls. Alternatively, rate m when the report states that the external centre contributed no development data and no development data are of unknown origin.
- **D2.2 p:** duplicate removal is asserted with no method ("no duplicate videos", "duplicates removed"); another source is asserted but not stated to be absent from development; or the control covers only part of the data.
- **D2.3 n:** the report shows duplicated content. This covers a known derivative with no control, a split described as proportions of frames or images from the same videos, and training and test patches drawn from the same frames. If the report also contains statements that conflict with a frame-level split, rate p instead.
- **D2.4 r:** the report says nothing.

### D3 Provenance and traceability
- **D3.1 m:** code is available together with either the evaluated data or a manifest. A manifest can be a case list, a split file, a citation to a fixed published split (an official challenge test set or a numbered fold definition), a whole public release used in full, or a deterministic selection rule applied to a public release.
- **D3.2 p:** code only, or data or a manifest only. "We replicate the setup of [x]" without a fixed case list is not a manifest. Code "released upon acceptance" counts as no code. Availability links that do not lead to the evaluated data are an assertion without record, so p.
- **D3.3 a:** data are "available on request" and there is no code and no manifest. With code or a manifest as well, rate p.
- **D3.4 n:** the report states that the data cannot be shared, are not public or are private, and gives no code or manifest.
- **D3.5 r:** the report says nothing.

### D4 to D6
- **D4:** rate m when the number of external cases (for example videos or sequences) or instances is given for every reported endpoint. Rate p when only totals are given. Rate n when an endpoint has zero support, or when classes or models named in the claim are omitted without explanation.
- **D5:** using accuracy alone for imbalanced multi-class recognition is p. A proxy that does not measure the claimed behaviour is n. Apply G2 when some settings in the claim have no metric.
- **D6:** rate m when the report describes how the reference was produced and states that it covers every evaluated case. Rate p when it gives only part of that. Rate n when the report shows there is no reference for the claimed behaviour, or when the reference covers only part of the data but the metrics need full coverage.

### D7 Source adequacy
- **D7.1 Applicability:** rate D7 only when the claim or the report compares, or interprets, internal against external performance. This includes calling external results "generalisation", saying they "replicate prior results", or blaming a difference on domain shift. In every other case, rate x.
- **D7.2:** rate m when internal performance is reported with the same metric on the same endpoint (the same task and class set). Rate p for the same metric on a different class set or endpoint. Rate n when an interpretation is made without internal performance.

### D8 Fixed model and operating rule
- **D8.1 Applicability:** D8 is rated for every study, and x is not used. The rated claim always concerns a model applied to data outside its development setting, and the rater instructions define re-training on external data as n, which requires D8 to be applicable. *This is a clarification of the protocol's x clause ("D7–D8 … when the study does not compare settings"), now limited to D7, and must be listed under "Changes after fixing the protocol". Under the literal reading, D8 would be x for 12 studies: S02, S03, S05, S06, S08, S09, S11, S12, S14, S15, S18 and S19.*
- **D8.2 Scope of "external data":** for a dataset or centre claim, the whole claimed source. For a patient, video or procedure claim, the evaluated cases.
- **D8.3 m:** the report explicitly states that the weights and the operating rule (thresholds and parameters) were fixed and not tuned on the external data.
- **D8.4 p:** any of the following. A fixed model is implied but not stated, for example by a held-out test design, "previously trained", "tested directly" or a deployed system. Thresholds or parameters were "empirically set" on data that are not named. A zero-shot estimate of the claimed model is clearly reported separately, but the claim rests on a tuned estimate.
- **D8.5 n:** the model was trained or fine-tuned on any part of the external data (as scoped in D8.2), or it was re-thresholded, or its hyperparameters or source-data composition were chosen from results on the external data, and the claim rests on that estimate. A zero-shot result for a different model, such as a "Base" baseline, does not change the rating.
- **D8.6 r:** the report says nothing.

### F Fine-tuning and test-time adaptation on external data
- **F1:** if the evaluated model was trained or fine-tuned on any data from the claimed external source, including that source's own training split or a separate model trained for each dataset, that source is development data. Then `external_as_defined` = no, D1 = n for dataset or centre claims, and D8 = n.
- **F2:** some test-time inputs are part of the task definition and are given to every method compared: the first-frame mask in one-shot video segmentation, and the initial box in single-target tracking. When the claim names such a task, these inputs are not development use. The rated object is then the whole procedure: the initial weights, the adaptation algorithm and its settings. Online updates that use these inputs or pseudo-labels the model generates itself are part of that procedure. D8 is n only if the procedure's settings were chosen from results on the external sets.
- **F3:** test-time adaptation that uses external labels beyond the task definition, or fine-tuning on labelled external frames for the reported estimate, is handled under F1.

### Study-level fields
- **E1 `external_as_defined` = yes** only if the evaluated model, fixed as described in F2, produced the reported estimate on data from a centre or data source that contributed nothing to any development step: pretraining, training, fine-tuning, or selection of hyperparameters or thresholds. This must be shown by the report or by the cited dataset's own documentation.
- **E2:** new videos from centres that may also have contributed development data get "no", because the centre is not shown to be new. A new procedure type at the development centre also gets "no".
- **C1 `claim_supported` = yes** only if the supportable claim equals the stated claim on behaviour, unit, setting and contrast. An interpretive addition that the evidence does not isolate makes it "no".

## 3. How the rater rules were reconciled

| Rater rule | Decision |
|---|---|
| A1: D7 x when there is no contrast; D8 still rated | Kept for D7 (D7.1). For D8, generalised to "always rated" (D8.1). |
| A2 / B rule: no external claim in abstract or conclusion, so rate the first external claim in the body | Kept (G1), extended to reports with no external claim at all. |
| A3: external dataset itself split and trained on, so D1 = D2 = D8 = n | Kept for D1 and D8 (F1). D2 = n only when shared content is shown (D2.3). |
| A4 / B rule: adaptation on external first-frame labels gives D8 = n; Base not rated | Base rule kept (D8.5). First-frame and initial-box inputs that the task defines are not counted (F2). |
| R1: one claim covering several settings, rate the lower | Kept, with an explicit combination rule (G2). Replaces A's "rate the first scenario". |
| R2: D7 rated when development and external results are presented or a difference is interpreted | Narrowed to an actual comparison or interpretation (D7.1). Same metric now also requires the same endpoint (D7.2). |
| R3: D8 rated even when D7 is x, if changes to the model or threshold are documented; separated zero-shot gives p | Replaced by D8.1 (always rated). The p rule is kept (D8.4). |
| R4: data on request gives D3 = a | Kept (D3.3). A's "on request gives n" is rejected because on-request access is not a statement that the data cannot be shared. |
| A: a published split cited by reference counts as a manifest | Kept only for fixed case lists (D3.1, D3.2). |
| A: a deterministic selection rule on a public release counts as a manifest | Kept (D3.1). |
| B: "detection" that is really presence recognition gives D5 = p | Replaced by G5. |
| A: prospective procedures with the frozen deployed system count as a source-level control | Kept (D1.1, D2.1). |
| B: duplicate assertion without method gives p (S10, S11) | Kept (D2.2) and applied in the same way to S13. |

## 4. Application to the 19 studies

Every cell was set under the rules above. For each disagreement, the source text was checked. Local full texts were used for S04, S09, S10, S13, S14, S15, S16 and S19. For the other studies, verbatim passages were requested from the web text from the rater URLs or, for S18, from the publisher mirror. Direct PDF download was blocked by the network proxy, so quotes for S01 to S03, S05 to S08, S11, S12, S17 and S18 are as extracted from the web text and were not checked against a local PDF. For S04, the numerical results in Tables IV and V are images and were not used. The final codes, cell changes and reasons are listed below. The same entries appear in `ratings/consensus.csv`.

### 4.1 Summary of adjudication

| Check | Disagreements resolved | Agreed cells corrected |
|---|---|---|
| D1 | 7 | 1 |
| D2 | 4 | 1 |
| D3 | 6 | 0 |
| D4 | 2 | 0 |
| D5 | 2 | 1 |
| D6 | 2 | 0 |
| D7 | 1 | 1 |
| D8 | 10 | 2 |
| claim_supported | 1 | 0 |
| **Total (D1-D8)** | **34** | **6** |

External as defined (E1): yes for 4 studies (S01, S13, S16, S17); no for 15.

Consensus distribution (count of m/p/n/r/a/x):

| Check | m | p | n | r | a | x |
|---|---|---|---|---|---|---|
| D1 | 5 | 5 | 8 | 1 | 0 | 0 |
| D2 | 1 | 13 | 3 | 2 | 0 | 0 |
| D3 | 0 | 9 | 3 | 6 | 1 | 0 |
| D4 | 4 | 10 | 1 | 4 | 0 | 0 |
| D5 | 13 | 3 | 3 | 0 | 0 | 0 |
| D6 | 4 | 10 | 2 | 3 | 0 | 0 |
| D7 | 3 | 1 | 3 | 0 | 0 | 12 |
| D8 | 0 | 11 | 8 | 0 | 0 | 0 |

### 4.2 Study records

**S01 (Arabian 2023)**: D1-D8 = p p p r m r m p; claim_supported = no; external_as_defined = yes.

- D1: A=p, B=r -> p. The report calls EndoVis 2019 "data from a different source" but gives no origin or disjointness record, so this is an assertion without record (D1.2).
- D3: A=p, B=r -> p. The external data are a public challenge release filtered by a stated deterministic rule (frames with non-Cholec80 classes removed), which counts as a manifest; no code is given (D3.1-D3.2).
- Supportable claim: A Cholec80-trained P-CSEM classifier, applied with no reported retraining to an EndoVis 2019 (HeiChole) subset restricted to Cholec80 tool classes, reached mAP 59.52% (base 58.57%), against 93.14% on Cholec80 test videos. External frame counts, class support and the external reference standard are not reported, so the estimate cannot be checked or sized.

**S02 (Batić 2024)**: D1-D8 = n p p r m r x n; claim_supported = no; external_as_defined = no.

- D1: A=p, B=n -> n. The claim unit is the downstream dataset. Cholec80 is in Endo700k pretraining and the models are fine-tuned on Cholec80-family training splits, so development and evaluation overlap at the dataset unit (F1, D1.3).
- D3: A=m, B=p -> p. Code is released, but the CholecSeg8k split is given only as "We replicate the evaluation setup of [24]", with no fixed case list; repository split files could not be verified (D3.2).
- D5: A=p, B=m -> m. The rated claim names triplet recognition (CholecT45 mAP) and segmentation (mIoU), and both metrics fit. Phase accuracy, the basis for A's p, is not part of the rated claim.
- D8: A=n, B=x -> n. D8 is always rated (D8.1). The evaluated models are trained or fine-tuned on the downstream datasets' training splits (F1).
- Supportable claim: After fine-tuning on Cholec80-family training splits, EndoViT exceeded ImageNet pretraining on CholecT45 fold-5 triplet mAP and gave the highest CholecSeg8k mIoU among the compared methods. These are same-source (Cholec80) benchmark results on data whose source is also in the Endo700k pretraining corpus, not an external validation.

**S03 (Batić 2023)**: D1-D8 = n p p r p r x n; claim_supported = no; external_as_defined = no.

- D1: A=p, B=n -> n. "testing only on one fold allows us to have CholecT45 images in the pretraining", and the downstream models are trained on the same datasets, so the data overlap at the dataset unit (F1, D1.3).
- D8: A=n, B=x -> n. D8 is always rated (D8.1). "We first train the models on the full downstream dataset." (Sec. 3) (F1).
- Supportable claim: After fine-tuning, Endo700k pretraining improved CholecT45 fold-5 triplet recognition mAP over ImageNet pretraining but not Cholec80 phase accuracy, on same-source data that are partly in the pretraining corpus. Two tasks do not establish the general claim that the benefit depends on task complexity, and there is no external evaluation. This is the preprint of S02, so the two are not independent.

**S04 (Chen 2024)**: D1-D8 = n p p p m p p n; claim_supported = no; external_as_defined = no.

- D1: A=B=p -> n. Correction. The claim unit is the public dataset, and each evaluated model was fine-tuned on that dataset's own training split ("use 2, 400 images of eight sequences (#1-8) for fine-tuning"). That is a split below the claimed unit (F1, D1.3).
- D7: A=B=m -> p. Correction. Internal IVIS-E instrument mIoU (Table III, "nearly 80% mIoU") covers 3 instrument classes. The external endpoints are 6-class type and 3-class part segmentation (EndoVis) and 8-class tissue/instrument segmentation (CholecSeg8k): the same metric on a different endpoint (D7.2).
- Supportable claim: After fine-tuning on each public dataset's own training split, SurgNet-pretrained UPerNet had higher mIoU than the compared methods on EndoVisSub2017-RIS sequences 9-10 and on a CholecSeg8k test split whose split unit is not stated (Tables IV-V); several baselines are copied from other papers. This supports the benefit of the pretraining after target-domain fine-tuning, not the performance of a fixed model on unseen data.

**S05 (Daneshgar Rahbar 2023)**: D1-D8 = n r p p p p x n; claim_supported = no; external_as_defined = no.

- D3: A=n, B=p -> p. The data-availability links lead to a generic Roboflow page and a PMC video page, so availability of the evaluated data is asserted without a usable record. Internet-video links are "available upon request", the EndoVis 17 split is described, and there is no code. Combined across settings: p (G2, D3.2-D3.3).
- D5: A=B=m -> p. Correction. The claimed evaluation dataset comprises DVR, Internet/NLM and EndoVis 17 data, but metrics are reported only for the DVR test set. Settings without a metric combine to p (G2).
- D6: A=r, B=p -> p. The reference production is described for DVR ("automatically generated using joint encoder information and forward kinematics. Hand-eye calibration errors are manually corrected."), but coverage is not stated and nothing is said for the other sets (G2).
- D8: A=n, B=x -> n. D8 is always rated (D8.1). EndoVis 17 "was utilized for both testing and training purposes", and the DVR model is trained on DVR training videos, i.e. on the claimed sources (F1).
- Supportable claim: On held-out ex vivo dVRK (DVR) test videos from the training source, EUGNet improved IoU and DSC by about 1.7 points over U-Net. No quantitative result is reported for the Internet/NLM videos or for EndoVis 17, so there is no evidence of performance on another data source.

**S06 (Du 2019)**: D1-D8 = p p p p p p x p; claim_supported = no; external_as_defined = no.

- D2: A=r, B=p -> p. The report asserts that the tracker needs no "offline training", so there are no development images, but it does not state the data used to set the parameters and gives no duplicate check. This is an assertion without record (D2.2).
- D5: A=p, B=m -> p. Distance error measures tracking on EndoVis, but the in vivo part of the claim ("promising performance on in vivo surgical instrument tracking") has no quantitative metric (Fig. 18), so p (G2).
- D8: A=m, B=x -> p. Under F2 the initial target box is a task input. "we use the same parameter setting through all experiments", but the parameters were "empirically set" and the patch number "selected" on data that are not stated, and the authors evaluated on EndoVis training sequences whose videos continue into the test set. A fixed procedure is implied, but it is not shown to be untuned on the source (D8.4).
- Supportable claim: On the EndoVis 2015 tracking test sets, scored by the organisers against unreleased ground truth, PAWSS (no offline training, one parameter setting for all experiments) had the lowest mean distance error among the submitted methods (29.66 px, robotic). Most test sequences continue videos whose earlier segments the authors annotated and evaluated, and performance on the other in vivo sequences is shown only qualitatively.

**S07 (Huang 2022)**: D1-D8 = r r r r n n m p; claim_supported = no; external_as_defined = no.

- D6: A=n, B=r -> n. "As there was no per-pixel depth ground truth label available" (Sec. III): the external depth claim has no reference standard, so the requirement is shown to fail.
- Supportable claim: A DB80-trained SDSNET, applied to a second laparoscopic dataset (ref. [28]) without whole-network retraining, had an image-reconstruction SSIM of 77.53 against 76.67 for Monodepth2. Depth accuracy against a depth reference and tool segmentation were not evaluated externally, and the size of the external test set is not reported.

**S08 (Jaspers 2024)**: D1-D8 = p p p p m p x p; claim_supported = no; external_as_defined = no.

- D1: A=m, B=p -> p. Test patients are excluded from SurgeNet pretraining, but the downstream train/test split level is not stated for CholecSeg8k or RAMIE. Patient disjointness between downstream training and test is shown for RARP only (D1.4, G2).
- D2: A=m, B=p -> p. The patient-level exclusion is a source-level control between pretraining and test data only. No control between downstream training and test frames is described for CholecSeg8k and RAMIE (D2.2).
- D8: A=n, B=x -> p. D8 is always rated (D8.1). The unit is the patient, so the external data are the test patients (D8.2). Models are trained on separate training patients with five-fold CV and early stopping, there is no statement that the test set was left untouched, and Fig. 1 reports Dice "from the fivefold cross-validation" (D8.4).
- claim_supported: A yes / B no -> no. It is unclear whether the reported Dice comes from the test set or from cross-validation, and the "heterogeneous" data also enlarge the pretraining set, so the diversity attribution is not isolated (C1).
- Supportable claim: On held-out test patients from three downstream datasets whose centres also supplied SurgeNet pretraining data, and after downstream training, adding heterogeneous surgical data to procedure-specific SSL data went with higher Dice (+5.0, 5.2 and 2.5%). It is unclear whether these Dice values come from the test set or from cross-validation; the added diversity is confounded with added pretraining volume; and no centre absent from development was evaluated.

**S09 (Khalid 2023)**: D1-D8 = m p r p n p x p; claim_supported = no; external_as_defined = no.

- D8: A=x, B=p -> p. D8 is always rated (D8.1). The default (argmax) result for injurious acts is reported separately (6/11 in the Go zone), but the abstract figures use a Go threshold modulated on these same evaluation videos ("after maximizing the probability threshold of the Go algorithm"): a separated zero-shot estimate with the claim resting on the tuned one (D8.4).
- Supportable claim: In 11 BDI videos and 11 expert-selected safe LC videos not used in training, a larger share of tool-tissue interactions in BDI videos lay outside GoNoGoNet's Go zone (zones read from one reference frame per minute). Under the default rule, 6 of 11 injury-causing interactions lay inside the Go zone; the abstract's 2 of 11 needs a Go threshold raised on these same videos. Detection accuracy for unsafe dissection and any prevention of BDI were not measured, and the centres are not shown to be new.

**S10 (Laplante 2022)**: D1-D8 = m p r m m m n p; claim_supported = no; external_as_defined = no.

- No changes. The raters agreed on every cell, and every cell is consistent with the log.
- Supportable claim: Against a >50% pixel consensus of 6 new experts on 47 frames from 25 new LC videos (7 institutions, whose overlap with the 136 development institutions is not reported), the previously trained GoNoGoNet reached mean Dice 0.58 (Go) and 0.80 (No-Go), with Go PPV 0.70 and No-Go sensitivity 0.80. Estimates vary with the consensus definition, there are no CIs, they apply only to frames selected for a full view of the hepatocystic triangle, and they cannot be replayed.

**S11 (Li 2023)**: D1-D8 = m p r p m m x p; claim_supported = yes; external_as_defined = no.

- D8: A=p, B=x -> p. D8 is always rated (D8.1). No model was trained on CVS6K, but the rule thresholds were "empirically set" (T_liver=100, T_cp=100) on data that are not stated (D8.4).
- Supportable claim: On 100 held-out videos (CVS6K) from the same public Cholec80/m2cai16-workflow source as the 17 development videos, the segmentation-plus-rule CVS pipeline had higher balanced accuracy than a re-implemented DeepCVS. The stated comparative claim is supported, but this is a held-out-video evaluation, not an other-centre validation.

**S12 (Liu 2022)**: D1-D8 = n p n p m m x p; claim_supported = no; external_as_defined = no.

- D1: A=n, B=p -> n. The claim's external element is the centre (test set "from its healthcare alliance"), but the report states that the annotated frames were "randomly assigned to training, validation, and test datasets" from videos collected at West China Hospital. That is a split below the centre unit (D1.3), and the alliance statement is contradicted by the report's own counts.
- D8: A=r, B=x -> p. D8 is always rated (D8.1). A held-out test design implies the test images were not used for training, but nothing is stated on model selection or thresholds (D8.4).
- Supportable claim: YOLOv3 detected four anatomic regions on 553 annotated frames that the report describes as randomly assigned from the same pool of frames from videos collected at West China Hospital. This conflicts with the statement that the test set came from an alliance hospital, so performance at another centre is not shown. The AI-versus-surgeon comparison rests on 28 still images from 2 videos.

**S13 (Madani 2022)**: D1-D8 = p p r n m m m p; claim_supported = no; external_as_defined = yes.

- D1: A=p, B=m -> p. The leave-Strasbourg-out design is stated, but Table 1 lists 15 development videos of "Unknown" institution, and the paper's ref. 15 is "The TUM LapChole dataset", so disjointness at the institution level cannot be verified (D1.4).
- D2: A=B=m -> p. Correction. "All duplicate videos were removed" is asserted with no method, and development videos of unknown origin rule out the other-centre path (D2.1-D2.2). Same treatment as S10 and S11.
- D4: A=r, B=n -> n. The claim concerns "the models'" performance, but the leave-institution-out results (Table 3) omit CholeNet's classes (liver, gallbladder, hepatocystic triangle) without explanation, and no external frame count is given (D4).
- Supportable claim: GoNoGoNet trained on videos from institutions other than Strasbourg segmented Go and No-Go zones on frames from Cholec80/M2CAI16-workflow videos with mean F1 0.63 and 0.81 (IoU 0.46 and 0.68), the same as a model trained within that institution (F1 0.63 and 0.80). The drop against full-dataset CV (F1 0.70 and 0.83) is measured on a different test set; the number of external frames is not reported; and CholeNet was not tested externally. The stated "diminished" performance is therefore not supported.

**S14 (Wang 2020)**: D1-D8 = n n n p m p x n; claim_supported = no; external_as_defined = no.

- No changes. The raters agreed on every cell, and every cell is consistent with the log.
- Supportable claim: Trained and tested on 50/30/20 frame partitions within each dataset, the sample-adaptation detector reached mAP 70.1% (m2cai16-tool-locations) and 77.3% (single-centre AJU-Set). These are within-dataset estimates, not evidence of performance at a centre unseen in development.

**S15 (Zhang 2020)**: D1-D8 = n n n p m p x n; claim_supported = no; external_as_defined = no.

- No changes. The raters agreed on every cell, and every cell is consistent with the log.
- Supportable claim: Trained and tested on 50/30/20 frame partitions within each dataset, the Modulated Anchoring Network reached mAP 69.6% (m2cai16-tool-locations) and 76.5% (single-centre AJU-Set, the same private dataset as S14). These are within-dataset estimates, not external validation.

**S16 (Zhao 2021a)**: D1-D8 = m p p m m p n n; claim_supported = no; external_as_defined = yes.

- D3: A=p, B=r -> p. EndoVis17/18 are used as whole public releases (a manifest), HKPWH has no availability statement, and there is no code statement. Combined: p (G2, D3.1-D3.2).
- D8: A=n, B=p -> n. Under F2 the first-frame mask is a task input, but the key adaptation hyperparameters were examined on EndoVis17 (Sec. 4.7, Fig. 8 "hyper-parameters selection"), and EndoVis15 was added to the source because it "can empirically bring 2-4% performance improvement on EndoVis17 and EndoVis18" (Sec. 4.1). Procedure settings were chosen on the scenario-1 external sets (D8.5, G2).
- Supportable claim: Given the labelled first frame of each target video and online adaptation, AOMA had higher mean IoU than the compared one-shot methods on EndoVis17/18 (77.1/68.4; adaptation hyperparameters and source composition chosen with these sets) and on 4 HKPWH sequences from another hospital (80.1). The source-trained Base model without adaptation reached 60.5/47.2/57.2. Source-domain performance is not reported, so the attribution to domain shift is not supported.

**S17 (Zhao 2021b)**: D1-D8 = p p p m m p n p; claim_supported = no; external_as_defined = yes.

- D3: A=p, B=r -> p. EndoVis18 is used in full as a public release (a manifest); HKPWH and code have no statement. Combined: p (G2).
- D4: A=m, B=p -> m. The single endpoint (a binary instrument mask) has its external cases reported for each set (15 EndoVis18 sequences; 8 HKPWH sequences), and D4 accepts cases or instances.
- D7: A=x, B=r -> n. The report interprets the external result against the source ("The base model trained on EndoVis17 cannot generalize well on target domains ... because of the distribution shift between two domains."), but no EndoVis17 performance is reported (D7.1-D7.2).
- D8: A=B=n -> p. Correction. Under F2 the first-frame mask is the defined input of the one-shot task. The adaptation hyperparameters are fixed values with no stated selection data, and the report does not show they were chosen on EndoVis18/HKPWH (it reports ablations on those sets), so a fixed procedure is implied, not stated (D8.4).
- Supportable claim: Given the first-frame mask of each target video and online self-adaptation, MDAL trained on EndoVis17 had higher IoU/Dice than the compared adaptive methods on EndoVis18 and on 8 HKPWH sequences from another hospital. The un-adapted Base model reached 58.0/61.7 IoU. Source-domain performance is not reported, so the attribution of the drop to distribution shift is not supported.

**S18 (Zhao 2019)**: D1-D8 = n n r m m p x n; claim_supported = no; external_as_defined = no.

- D2: A=n, B=r -> n. Training and test patches for each dataset are drawn from the same frame set (e.g. "500 frames, 600 test patches, and 2100 training patches"), so development and evaluation share video content (D2.3).
- D8: A=n, B=x -> n. D8 is always rated (D8.1). "this work used each single dataset to train a specific model" (F1).
- Supportable claim: With a separate CNN trained on patches from each of eight datasets, the tracker had mean pixel errors comparable to or lower than four other trackers on the same datasets. No model was evaluated on a source it was not trained on.

**S19 (Zheng 2023)**: D1-D8 = m m a p n n x p; claim_supported = no; external_as_defined = no.

- D1: A=m, B=p -> m. The 12 partial nephrectomies were performed prospectively with the deployed LSQS, so they cannot be in the development data (urological videos of other procedure types plus Cholec80). Prospective use of the frozen system shows disjointness at the procedure unit (D1.1).
- D2: A=m, B=r -> m. For the same reason, frames come from procedures that did not exist when the model was developed, which is a source-level control (D2.1).
- D3: A=n, B=a -> a. "Data can be obtained from corresponding authors upon reasonable request." with no code or manifest (D3.3).
- D8: A=B=x -> p. Correction. D8 is always rated (D8.1). The trained PaddleSeg model was converted and deployed, and the OR thresholds were set beforehand on 20 separate videos, so no tuning on the validation procedures is described. However, there is no explicit fixed-model statement, and the thresholds were derived from PSPNet outputs, not from the deployed model (D8.4).
- Supportable claim: In 12 partial nephrectomies at the development centre (one non-expert and one expert operator, 3 procedures per condition), the share of extracted frames that LSQS itself classed as "excellent" rose from 50.78% to 81.67% when the non-expert used LSQS. There is no independent reference for laparoscope control and no segmentation accuracy on these procedures, and the thresholds were derived with a model (PSPNet) other than the one deployed (PaddleSeg DeepLabv3+).

