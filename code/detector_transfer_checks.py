"""Case 2 detector checks. Runs on CPU; needs numpy, pandas, pillow.

Inputs
  --pred      CSV of detector outputs, one row per box: image, cls, conf, x1, y1, x2, y2 (pixels, xyxy).
              `image` is the file name (no folder). Include every output down to the confidence floor used.
  --images    folder(s) with the source images, comma-separated (train,val,test folders are fine).
  --labels    folder(s) with YOLO label files (<image stem>.txt; lines "cls cx cy w h", normalised).
  --splits    CSV: image, split  (split in train/val/test/external)
  --ext-json  folder with the external LabelMe-style JSON files (shapes: label, points, shape_type)
  --ext-map   CSV: label, cls    (external polygon label -> detector class id; leave cls empty if unmapped)
  --groups    optional CSV: image, group (patient or procedure) for clustered bootstrap intervals
  --out       output folder

Outputs (all small text files to send back)
  ap_by_split_class.csv      AP50 per class and split (train = positive control), AP at IoU 0.1, class-agnostic AP50
  convention_check.csv       AP50 (test and train) after common box-convention transformations; the largest value
                             should be the "as is" row - if another row is much higher, the pipeline has a bug
  output_rates.csv           output rate per class, site and threshold (0.05, 0.25) for the re-trained model
  external_recall.csv        recall at IoU 0.5 on mappable external polygons (bounding box of each polygon), per class
  summary.json               headline numbers with 95% intervals
  overlays/                  20 random source images with reference (green) and top predictions (red) drawn
"""
import argparse
import glob
import json
import os

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw

THRS = (0.05, 0.25)


def iou_matrix(a, b):
    """a: (n,4), b: (m,4) xyxy"""
    if len(a) == 0 or len(b) == 0:
        return np.zeros((len(a), len(b)))
    x1 = np.maximum(a[:, None, 0], b[None, :, 0]); y1 = np.maximum(a[:, None, 1], b[None, :, 1])
    x2 = np.minimum(a[:, None, 2], b[None, :, 2]); y2 = np.minimum(a[:, None, 3], b[None, :, 3])
    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    aa = (a[:, 2] - a[:, 0]) * (a[:, 3] - a[:, 1]); bb = (b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])
    return inter / (aa[:, None] + bb[None, :] - inter + 1e-12)


def match(pred, gt, thr):
    """Greedy one-to-one matching by confidence within each image (class filtering done by caller).
    Returns arrays conf, tp for predictions, and number of reference objects."""
    confs, tps, npos = [], [], 0
    for img, g in gt.groupby("image"):
        npos += len(g)
    for img, p in pred.groupby("image"):
        p = p.sort_values("conf", ascending=False)
        g = gt[gt.image == img]
        used = np.zeros(len(g), bool)
        I = iou_matrix(p[["x1", "y1", "x2", "y2"]].to_numpy(float), g[["x1", "y1", "x2", "y2"]].to_numpy(float))
        for k in range(len(p)):
            hit = False
            if I.shape[1]:
                cand = np.where(~used & (I[k] >= thr))[0]
                if len(cand):
                    j = cand[np.argmax(I[k, cand])]; used[j] = True; hit = True
            confs.append(p.conf.iloc[k]); tps.append(hit)
    return np.array(confs), np.array(tps, bool), npos


def ap101(conf, tp, npos):
    if npos == 0:
        return np.nan
    if len(conf) == 0:
        return 0.0
    o = np.argsort(-conf); tp = tp[o]
    ctp = np.cumsum(tp); cfp = np.cumsum(~tp)
    rec = ctp / npos; prec = ctp / np.maximum(ctp + cfp, 1)
    prec = np.maximum.accumulate(prec[::-1])[::-1]
    rs = np.linspace(0, 1, 101)
    idx = np.searchsorted(rec, rs, side="left")
    return float(np.mean([prec[i] if i < len(prec) else 0 for i in idx]))


def ap_table(pred, gt, imgs, thr=0.5, agnostic=False):
    pred = pred[pred.image.isin(imgs)]; gt = gt[gt.image.isin(imgs)]
    if agnostic:
        c, t, n = match(pred, gt, thr)
        return {"all": ap101(c, t, n)}
    out = {}
    for k in sorted(set(gt.cls) | set(pred.cls)):
        c, t, n = match(pred[pred.cls == k], gt[gt.cls == k], thr)
        out[int(k)] = ap101(c, t, n)
    return out


