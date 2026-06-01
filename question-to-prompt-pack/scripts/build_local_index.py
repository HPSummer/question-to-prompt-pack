from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


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


def unique(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        normalized = item.strip().lower()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        out.append(normalized)
    return out


def infer_task_types(description: str) -> list[str]:
    desc = description.lower()
    mapping = {
        "coding": ["code", "repo", "debug", "refactor", "test", "build", "cursor", "代码", "调试", "测试", "开发"],
        "research": ["research", "paper", "literature", "citation", "evidence", "科研", "论文", "文献"],
        "writing": ["write", "edit", "translate", "polish", "document", "写作", "润色", "翻译"],
        "video": ["video", "storyboard", "voiceover", "subtitle", "youtube", "视频", "分镜", "字幕"],
        "image": ["image", "figure", "plot", "visual", "diagram", "图片", "图像", "绘图"],
        "data": ["data", "spreadsheet", "csv", "database", "pdf", "数据", "表格"],
        "automation": [
            "automation",
            "reminder",
            "monitor",
            "schedule",
            "cron",
            "periodic",
            "daily",
            "weekly",
            "discovery",
            "自动化",
            "提醒",
            "监控",
            "每天",
            "每日",
            "每周",
            "定期",
            "发现",
            "检查",
        ],
        "planning": ["plan", "decision", "learning", "task", "roadmap", "规划", "计划", "任务"],
    }
    found = []
    for task_type, words in mapping.items():
        if any(word in desc for word in words):
            found.append(task_type)
    return found or ["general"]


def risk_level(text: str) -> str:
    lower = text.lower()
    high = [
        "secret",
        "credential",
        "api key",
        "private key",
        "password",
        "bypass approval",
        "disable security",
        "api token",
        "access token",
        "auth token",
        "secret token",
    ]
    review = ["shell", "command", "install", "auth", "download", "execute", "network", "subprocess", "curl"]
    if any(word in lower for word in high):
        return "high"
    return "review" if any(word in lower for word in review) else "low"


def infer_trigger_phrases(name: str, description: str) -> list[str]:
    phrases = [name]
    quoted = re.findall(r"`([^`]{3,60})`", description)
    phrases.extend(quoted)
    for pattern in [r"use when ([^.]+)", r"when the user ([^.]+)", r"用于([^。]+)"]:
        phrases.extend(match.strip() for match in re.findall(pattern, description, flags=re.I))
    return unique(phrases)[:12]


def infer_tools(text: str) -> list[str]:
    tools = []
    lower = text.lower()
    mapping = {
        "python": ["python", ".py"],
        "node": ["node", "npm", "javascript", "typescript"],
        "matlab": ["matlab", ".m"],
        "github": ["github", "gh ", "git "],
        "browser": ["browser", "playwright", "selenium"],
        "shell": ["shell", "powershell", "bash", "command"],
    }
    for tool, needles in mapping.items():
        if any(needle in lower for needle in needles):
            tools.append(tool)
    return tools


def build_index(skills_dir: Path) -> list[dict]:
    records = []
    now = datetime.now(timezone.utc).isoformat()
    for skill_md in sorted(skills_dir.glob("**/SKILL.md")):
        if ".git" in skill_md.parts or "__pycache__" in skill_md.parts:
            continue
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        name = fm.get("name") or skill_md.parent.name
        description = fm.get("description", "")
        task_types = infer_task_types(description)
        records.append(
            {
                "id": name,
                "name": name,
                "description": description,
                "source": "local",
                "path_or_url": str(skill_md.parent),
                "domains": task_types,
                "task_types": task_types,
                "trigger_phrases": infer_trigger_phrases(name, description),
                "tools_required": infer_tools(text),
                "risk_level": risk_level(text),
                "trust_level": "trusted",
                "summary": description[:500],
                "last_seen": now,
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills-dir", default=str(Path.home() / ".codex" / "skills"))
    parser.add_argument("--out", default="skill-index.json")
    args = parser.parse_args()

    index = build_index(Path(args.skills_dir))
    Path(args.out).write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(index)} skill records to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
