# Question Coaching Loop

Load this reference only when the user wants to improve questioning ability, asks why a prompt was rewritten, or requests training/feedback.

## Purpose

Help users become better at asking AI for work, without turning every request into a lesson.

Default rule:

```text
Teach one reusable questioning move, not a full lecture.
```

## Coaching Output

Use this compact coaching block after the prompt pack only when helpful:

```text
Question upgrade:
- Missing piece:
- Why it matters:
- Reusable pattern:
```

Keep it to 3 bullets. Do not include a score unless the user asks for training, scoring, or deliberate practice.

## Reusable Patterns

### Task Request

```text
Goal + context + output format + constraints + execution mode
```

### Research Request

```text
Topic + current hypothesis + evidence needed + source scope + output artifact
```

### Coding Request

```text
Observed behavior + expected behavior + repro steps + files/logs + validation command
```

### Decision Request

```text
Options + criteria + constraints + risk tolerance + time horizon
```

### Creative Request

```text
Audience + message + format + style references + constraints + delivery channel
```

## Training Mode

Use training mode when the user explicitly asks to improve questioning ability.

```text
Question diagnosis:
- Strength:
- Weak spot:
- Highest-leverage addition:

Better prompt:
{prompt}

Next exercise:
Rewrite one similar request using:
Goal + context + output format + constraints.
```

## Guardrails

- Do not expose hidden chain-of-thought.
- Do not over-coach simple execution requests.
- Prefer concrete rewrites over abstract advice.
- Preserve the user's natural style unless they ask for a different style.
