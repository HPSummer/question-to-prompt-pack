# User Style Profile

Load this reference only when the user asks to remember working style, calibrate repeated behavior, or improve long-term prompt/routing efficiency.

## Purpose

Keep the user's repeated, non-sensitive collaboration preferences explicit and lightweight.

Do not claim permanent memory unless a persistent profile file exists and the user has asked to use it.

## Profile Location

Suggested project-local file:

```text
.question-to-prompt-pack/user-style-profile.json
```

Use the bundled schema:

```text
assets/user-style-profile.schema.json
```

## Update Rules

- One occurrence: treat as an assumption only.
- Repeated occurrence: treat as a working thread preference.
- Explicit confirmation: write or update the profile if the user asks for persistence.
- User correction: override immediately.
- Sensitive data: never store.

## Minimal Profile

```json
{
  "version": "1.0",
  "language": "zh-CN",
  "tone": "direct",
  "answer_structure": "tiny-frame-first",
  "depth": "tiny",
  "default_frame": "tiny",
  "common_domains": ["research", "matlab", "obsidian"],
  "recurring_constraints": ["avoid overthinking", "save tokens"],
  "verification_level": "normal",
  "dislikes": ["long generic coaching"],
  "routing_preference": {
    "prompting": "question-to-prompt-pack"
  }
}
```

## Use In Responses

Apply profile preferences silently unless useful to mention.

When profile affects output, a short note is enough:

```text
Applied profile: concise Chinese, tiny frame first, avoid overthinking.
```

Do not show the full profile unless the user asks.
