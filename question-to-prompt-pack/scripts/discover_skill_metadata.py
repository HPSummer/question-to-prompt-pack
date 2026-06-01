from __future__ import annotations

import argparse
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
GITHUB_RE = re.compile(r"^https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$")


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def risk_level(text: str) -> str:
    lower = text.lower()
    high = ["secret", "credential", "api key", "private key", "password", "api token", "access token", "auth token"]
    review = ["shell", "command", "install", "auth", "download", "execute", "network", "subprocess", "curl"]
    if any(word in lower for word in high):
        return "high"
    return "review" if any(word in lower for word in review) else "low"


def task_types(description: str) -> list[str]:
    lower = description.lower()
    mapping = {
        "coding": ["code", "repo", "debug", "refactor", "test", "build", "代码", "调试"],
        "research": ["research", "paper", "literature", "citation", "科研", "论文", "文献"],
        "writing": ["write", "edit", "translate", "polish", "document", "写作", "润色"],
        "video": ["video", "storyboard", "voiceover", "subtitle", "视频", "字幕"],
        "image": ["image", "figure", "plot", "visual", "图片", "绘图"],
        "data": ["data", "spreadsheet", "csv", "database", "pdf", "数据"],
        "automation": [
            "automation",
            "reminder",
            "monitor",
            "schedule",
            "periodic",
            "daily",
            "weekly",
            "discovery",
            "自动化",
            "每天",
            "每日",
            "每周",
            "定期",
            "发现",
            "检查",
        ],
        "planning": ["plan", "decision", "learning", "task", "规划", "任务"],
    }
    found = [name for name, words in mapping.items() if any(word in lower for word in words)]
    return found or ["general"]


def record_from_skill(text: str, source: str, path_or_url: str, trust_level: str) -> dict:
    fm = parse_frontmatter(text)
    name = fm.get("name") or Path(path_or_url).parent.name or "unknown-skill"
    description = fm.get("description", "")
    types = task_types(description)
    return {
        "id": name,
        "name": name,
        "description": description,
        "source": source,
        "path_or_url": path_or_url,
        "domains": types,
        "task_types": types,
        "trigger_phrases": [name],
        "tools_required": [],
        "risk_level": risk_level(text),
        "trust_level": trust_level,
        "summary": description[:500],
        "last_seen": datetime.now(timezone.utc).isoformat(),
    }


def scan_local(path: Path, trust_level: str) -> list[dict]:
    records = []
    for skill_md in sorted(path.glob("**/SKILL.md")):
        if ".git" in skill_md.parts or "__pycache__" in skill_md.parts:
            continue
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        records.append(record_from_skill(text, "local-review", str(skill_md.parent), trust_level))
    return records


def github_api_url(repo_url: str) -> str:
    match = GITHUB_RE.match(repo_url)
    if not match:
        raise ValueError("Only repository URLs like https://github.com/owner/repo are supported.")
    owner, repo = match.groups()
    return f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "skill-router-registry"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "skill-router-registry"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def raw_github_url(repo_url: str, skill_path: str) -> str:
    match = GITHUB_RE.match(repo_url)
    if not match:
        raise ValueError("Only repository URLs like https://github.com/owner/repo are supported.")
    owner, repo = match.groups()
    return f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{skill_path}"


def scan_github(repo_url: str, trust_level: str, limit: int) -> list[dict]:
    tree = fetch_json(github_api_url(repo_url))
    skill_paths = [
        item["path"]
        for item in tree.get("tree", [])
        if item.get("type") == "blob" and item.get("path", "").endswith("SKILL.md")
    ][:limit]
    records = []
    for skill_path in skill_paths:
        raw_url = raw_github_url(repo_url, skill_path)
        text = fetch_text(raw_url)
        records.append(record_from_skill(text, "github", raw_url, trust_level))
    return records


def merge_records(existing: list[dict], new_records: list[dict]) -> list[dict]:
    merged = {record.get("id") or record.get("name"): record for record in existing}
    for record in new_records:
        key = record.get("id") or record.get("name")
        if not key:
            continue
        existing_record = merged.get(key)
        if existing_record and existing_record.get("trust_level") == "trusted":
            record["trust_level"] = "review"
        merged[key] = record
    return list(merged.values())


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover SKILL.md metadata without installing or executing skills.")
    parser.add_argument("--repo", help="GitHub repository URL, for example https://github.com/openai/skills")
    parser.add_argument("--path", help="Local directory to scan")
    parser.add_argument("--out", default="skill-index.review.json")
    parser.add_argument("--merge-index", help="Existing registry JSON to merge with")
    parser.add_argument("--trust-level", choices=["review", "unknown"], default="review")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    if bool(args.repo) == bool(args.path):
        raise SystemExit("Provide exactly one of --repo or --path.")

    if args.repo:
        parsed = urlparse(args.repo)
        if parsed.scheme != "https" or parsed.netloc != "github.com":
            raise SystemExit("Only https://github.com repository URLs are supported.")
        records = scan_github(args.repo, args.trust_level, args.limit)
    else:
        records = scan_local(Path(args.path), args.trust_level)

    if args.merge_index and Path(args.merge_index).exists():
        existing = json.loads(Path(args.merge_index).read_text(encoding="utf-8"))
        records = merge_records(existing, records)

    Path(args.out).write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(records)} review records to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
