"""Agreement and prevalence of the evidence checks in published external validations.

Usage: python published_study_agreement.py RATER1.csv RATER2.csv CONSENSUS.csv OUT_DIR
Each CSV: study_id, D1..D8 with codes m (met), p (partly met), n (not met), r (not reported),
a (not assessable), x (not applicable); CONSENSUS.csv also has claim_supported (yes/no).
"""
import os
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CHECKS = [f"D{i}" for i in range(1, 9)]
NAMES = ["Clinical-unit identity", "Content identity", "Provenance and traceability", "Endpoint estimability",
         "Endpoint–claim alignment", "Reference sufficiency", "Source adequacy", "Fixed model and operating rule"]
CODES = ["m", "p", "n", "r", "a", "x"]
LAB = dict(m="Met", p="Partly met", n="Not met", r="Not reported", a="Not assessable", x="Not applicable")
COL = dict(m="#c5dfb0", p="#fbe38c", n="#f4a68f", r="#e4e4e4", a="#9a9a9a", x="#ffffff")


def kappa(a, b):
    a = np.asarray(a); b = np.asarray(b)
    cats = sorted(set(a) | set(b))
    po = np.mean(a == b)
    pe = sum(np.mean(a == c) * np.mean(b == c) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else np.nan


def wilson(k, n, z=1.96):
    if n == 0:
        return np.nan, np.nan
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def load_ratings(r1, r2, cons):
    tables = []
    for path in (r1, r2, cons):
        table = pd.read_csv(path, dtype=str)
        missing = set(["study_id", *CHECKS]) - set(table.columns)
        if missing or table.empty:
            raise ValueError(f"{path}: empty table or missing columns: {sorted(missing)}")
        if table.study_id.isna().any() or table.study_id.str.strip().eq("").any() or table.study_id.duplicated().any():
            raise ValueError(f"{path}: study_id must be nonempty and unique")
        if not table[CHECKS].isin(CODES).all().all():
            raise ValueError(f"{path}: invalid or missing rating code")
        tables.append(table.set_index("study_id"))
    if not (set(tables[0].index) == set(tables[1].index) == set(tables[2].index)):
        raise ValueError("Rater and consensus study IDs must match exactly")
    if "claim_supported" not in tables[2] or not tables[2].claim_supported.isin(["yes", "no"]).all():
        raise ValueError("Consensus claim_supported must contain yes or no")
    ids = sorted(tables[0].index)
    return tuple(table.loc[ids] for table in tables)


def main(r1, r2, cons, out, B=5000, seed=20261030):
    A, Bd, C = load_ratings(r1, r2, cons)
    os.makedirs(out, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []
    for d in CHECKS:
        a, b = A[d].values, Bd[d].values
        k = kappa(a, b)
        a2 = np.where(a == "m", "m", "o"); b2 = np.where(b == "m", "m", "o")
        bs = [kappa(*(lambda i: (a[i], b[i]))(rng.integers(0, len(a), len(a)))) for _ in range(B)]
        rows.append(dict(check=d, name=NAMES[CHECKS.index(d)], studies=len(a), agreement=np.mean(a == b),
                         kappa=k, kappa_lo=np.nanquantile(bs, 0.025), kappa_hi=np.nanquantile(bs, 0.975),
                         kappa_met_vs_other=kappa(a2, b2)))
    pd.DataFrame(rows).to_csv(os.path.join(out, "agreement.csv"), index=False)

    rows = []
    for d in CHECKS:
        n = len(C)
        for c in CODES:
            k = int((C[d] == c).sum()); lo, hi = wilson(k, n)
            rows.append(dict(check=d, rating=LAB[c], n=k, total=n, pct=100 * k / n, lo=100 * lo, hi=100 * hi))
    prev = pd.DataFrame(rows); prev.to_csv(os.path.join(out, "prevalence.csv"), index=False)
    req = C[CHECKS].apply(lambda r: all(v in ("m", "x") for v in r), axis=1)
    summ = dict(studies=len(C), all_required_checks_met=int(req.sum()),
                claim_supported=int((C.get("claim_supported", pd.Series(dtype=str)) == "yes").sum()))
    pd.Series(summ).to_csv(os.path.join(out, "summary.csv"))

    # figure: stacked bars in the style of published risk-of-bias summaries
    mpl.rcParams.update({"font.family": "Inter", "font.size": 6.5, "axes.linewidth": 0.5,
                         "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42})
    fig, ax = plt.subplots(figsize=(120 / 25.4, 62 / 25.4))
    for i, d in enumerate(CHECKS):
        left = 0
        for c in CODES:
            v = 100 * (C[d] == c).mean()
            if v:
                ax.barh(i, v, left=left, height=0.62, color=COL[c], edgecolor="#222222", lw=0.45)
                left += v
    ax.set_yticks(range(8)); ax.set_yticklabels([f"D{i + 1} {n}" for i, n in enumerate(NAMES)])
    ax.invert_yaxis(); ax.set_xlim(0, 100); ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel(f"Studies (%), n={len(C)}"); ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
    hs = [mpl.patches.Rectangle((0, 0), 1, 1, fc=COL[c], ec="#222222", lw=0.45) for c in CODES]
    ax.legend(hs, [LAB[c] for c in CODES], ncol=6, frameon=False, loc="lower left", bbox_to_anchor=(-0.45, 1.0),
              fontsize=5.6, handlelength=1, columnspacing=0.8, handletextpad=0.3)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(out, f"Figure4_published_studies.{ext}"), dpi=600, bbox_inches="tight")
    print(pd.read_csv(os.path.join(out, "agreement.csv")).round(2).to_string(index=False)); print(summ)


if __name__ == "__main__":
    main(*sys.argv[1:5])
