from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from discover_skill_metadata import merge_records, scan_github
from search_skill_index import route_payload, render_route


DEFAULT_SOURCES = [
    "https://github.com/openai/skills",
    "https://github.com/HPSummer/question-to-prompt-pack",
    "https://github.com/HPSummer/skill-router-registry",
]


def default_cache_path(base: Path) -> Path:
    return base / ".question-to-prompt-pack" / "skill-discovery-cache.json"


def read_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def route_from_records(query: str, records: list[dict], top: int) -> dict:
    return route_payload(query, records, top)


def should_discover(payload: dict, min_confidence: str) -> bool:
    order = {"low": 0, "medium": 1, "high": 2}
    return order.get(payload.get("confidence", "low"), 0) < order[min_confidence]


def installation_hint(best: dict | None) -> str:
    if not best:
        return "No install hint available until a candidate is selected."
    url = best.get("path_or_url", "")
    name = best.get("name", "selected-skill")
    if "raw.githubusercontent.com" in url:
        return (
            "Review the candidate SKILL.md first. If approved, install from the source repository "
            "or copy the reviewed skill folder into your Codex skills directory. "
            f"Candidate: {name}"
        )
    return f"If approved, install or enable {name}; do not auto-run remote code."


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Route from local skills first, then cached discovery, then optional GitHub metadata discovery."
    )
    parser.add_argument("query")
    parser.add_argument("--local-index", default="skill-index.json")
    parser.add_argument("--cache")
    parser.add_argument("--base", default=".")
    parser.add_argument("--source", action="append", help="Approved GitHub repo URL. Can be repeated.")
    parser.add_argument("--discover", action="store_true", help="Allow metadata-only GitHub discovery when local/cache route is weak.")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--min-confidence", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--format", choices=["route", "json"], default="route")
    args = parser.parse_args()

    base = Path(args.base)
    cache_path = Path(args.cache) if args.cache else default_cache_path(base)
    local_records = read_json(Path(args.local_index))
    cache_records = read_json(cache_path)

    route = route_from_records(args.query, merge_records(local_records, cache_records), args.top)
    discovered = []

    if args.discover and should_discover(route, args.min_confidence):
        sources = args.source or DEFAULT_SOURCES
        for source in sources:
            try:
                discovered.extend(scan_github(source, "review", args.limit))
            except Exception as exc:  # noqa: BLE001 - discovery should fail soft.
                print(f"Discovery warning for {source}: {exc}", file=sys.stderr)

        if discovered:
            cache_records = merge_records(cache_records, discovered)
            write_json(cache_path, cache_records)
            route = route_from_records(args.query, merge_records(local_records, cache_records), args.top)

    best = route["results"][0] if route.get("results") else None
    route["discovery"] = {
        "cache_path": str(cache_path),
        "discovered_records": len(discovered),
        "install_guidance": installation_hint(best) if best and best.get("trust_level") != "trusted" else None,
    }

    if args.format == "json":
        print(json.dumps(route, ensure_ascii=False, indent=2))
    else:
        print(render_route(route))
        if route["discovery"]["discovered_records"]:
            print(f"Discovery: cached {route['discovery']['discovered_records']} review records at {cache_path}")
        if route["discovery"]["install_guidance"]:
            print(f"Install guidance: {route['discovery']['install_guidance']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
