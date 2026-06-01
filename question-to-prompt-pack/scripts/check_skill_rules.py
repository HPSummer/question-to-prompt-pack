from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED = {
    "SKILL.md": [
        "Hard Trigger Rules",
        "Token Budget Ladder",
        "Tiny Frame",
        "Feedback Loop",
        "Habit Profile",
        "Do not expose hidden chain-of-thought",
    ],
    "references/test-cases.md": [
        "Token-Saving Simple Request",
        "Direct Execution Override",
        "Understanding Confidence",
        "Result Feedback",
    ],
    "references/golden-examples.md": [
        "Tiny Frame",
        "Frame First",
        "Feedback Loop",
    ],
}


def main() -> int:
    missing: list[str] = []
    for rel, needles in REQUIRED.items():
        path = ROOT / rel
        if not path.exists():
            missing.append(f"{rel}: file missing")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                missing.append(f"{rel}: missing {needle!r}")

    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if len(skill_text) > 9000:
        missing.append(f"SKILL.md: too large ({len(skill_text)} chars > 9000)")

    if missing:
        print("Rule check failed:")
        for item in missing:
            print(f"- {item}")
        return 1

    print("Rule check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
