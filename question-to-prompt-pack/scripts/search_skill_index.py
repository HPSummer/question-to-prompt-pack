from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path


WORD_RE = re.compile(r"[A-Za-z0-9_\-\u4e00-\u9fff]+")
CONFIDENCE_ORDER = {"low": 0, "medium": 1, "high": 2}
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "for",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "the",
    "this",
    "to",
    "with",
    "帮我",
    "我的",
    "一个",
    "这个",
}

QUERY_ALIASES = {
    "大白话": ["prompt", "question", "framing", "question-to-prompt", "提示词", "提问"],
    "提示词": ["prompt", "question-to-prompt", "framing"],
    "提问": ["question", "prompt", "framing"],
    "问题": ["question", "prompt"],
    "转成": ["convert", "transform"],
    "转换": ["convert", "transform"],
    "科研": ["research", "paper", "literature"],
    "论文": ["paper", "literature", "writing"],
    "文献": ["literature", "citation", "paper"],
    "视频": ["video", "storyboard", "subtitle"],
    "字幕": ["subtitle", "caption", "video"],
    "代码": ["code", "debug", "review"],
    "调试": ["debug", "code"],
    "审查": ["review", "scan"],
    "优化": ["optimize", "improve"],
    "每天": ["daily", "automation", "schedule"],
    "每日": ["daily", "automation", "schedule"],
    "每周": ["weekly", "automation", "schedule"],
    "定期": ["periodic", "automation", "schedule"],
    "发现": ["discovery", "search"],
    "检查": ["monitor", "scan", "review"],
    "图片": ["image", "figure", "visual"],
    "图像": ["image", "figure", "visual"],
    "数据": ["data", "spreadsheet", "database"],
    "写作": ["writing", "draft", "polish"],
}

TASK_KEYWORDS = {
    "coding": [
        "code",
        "repo",
        "debug",
        "bug",
        "refactor",
        "test",
        "build",
        "cursor",
        "codex",
        "react",
        "frontend",
        "webapp",
        "web",
        "dashboard",
        "代码",
        "调试",
        "重构",
        "测试",
        "仓库",
        "开发",
    ],
    "research": [
        "research",
        "paper",
        "literature",
        "citation",
        "evidence",
        "experiment",
        "科研",
        "论文",
        "文献",
        "引用",
        "证据",
        "实验",
    ],
    "writing": ["write", "edit", "translate", "polish", "document", "draft", "写作", "润色", "翻译", "文档"],
    "video": ["video", "storyboard", "voiceover", "subtitle", "youtube", "视频", "分镜", "旁白", "字幕"],
    "image": ["image", "figure", "plot", "visual", "diagram", "图片", "图像", "绘图", "可视化", "图表"],
    "data": ["data", "spreadsheet", "csv", "database", "pdf", "dataset", "数据", "表格", "数据库"],
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
        "定时",
        "每天",
        "每日",
        "每周",
        "定期",
        "发现",
        "检查",
    ],
    "planning": [
        "plan",
        "decision",
        "learning",
        "task",
        "roadmap",
        "prompt",
        "question",
        "framing",
        "规划",
        "计划",
        "决策",
        "学习",
        "任务",
        "提示词",
        "提问",
        "大白话",
    ],
}

FIELD_WEIGHTS = {
    "name": 4.0,
    "description": 2.5,
    "summary": 1.8,
    "domains": 2.0,
    "task_types": 2.5,
    "trigger_phrases": 3.0,
}

DOMAIN_REQUIREMENTS = {
    "matlab": ["matlab", "simulink", "uifigure", "uihtml", ".m", "matlab"],
}


def tokenize(text: str) -> list[str]:
    tokens = [word.lower() for word in WORD_RE.findall(text)]
    return [token for token in tokens if token not in STOPWORDS and len(token) > 1]


def expand_query_tokens(query: str) -> list[str]:
    tokens = tokenize(query)
    lower = query.lower()
    for phrase, aliases in QUERY_ALIASES.items():
        if phrase.lower() in lower:
            tokens.extend(alias.lower() for alias in aliases)
    return tokens


def as_text(value: object) -> str:
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    if isinstance(value, dict):
        return " ".join(str(item) for item in value.values())
    return str(value or "")


def infer_task_type(query: str) -> str:
    expanded = " ".join([query.lower(), *expand_query_tokens(query)])
    hits: dict[str, int] = {}
    for task_type, keywords in TASK_KEYWORDS.items():
        hits[task_type] = sum(1 for word in keywords if word.lower() in expanded)
    best, count = max(hits.items(), key=lambda item: item[1])
    return best if count else "general"


def domain_mismatch_penalty(query: str, record: dict) -> float:
    lower_query = query.lower()
    record_text = (
        as_text(record.get("name"))
        + " "
        + as_text(record.get("description"))
        + " "
        + as_text(record.get("summary"))
    ).lower()
    penalty = 0.0
    for domain, required_markers in DOMAIN_REQUIREMENTS.items():
        if domain in record_text and not any(marker in lower_query for marker in required_markers):
            penalty += 30.0
    return penalty


def route_bonus(query: str, record: dict) -> tuple[float, list[str]]:
    lower_query = query.lower()
    name = as_text(record.get("name")).lower()
    description = as_text(record.get("description")).lower()
    bonus = 0.0
    matches: list[str] = []

    if any(word in lower_query for word in ["react", "frontend", "webapp", "web app"]):
        if name in {"codex-execution-loop", "codex-task-framing"}:
            bonus += 10.0
            matches.append("frontend-generic")

    if "matlab" in lower_query and "matlab" in name:
        bonus += 4.0
        matches.append("explicit-matlab")
        if any(word in lower_query for word in ["审查", "review"]) and "review" in description:
            bonus += 3.0
            matches.append("review-intent")

    return bonus, matches


