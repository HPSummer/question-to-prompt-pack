from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


CONFIDENCE = {"low": 0, "medium": 1, "high": 2}
INTERNAL_ROUTING_SKILLS = {"question-to-prompt-pack", "skill-router-registry"}


def default_cases() -> list[dict]:
    return [
        {
            "id": "video-001",
            "query": "make an explainer video with subtitles",
            "expected_task_type": "video",
            "expected_best_skill": "seedance-2-pro-video",
            "min_confidence": "medium",
        },
        {
            "id": "prompt-001",
            "query": "把我的大白话问题转成一个更清晰的提示词",
            "expected_task_type": "planning",
            "expected_route_required": False,
            "min_confidence": "low",
        },
        {
            "id": "matlab-001",
            "query": "review this MATLAB control code",
            "expected_task_type": "coding",
            "expected_best_skill_any": ["matlab", "matlab-review-code", "matlab-agentic-toolkit:matlab-review-code"],
            "min_confidence": "medium",
        },
        {
            "id": "ambiguous-001",
            "query": "help me with this",
            "expected_task_type": "general",
            "expected_route_required": False,
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


def expected_skills(case: dict) -> list[str] | None:
    if "expected_best_skill_any" in case:
        return list(case["expected_best_skill_any"])
    if "expected_best_skill" in case:
        value = case["expected_best_skill"]
        return [value] if value is not None else []
    return None


def route_required(result: dict) -> bool:
    best_skill = result.get("best_skill")
    if not best_skill or best_skill in INTERNAL_ROUTING_SKILLS:
        return False
    return CONFIDENCE.get(result.get("confidence", "low"), 0) >= CONFIDENCE["medium"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate routing quality on benchmark cases.")
    parser.add_argument("--index", required=True)
    parser.add_argument("--cases", help="JSONL benchmark file. Defaults to built-in smoke cases.")
    parser.add_argument("--report", help="Optional JSON report path.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on any checked mismatch.")
    args = parser.parse_args()
    index = Path(args.index)
    cases = load_cases(Path(args.cases) if args.cases else None)

    failures = []
    report = []
    checked = {"task_type": 0, "best_skill": 0, "route_required": 0, "confidence": 0}
    passed = {"task_type": 0, "best_skill": 0, "route_required": 0, "confidence": 0}

    for case in cases:
        result = run_case(index, case["query"])
        case_id = case.get("id", case["query"])

        if "expected_task_type" in case:
            checked["task_type"] += 1
            ok = result.get("task_type") == case["expected_task_type"]
            passed["task_type"] += int(ok)
            if not ok:
                failures.append(f"{case_id}: task_type {result.get('task_type')!r} != {case['expected_task_type']!r}")

        skills = expected_skills(case)
        if skills is not None:
            checked["best_skill"] += 1
            actual = result.get("best_skill")
            ok = actual in skills
            passed["best_skill"] += int(ok)
            if not ok:
                failures.append(f"{case_id}: best_skill {actual!r} not in {skills!r}")

        if "expected_route_required" in case:
            checked["route_required"] += 1
            actual_required = route_required(result)
            ok = actual_required == case["expected_route_required"]
            passed["route_required"] += int(ok)
            if not ok:
                failures.append(
                    f"{case_id}: route_required {actual_required!r} != {case['expected_route_required']!r}"
                )

        if "min_confidence" in case:
            checked["confidence"] += 1
            ok = CONFIDENCE.get(result.get("confidence", "low"), 0) >= CONFIDENCE[case["min_confidence"]]
            passed["confidence"] += int(ok)
            if not ok:
                failures.append(f"{case_id}: confidence {result.get('confidence')!r} < {case['min_confidence']!r}")

        report.append(
            {
                "id": case_id,
                "query": case["query"],
                "expected_task_type": case.get("expected_task_type"),
                "actual_task_type": result.get("task_type"),
                "expected_best_skill": skills,
                "actual_best_skill": result.get("best_skill"),
                "expected_route_required": case.get("expected_route_required"),
                "actual_route_required": route_required(result),
                "confidence": result.get("confidence"),
            }
        )

    if args.report:
        Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Route evaluation checked {len(cases)} cases.")
    for key in ["task_type", "best_skill", "route_required", "confidence"]:
        total = checked[key]
        if total:
            print(f"- {key}: {passed[key]}/{total}")

    if failures:
        print("Route evaluation mismatches:")
        for failure in failures[:30]:
            print(f"- {failure}")
        if len(failures) > 30:
            print(f"- ... {len(failures) - 30} more")
        return 1 if args.strict else 0

    print("Route evaluation passed for all checked expectations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