def load_yolo(label_dirs, sizes):
    rows = []
    for d in label_dirs:
        for f in glob.glob(os.path.join(d, "*.txt")):
            stem = os.path.splitext(os.path.basename(f))[0]
            img = sizes.get(stem)
            if img is None:
                continue
            name, (W, H) = img
            for line in open(f):
                v = line.split()
                if len(v) < 5:
                    continue
                c, cx, cy, w, h = int(float(v[0])), *map(float, v[1:5])
                rows.append((name, c, (cx - w / 2) * W, (cy - h / 2) * H, (cx + w / 2) * W, (cy + h / 2) * H))
    return pd.DataFrame(rows, columns=["image", "cls", "x1", "y1", "x2", "y2"])


def transforms(pred, sizes_by_name):
    """Common convention errors, applied to the predictions."""
    p = pred.copy()
    W = p.image.map(lambda n: sizes_by_name[n][0]); H = p.image.map(lambda n: sizes_by_name[n][1])
    out = {"as is": p}
    q = p.copy(); q["x2"] = p.x1 + p.x2; q["y2"] = p.y1 + p.y2; out["xywh read as xyxy"] = q
    q = p.copy(); w = p.x2 - p.x1; h = p.y2 - p.y1
    q["x1"] = p.x1 - w / 2; q["y1"] = p.y1 - h / 2; q["x2"] = p.x1 + w / 2; q["y2"] = p.y1 + h / 2; out["centre read as corner"] = q
    q = p.copy(); q[["x1", "x2"]] = p[["x1", "x2"]].mul(W, axis=0); q[["y1", "y2"]] = p[["y1", "y2"]].mul(H, axis=0)
    out["normalised read as pixels"] = q
    q = p.copy(); q["x1"], q["y1"], q["x2"], q["y2"] = p.y1, p.x1, p.y2, p.x2; out["x and y swapped"] = q
    q = p.copy(); q["cls"] = p.cls + 1; out["class index +1"] = q
    q = p.copy(); q["cls"] = p.cls - 1; out["class index -1"] = q
    return out


