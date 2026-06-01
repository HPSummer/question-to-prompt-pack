# Question to Prompt Pack

> Turn rough questions into concise collaboration frames and copyable prompts.

Question to Prompt Pack is a Codex skill for improving user-AI communication. It does not simply make prompts longer. It helps an AI quickly decide whether to answer directly, ask a clarifying question, show a compact collaboration frame, or generate a full prompt pack.

中文说明见 [README.zh-CN.md](README.zh-CN.md).

## Why This Exists

Many prompt tools over-expand simple requests. This skill is designed around one rule:

```text
Use the smallest frame that prevents misunderstanding.
```

It helps with:

- turning plain-language questions into structured prompts
- avoiding overthinking and token waste
- showing a concise, user-editable interpretation before execution
- preserving the user's natural style
- adapting to thread-level preferences through lightweight feedback

## Core Behaviors

- `Tiny Frame`: default for simple requests
- `Compact Frame`: when the user wants to inspect the AI's understanding
- `Full Frame`: when the task is complex or needs assumptions and quality criteria
- `Training Frame`: when the user wants coaching on how to ask better
- `Direct Execution`: when the user says to just do the task

## Example

User:

```text
Use $question-to-prompt-pack, save tokens:
Turn this into a better prompt: help me plan tomorrow.
```

Expected style:

```text
I understand this as:
- Goal: create a practical plan for tomorrow
- Missing/assumed context: assume work + personal tasks
- Best output: time blocks + top priorities
- Mode: tiny prompt rewrite

Draft prompt:
Help me plan tomorrow with time blocks, top 3 priorities, realistic breaks, and a fallback version if the day gets busy. Ask up to 3 questions first only if needed.

Say "expand" if you want the full collaboration frame.
```

## Installation

Copy the skill folder into your Codex skills directory:

```powershell
Copy-Item -LiteralPath .\question-to-prompt-pack -Destination "$env:USERPROFILE\.codex\skills\question-to-prompt-pack" -Recurse -Force
```

Then restart or refresh Codex so the skill list is reloaded.

## Validate

Run the bundled rule check:

```powershell
python .\question-to-prompt-pack\scripts\check_skill_rules.py
```

If you have the system skill creator available, also run:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .\question-to-prompt-pack
```

## Repository Layout

```text
question-to-prompt-pack/
  SKILL.md
  agents/openai.yaml
  references/
    collaboration-frame.md
    golden-examples.md
    interactive-workflow.md
    prompt-pack-patterns.md
    test-cases.md
  scripts/
    check_skill_rules.py
```

## License

MIT. See [LICENSE](LICENSE).
