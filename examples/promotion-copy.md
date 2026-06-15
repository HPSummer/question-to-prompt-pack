# Promotion Copy

Use these snippets when sharing Question to Prompt Pack in a README, post, release note, or demo.

## 30-Second Pitch

Question to Prompt Pack is a Codex skill that turns rough user requests into the smallest useful collaboration frame, then routes the task to the right skill only when needed. It is built for people who want better AI communication without bloated prompt templates.

## One-Line Description

Turn rough questions into concise prompt packs and safe Codex skill routes.

## What Makes It Different

- It optimizes for the smallest frame that prevents misunderstanding.
- It can answer directly, clarify, generate a prompt, or route to a skill.
- It uses local skills first and treats GitHub discovery as metadata-only review.
- It preserves the user's natural style instead of forcing a rigid prompt template.
- It includes benchmark cases and CI-friendly validation.

## Demo Prompt

```text
Use $question-to-prompt-pack:
I want to build a personal research productivity MVP, but I do not know how to structure the task.
```

## Expected Demo Output Shape

```text
I understand this as:
- Goal: design a small research productivity MVP
- Missing/assumed context: assume solo researcher, notes + papers + tasks
- Best output: PRD-style build plan
- Mode: tiny planning + route

Prompt pack:
...

Route:
- Task type: research/planning
- Best skill: ...
- Confidence: medium
- Next action: ...
```

## Chinese Pitch

Question to Prompt Pack 是一个 Codex skill：把大白话问题先压缩成最小必要协作框架，再判断是直接回答、追问、生成提示词，还是路由到合适的 skill。它适合想推广可复用 AI 工作流的人，重点不是“把 prompt 写长”，而是减少误解和 token 浪费。