def wilson(k, n, z=1.96):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def main():
    ap = argparse.ArgumentParser()
    for a in ("--pred", "--images", "--labels", "--splits", "--ext-json", "--ext-map", "--out"):
        ap.add_argument(a, required=a not in ("--ext-json", "--ext-map"))
    ap.add_argument("--groups"); ap.add_argument("--B", type=int, default=2000)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    pred = pd.read_csv(a.pred)
    splits = pd.read_csv(a.splits)
    sizes, sizes_by_name, paths = {}, {}, {}
    for d in a.images.split(","):
        for f in glob.glob(os.path.join(d, "*")):
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                with Image.open(f) as im:
                    wh = im.size
                n = os.path.basename(f); sizes[os.path.splitext(n)[0]] = (n, wh); sizes_by_name[n] = wh; paths[n] = f
    gt = load_yolo(a.labels.split(","), sizes)
    imgs = {s: set(splits[splits.split == s].image) for s in splits.split.unique()}
    print("reference boxes:", len(gt), "predictions:", len(pred), "outputs per image:",
          round(len(pred) / max(pred.image.nunique(), 1), 1))

    # 1. positive control and per-class AP
    rows = []
    for s in ("train", "val", "test"):
        if s not in imgs:
            continue
        for k, v in ap_table(pred, gt, imgs[s]).items():
            n = int(((gt.cls == k) & gt.image.isin(imgs[s])).sum())
            rows.append(dict(split=s, cls=k, n_reference=n, AP50=v, AP10=ap_table(pred[pred.cls == k], gt[gt.cls == k], imgs[s], 0.1).get(k)))
        rows.append(dict(split=s, cls="class-agnostic", n_reference=int(gt.image.isin(imgs[s]).sum()),
                         AP50=ap_table(pred, gt, imgs[s], agnostic=True)["all"], AP10=np.nan))
    apt = pd.DataFrame(rows); apt.to_csv(os.path.join(a.out, "ap_by_split_class.csv"), index=False)

    # 2. convention check
    rows = []
    for name, p in transforms(pred, sizes_by_name).items():
        r = dict(transformation=name)
        for s in ("train", "test"):
            if s in imgs:
                v = [x for x in ap_table(p, gt, imgs[s]).values() if not np.isnan(x)]
                r[f"mAP50_{s}"] = float(np.mean(v)) if v else np.nan
        rows.append(r)
    pd.DataFrame(rows).to_csv(os.path.join(a.out, "convention_check.csv"), index=False)

    # 3. output rates per class and site
    rows = []
    for site, s in (("Zhuhai test", "test"), ("Macau", "external")):
        if s not in imgs:
            continue
        S = imgs[s]; n = len(S)
        for k in sorted(pred.cls.unique()):
            for t in THRS:
                hit = pred[(pred.cls == k) & (pred.conf >= t) & pred.image.isin(S)].image.nunique()
                lo, hi = wilson(hit, n)
                rows.append(dict(site=site, cls=int(k), threshold=t, frames=n, frames_with_output=hit,
                                 rate=hit / n if n else np.nan, lo=lo, hi=hi))
    pd.DataFrame(rows).to_csv(os.path.join(a.out, "output_rates.csv"), index=False)

    # 4. external recall on mappable polygons
    summary = {}
    if a.ext_json and a.ext_map:
        mp = pd.read_csv(a.ext_map).dropna(subset=["cls"]); mp["cls"] = mp.cls.astype(int)
        lab2cls = dict(zip(mp.label, mp.cls))
        ref = []
        for f in glob.glob(os.path.join(a.ext_json, "*.json")):
            J = json.load(open(f, encoding="utf-8"))
            name = os.path.basename(J.get("imagePath", os.path.splitext(os.path.basename(f))[0] + ".png"))
            for sh in J.get("shapes", []):
                if sh.get("shape_type", "polygon") != "polygon" or sh.get("label") not in lab2cls:
                    continue
                pts = np.array(sh["points"], float)
                ref.append((name, lab2cls[sh["label"]], pts[:, 0].min(), pts[:, 1].min(), pts[:, 0].max(), pts[:, 1].max()))
        ref = pd.DataFrame(ref, columns=["image", "cls", "x1", "y1", "x2", "y2"])
        rows = []
        for k, g in ref.groupby("cls"):
            for t in THRS:
                p = pred[(pred.cls == k) & (pred.conf >= t) & pred.image.isin(set(g.image))]
                c, tp, n = match(p, g, 0.5)
                found = int(tp.sum()); lo, hi = wilson(found, n)
                rows.append(dict(cls=int(k), threshold=t, reference_objects=n, matched=found,
                                 recall=found / n if n else np.nan, lo=lo, hi=hi))
        pd.DataFrame(rows).to_csv(os.path.join(a.out, "external_recall.csv"), index=False)
        summary["external_reference_objects"] = int(len(ref))

    # 5. headline with clustered bootstrap over groups for test mAP50
    v = apt[(apt.split == "test") & (apt.cls != "class-agnostic")].AP50.dropna()
    summary["test_mAP50"] = float(v.mean()) if len(v) else None
    vt = apt[(apt.split == "train") & (apt.cls != "class-agnostic")].AP50.dropna()
    summary["train_mAP50_positive_control"] = float(vt.mean()) if len(vt) else None
    if a.groups and "test" in imgs:
        G = pd.read_csv(a.groups); G = G[G.image.isin(imgs["test"])]
        groups = G.group.unique(); rng = np.random.default_rng(20261030); bs = []
        for _ in range(a.B):
            pick = rng.choice(groups, len(groups))
            ims = [];
            for gi, gname in enumerate(pick):
                ims += [(f"{gi}__{x}") for x in G[G.group == gname].image]
            # rename images per draw so repeated groups count separately
            mp_ = {x: x.split("__", 1)[1] for x in ims}
            P = pd.concat([pred[pred.image == mp_[x]].assign(image=x) for x in ims]) if ims else pred.iloc[:0]
            T = pd.concat([gt[gt.image == mp_[x]].assign(image=x) for x in ims]) if ims else gt.iloc[:0]
            vals = [z for z in ap_table(P, T, set(ims)).values() if not np.isnan(z)]
            bs.append(np.mean(vals) if vals else np.nan)
        summary["test_mAP50_95CI_clustered"] = [float(np.nanquantile(bs, 0.025)), float(np.nanquantile(bs, 0.975))]
        summary["test_groups"] = int(len(groups))
    json.dump(summary, open(os.path.join(a.out, "summary.json"), "w"), indent=1)

    # 6. overlays
    od = os.path.join(a.out, "overlays"); os.makedirs(od, exist_ok=True)
    rng = np.random.default_rng(1)
    pool = sorted(imgs.get("test", set()) | imgs.get("train", set()))
    for n in rng.choice(pool, min(20, len(pool)), replace=False):
        if n not in paths:
            continue
        im = Image.open(paths[n]).convert("RGB"); d = ImageDraw.Draw(im)
        for r in gt[gt.image == n].itertuples():
            d.rectangle([r.x1, r.y1, r.x2, r.y2], outline=(0, 200, 0), width=3); d.text((r.x1 + 3, r.y1 + 3), str(r.cls), fill=(0, 200, 0))
        for r in pred[pred.image == n].sort_values("conf", ascending=False).head(10).itertuples():
            d.rectangle([r.x1, r.y1, r.x2, r.y2], outline=(230, 0, 0), width=2)
            d.text((r.x1 + 3, r.y2 - 12), f"{r.cls}:{r.conf:.2f}", fill=(230, 0, 0))
        im.save(os.path.join(od, os.path.splitext(n)[0] + "_overlay.jpg"), quality=85)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
