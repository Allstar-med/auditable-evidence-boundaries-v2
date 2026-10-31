"""Case 1 clip-classifier checks (CPU; numpy and pandas).

Input: CSV with one row per validation clip of the accepted partition (repair 2), and optionally of the
supplied partition: partition, clip, patient, y_true, y_pred  (class names or ids).

  python clip_classifier_checks.py clips.csv OUT_DIR

Outputs: per-partition accuracy and balanced accuracy with patient-clustered 95% bootstrap intervals,
per-class recall and support, per-patient accuracy, and the confusion matrix.
"""
import json
import os
import sys

import numpy as np
import pandas as pd


def metrics(d):
    acc = float((d.y_true == d.y_pred).mean())
    ok = (d.y_true == d.y_pred)
    rec = ok.groupby(d.y_true).mean()
    return acc, float(rec.mean())


def main(path, out, B=5000, seed=20261030):
    os.makedirs(out, exist_ok=True)
    D = pd.read_csv(path)
    res = {}
    for part, d in D.groupby("partition"):
        acc, bal = metrics(d)
        pats = d.patient.unique(); rng = np.random.default_rng(seed); bs = []
        for _ in range(B):
            pick = rng.choice(pats, len(pats))
            dd = pd.concat([d[d.patient == p] for p in pick])
            bs.append(metrics(dd))
        bs = np.array(bs)
        res[part] = dict(clips=int(len(d)), patients=int(len(pats)), accuracy=acc,
                         accuracy_95CI=[float(np.quantile(bs[:, 0], .025)), float(np.quantile(bs[:, 0], .975))],
                         balanced_accuracy=bal,
                         balanced_accuracy_95CI=[float(np.nanquantile(bs[:, 1], .025)), float(np.nanquantile(bs[:, 1], .975))])
        ok = (d.y_true == d.y_pred)
        pd.DataFrame(dict(support=ok.groupby(d.y_true).size(), recall=ok.groupby(d.y_true).mean())) \
            .to_csv(os.path.join(out, f"{part}_per_class.csv"))
        pd.DataFrame(dict(clips=ok.groupby(d.patient).size(), accuracy=ok.groupby(d.patient).mean())) \
            .to_csv(os.path.join(out, f"{part}_per_patient.csv"))
        pd.crosstab(d.y_true, d.y_pred).to_csv(os.path.join(out, f"{part}_confusion.csv"))
    json.dump(res, open(os.path.join(out, "summary.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
