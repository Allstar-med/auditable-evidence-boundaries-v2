#!/usr/bin/env python3
"""Check split identities and exact file hashes in a CSV manifest.

Written from the recorded study methods; the original source file was unavailable.
No clinical records are included in this script.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
import pandas as pd

REQUIRED = {"sample_id", "clinical_unit_id", "sha256", "split"}
SPLITS = {"train", "validation", "val", "test"}
SHA256_RE = re.compile(r"[0-9a-fA-F]{64}\Z")

def file_sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def audit_manifest(df):
    missing = sorted(REQUIRED-set(df.columns))
    if missing:
        raise ValueError("Missing required columns: "+", ".join(missing))
    if df.empty:
        raise ValueError("Manifest is empty")
    df = df.copy()
    for column in sorted(REQUIRED):
        for row, value in enumerate(df[column], start=1):
            if pd.isna(value) or not str(value).strip():
                raise ValueError(f"Invalid {column} at row {row}: value is missing")
            if column == "sha256" and not SHA256_RE.fullmatch(str(value).strip()):
                raise ValueError(f"Invalid sha256 at row {row}: expected 64 hexadecimal characters")
            if column == "split" and str(value).strip() not in SPLITS:
                raise ValueError(f"Invalid split at row {row}: expected train, validation, val, or test")
        df[column] = df[column].astype(str).str.strip()
    df["sha256"] = df["sha256"].str.lower()
    train=set(df.loc[df["split"].eq("train"),"clinical_unit_id"].dropna().astype(str))
    val=set(df.loc[df["split"].isin(["validation","val","test"]),"clinical_unit_id"].dropna().astype(str))
    overlap=sorted(train & val)
    dup=df.groupby("sha256").size()
    dup_hashes=set(dup[dup>=2].index.astype(str))
    cross_split=int((df.groupby("sha256")["split"].nunique()>1).sum())
    cross=0
    if "source_prefix" in df.columns:
        g=df[df["sha256"].astype(str).isin(dup_hashes)].groupby("sha256")["source_prefix"].nunique()
        cross=int((g>1).sum())
    label_cols=[c for c in df.columns if c.startswith("label_")]
    estimability={}
    for c in label_cols:
        estimability[c]=sorted(df.loc[df["split"].isin(["validation","val","test"]),c].dropna().astype(str).unique().tolist())
    return {
        "records": int(len(df)),
        "unique_sha256": int(df["sha256"].nunique(dropna=True)),
        "duplicate_records": int(len(df)-df["sha256"].nunique(dropna=True)),
        "duplicate_hash_groups": int((dup>=2).sum()),
        "cross_split_hash_groups": cross_split,
        "cross_prefix_hash_groups": cross if "source_prefix" in df.columns else None,
        "clinical_unit_overlap_count": len(overlap),
        "clinical_unit_overlap": overlap,
        "endpoint_support": estimability,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--out", default="audit_result.json")
    args=ap.parse_args()
    df=pd.read_csv(args.manifest, dtype=str)
    result=audit_manifest(df)
    result["manifest_file_sha256"]=file_sha256(args.manifest)
    Path(args.out).write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__":
    main()
