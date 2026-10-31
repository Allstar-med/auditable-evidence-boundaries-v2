"""Check that the published analytic reference has stable decimal values."""

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "code" / "run_provenance_stress.py"


class ProvenanceStressTests(unittest.TestCase):
    def test_generated_reference_uses_exact_one_decimal_percentages(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            subprocess.run([sys.executable, str(SCRIPT)], cwd=temporary_directory, check=True, capture_output=True)
            with (Path(temporary_directory) / "provenance_stress_reference.csv").open(newline="") as stream:
                rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 10)
        self.assertEqual(rows[2]["duplicate_pair_detectability_reference_pct"], "64.0")
        self.assertEqual(rows[7]["procedure_source_field_retained_pct"], "30.0")
        self.assertEqual(rows[9]["duplicate_pair_detectability_reference_pct"], "1.0")


if __name__ == "__main__":
    unittest.main()
