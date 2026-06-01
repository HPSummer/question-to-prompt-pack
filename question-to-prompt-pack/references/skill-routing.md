# Skill Routing

This reference keeps routing detail outside `SKILL.md`. Load it only when the user asks for routing behavior, GitHub discovery, registry maintenance, or debugging route quality.

## Route Record

Compact index records should include:

```json
{
  "id": "question-to-prompt-pack",
  "name": "question-to-prompt-pack",
  "description": "Short trigger description from SKILL.md",
  "source": "local | github | local-review",
  "path_or_url": "local path or GitHub URL",
  "domains": ["planning"],
  "task_types": ["planning"],
  "trigger_phrases": [],
  "tools_required": [],
  "risk_level": "low | review | high",
  "trust_level": "trusted | review | unknown",
  "summary": "sub-500 character routing summary",
  "last_seen": "ISO timestamp"
}
```

## Trust Levels

- `trusted`: local installed skill, official source, or user-approved source.
- `review`: known source or changed skill needing inspection.
- `unknown`: discovered but not reviewed.

The registry is a routing index, not a safety guarantee.

## Risk Levels

- `low`: instruction-only skill with no obvious execution or credential risk.
- `review`: mentions shell commands, package installs, network access, downloads, auth, or file mutation.
- `high`: asks for secrets, credentials, API keys, auth/access tokens, private keys, passwords, or bypassing approvals.

Do not mark normal context-budget terms such as "token budget" or "save tokens" as high risk unless they refer to authentication tokens.

## Routing Policy

Default output:

```text
Route:
- Task type:
- Best skill:
- Why:
- Confidence:
- Next action:
```

Rules:

- Search compact metadata first.
- Show at most 5 candidate summaries.
- Load references only after selecting a skill.
- Load zero or one full `SKILL.md` by default.
- Use multiple skills only when the task clearly has independent phases.
- If no suitable skill is found, answer directly or ask one clarification question.

## GitHub Discovery

Discovery updates an index. It must not auto-install or auto-run skills.

Pipeline:

```text
discover repo/path
-> find SKILL.md files
-> parse name and description
-> create compact registry record
-> assign trust/risk
-> mark as review unless source is trusted
-> never auto-install
```

Commands:

```powershell
python .\question-to-prompt-pack\scripts\discover_skill_metadata.py --repo https://github.com/openai/skills --out skill-index.review.json
python .\question-to-prompt-pack\scripts\discover_skill_metadata.py --path .\some-skills-repo --out skill-index.review.json
```

Use discovery summaries only. Do not paste large search results into chat.
