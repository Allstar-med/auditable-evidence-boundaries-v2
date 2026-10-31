"""Near-duplicate analysis of consecutive Endoscapes test keyframes (reproduces endoscapes_adjacent.csv and cross.npy).

Usage: python endoscapes_near_duplicates.py ENDOSCAPES_TEST_DIR OUT_DIR
Each image is reduced to a 256-bit difference hash (16 x 16 gradient signs of a 17 x 16 greyscale thumbnail).
Distances between consecutive keyframes of the same video are compared with 20 000 random pairs from
different videos (seed 1).
"""
import os
import re
import sys

import numpy as np
import pandas as pd
from PIL import Image
from distance_summary import write_summary

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
rows = []
for f in sorted(x for x in os.listdir(src) if x.endswith(".jpg")):
    v, fr = map(int, re.match(r"(\d+)_(\d+)\.jpg", f).groups())
    g = np.asarray(Image.open(os.path.join(src, f)).convert("L").resize((17, 16), Image.BILINEAR), dtype=np.int16)
    rows.append((f, v, fr, np.packbits((g[:, 1:] > g[:, :-1]).flatten())))
df = pd.DataFrame(rows, columns=["file", "video", "frame", "h"]).sort_values(["video", "frame"]).reset_index(drop=True)
H = np.stack(df.h.values); POP = np.array([bin(i).count("1") for i in range(256)])
dist = lambda a, b: int(POP[np.bitwise_xor(H[a], H[b])].sum())
adj = []
for v, g in df.groupby("video"):
    idx = g.index.values
    for a, b in zip(idx[:-1], idx[1:]):
        adj.append((v, (df.frame[b] - df.frame[a]) / 25, dist(a, b), a, b))
adj = pd.DataFrame(adj, columns=["video", "gap_s", "d", "a", "b"])
rng = np.random.default_rng(1); cross = []
while len(cross) < 20000:
    a, b = rng.integers(0, len(df), 2)
    if df.video[a] != df.video[b]:
        cross.append(dist(a, b))
cross = np.array(cross); thr = np.percentile(cross, 0.1)
adj.to_csv(os.path.join(out, "endoscapes_adjacent.csv"), index=False); np.save(os.path.join(out, "cross.npy"), cross)
df.drop(columns="h").to_csv(os.path.join(out, "endoscapes_files.csv"), index=False)
write_summary(adj.d, cross, os.path.join(out, "distance_histograms.json"))
print(f"{len(df)} keyframes, {df.video.nunique()} videos; threshold {thr}; "
      f"{(adj.d < thr).sum()} of {len(adj)} adjacent pairs below ({100 * (adj.d < thr).mean():.1f}%)")
