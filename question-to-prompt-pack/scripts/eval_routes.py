from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


CONFIDENCE = {"low": 0, "medium": 1, "high": 2}


def default_cases() -> list[dict]:
    return [
        {
            "id": "video-001",
            "query": "make an explainer video with subtitles",
            "expected_task_type": "video",
            "expected_best_skill": "seedance-2-pro-video",
            "min_confidence": "high",
        },
        {
            "id": "prompt-001",
            "query": "把我的大白话问题转成一个更清晰的提示词",
            "expected_task_type": "planning",
            "expected_best_skill": "question-to-prompt-pack",
            "min_confidence": "high",
        },
        {
            "id": "matlab-001",
            "query": "review this MATLAB control code",
            "expected_task_type": "coding",
            "expected_best_skill": "matlab-review-code",
            "min_confidence": "high",
        },
        {
            "id": "ambiguous-001",
            "query": "help me with this",
            "expected_task_type": "general",
            "expected_best_skill": None,
            "min_confidence": "low",
        },
    ]


def load_cases(path: Path | None) -> list[dict]:
    if path is None:
        return default_cases()
    cases = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            cases.append(json.loads(stripped))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
    return cases


def run_case(index: Path, query: str) -> dict:
    script = Path(__file__).with_name("search_skill_index.py")
    command = [sys.executable, str(script), query, "--index", str(index), "--format", "json"]
    completed = subprocess.run(command, check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return json.loads(completed.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate routing quality on a tiny benchmark.")
    parser.add_argument("--index", required=True)
    parser.add_argument("--cases", help="JSONL benchmark file. Defaults to built-in smoke cases.")
    parser.add_argument("--report", help="Optional JSON report path.")
    args = parser.parse_args()
    index = Path(args.index)
    cases = load_cases(Path(args.cases) if args.cases else None)

    failures = []
    report = []
    for case in cases:
        result = run_case(index, case["query"])
        case_id = case.get("id", case["query"])
        if result.get("task_type") != case["expected_task_type"]:
            failures.append(
                f"{case_id}: task_type {result.get('task_type')!r} != {case['expected_task_type']!r}"
            )
        if result.get("best_skill") != case["expected_best_skill"]:
            failures.append(
                f"{case_id}: best_skill {result.get('best_skill')!r} != {case['expected_best_skill']!r}"
            )
        if CONFIDENCE[result.get("confidence", "low")] < CONFIDENCE[case["min_confidence"]]:
            failures.append(f"{case_id}: confidence {result.get('confidence')!r} < {case['min_confidence']!r}")
        report.append(
            {
                "id": case_id,
                "query": case["query"],
                "expected_task_type": case["expected_task_type"],
                "actual_task_type": result.get("task_type"),
                "expected_best_skill": case["expected_best_skill"],
                "actual_best_skill": result.get("best_skill"),
                "confidence": result.get("confidence"),
            }
        )

    if args.report:
        Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if failures:
        print("Route evaluation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Route evaluation passed for {len(cases)} cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
