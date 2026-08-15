"""Report traceability from selected normative requirements to tests."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "audit" / "spec_coverage.json"
TEST_ROOT = ROOT / "tests"


def test_names() -> set[str]:
    names: set[str] = set()
    for path in TEST_ROOT.glob("test_*.py"):
        names.update(re.findall(r"def (test_[A-Za-z0-9_]+)\(", path.read_text()))
    return names


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min", type=float, default=0.0,
                        help="minimum percentage of requirements marked covered")
    args = parser.parse_args()
    requirements = json.loads(MATRIX.read_text(encoding="utf-8"))["requirements"]
    known_tests = test_names()
    invalid = [
        f"{item['id']}: {test}"
        for item in requirements
        for test in item["tests"]
        if test not in known_tests
    ]
    covered = sum(item["status"] == "covered" for item in requirements)
    percentage = 100 * covered / len(requirements) if requirements else 0.0
    if invalid:
        print("Unknown test references: " + "; ".join(invalid))
        return 1
    print(f"spec_requirements={len(requirements)}")
    print(f"covered={covered}")
    print(f"coverage_percent={percentage:.1f}")
    return 0 if percentage >= args.min else 1


if __name__ == "__main__":
    sys.exit(main())
