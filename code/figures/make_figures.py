"""Figures of the manuscript. Usage: python make_figures.py OUT_DIR

Environment variables: ENDOSCAPES_ROOT (folder with test/ and semseg/ of Endoscapes2023; panels 2D and 3D),
CLINICAL_FRAME (path stem of the clinical frame and its LabelMe JSON; panel 3C, not distributed).

Style taken from figures published in The Lancet Digital Health (2026; 8(9)): thin black outlines,
pastel traffic-light fills for assessments (as in risk-of-bias plots), black and white markers for data,
regular-weight sans-serif type, plain panel titles led by a bold capital letter, midline decimal points,
and no grid lines.
"""
import os
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

from figdata import ARCHIVE, CASE1, FIRING, MACAU, SOURCE

OUT = sys.argv[1] if len(sys.argv) > 1 else "figures"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "code"))
from distance_summary import load_distances
ENDO = os.environ.get("ENDOSCAPES_ROOT", "")
CLIN = os.environ.get("CLINICAL_FRAME", "")
os.makedirs(OUT, exist_ok=True)

mpl.rcParams.update({
    "font.family": "Inter", "font.size": 6.5, "axes.titlesize": 6.5, "axes.labelsize": 6.5,
    "xtick.labelsize": 6, "ytick.labelsize": 6, "legend.fontsize": 6, "axes.linewidth": 0.5,
    "xtick.major.width": 0.5, "ytick.major.width": 0.5, "xtick.major.size": 2.2, "ytick.major.size": 2.2,
    "axes.edgecolor": "#222222", "axes.spines.top": False, "axes.spines.right": False,
    "pdf.fonttype": 42, "svg.fonttype": "none", "figure.dpi": 150})

MM = 1 / 25.4
K = "#222222"; GREY = "#6f6f6f"; LINE = "#222222"
MET, PART, NOT, UNK, NA = "#c5dfb0", "#fbe38c", "#f4a68f", "#e4e4e4", "#ffffff"   # traffic-light fills
LOST = "#9a9a9a"
TINT1, TINT2, TINT3 = "#dde6ef", "#a3b9d1", "#4f6f93"                               # single-hue tints
EW = 0.45


def mid(x, nd):
    return f"{x:.{nd}f}".replace(".", "·")


def ptitle(fig, x, y, letter, text):
    fig.text(x, y, letter, fontsize=8, fontweight="semibold", color=K, va="baseline")
    fig.text(x + 0.017, y, text, fontsize=6.8, color=K, va="baseline")


def save(fig, name):
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=600, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


# ------------------------------------------------------------------ assessments (Figure 1B)
CHECKS = ["Clinical-unit identity", "Content identity", "Provenance and traceability",
          "Endpoint estimability", "Endpoint–claim alignment", "Reference sufficiency",
          "Source adequacy", "Fixed model and operating rule"]
LAYERS = [("Partition", 0, 3), ("Endpoint", 3, 6), ("Comparison", 6, 8)]
ROWS = ["Case 1, supplied partition*", "Case 1, repair 1 (12/5)*", "Case 1, repair 2 (13/4)*",
        "Case 2, archived comparison", "Case 2, executed reconstruction"]
# one code per check, in the order of CHECKS: m met, p partly met, n not met, u not reported or not
# assessable, x not applicable. The evidence behind every code is listed in appendix table S2.
R = ["nrprrrxx",
     "mrpnrrxx",
     "mrpmrrxx",
     "aanrnnaa",
     "ppmrmnnm"]
CLAIM = ["No claim about unseen patients", "No claim covering all classes", "Internal estimate, 4 patients",
         "Output rates only (descriptive)", "No transfer claim"]
FILL = dict(m=MET, p=PART, n=NOT, r=UNK, a=LOST, x=NA)
SYM = dict(m="+", p="~", n="–", r="?", a="×", x="")
LEG = [("m", "Met"), ("p", "Partly met"), ("n", "Not met"), ("r", "Not reported"), ("a", "Not assessable"),
       ("x", "Not applicable")]


