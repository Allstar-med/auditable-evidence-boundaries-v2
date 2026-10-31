"""Store distance distributions without image names, frame indices or video identifiers."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def counts(values):
    values = np.asarray(values)
    if values.ndim != 1 or not len(values) or not np.isfinite(values).all():
        raise ValueError("Distances must be a nonempty, finite vector")
    if not np.equal(values, np.floor(values)).all() or ((values < 0) | (values > 256)).any():
        raise ValueError("256-bit hash distances must be integers from 0 to 256")
    return np.bincount(values.astype(int), minlength=257).tolist()


def write_summary(adjacent, cross, output):
    summary = {"hash_bits": 256, "adjacent_counts": counts(adjacent), "cross_counts": counts(cross)}
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def load_distances(path):
    """Expand histograms for statistics and plotting; original pair order is not retained."""
    summary = json.loads(Path(path).read_text(encoding="utf-8"))
    if summary.get("hash_bits") != 256:
        raise ValueError("Expected 256-bit distance histograms")
    result = []
    for key in ("adjacent_counts", "cross_counts"):
        hist = np.asarray(summary[key])
        if hist.shape != (257,) or not np.issubdtype(hist.dtype, np.integer) or (hist < 0).any() or not hist.sum():
            raise ValueError(f"Invalid {key}")
        result.append(np.repeat(np.arange(257), hist))
    return tuple(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("adjacent_csv")
    parser.add_argument("cross_npy")
    parser.add_argument("output_json")
    args = parser.parse_args()
    write_summary(pd.read_csv(args.adjacent_csv)["d"], np.load(args.cross_npy, allow_pickle=False), args.output_json)
