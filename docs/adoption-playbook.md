# Adoption Playbook

Use this playbook to promote Question to Prompt Pack without over-explaining it.

## Positioning

Primary message:

```text
Turn rough questions into concise prompt packs and safe Codex skill routes.
```

Chinese message:

```text
把大白话问题变成可执行提示词包，并在需要时安全路由到合适的 Codex skill。
```

Do not position it as a generic prompt optimizer. The stronger claim is:

```text
Use the smallest frame that prevents misunderstanding.
```

## Target Users

| Segment | Pain | Demo to show |
|---|---|---|
| Researchers and students | Rough ideas become unfocused AI answers | Research MVP or weekly research plan |
| Codex/Cursor power users | Many skills, unclear entry point | "Which skill should handle this?" |
| Skill authors | Need better examples, routing, and validation | Benchmark + quality check workflow |
| Teams testing AI workflows | Need safer remote discovery | Metadata-only GitHub discovery |

## Launch Checklist

- Pin the repository and add topics: `codex`, `skills`, `prompt-engineering`, `ai-workflow`, `routing`.
- Create a release with the current validation output.
- Include one GIF or short screen recording showing a rough request becoming a prompt pack.
- Post one English and one Chinese launch note.
- Ask early users for one realistic benchmark case, not broad praise.

## 7-Day Promotion Plan

| Day | Action | Output |
|---:|---|---|
| 1 | Publish release and pin repo | Release notes + README link |
| 2 | Share 30-second demo | Short post with before/after |
| 3 | Ask for benchmark cases | GitHub issue template link |
| 4 | Share safety model | Metadata-only discovery explanation |
| 5 | Share researcher workflow demo | Chinese/English example |
| 6 | Share skill-author demo | How to add a benchmark and validate |
| 7 | Summarize feedback | New cases, fixes, next release plan |

## Post Templates

### English

```text
I built Question to Prompt Pack, a Codex skill that turns rough requests into the smallest useful prompt pack, then routes to another skill only when needed.

It is not a "make my prompt longer" tool. The rule is: use the smallest frame that prevents misunderstanding.

Demo:
{before}
-> {after}

Repo: {url}
```

### Chinese

```text
我做了一个 Codex skill：Question to Prompt Pack。

它不是把 prompt 写长，而是把大白话问题先压缩成最小必要协作框架，再判断是直接回答、追问、生成提示词，还是路由到合适的 skill。

核心规则：用最小的框架，避免最大的误解。

示例：
{before}
-> {after}

仓库：{url}
```

## Success Metrics

- Stars and installs are useful, but not enough.
- Better early metric: number of realistic benchmark cases contributed by users.
- Best signal: users say it reduced clarification turns or routed to the right skill faster.
