"""Exact and near-duplicate audit of a public surgical-video dataset across its official splits.

Usage:
  python public_duplicate_audit.py NAME SPLITS_CSV OUT_DIR [--workers 8]

SPLITS_CSV has columns: path, split, video   (one row per image; video = source video or procedure id)

Outputs (small text files):
  NAME_exact.csv     exact (SHA-256) duplicate groups: size, splits involved, videos involved
  NAME_near.csv      cross-split near-duplicate pairs by 64-bit difference hash, counted at Hamming distance 0..8
  NAME_summary.json  headline counts
Images are read only on this computer; nothing is uploaded.
"""
import argparse
import hashlib
import json
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from PIL import Image


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    with Image.open(path) as im:
        g = np.asarray(im.convert("L").resize((9, 8), Image.BILINEAR), dtype=np.int16)
    bits = (g[:, 1:] > g[:, :-1]).flatten()
    return h.hexdigest(), int(np.packbits(bits).view(">u8")[0])


POP = np.array([bin(i).count("1") for i in range(256)], dtype=np.uint8)


def hamming(a, b):
    """a: (n,) uint64, b: (m,) uint64 -> (n,m) distances"""
    x = np.bitwise_xor(a[:, None], b[None, :])
    return POP[x.view(np.uint8).reshape(x.shape + (8,))].sum(-1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name"); ap.add_argument("splits"); ap.add_argument("out")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    S = pd.read_csv(a.splits)
    with ProcessPoolExecutor(a.workers) as ex:
        res = list(ex.map(digest, S.path, chunksize=64))
    S["sha256"] = [r[0] for r in res]; S["dhash"] = np.array([r[1] for r in res], dtype=np.uint64)

    g = S.groupby("sha256")
    ex_rows = []
    for h, d in g:
        if len(d) > 1:
            ex_rows.append(dict(sha256=h, size=len(d), splits="|".join(sorted(d.split.unique())),
                                videos="|".join(sorted(map(str, d.video.unique()))), cross_split=d.split.nunique() > 1,
                                cross_video=d.video.nunique() > 1))
    E = pd.DataFrame(ex_rows); E.to_csv(os.path.join(a.out, f"{a.name}_exact.csv"), index=False)

    splits = sorted(S.split.unique()); near = []
    for i in range(len(splits)):
        for j in range(i + 1, len(splits)):
            A = S[S.split == splits[i]]; B = S[S.split == splits[j]]
            hb = B.dhash.to_numpy(np.uint64); counts = np.zeros(9, int)
            for k in range(0, len(A), 2000):
                D = hamming(A.dhash.to_numpy(np.uint64)[k:k + 2000], hb)
                for t in range(9):
                    counts[t] += int((D <= t).sum())
            near.append(dict(split_a=splits[i], split_b=splits[j], **{f"pairs_hamming_le_{t}": int(counts[t]) for t in range(9)}))
    pd.DataFrame(near).to_csv(os.path.join(a.out, f"{a.name}_near.csv"), index=False)
    summ = dict(dataset=a.name, images=len(S), unique_sha256=int(S.sha256.nunique()),
                exact_groups=int(len(E)), exact_groups_cross_split=int(E.cross_split.sum()) if len(E) else 0,
                exact_groups_cross_video=int(E.cross_video.sum()) if len(E) else 0,
                videos=int(S.video.nunique()), splits={s: int((S.split == s).sum()) for s in splits})
    json.dump(summ, open(os.path.join(a.out, f"{a.name}_summary.json"), "w"), indent=1)
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
