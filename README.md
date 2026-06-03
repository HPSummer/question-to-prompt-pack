# Question to Prompt Pack

> One unified entry point: understand a rough question, generate a concise prompt pack, then route the task to the right Codex skill.

Question to Prompt Pack is a Codex skill for improving user-AI communication. It does not simply make prompts longer. It helps an AI quickly decide whether to answer directly, ask a clarifying question, show a compact collaboration frame, generate a full prompt pack, or route the task to the best skill for execution.

中文说明见 [README.zh-CN.md](README.zh-CN.md).

## Why This Exists

Many prompt tools over-expand simple requests. This skill is designed around one rule:

```text
Use the smallest frame that prevents misunderstanding.
```

Unified chain:

```text
rough user question
-> question-to-prompt-pack aligns intent
-> built-in skill routing selects a skill
-> selected skill executes the task
-> feedback updates prompt/routing preference
```

It helps with:

- turning plain-language questions into structured prompts
- avoiding overthinking and token waste
- showing a concise, user-editable interpretation before execution
- deciding which Codex skill should execute the task
- teaching one reusable questioning pattern when useful
- preserving non-sensitive collaboration preferences in a local profile
- preserving the user's natural style
- adapting to thread-level preferences through lightweight feedback

## Core Behaviors

- `Tiny Frame`: default for simple requests
- `Compact Frame`: when the user wants to inspect the AI's understanding
- `Full Frame`: when the task is complex or needs assumptions and quality criteria
- `Training Frame`: when the user wants coaching on how to ask better
- `Skill Route`: when a specialized skill should execute the framed task
- `Direct Execution`: when the user says to just do the task

## Question Coaching Loop

When the user wants to improve questioning ability, or when a request is missing a high-leverage detail, add a tiny coaching block:

```text
Question upgrade:
- Missing piece:
- Why it matters:
- Reusable pattern:
```

Default pattern:

```text
Goal + context + output format + constraints + execution mode
```

Do not force coaching into ordinary execution requests.

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

Route:
- Task type: planning
- Best skill: none
- Confidence: high
- Next action: answer directly

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
    question-coaching.md
    skill-routing.md
    test-cases.md
    user-style-profile.md
  assets/
    user-style-profile.schema.json
  scripts/
    build_local_index.py
    check_skill_rules.py
    discover_skill_metadata.py
    eval_routes.py
    profile_manager.py
    search_skill_index.py
    validate_unified_cases.py
benchmarks/
  unified-cases.jsonl
```

## Usage

Use it as the only front door:

```text
Use $question-to-prompt-pack:
Understand my rough request, generate a concise prompt pack, choose the best skill, and give the minimum execution plan.

I want to build a personal research productivity MVP.
```

Initialize a local user style profile:

```powershell
python .\question-to-prompt-pack\scripts\profile_manager.py --init --validate
```

Validate the unified benchmark:

```powershell
python .\question-to-prompt-pack\scripts\validate_unified_cases.py --cases .\benchmarks\unified-cases.jsonl
```

## License

MIT. See [LICENSE](LICENSE).