def weak_generic_penalty(query: str, record: dict, matched: list[str]) -> float:
    lower_query = query.lower()
    name = as_text(record.get("name")).lower()
    description = as_text(record.get("description")).lower()
    weak_tokens = {"build", "task:coding", "task:planning"}
    non_weak = [match for match in matched if match not in weak_tokens]
    if non_weak:
        return 0.0

    if "react" in lower_query or "frontend" in lower_query:
        if not any(word in name + " " + description for word in ["react", "frontend", "webapp", "javascript", "typescript"]):
            return 6.0

    return 0.0


def score(query: str, record: dict) -> tuple[float, list[str]]:
    q_tokens = expand_query_tokens(query)
    if not q_tokens:
        return 0.0, []

    matched: list[str] = []
    score_value = 0.0
    seen: set[tuple[str, str]] = set()

    for field, weight in FIELD_WEIGHTS.items():
        field_text = as_text(record.get(field)).lower()
        if not field_text:
            continue
        field_tokens = set(tokenize(field_text))
        for token in q_tokens:
            if (field, token) in seen:
                continue
            if token in field_tokens or token in field_text:
                seen.add((field, token))
                score_value += weight
                if len(matched) < 5 and token not in matched:
                    matched.append(token)

    task_type = infer_task_type(query)
    record_types = set(tokenize(as_text(record.get("task_types")) + " " + as_text(record.get("domains"))))
    if task_type != "general" and task_type in record_types:
        score_value += 3.0
        matched.append(f"task:{task_type}")

    name = as_text(record.get("name")).lower()
    if name and name in query.lower():
        score_value += 5.0
        matched.append("exact-name")

    if matched:
        trust = as_text(record.get("trust_level")).lower()
        risk = as_text(record.get("risk_level")).lower()
        if trust == "trusted":
            score_value += 0.4
        if risk == "high":
            score_value -= 1.0
        elif risk == "review":
            score_value -= 0.2
        score_value -= domain_mismatch_penalty(query, record)
        score_value -= weak_generic_penalty(query, record, matched)

    bonus, bonus_matches = route_bonus(query, record)
    if bonus:
        score_value += bonus
        matched.extend(match for match in bonus_matches if match not in matched)

    return score_value / math.sqrt(max(len(q_tokens), 1)), matched


def confidence(top_score: float, second_score: float) -> str:
    margin = top_score - second_score
    if top_score >= 4.0 and margin >= 0.7:
        return "high"
    if top_score >= 2.0:
        return "medium"
    return "low"


def next_action(confidence_value: str, best: dict | None) -> str:
    if best is None:
        return "use question-to-prompt-pack or ask one clarification question"
    if confidence_value == "high":
        return f"load only {best.get('name')} and execute the task"
    if confidence_value == "medium":
        return "show the top candidates, recommend one, then load only the selected skill"
    return "ask one clarification question before loading any skill"


def route_payload(query: str, records: list[dict], top: int) -> dict:
    ranked = sorted(((score(query, record), record) for record in records), key=lambda item: item[0][0], reverse=True)
    results = []
    for (score_value, matches), record in ranked[:top]:
        if score_value <= 0:
            continue
        results.append(
            {
                "score": round(score_value, 3),
                "name": record.get("name"),
                "description": record.get("description"),
                "path_or_url": record.get("path_or_url"),
                "trust_level": record.get("trust_level"),
                "risk_level": record.get("risk_level"),
                "task_types": record.get("task_types", []),
                "matches": matches[:6],
            }
        )

    best = results[0] if results else None
    second_score = results[1]["score"] if len(results) > 1 else 0.0
    top_score = best["score"] if best else 0.0
    confidence_value = confidence(top_score, second_score)
    if not best:
        confidence_value = "low"

    return {
        "query": query,
        "task_type": infer_task_type(query),
        "best_skill": best["name"] if best else None,
        "confidence": confidence_value,
        "next_action": next_action(confidence_value, best),
        "results": results,
    }


def render_route(payload: dict) -> str:
    results = payload["results"]
    best = results[0] if results else None
    if not best:
        return "\n".join(
            [
                "Route:",
                f"- Task type: {payload['task_type']}",
                "- Best skill: none",
                "- Why: no indexed skill matched the task metadata",
                f"- Confidence: {payload['confidence']}",
                f"- Next action: {payload['next_action']}",
            ]
        )

    why_parts = []
    if best.get("matches"):
        why_parts.append("matched " + ", ".join(best["matches"][:4]))
    if best.get("trust_level"):
        why_parts.append(f"trust={best['trust_level']}")
    if best.get("risk_level"):
        why_parts.append(f"risk={best['risk_level']}")
    why = "; ".join(why_parts) or "best metadata match"

    lines = [
        "Route:",
        f"- Task type: {payload['task_type']}",
        f"- Best skill: {best['name']}",
        f"- Why: {why}",
        f"- Confidence: {payload['confidence']}",
        f"- Next action: {payload['next_action']}",
    ]

    if payload["confidence"] != "high" and len(results) > 1:
        alternatives = ", ".join(item["name"] for item in results[1:3] if item.get("name"))
        if alternatives:
            lines.append(f"- Alternatives: {alternatives}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--index", default="skill-index.json")
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--format", choices=["route", "json"], default="route")
    args = parser.parse_args()

    records = json.loads(Path(args.index).read_text(encoding="utf-8"))
    payload = route_payload(args.query, records, args.top)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_route(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
