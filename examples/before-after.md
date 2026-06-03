# Before / After Demos

These demos show why Question to Prompt Pack is more than a prompt rewriter.

## 1. Rough Planning

Before:

```text
I want to build a personal research productivity MVP.
```

After:

```text
I understand this as:
- Goal: define a small research productivity tool users can build and test quickly
- Missing/assumed context: assume solo researcher, Codex/Cursor development, notes + tasks + papers
- Best output: MVP scope, core workflows, data model, build plan
- Mode: tiny planning + route

Prompt pack:
Help me design a personal research productivity tool MVP. Focus on the minimum usable workflow for capturing research tasks, linking papers/notes, planning weekly execution, and reviewing progress. Output a PRD-style plan with user stories, core screens, data model, implementation phases, and validation checks.

Route:
- Task type: research/planning
- Best skill: research-execution-copilot
- Confidence: medium
- Next action: recommend route, then load selected skill if user confirms
```

## 2. Prompt Rewrite

Before:

```text
help me plan tomorrow
```

After:

```text
Prompt pack:
Help me plan tomorrow with time blocks, the top 3 priorities, realistic breaks, and a fallback version if the day gets busy. Ask up to 3 questions first only if needed.

Route:
- Best skill: none
- Next action: answer directly
```

## 3. Question Coaching

Before:

```text
训练我的提问能力：我该怎么问 AI 做科研任务规划？
```

After:

```text
Question diagnosis:
- Strength: clear goal, wants to improve AI collaboration
- Weak spot: missing research domain, time scale, and expected artifact
- Highest-leverage addition: specify artifact and constraints

Better prompt:
请作为科研任务规划助手，帮我把“低推力轨迹优化”方向的一周科研任务拆成可执行计划。请输出目标、关键文献/代码任务、每日时间块、验证指标和风险项。默认我使用 MATLAB、Python 和 Obsidian。

Reusable pattern:
研究方向 + 时间尺度 + 输出 artifact + 工具约束 + 验证标准
```

## 4. Skill Routing

Before:

```text
review this MATLAB control code
```

After:

```text
I understand this as:
- Goal: review MATLAB control code for correctness and quality
- Missing/assumed context: code file and validation command needed
- Best output: findings + fixes + test suggestions
- Mode: route skill

Route:
- Task type: coding
- Best skill: matlab-review-code
- Confidence: high
- Next action: load MATLAB review skill and inspect the code
```

## 5. Ambiguous Request

Before:

```text
帮我优化一下
```

After:

```text
I need one clarification before optimizing:
What should be optimized: code performance, writing quality, UI, research plan, or prompt clarity?
```

## 6. High-Stakes Decision

Before:

```text
帮我评估这个投资机会
```

After:

```text
I understand this as:
- Goal: evaluate an investment opportunity
- Missing/assumed context: asset, time horizon, risk tolerance, liquidity needs, current data
- Best output: decision framework, risks, verification checklist
- Mode: compact + verification

Prompt pack:
Help me evaluate this investment opportunity using current sources. Ask for the asset, time horizon, risk tolerance, liquidity needs, alternatives, and downside scenario. Output a structured risk/return analysis, key uncertainties, verification checklist, and decision criteria. Do not present this as financial advice.
```

## 7. Research Note

Before:

```text
帮我把一篇论文整理成 Obsidian 文献笔记
```

After:

```text
Prompt pack:
Convert this paper into an Obsidian literature note with YAML frontmatter, summary, methods, key equations, claims/evidence, limitations, related concepts, and [[double links]]. Put it under 02_literature and include tags.

Route:
- Task type: research
- Best skill: literature-review or citation-management
- Confidence: medium
- Next action: choose based on whether source metadata/citations are needed
```

## 8. GitHub Skill Discovery

Before:

```text
每天检查 GitHub 上有没有新的 Codex skills
```

After:

```text
Prompt pack:
Create a safe recurring workflow that checks user-approved GitHub repositories for new or changed SKILL.md files, indexes metadata only, marks unknown skills for review, and summarizes new candidates without installing or executing remote code.

Route:
- Task type: automation
- Best skill: question-to-prompt-pack internal routing/discovery scripts + automation
- Confidence: medium
- Next action: create scheduled discovery only after user approval
```

## 9. Direct Override

Before:

```text
直接把下面的问题改成最终提示词，不要展示框架。
```

After:

```text
{final prompt only}
```

## 10. User Profile

Before:

```text
我希望你以后默认中文、简洁、先给 tiny frame，避免过度思考。
```

After:

```text
Working preference noted for this thread:
- language: zh-CN
- default_frame: tiny
- depth: concise
- dislikes: overthinking

If you want this persisted in the project, I can create .question-to-prompt-pack/user-style-profile.json.
```
