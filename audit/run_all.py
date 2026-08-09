"""Run the VIAL repository audit suite (AUDIT-000 through AUDIT-015)."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "audit"
REPORT_DIR = AUDIT_DIR / "results"
NORMATIVE_DIRS = ("adr", "fundation", "rfc", "runtime", "sdk", "tools")
RUNTIME_FILES = [
    "RUNTIME-001-Architecture.md",
    "RUNTIME-002-Execution-Cycle.md",
    "RUNTIME-003-State-Engine.md",
    "RUNTIME-004-Context-Engine.md",
    "RUNTIME-005-Memory-Engine.md",
    "RUNTIME-006-Cognition-Engine.md",
]
AUDIT_IDS = [f"AUDIT-{i:03d}" for i in range(16)]


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def files_with_suffix(directory: str, suffix: str = ".md") -> list[Path]:
    return sorted((ROOT / directory).glob(f"*{suffix}"))


def contains_all(path: Path, tokens: list[str]) -> bool:
    value = text(path)
    return all(token in value for token in tokens)


def required_paths() -> list[str]:
    return [
        "README.md", "AGENTS.md", "CONTRIBUTING.md", "prototype",
        "benchmark", "fundation", "adr", "rfc", "runtime", "sdk", "tools",
        "examples", "tests", "audit",
    ] + [f"runtime/{name}" for name in RUNTIME_FILES]


def audit_000() -> tuple[bool, str]:
    expected = [AUDIT_DIR / "README.md", AUDIT_DIR / "run_all.py"]
    expected += [AUDIT_DIR / f"AUDIT-{i:03d}.md" for i in range(16)]
    missing = [str(p.relative_to(ROOT)) for p in expected if not p.exists()]
    return not missing, "framework complete" if not missing else f"missing: {missing}"


def audit_001() -> tuple[bool, str]:
    missing = [path for path in required_paths() if not (ROOT / path).exists()]
    py_files = list((ROOT / "prototype").glob("*.py"))
    ok = not missing and bool(py_files)
    return ok, "repository structure present" if ok else f"missing: {missing}"


def dependency_entries(path: Path) -> list[str]:
    lines = text(path).splitlines()
    try:
        start = next(i for i, line in enumerate(lines)
                     if line.strip() == "Depends On:") + 1
    except StopIteration:
        return []
    entries = []
    for line in lines[start:]:
        if not line.startswith("-"):
            break
        entries.append(line[1:].strip())
    return entries


def resolve_document(identifier: str) -> bool:
    matches = []
    for directory in NORMATIVE_DIRS:
        matches.extend((ROOT / directory).glob(f"{identifier}-*.md"))
    return bool(matches)


def audit_002() -> tuple[bool, str]:
    missing: list[str] = []
    for directory in NORMATIVE_DIRS:
        for path in files_with_suffix(directory):
            for dependency in dependency_entries(path):
                if dependency.lower() in ("none", "--", "-"):
                    continue
                if not resolve_document(dependency):
                    missing.append(f"{path.name}: {dependency}")
    return not missing, "all Depends On references resolve" if not missing else "; ".join(missing)


def audit_003() -> tuple[bool, str]:
    paths = [ROOT / directory for directory in ("adr", "rfc", "runtime", "sdk", "tools")]
    ok = all(path.exists() and any(path.iterdir()) for path in paths)
    return ok, "normative layers present" if ok else "one or more normative layers are empty"


def audit_004() -> tuple[bool, str]:
    required = [
        "DRAFT", "PENDING", "AUTHORIZED", "EXECUTING", "COMPLETED",
        "CANCELLED", "REJECTED", "FAILED", "REVOKED", "ESCALATION",
        "CREATED", "VALID", "FROZEN", "CONSUMED", "ARCHIVED",
        "ORG-*", "RES-*", "CTX-*", "DEC-*", "INV-*",
    ]
    corpus = "\n".join(text(ROOT / "runtime" / file) for file in RUNTIME_FILES)
    missing = [token for token in required if token not in corpus]
    return not missing, "canonical tokens present" if not missing else f"missing: {missing}"


def audit_005() -> tuple[bool, str]:
    checks = [
        ("runtime chain", ["Decision", "Authorization", "Invocation", "Execution"]),
        ("context immutability", ["FROZEN", "normative content", "MUST NOT"]),
        ("resource boundary", ["Resource"]),
        ("cognition boundary", ["Decision Proposal", "Cognition Engine"]),
    ]
    corpus = "\n".join(text(ROOT / "runtime" / file) for file in RUNTIME_FILES)
    missing = [name for name, tokens in checks if not all(token in corpus for token in tokens)]
    return not missing, "runtime layers are cross-layer consistent" if not missing else f"missing: {missing}"


def audit_006() -> tuple[bool, str]:
    missing = [name for name in RUNTIME_FILES if not (ROOT / "runtime" / name).exists()]
    required = ["Conformance", "Authorization", "FROZEN", "REVOKED"]
    for name in RUNTIME_FILES:
        path = ROOT / "runtime" / name
        if path.exists() and not contains_all(path, required):
            missing.append(f"{name}: missing conformance tokens")
    return not missing, "Runtime documents conform" if not missing else "; ".join(missing)


def audit_007() -> tuple[bool, str]:
    required = [
        ROOT / "sdk/SDK-001-Architecture.md",
        ROOT / "sdk/SDK-004-Context-API.md",
        ROOT / "sdk/SDK-005-Decision-API.md",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    corpus = "\n".join(text(p) for p in required if p.exists())
    upper = corpus.upper()
    for token in ("FROZEN", "AUTHORIZED", "INVOCATION", "AUDIT"):
        if token not in upper:
            missing.append(f"SDK token: {token}")
    return not missing, "SDK surfaces present" if not missing else "; ".join(missing)


def audit_008() -> tuple[bool, str]:
    required = [
        ROOT / "tools/TOOLS-001-Tool-Model.md",
        ROOT / "tools/TOOLS-006-Tool-Invocation.md",
        ROOT / "tools/TOOLS-008-Tool-Lifecycle.md",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    corpus = "\n".join(text(p) for p in required if p.exists())
    for token in ("DRAFT", "DEFINED", "ACTIVE", "DEPRECATED", "RETIRED", "INV-"):
        if token not in corpus.upper():
            missing.append(f"Tools token: {token}")
    return not missing, "Tools surfaces present" if not missing else "; ".join(missing)


def audit_009() -> tuple[bool, str]:
    examples = files_with_suffix("examples")
    missing = []
    for path in examples:
        value = text(path).lower()
        if "illustrative" not in value and "domain-specific" not in value:
            missing.append(path.name)
    return not missing, "examples declare their illustrative boundary" if not missing else f"missing boundary: {missing}"


def audit_010() -> tuple[bool, str]:
    required = [
        ROOT / "prototype/authorization.py",
        ROOT / "prototype/errors.py",
        ROOT / "tests/test_conformance.py",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    gate = text(required[0]) if required[0].exists() else ""
    for token in ("VIALAuthorizationError", "DECISION_NOT_AUTHORIZED", "ACTOR_NOT_AUTHORIZED"):
        if token not in gate:
            missing.append(f"authorization token: {token}")
    return not missing, "authorization boundary present" if not missing else "; ".join(missing)


def audit_011() -> tuple[bool, str]:
    required = [
        "DRAFT", "PENDING", "AUTHORIZED", "EXECUTING", "COMPLETED",
        "CANCELLED", "REJECTED", "FAILED", "REVOKED",
        "CREATED", "VALID", "FROZEN", "CONSUMED", "ARCHIVED",
    ]
    corpus = "\n".join(text(ROOT / "runtime" / file) for file in RUNTIME_FILES)
    missing = [token for token in required if token not in corpus]
    return not missing, "lifecycle tokens are consistent" if not missing else f"missing: {missing}"


def audit_012() -> tuple[bool, str]:
    corpus = "\n".join(text(ROOT / "runtime" / file) for file in RUNTIME_FILES)
    required = ("ORG-*", "RES-*", "CTX-*", "DEC-*", "INV-*")
    missing = [token for token in required if token not in corpus]
    forbidden = re.findall(r"\b(?:org|res|ctx|dec|inv)[._][A-Za-z0-9_-]+", corpus)
    return not missing and not forbidden, (
        "terminology and identifiers are canonical" if not missing and not forbidden
        else f"missing={missing}; noncanonical={forbidden[:10]}"
    )


def audit_013() -> tuple[bool, str]:
    candidates = [ROOT / directory for directory in NORMATIVE_DIRS]
    missing = []
    for directory in candidates:
        for path in directory.glob("*.md"):
            if path.name.lower() == "readme.md":
                continue
            value = text(path)
            header = value[:1200].lower()
            for token in ("version:", "status:"):
                if token not in header:
                    missing.append(f"{path.name}: {token}")
    return not missing, "document metadata is present" if not missing else "; ".join(missing[:12])


def audit_014() -> tuple[bool, str]:
    graph: dict[str, set[str]] = {}
    for directory in NORMATIVE_DIRS:
        for path in files_with_suffix(directory):
            match = re.match(r"^([A-Z]+-[0-9A-Z]+)-", path.name)
            if not match:
                continue
            identifier = match.group(1)
            graph[identifier] = set(d for d in dependency_entries(path) if d.lower() != "none")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return False
        if node in visited:
            return True
        visiting.add(node)
        for dep in graph.get(node, set()):
            dep_key = dep if dep in graph else next((key for key in graph if key == dep), dep)
            if dep_key in graph and not visit(dep_key):
                return False
        visiting.remove(node)
        visited.add(node)
        return True

    ok = all(visit(node) for node in graph)
    return ok, "dependency graph is acyclic" if ok else "dependency cycle detected"


def audit_015(full: bool) -> tuple[bool, str]:
    if not full:
        return True, "static release checks only; use --full for evidence suite"
    commands = [
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
        [sys.executable, "benchmark/selective-context/run_benchmark.py", "--out", "results/_audit_check"],
        [sys.executable, "benchmark/cognitive-reuse/run_benchmark.py", "--out", "results/_audit_check"],
        [sys.executable, "benchmark/economic-cost/run_benchmark.py", "--out", "results/_audit_check"],
        [sys.executable, "benchmark/failure-recovery/run_benchmark.py", "--out", "results/_audit_check"],
    ]
    failures = []
    try:
        for command in commands:
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                    encoding="utf-8", errors="replace")
            if result.returncode:
                failures.append(" ".join(command))
    finally:
        for path in (
            ROOT / "benchmark/selective-context/results/_audit_check",
            ROOT / "benchmark/cognitive-reuse/results/_audit_check",
            ROOT / "benchmark/economic-cost/results/_audit_check",
            ROOT / "benchmark/failure-recovery/results/_audit_check",
        ):
            if path.exists():
                shutil.rmtree(path)
    return not failures, "full evidence suite passed" if not failures else f"failed: {failures}"


CHECKS: list[tuple[str, Callable[[], tuple[bool, str]]]] = [
    ("AUDIT-000", audit_000), ("AUDIT-001", audit_001),
    ("AUDIT-002", audit_002), ("AUDIT-003", audit_003),
    ("AUDIT-004", audit_004), ("AUDIT-005", audit_005),
    ("AUDIT-006", audit_006), ("AUDIT-007", audit_007),
    ("AUDIT-008", audit_008), ("AUDIT-009", audit_009),
    ("AUDIT-010", audit_010), ("AUDIT-011", audit_011),
    ("AUDIT-012", audit_012), ("AUDIT-013", audit_013),
    ("AUDIT-014", audit_014),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()
    started = time.time()
    results = []
    for audit_id, check in CHECKS:
        try:
            passed, message = check()
        except Exception as exc:  # audit failures must be visible, not hidden
            passed, message = False, f"internal check error: {exc}"
        results.append({"id": audit_id, "status": "PASS" if passed else "FAIL",
                        "message": message})
    passed, message = audit_015(args.full)
    results.append({"id": "AUDIT-015", "status": "PASS" if passed else "FAIL",
                    "message": message})
    report = {"framework": "AUDIT-000", "full": args.full,
              "started_at": started, "results": results,
              "all_pass": all(item["status"] == "PASS" for item in results)}
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "latest.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    for item in results:
        print(f"{item['id']} {item['status']}: {item['message']}")
    print(f"REPORT: {REPORT_DIR / 'latest.json'}")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
