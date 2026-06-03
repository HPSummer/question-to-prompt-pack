from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_PROFILE = {
    "version": "1.0",
    "language": "zh-CN",
    "tone": "direct",
    "answer_structure": "tiny-frame-first",
    "depth": "tiny",
    "default_frame": "tiny",
    "common_domains": [],
    "recurring_constraints": ["avoid overthinking", "save tokens"],
    "verification_level": "normal",
    "dislikes": ["long generic coaching"],
    "routing_preference": {
        "prompting": "question-to-prompt-pack"
    },
}


ALLOWED_DEPTH = {"tiny", "normal", "deep", "training"}
ALLOWED_FRAME = {"tiny", "compact", "full", "direct"}
ALLOWED_VERIFICATION = {"low", "normal", "high"}


def default_profile_path(base: Path) -> Path:
    return base / ".question-to-prompt-pack" / "user-style-profile.json"


def load_profile(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_profile(profile: dict) -> list[str]:
    problems = []
    if profile.get("depth") not in ALLOWED_DEPTH:
        problems.append("depth must be one of tiny, normal, deep, training")
    if profile.get("default_frame") not in ALLOWED_FRAME:
        problems.append("default_frame must be one of tiny, compact, full, direct")
    if profile.get("verification_level") not in ALLOWED_VERIFICATION:
        problems.append("verification_level must be one of low, normal, high")
    for key in ["common_domains", "recurring_constraints", "dislikes"]:
        if not isinstance(profile.get(key, []), list):
            problems.append(f"{key} must be a list")
    if not isinstance(profile.get("routing_preference", {}), dict):
        problems.append("routing_preference must be an object")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or validate a question-to-prompt-pack user style profile.")
    parser.add_argument("--path", help="Profile path. Defaults to .question-to-prompt-pack/user-style-profile.json")
    parser.add_argument("--init", action="store_true", help="Create profile if missing")
    parser.add_argument("--validate", action="store_true", help="Validate profile")
    parser.add_argument("--base", default=".", help="Base directory for default profile path")
    args = parser.parse_args()

    path = Path(args.path) if args.path else default_profile_path(Path(args.base))

    if args.init:
        if path.exists():
            print(f"Profile already exists: {path}")
        else:
            profile = dict(DEFAULT_PROFILE)
            profile["updated_at"] = datetime.now(timezone.utc).isoformat()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"Wrote profile: {path}")

    if args.validate:
        if not path.exists():
            print(f"Profile missing: {path}")
            return 1
        problems = validate_profile(load_profile(path))
        if problems:
            print("Profile validation failed:")
            for problem in problems:
                print(f"- {problem}")
            return 1
        print(f"Profile validation passed: {path}")

    if not args.init and not args.validate:
        parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
