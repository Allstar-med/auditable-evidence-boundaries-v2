"""Tests for the manifest checker."""

import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from validation_integrity_auditor import audit_manifest


class AuditManifestTests(unittest.TestCase):
    def test_rejects_empty_manifest(self):
        rows = pd.DataFrame(columns=["sample_id", "clinical_unit_id", "sha256", "split"])
        with self.assertRaisesRegex(ValueError, "empty"):
            audit_manifest(rows)

    def test_rejects_missing_sha256_instead_of_counting_it_as_duplicate(self):
        rows = pd.DataFrame(
            [
                {"sample_id": "S1", "clinical_unit_id": "U1", "sha256": "0" * 64, "split": "train"},
                {"sample_id": "S2", "clinical_unit_id": "U2", "sha256": None, "split": "validation"},
            ]
        )
        with self.assertRaisesRegex(ValueError, "sha256.*row 2"):
            audit_manifest(rows)

    def test_rejects_missing_clinical_unit_instead_of_silently_omitting_overlap(self):
        rows = pd.DataFrame(
            [
                {"sample_id": "S1", "clinical_unit_id": "U1", "sha256": "0" * 64, "split": "train"},
                {"sample_id": "S2", "clinical_unit_id": None, "sha256": "1" * 64, "split": "validation"},
            ]
        )
        with self.assertRaisesRegex(ValueError, "clinical_unit_id.*row 2"):
            audit_manifest(rows)

    def test_rejects_unknown_split_instead_of_silently_excluding_record(self):
        rows = pd.DataFrame(
            [{"sample_id": "S1", "clinical_unit_id": "U1", "sha256": "0" * 64, "split": "holdout"}]
        )
        with self.assertRaisesRegex(ValueError, "split.*row 1"):
            audit_manifest(rows)

    def test_rejects_malformed_hash_instead_of_treating_it_as_content_digest(self):
        rows = pd.DataFrame(
            [{"sample_id": "S1", "clinical_unit_id": "U1", "sha256": "not-a-hash", "split": "train"}]
        )
        with self.assertRaisesRegex(ValueError, "sha256.*row 1"):
            audit_manifest(rows)

    def test_rejects_blank_sample_id(self):
        rows = pd.DataFrame(
            [{"sample_id": " ", "clinical_unit_id": "U1", "sha256": "0" * 64, "split": "train"}]
        )
        with self.assertRaisesRegex(ValueError, "sample_id.*row 1"):
            audit_manifest(rows)

    def test_hash_comparison_is_case_insensitive(self):
        rows = pd.DataFrame(
            [
                {"sample_id": "S1", "clinical_unit_id": "U1", "sha256": "a" * 64, "split": "train"},
                {"sample_id": "S2", "clinical_unit_id": "U2", "sha256": "A" * 64, "split": "validation"},
            ]
        )
        result = audit_manifest(rows)
        self.assertEqual(result["unique_sha256"], 1)
        self.assertEqual(result["duplicate_records"], 1)

    def test_counts_real_duplicate_and_clinical_overlap(self):
        rows = pd.DataFrame(
            [
                {"sample_id": "S1", "clinical_unit_id": "U1", "sha256": "a" * 64, "split": "train", "source_prefix": "A"},
                {"sample_id": "S2", "clinical_unit_id": "U1", "sha256": "a" * 64, "split": "validation", "source_prefix": "B"},
            ]
        )
        result = audit_manifest(rows)
        self.assertEqual(result["duplicate_records"], 1)
        self.assertEqual(result["duplicate_hash_groups"], 1)
        self.assertEqual(result["cross_prefix_hash_groups"], 1)
        self.assertEqual(result["cross_split_hash_groups"], 1)
        self.assertEqual(result["clinical_unit_overlap_count"], 1)

    def test_same_split_duplicates_are_not_reported_as_cross_split(self):
        rows = pd.DataFrame(
            [
                {"sample_id": "S1", "clinical_unit_id": "U1", "sha256": "a" * 64, "split": "train"},
                {"sample_id": "S2", "clinical_unit_id": "U2", "sha256": "a" * 64, "split": "train"},
            ]
        )
        self.assertEqual(audit_manifest(rows)["cross_split_hash_groups"], 0)


if __name__ == "__main__":
    unittest.main()
