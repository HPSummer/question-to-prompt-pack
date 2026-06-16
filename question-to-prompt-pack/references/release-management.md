# Release Management

Load this only when maintaining, publishing, promoting, or auditing this skill as a GitHub project.

## Release Readiness Checklist

- `SKILL.md` stays concise and passes `scripts/check_skill_rules.py`.
- `agents/openai.yaml` matches the current purpose and default prompt.
- `README.md` and `README.zh-CN.md` show a quick demo, install path, benchmark status, and safety model.
- `examples/before-after.md` includes at least one simple prompt rewrite, one routing example, one ambiguous request, and one high-stakes request.
- `examples/promotion-copy.md` has current launch copy.
- `benchmarks/unified-cases.jsonl` validates with at least 50 cases.
- GitHub discovery remains metadata-only and never auto-installs remote skills.
- `.gitignore` excludes local caches, generated indexes, and Python artifacts.
- CI runs `scripts/run_quality_checks.py`.

## Versioning

Use semantic versioning:

- Patch: documentation, examples, benchmark additions, route tuning with no behavior contract change.
- Minor: new workflow mode, new script, new profile field, or broader discovery behavior.
- Major: changed output contract, changed trust model, or incompatible profile/index schema.

Recommended tag format:

```text
v0.1.0
```

## Release Notes Template

```markdown
## Summary

- 

## Changed

- 

## Validation

- `python question-to-prompt-pack/scripts/run_quality_checks.py --repo-root .`

## Safety

- Discovery remains metadata-only.
- No remote code is installed or executed automatically.
```

## Promotion Checklist

- Pin the quick demo near the top of the repository.
- Use the one-line description: "Turn rough questions into concise prompt packs and safe Codex skill routes."
- Link to before/after examples instead of explaining every mode.
- Mention the trust model: local first, cache second, GitHub metadata-only after approval.
- Show the quality command so users can verify the package themselves.
- Add GitHub topics: `codex`, `skills`, `prompt-engineering`, `ai-workflow`, `routing`.
- Ask users to contribute benchmark cases through the GitHub issue template.
