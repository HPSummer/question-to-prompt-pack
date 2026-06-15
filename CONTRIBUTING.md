# Contributing

Thanks for helping improve Question to Prompt Pack. The project stays useful when it remains small, testable, and safe to install.

## What To Improve

- Add realistic benchmark cases in `benchmarks/unified-cases.jsonl`.
- Improve routing behavior in `question-to-prompt-pack/scripts/search_skill_index.py`.
- Tighten trust and discovery rules in `question-to-prompt-pack/references/skill-routing.md`.
- Improve examples in `examples/before-after.md` when they reflect real usage.
- Keep `question-to-prompt-pack/SKILL.md` concise; move detailed guidance to `references/`.

## Quality Bar

Before opening a PR, run:

```bash
python question-to-prompt-pack/scripts/run_quality_checks.py --repo-root .
```

For routing changes, also build an index from your local skills and run a smoke evaluation:

```bash
python question-to-prompt-pack/scripts/build_local_index.py --out skill-index.json
python question-to-prompt-pack/scripts/eval_routes.py --index skill-index.json --strict
```

## Benchmark Case Format

Add one JSON object per line:

```json
{"id":"unified-051","query":"turn this into a launch checklist","expected_frame":"tiny","expected_task_type":"planning","expected_route_required":false,"expected_coaching":"normal","notes":"simple planning prompt"}
```

Use realistic user wording, including short or messy inputs. Do not add cases that require private data or credentials.

## Safety Rules

- Discovery must stay metadata-only: read `SKILL.md`, create review records, never auto-install.
- Do not add scripts that collect secrets, tokens, cookies, or private repository contents.
- Do not make remote GitHub skills trusted by default.
- Keep user profiles local and non-sensitive.

## Pull Request Checklist

- `SKILL.md` still validates and stays under the size limit.
- New cases pass `validate_unified_cases.py`.
- Any routing change includes at least one benchmark or example.
- README examples still match the actual behavior.
