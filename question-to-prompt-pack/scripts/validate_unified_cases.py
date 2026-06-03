from __future__ import annotations

import argparse
import json
from pathlib import Path


ALLOWED_FRAMES = {"tiny", "compact", "full", "training", "direct", "clarify"}
ALLOWED_TASK_TYPES = {
    "automation",
    "coding",
    "data",
    "decision",
    "general",
    "image",
    "planning",
    "research",
    "video",
    "writing",
}
ALLOWED_COACHING = {"none", "normal", "training"}
REQUIRED_FIELDS = {
    "id",
    "query",
    "expected_frame",
    "expected_task_type",
    "expected_route_required",
    "expected_coaching",
}


def load_jsonl(path: Path) -> list[dict]:
    cases = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            item = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
        item["_line"] = line_number
        cases.append(item)
    return cases


def validate_case(case: dict) -> list[str]:
    problems = []
    line = case.get("_line", "?")
    missing = REQUIRED_FIELDS - set(case)
    if missing:
        problems.append(f"line {line}: missing fields {sorted(missing)}")
    if case.get("expected_frame") not in ALLOWED_FRAMES:
        problems.append(f"line {line}: invalid expected_frame {case.get('expected_frame')!r}")
    if case.get("expected_task_type") not in ALLOWED_TASK_TYPES:
        problems.append(f"line {line}: invalid expected_task_type {case.get('expected_task_type')!r}")
    if not isinstance(case.get("expected_route_required"), bool):
        problems.append(f"line {line}: expected_route_required must be boolean")
    if case.get("expected_coaching") not in ALLOWED_COACHING:
        problems.append(f"line {line}: invalid expected_coaching {case.get('expected_coaching')!r}")
    query = case.get("query")
    if not isinstance(query, str) or len(query.strip()) < 4:
        problems.append(f"line {line}: query must be a realistic non-empty string")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate unified question-to-prompt benchmark cases.")
    parser.add_argument("--cases", required=True)
    parser.add_argument("--min-cases", type=int, default=10)
    args = parser.parse_args()

    cases = load_jsonl(Path(args.cases))
    problems = []
    if len(cases) < args.min_cases:
        problems.append(f"expected at least {args.min_cases} cases, found {len(cases)}")

    ids = set()
    for case in cases:
        if case.get("id") in ids:
            problems.append(f"line {case.get('_line')}: duplicate id {case.get('id')!r}")
        ids.add(case.get("id"))
        problems.extend(validate_case(case))

    if problems:
        print("Unified benchmark validation failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print(f"Unified benchmark validation passed for {len(cases)} cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
