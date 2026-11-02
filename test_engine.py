import json
import subprocess
import sys
import unittest
from pathlib import Path

from engine import evaluate


def example():
    return json.loads(Path(__file__).with_name("example.json").read_text(encoding="utf-8"))


class AcceptanceTests(unittest.TestCase):
    def test_example_cli(self):
        proc = subprocess.run([sys.executable, "cli.py", "example.json"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), evaluate(example()))

    def test_gap_does_not_move_booking(self):
        rows = evaluate(example())
        self.assertEqual([r["status"] for r in rows], ["scheduled","nonexistent","scheduled","excluded"])
        self.assertTrue(rows[0]["utc"].endswith("07:30:00+00:00"))
        self.assertTrue(rows[2]["utc"].endswith("06:30:00+00:00"))

    def test_repeated_hour_uses_explicit_fold(self):
        data = dict(example(), start="2025-11-02T01:30:00", count=1)
        self.assertTrue(evaluate(data)[0]["ambiguous"])
        self.assertIn("05:30",evaluate(data)[0]["utc"])
        self.assertIn("06:30",evaluate(dict(data, ambiguous="later"))[0]["utc"])
