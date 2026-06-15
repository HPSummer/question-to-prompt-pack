from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(command: list[str], cwd: Path) -> int:
    print("+ " + " ".join(command))
    completed = subprocess.run(command, cwd=str(cwd))
    return completed.returncode


def assert_json(path: Path) -> list[str]:
    problems: list[str] = []
    if not path.exists():
        return problems
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        problems.append(f"{path}: invalid JSON: {exc}")
    return problems


def assert_text_contains(path: Path, needles: list[str]) -> list[str]:
    problems: list[str] = []
    if not path.exists():
        problems.append(f"{path}: file missing")
        return problems
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            problems.append(f"{path}: missing {needle!r}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Run repository quality checks for question-to-prompt-pack.")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--skip-benchmark", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    skill_root = repo_root / "question-to-prompt-pack"
    scripts = skill_root / "scripts"

    checks = [
        ([sys.executable, str(scripts / "check_skill_rules.py")], repo_root),
    ]

    benchmark = repo_root / "benchmarks" / "unified-cases.jsonl"
    if not args.skip_benchmark and benchmark.exists():
        checks.append(
            (
                [
                    sys.executable,
                    str(scripts / "validate_unified_cases.py"),
                    "--cases",
                    str(benchmark),
                    "--min-cases",
                    "50",
                ],
                repo_root,
            )
        )

    failures = 0
    for command, cwd in checks:
        failures += int(run(command, cwd) != 0)

    structural_problems: list[str] = []
    structural_problems.extend(assert_json(repo_root / "sources.example.json"))
    structural_problems.extend(assert_json(skill_root / "assets" / "user-style-profile.schema.json"))
    structural_problems.extend(
        assert_text_contains(
            repo_root / "README.md",
            [
                "metadata-only",
                "Routing Benchmark Snapshot",
                "Skill Discovery and Routing",
            ],
        )
    )
    structural_problems.extend(
        assert_text_contains(
            repo_root / "README.zh-CN.md",
            [
                "metadata-only",
                "Benchmark",
                "Skill 发现与调用",
            ],
        )
    )

    if structural_problems:
        print("Structural checks failed:")
        for problem in structural_problems:
            print(f"- {problem}")
        failures += 1

    if failures:
        print(f"Quality checks failed: {failures}")
        return 1

    print("Quality checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