def figure1():
    fig = plt.figure(figsize=(180 * MM, 96 * MM))

    # A: evidence chain
    ax = fig.add_axes([0.0, 0.0, 0.32, 0.92]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ptitle(fig, 0.0, 0.955, "A", "Claim-indexed evidence chain")
    blocks = [("Claim", "Behaviour, unit of generalisation,\nsetting and, for comparisons, contrast", []),
              ("Partition evidence", "Is the evaluation set independent of\ndevelopment at the claimed unit?",
               CHECKS[0:3]),
              ("Endpoint evidence", "Does the metric, with this reference,\nmeasure the claimed behaviour?",
               CHECKS[3:6]),
              ("Comparison evidence", "Is a difference between settings\nattributable to the setting?",
               CHECKS[6:8]),
              ("Supportable claim", "The strongest claim that every\nrequired check allows", [])]
    heights = [0.12, 0.24, 0.24, 0.20, 0.12]
    gap = 0.02
    y = 1.0
    for (title, q, chips), h in zip(blocks, heights):
        y0 = y - h
        ax.add_patch(FancyBboxPatch((0.02, y0), 0.96, h, boxstyle="round,pad=0,rounding_size=0.03",
                                    fc="#f0f0f0" if chips else "#ffffff", ec=LINE, lw=EW))
        ax.text(0.06, y - 0.020, title, fontsize=6.5, fontweight="semibold", color=K, va="top")
        ax.text(0.06, y - 0.046, q, fontsize=5.6, color=GREY, va="top", linespacing=1.25)
        if title == "Comparison evidence":
            ax.text(0.95, y - 0.026, "transfer claims only", fontsize=5.2, color=GREY, va="top", ha="right",
                    style="italic")
        cy = y - 0.137
        for c in chips:
            ax.add_patch(FancyBboxPatch((0.06, cy - 0.016), 0.88, 0.031,
                                        boxstyle="round,pad=0,rounding_size=0.012", fc="#ffffff", ec=LINE, lw=0.35))
            ax.text(0.09, cy - 0.0005, c, fontsize=5.6, color=K, va="center")
            cy -= 0.038
        if title != "Supportable claim":
            ax.add_patch(Polygon([(0.475, y0 - 0.004), (0.525, y0 - 0.004), (0.5, y0 - gap + 0.004)],
                                 closed=True, fc=K, ec="none"))
        y = y0 - gap

    # B: traffic-light assessment
    ax = fig.add_axes([0.375, 0.0, 0.625, 0.92])
    nr, nc = len(ROWS), len(CHECKS)
    ax.set_xlim(-5.3, nc + 4.9); ax.set_ylim(nr + 2.95, -2.25); ax.axis("off")
    ptitle(fig, 0.37, 0.955, "B", "Evidence profiles of the two pipelines")
    for name, a, b in LAYERS:
        ax.plot([a + 0.1, b - 0.1], [-1.25, -1.25], color=K, lw=0.5)
        ax.text((a + b) / 2, -1.38, name, ha="center", va="bottom", fontsize=6.0, color=K)
    for j in range(nc):
        ax.text(j + 0.5, -0.62, f"D{j + 1}", ha="center", va="center", fontsize=6.0, color=K, fontweight="semibold")
    ax.text(nc + 0.4, -0.62, "Supportable claim", ha="left", va="center", fontsize=6.0, color=K,
            fontweight="semibold")
    ax.plot([-5.3, nc + 4.9], [-0.18, -0.18], color=K, lw=0.5)
    for i, (rname, codes) in enumerate(zip(ROWS, R)):
        yy = i + 0.5
        ax.text(-5.25, yy, rname, ha="left", va="center", fontsize=6.0, color=K)
        for j, c in enumerate(codes):
            if c == "x":
                ax.scatter([j + 0.5], [yy], s=118, marker="o", facecolors=NA, edgecolors="#777777",
                           linewidths=0.4, linestyle=(0, (2, 1.5)))
                continue
            ax.scatter([j + 0.5], [yy], s=135, marker="o", facecolors=FILL[c], edgecolors=LINE, linewidths=EW,
                       zorder=2)
            ax.text(j + 0.5, yy + 0.03, SYM[c], ha="center", va="center", fontsize=7.4,
                    color="white" if c == "a" else K,
                    fontweight="semibold", zorder=3)
        ax.text(nc + 0.4, yy, CLAIM[i], ha="left", va="center", fontsize=5.8, color=K)
        if i == 2:
            ax.plot([-5.3, nc + 4.9], [i + 1, i + 1], color="#a0a0a0", lw=0.35)
    ax.plot([-5.3, nc + 4.9], [nr + 0.04, nr + 0.04], color=K, lw=0.5)
    for j, nm in enumerate(CHECKS):
        col, row = divmod(j, 4)
        ax.text(-5.25 + col * 6.6, nr + 0.6 + row * 0.40, f"D{j + 1}", fontsize=5.6, color=K, va="center",
                fontweight="semibold")
        ax.text(-5.25 + col * 6.6 + 0.62, nr + 0.6 + row * 0.40, nm, fontsize=5.6, color=K, va="center")
    pos = [(-5.25, 0), (-2.1, 0), (1.3, 0), (-5.25, 1), (-2.1, 1), (1.3, 1)]
    for (c, lab), (x, row) in zip(LEG, pos):
        yy = nr + 2.3 + row * 0.42
        if c == "x":
            ax.scatter([x + 0.18], [yy], s=40, facecolors=NA, edgecolors="#777777", linewidths=0.5,
                       linestyle=(0, (2, 1.5)))
        else:
            ax.scatter([x + 0.18], [yy], s=45, facecolors=FILL[c], edgecolors=LINE, linewidths=0.4, zorder=2)
            ax.text(x + 0.18, yy + 0.02, SYM[c], ha="center", va="center", fontsize=5.2, fontweight="semibold",
                    color="white" if c == "a" else K, zorder=3)
        ax.text(x + 0.46, yy, lab, fontsize=5.6, color=K, va="center")
    ax.text(4.6, nr + 2.3, "*Ratings rest on counts transcribed from project records.", fontsize=5.4, color=GREY,
            va="center")
    save(fig, "Figure1")


# ------------------------------------------------------------------ Figure 2
def figure2():
    fig = plt.figure(figsize=(180 * MM, 132 * MM))
    ax = fig.add_axes([0.1, 0.6350, 0.26, 0.2800])
    ptitle(fig, 0.0, 0.965, "A", "Case 1: allocation of the 17 patients")
    rows = [("Supplied partition", CASE1["supplied"]), ("Repair 1", CASE1["repair1"]), ("Repair 2", CASE1["repair2"])]
    cols = [("both", "In both sets", NOT), ("train_only", "Development only", TINT1),
            ("val_only", "Validation only", TINT3)]
    for i, (nm, d) in enumerate(rows):
        x = 0
        for k, lab, c in cols:
            v = d[k]
            if v:
                ax.barh(i, v, left=x, height=0.56, color=c, edgecolor=LINE, lw=EW)
                ax.text(x + v / 2, i, str(v), ha="center", va="center", fontsize=6.2, color="white" if c == TINT3 else K)
            x += v
    ax.set_yticks(range(3)); ax.set_yticklabels([r[0] for r in rows]); ax.invert_yaxis()
    ax.set_xlim(0, 17); ax.set_xticks([0, 5, 10, 15, 17]); ax.set_xlabel("Patients")
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    hs = [Rectangle((0, 0), 1, 1, fc=c, ec=LINE, lw=EW) for _, _, c in cols]
    fig.legend(hs, [l for _, l, _ in cols], ncol=3, frameon=False, loc="lower left", bbox_to_anchor=(0.0, 0.49),
               handlelength=1.0, handleheight=0.9, columnspacing=1.0, handletextpad=0.4)

    ax = fig.add_axes([0.43, 0.6350, 0.15, 0.2800])
    ptitle(fig, 0.405, 0.965, "B", "Reported accuracy")
    acc = [CASE1["supplied"]["accuracy"], None, CASE1["repair2"]["accuracy"]]
    for i, a in enumerate(acc):
        if a is None:
            ax.text(0.5, i, "Not estimable: no\ncutting-class clips\nin validation", ha="center", va="center",
                    fontsize=5.6, color=K, linespacing=1.15)
        else:
            ax.plot(a, i, "s", ms=4.2, color=K)
            ax.text(a, i - 0.30, mid(a * 100, 1) + "%", ha="center", va="bottom", fontsize=6.0, color=K)
    ax.set_ylim(2.5, -0.5); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlim(0, 1.05); ax.set_xticks([0, 0.5, 1]); ax.set_xticklabels(["0", "50", "100"])
    ax.set_xlabel("Accuracy (%)")
    ax.text(0.758, 2.36, "726 clips", ha="center", va="bottom", fontsize=5.4, color=GREY)

    ax = fig.add_axes([0.665, 0.6350, 0.33, 0.2800])
    ptitle(fig, 0.645, 0.965, "C", "Case 2: exact-content audit of 781 external image records")
    single = ARCHIVE["records"] - (ARCHIVE["dup_groups"] + ARCHIVE["repeated"])
    rep_cross = ARCHIVE["cross_records"] - ARCHIVE["cross_groups"]
    rep_within = ARCHIVE["repeated"] - rep_cross
    cats = [("Unique image, single record", single, TINT1),
            ("First record of a duplicated image", ARCHIVE["dup_groups"], TINT2),
            ("Repeat, group within one prefix", rep_within, PART),
            ("Repeat, group spanning prefixes", rep_cross, NOT)]
    assert sum(c[1] for c in cats) == ARCHIVE["records"]
    ncol = 40; k = 0
    for nm, n, c in cats:
        for _ in range(n):
            r, q = divmod(k, ncol)
            ax.add_patch(Rectangle((q, -r), 0.86, 0.86, fc=c, ec=LINE, lw=0.12))
            k += 1
    nrow = int(np.ceil(k / ncol))
    ax.set_xlim(-0.2, ncol); ax.set_ylim(-nrow - 0.2, 1.0); ax.set_aspect("equal", anchor="N"); ax.axis("off")
    hs = [Rectangle((0, 0), 1, 1, fc=c, ec=LINE, lw=EW) for _, _, c in cats]
    fig.legend(hs, [f"{nm} ({n})" for nm, n, _ in cats], frameon=False, loc="lower left",
               bbox_to_anchor=(0.645, 0.475), ncol=2, handlelength=1.0, handleheight=0.9, columnspacing=0.8,
               handletextpad=0.4, fontsize=5.6)

    # D–E: near-duplicate keyframes in a public benchmark (Endoscapes test split, CC BY-NC-SA 4.0)
    import pandas as pd
    from PIL import Image
    root = os.path.join(ENDO, "test")
    adjacent, cross = load_distances(os.path.join(REPO, "data", "public", "distance_histograms.json"))
    thr = np.percentile(cross, 0.1)
    pairs = [("167_14450.jpg", "167_14575.jpg", 29), ("170_53175.jpg", "170_53300.jpg", 32)]
    ptitle(fig, 0.0, 0.445, "D", "Public benchmark: keyframes 5 s apart in one operation")
    w, h, x0, y0, gap = 0.205, 0.165, 0.0, 0.245, 0.012
    for r, (fa, fb, d) in enumerate(pairs):
        for c, fn in enumerate((fa, fb)):
            axi = fig.add_axes([x0 + c * (w + gap), y0 - r * (h + 0.03), w, h])
            if os.path.exists(os.path.join(root, fn)):
                axi.imshow(Image.open(os.path.join(root, fn)).convert("RGB"))
            else:
                axi.text(0.5, 0.5, fn + "\n(set ENDOSCAPES_ROOT)", ha="center", va="center", fontsize=5, transform=axi.transAxes)
            axi.set_xticks([]); axi.set_yticks([])
            for sp in axi.spines.values():
                sp.set_visible(True); sp.set_linewidth(0.4); sp.set_color(K)
            axi.text(0.02, 0.96, ("t" if c == 0 else "t + 5 s"), transform=axi.transAxes, fontsize=5.8, color="white",
                     va="top", ha="left", fontweight="semibold")
        fig.text(x0 + 2 * w + gap + 0.006, y0 - r * (h + 0.03) + h / 2, f"Distance\n{d}", fontsize=5.6, color=K,
                 va="center", linespacing=1.2)
    ax = fig.add_axes([0.565, 0.085, 0.42, 0.31])
    ptitle(fig, 0.53, 0.445, "E", "Image distance of keyframe pairs")
    bins = np.arange(0, 141, 4)
    ax.hist(cross, bins=bins, density=True, color=TINT1, edgecolor=LINE, lw=0.35, label="Different operations (20 000 random pairs)")
    ax.hist(adjacent, bins=bins, density=True, histtype="step", color=K, lw=0.9, label=f"Adjacent keyframes, same operation (n={len(adjacent)})")
    k = int((adjacent < thr).sum())
    ax.set_ylim(0, ax.get_ylim()[1] * 1.45)
    ax.plot([thr, thr], [0, ax.get_ylim()[1] * 0.62], color=K, lw=0.6, ls=(0, (3, 2)))
    ax.text(2, ax.get_ylim()[1] * 0.76, f"Left of dashed line: {k} of {len(adjacent)}\nadjacent pairs ({mid(100 * k / len(adjacent), 1)}%), closer\nthan 99·9% of pairs from\ndifferent operations",
            ha="left", va="top", fontsize=5.6, color=K, linespacing=1.2)
    ax.set_xlabel("Difference-hash distance (bits of 256)"); ax.set_ylabel("Density")
    ax.set_xlim(0, 140); ax.set_yticks([])
    ax.legend(frameon=False, loc="upper left", fontsize=5.6, handlelength=1.4, bbox_to_anchor=(0.0, 1.0))
    save(fig, "Figure2")


# ------------------------------------------------------------------ Figure 3
def figure3():
    import json
    import pandas as pd
    from PIL import Image, ImageDraw
    fig = plt.figure(figsize=(180 * MM, 138 * MM))
    names = [f[0] for f in FIRING]

    # A: archived output rates
    ptitle(fig, 0.0, 0.965, "A", "Archived output rate at two confidence thresholds")
    for p, (thr, iz, im, x0) in enumerate(((0.05, 1, 2, 0.11), (0.25, 3, 4, 0.33))):
        ax = fig.add_axes([x0, 0.66, 0.19, 0.25])
        for i, f in enumerate(FIRING):
            ax.plot([f[im], f[iz]], [i, i], color=K, lw=0.5, zorder=1)
            ax.plot(f[iz], i, "o", ms=4.0, mfc=K, mec=K, mew=0.5, zorder=2)
            ax.plot(f[im], i, "o", ms=4.0, mfc="white", mec=K, mew=0.7, zorder=3)
        ax.set_ylim(len(FIRING) - 0.5, -0.5)
        ax.set_yticks(range(len(FIRING))); ax.set_yticklabels(names if p == 0 else [])
        ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
        ax.set_xlim(-2, 100); ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xlabel("Frames with an output (%)")
        ax.set_title("Confidence ≥" + mid(thr, 2), fontsize=6.2, color=K, pad=4)
    ax.plot([], [], "o", mfc=K, mec=K, ms=4, label="Zhuhai (source)")
    ax.plot([], [], "o", mfc="white", mec=K, ms=4, label="Macau (target)")
    fig.legend(*ax.get_legend_handles_labels(), frameon=False, loc="lower left", bbox_to_anchor=(0.11, 0.535), ncol=2,
               handletextpad=0.3)

    # B: source adequacy
    ax = fig.add_axes([0.70, 0.70, 0.28, 0.17])
    ptitle(fig, 0.60, 0.965, "B", "Source-site adequacy (case 2)")
    pts = [("15-class re-training", SOURCE["recon15_ap50"]), ("2-class recovered", SOURCE["twoclass_ap50"])]
    for i, (nm, v) in enumerate(pts):
        ax.plot(v, i, "s", ms=4.2, mfc=K, mec=K)
        ax.text(v, i - 0.32, mid(v, 3) if v > 0.001 else "<0·001", fontsize=5.8, color=K, va="bottom", ha="center")
    ax.set_xscale("log"); ax.set_xlim(1e-5, 2); ax.set_xticks([1e-4, 1e-2, 1])
    ax.set_xticklabels(["0·0001", "0·01", "1"]); ax.minorticks_off()
    ax.set_ylim(1.6, -0.8); ax.set_yticks(range(2)); ax.set_yticklabels([p[0] for p in pts])
    ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
    ax.set_xlabel("Conditional source-test AP50 (log scale)")
    fig.text(0.60, 0.93, "Archived mAP50 0·316 not plotted: model and test set not retained", fontsize=5.4,
             color=GREY, va="top")

    # C: sparse clinical annotation (Zhuhai archive), D: exhaustive public annotation (Endoscapes)
    ptitle(fig, 0.0, 0.475, "C", "Clinical annotation: sparse polygons and lines")
    stem = CLIN
    if stem and os.path.exists(stem + ".jpg"):
        im = Image.open(stem + ".jpg").convert("RGB")
        J = json.load(open(stem + ".json", encoding="utf-8"))
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
        for sh in J["shapes"]:
            pts_ = [tuple(map(float, q)) for q in sh["points"]]
            t = sh.get("shape_type")
            if t == "polygon":
                dr.polygon(pts_, fill=(251, 227, 140, 95), outline=(251, 227, 140, 255))
            elif t in ("linestrip", "line"):
                dr.line(pts_, fill=(120, 200, 255, 255), width=7)
            elif t == "rectangle":
                dr.rectangle([pts_[0], pts_[1]], outline=(244, 120, 100, 255), width=6)
        im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB").crop((0, 60, 1920, 1080))
    else:
        im = Image.new("RGB", (1920, 1020), (235, 235, 235))
    axi = fig.add_axes([0.0, 0.225, 0.30, 0.215]); axi.set_anchor("N"); axi.imshow(im); axi.set_xticks([]); axi.set_yticks([])
    for sp in axi.spines.values():
        sp.set_visible(True); sp.set_linewidth(0.4); sp.set_color(K)
    hs = [Rectangle((0, 0), 1, 1, fc="#fbe38c", ec="#c9a227", lw=0.5),
          mpl.lines.Line2D([0], [0], color="#78c8ff", lw=1.6), Rectangle((0, 0), 1, 1, fc="none", ec="#f47864", lw=1)]
    fig.legend(hs, ["Polygon (partial region)", "Line or line strip", "Box (instrument tip)"], frameon=False, ncol=2,
               loc="lower left", bbox_to_anchor=(0.0, 0.155), fontsize=5.6, handlelength=1.2, columnspacing=0.8,
               handletextpad=0.4)

    ptitle(fig, 0.325, 0.475, "D", "Public reference: structures outlined in full")
    eroot = ENDO
    fn = "176_12425"
    if os.path.exists(os.path.join(eroot, "test", fn + ".jpg")):
        im = Image.open(os.path.join(eroot, "test", fn + ".jpg")).convert("RGB")
        m = np.array(Image.open(os.path.join(eroot, "semseg", fn + ".png")))
    else:
        im = Image.new("RGB", (854, 480), (235, 235, 235)); m = np.zeros((480, 854), np.uint8)
    pal = {1: (120, 190, 110), 2: (245, 205, 70), 3: (230, 110, 90), 4: (90, 140, 200), 5: (170, 120, 200),
           6: (200, 200, 200)}
    rgba = np.zeros(m.shape + (4,), np.uint8)
    for k, c in pal.items():
        rgba[m == k] = (*c, 150)
    im = Image.alpha_composite(im.convert("RGBA"), Image.fromarray(rgba, "RGBA")).convert("RGB")
    axi = fig.add_axes([0.325, 0.225, 0.30, 0.215]); axi.set_anchor("N"); axi.imshow(im); axi.set_xticks([]); axi.set_yticks([])
    for sp in axi.spines.values():
        sp.set_visible(True); sp.set_linewidth(0.4); sp.set_color(K)
    names_ = ["Cystic plate", "Hepatocystic triangle", "Cystic artery", "Cystic duct", "Gallbladder", "Tool"]
    hs = [Rectangle((0, 0), 1, 1, fc=np.array(pal[k]) / 255, ec=LINE, lw=0.3) for k in range(1, 7)]
    fig.legend(hs, names_, frameon=False, ncol=3, loc="lower left", bbox_to_anchor=(0.325, 0.155), fontsize=5.6,
               handlelength=1.0, handleheight=0.9, columnspacing=0.8, handletextpad=0.4)

    # E: composition of the external (Macau) reference
    ptitle(fig, 0.665, 0.475, "E", "Case 2 external reference standard")
    panels = [(0.375, "Images", [(MACAU["annotated_images"], TINT3), (MACAU["unique_images"] - MACAU["annotated_images"], "#ffffff")], 500),
              (0.265, "Shapes", [(MACAU["mappable_polygons"], TINT2), (MACAU["polygons"] - MACAU["mappable_polygons"], TINT1),
                                 (MACAU["line_strips"], "#ffffff"), (MACAU["lines"], "#f2f2f2")], 550)]
    for y0, unit, segs, xmax in panels:
        ax = fig.add_axes([0.72, y0, 0.265, 0.055])
        x = 0
        for v, c in segs:
            ax.barh(0, v, left=x, height=0.8, color=c, edgecolor=LINE, lw=EW)
            ax.text(x + v / 2, 0, str(v), ha="center", va="center", fontsize=5.6, color="white" if c == TINT3 else K)
            x += v
        ax.set_xlim(0, xmax); ax.set_ylim(-0.6, 0.6); ax.set_yticks([0]); ax.set_yticklabels([unit])
        ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
        ax.set_xticks([0, 100, 200, 300, 400, 500]); ax.tick_params(axis="x", labelsize=5.6)
    cs = [TINT3, "#ffffff", TINT2, TINT1, "#ffffff", "#f2f2f2"]
    labs = ["Annotated image", "Unannotated image", "Polygon, detector class", "Polygon, other label",
            "Line strip", "Line"]
    hs = [Rectangle((0, 0), 1, 1, fc=c, ec=LINE, lw=EW) for c in cs]
    fig.legend(hs, labs, frameon=False, loc="lower left", bbox_to_anchor=(0.665, 0.12), ncol=2, fontsize=5.6,
               handlelength=1.0, handleheight=0.9, columnspacing=0.8, handletextpad=0.4)
    save(fig, "Figure3")


def figure4():
    import pandas as pd
    C = pd.read_csv(os.path.join(REPO, "data", "published_studies", "consensus.csv"), dtype=str).set_index("study_id")
    S = pd.read_csv(os.path.join(REPO, "data", "published_studies", "sample.csv"), dtype=str).set_index("study_id")
    Dc = [f"D{i}" for i in range(1, 9)]
    order = ["m", "p", "n", "r", "a", "x"]
    lab = dict(m="Met", p="Partly met", n="Not met", r="Not reported", a="Not assessable", x="Not applicable")
    fig = plt.figure(figsize=(180 * MM, 150 * MM))
    # A: summary
    ax = fig.add_axes([0.20, 0.72, 0.52, 0.22])
    ptitle(fig, 0.0, 0.965, "A", f"Published external validations (n={len(C)}): rating of each check")
    for i, d in enumerate(Dc):
        left = 0
        for c in order:
            v = 100 * (C[d] == c).mean()
            if v:
                ax.barh(i, v, left=left, height=0.62, color=FILL[c] if c != "x" else "#ffffff", edgecolor=LINE, lw=EW)
                left += v
    ax.set_yticks(range(8)); ax.set_yticklabels([f"D{i + 1}  {n}" for i, n in enumerate(CHECKS)])
    ax.invert_yaxis(); ax.set_xlim(0, 100); ax.set_xticks([0, 25, 50, 75, 100]); ax.set_xlabel("Studies (%)")
    ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
    hs = [Rectangle((0, 0), 1, 1, fc=FILL[c] if c != "x" else "#ffffff", ec=LINE, lw=EW) for c in order]
    ax.legend(hs, [lab[c] for c in order], frameon=False, loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=5.8,
              handlelength=1.0, handleheight=0.9)
    # B: per-study traffic light
    ax = fig.add_axes([0.0, 0.0, 1.0, 0.62])
    ptitle(fig, 0.0, 0.625, "B", "Rating of each study")
    n = len(C)
    ax.set_xlim(-3.4, 8 + 4.2); ax.set_ylim(n + 0.3, -1.4); ax.axis("off")
    for j, d in enumerate(Dc):
        ax.text(j + 0.5, -0.75, d, ha="center", va="center", fontsize=6.0, fontweight="semibold", color=K)
    ax.text(8.55, -0.75, "External as\ndefined", ha="center", va="center", fontsize=5.6, fontweight="semibold", linespacing=1.1)
    ax.text(9.85, -0.75, "Claim\nsupported", ha="center", va="center", fontsize=5.6, fontweight="semibold", linespacing=1.1)
    ax.plot([-3.4, 10.6], [-0.2, -0.2], color=K, lw=0.5)
    for i, sid in enumerate(C.index):
        yy = i + 0.4
        ax.text(-3.35, yy, S.loc[sid, "short"].replace(" 2021a", " 2021 (a)").replace(" 2021b", " 2021 (b)").replace("Laplante 2022", "Laplante 2023").replace("Jaspers 2024", "Jaspers 2025"),
                ha="left", va="center", fontsize=5.8, color=K)
        for j, d in enumerate(Dc):
            c = C.loc[sid, d]
            if c == "x":
                ax.scatter([j + 0.5], [yy], s=52, facecolors=NA, edgecolors="#777777", linewidths=0.5, linestyle=(0, (2, 1.5)))
                continue
            ax.scatter([j + 0.5], [yy], s=60, facecolors=FILL[c], edgecolors=LINE, linewidths=EW, zorder=2)
            ax.text(j + 0.5, yy + 0.03, SYM[c], ha="center", va="center", fontsize=6.0, fontweight="semibold",
                    color="white" if c == "a" else K, zorder=3)
        for x, val in ((8.55, C.loc[sid, "external_as_defined"]), (9.85, C.loc[sid, "claim_supported"])):
            ax.text(x, yy, "Yes" if val == "yes" else "No", ha="center", va="center", fontsize=5.8,
                    color=K if val == "yes" else GREY, fontweight="semibold" if val == "yes" else "normal")
    ax.plot([-3.4, 10.6], [n - 0.15, n - 0.15], color=K, lw=0.5)
    ax.text(-3.35, n + 0.15, "Full citations of the 19 studies, and the evidence behind each rating, are given in the appendix (pp 15–17).",
            fontsize=5.4, color=GREY, va="top")
    save(fig, "Figure4")


def figure_s1():
    fig, ax = plt.subplots(figsize=(80 * MM, 62 * MM))
    r = np.linspace(0, 1, 201)
    ax.plot(r * 100, r * 100, color=K, lw=0.9, label="Check needing one field per record: r")
    ax.plot(r * 100, r ** 2 * 100, color=K, lw=0.9, ls=(0, (3, 1.6)), label="Exact duplicate-pair check: r²")
    ax.set_xlabel("Records retaining the required field, r (%)"); ax.set_ylabel("Checks still possible (%)")
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.set_aspect("equal")
    ax.legend(frameon=False, loc="upper left", fontsize=5.8)
    save(fig, "FigureS1")


if __name__ == "__main__":
    figure1(); figure2(); figure3(); figure4(); figure_s1()
    print("written to", OUT)
