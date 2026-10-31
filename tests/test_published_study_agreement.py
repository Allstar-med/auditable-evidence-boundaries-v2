"""Tests for the agreement statistics and for the archived published-study tables."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "code" / "published_study_agreement.py"
DATA = ROOT / "data" / "published_studies"

spec = importlib.util.spec_from_file_location("psa", SCRIPT)
psa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(psa)
sys.path.insert(0, str(ROOT / "code"))
from distance_summary import load_distances


class StatisticsTests(unittest.TestCase):
    def test_kappa_perfect_and_chance(self):
        self.assertAlmostEqual(psa.kappa(list("mmnn"), list("mmnn")), 1.0)
        self.assertAlmostEqual(psa.kappa(list("mnmn"), list("mmnn")), 0.0)

    def test_wilson_known_values(self):
        lo, hi = psa.wilson(4, 19)
        self.assertAlmostEqual(lo, 0.0851, places=3)
        self.assertAlmostEqual(hi, 0.4334, places=3)
        lo, hi = psa.wilson(305, 781)
        self.assertAlmostEqual(lo, 0.357, places=3)
        self.assertAlmostEqual(hi, 0.425, places=3)


class InputValidationTests(unittest.TestCase):
    def check_invalid(self, change, message):
        with tempfile.TemporaryDirectory() as tmp:
            tables = [pd.read_csv(DATA / name) for name in ("extraction_1.csv", "extraction_2.csv", "consensus.csv")]
            change(tables)
            paths = [Path(tmp) / f"ratings_{i}.csv" for i in range(3)]
            for table, path in zip(tables, paths):
                table.to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, message):
                psa.load_ratings(*paths)

    def test_missing_study_is_not_silently_dropped(self):
        self.check_invalid(lambda t: t.__setitem__(1, t[1].iloc[1:]), "must match exactly")

    def test_duplicate_study_is_rejected(self):
        self.check_invalid(lambda t: t.__setitem__(0, pd.concat([t[0], t[0].iloc[:1]])), "unique")

    def test_unknown_rating_is_rejected(self):
        self.check_invalid(lambda t: t[0].loc.__setitem__((0, "D1"), "unknown"), "rating code")


class ArchivedTablesTests(unittest.TestCase):
    def test_rerun_reproduces_archived_tables(self):
        with tempfile.TemporaryDirectory() as out:
            subprocess.run([sys.executable, str(SCRIPT), str(DATA / "extraction_1.csv"), str(DATA / "extraction_2.csv"),
                            str(DATA / "consensus.csv"), out], check=True, capture_output=True)
            for name in ("agreement.csv", "prevalence.csv"):
                new = pd.read_csv(Path(out) / name)
                old = pd.read_csv(DATA / name)
                pd.testing.assert_frame_equal(new, old, check_exact=False, atol=1e-9)

    def test_consensus_covers_nineteen_studies(self):
        c = pd.read_csv(DATA / "consensus.csv")
        self.assertEqual(len(c), 19)
        self.assertEqual(int((c.claim_supported == "yes").sum()), 1)


class NearDuplicateTablesTests(unittest.TestCase):
    def test_archived_near_duplicate_result(self):
        import numpy as np
        adjacent, cross = load_distances(ROOT / "data" / "public" / "distance_histograms.json")
        thr = np.percentile(cross, 0.1)
        self.assertEqual(len(cross), 20000)
        self.assertEqual(len(adjacent), 1623)
        self.assertEqual(int((adjacent < thr).sum()), 382)


if __name__ == "__main__":
    unittest.main()
