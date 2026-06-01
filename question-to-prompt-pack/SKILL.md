---
name: question-to-prompt-pack
description: "Convert a user's natural-language question into a collaboration frame and prompt pack. Use when the user wants their rough question transformed into a clearer communication structure, wants to inspect and adjust the AI's understanding before execution, or wants prompts that improve user-AI communication efficiency and preserve the user's style."
---

# Question To Prompt Pack

## Purpose

Use this skill as a communication alignment layer: convert a rough user question into the smallest useful frame, then generate a copyable prompt or proceed with execution.

Default behavior: save tokens, avoid overthinking, preserve the user's natural style.

## Main Algorithm

1. Preserve the raw question.
2. Estimate understanding confidence.
3. Apply hard trigger rules.
4. Choose the smallest frame that prevents misunderstanding.
5. Generate one prompt or execute directly.
6. Use feedback only when calibrating, testing, or correcting.

## Understanding Confidence

| Confidence | Signs | Behavior |
|---|---|---|
| High | goal/output obvious, low risk | Tiny Frame or direct execution |
| Medium | goal clear but depth/format/context may vary | Tiny with assumptions or Compact |
| Low | intent unclear, high stakes, missing context changes result | Clarify First or Full |

Do not display confidence unless useful.

## Hard Trigger Rules

| User signal | Required behavior |
|---|---|
| direct / just do it / execute | Skip frame unless blocked |
| save tokens / short / quick | Tiny Frame only |
| turn this into a prompt | Tiny Frame + one draft prompt |
| show framing / show understanding / let me adjust | Compact or Full |
| train my questioning / score / teach me how to ask | Training |
| high-stakes or freshness-sensitive | Compact with verification |
| coding implementation | Execute and validate unless ambiguity blocks |
| negative feedback on prior output | Apply feedback loop before regenerating |

Follow explicit user instruction first unless safety, verification, or missing context requires clarification.

## Token Budget Ladder

- `Tiny`: default; 4 bullets max + one draft prompt.
- `Compact`: seven collaboration fields, one line each.
- `Full`: compact + assumptions + adjustment menu + quality criteria.
- `Training`: full + score + feedback + next exercise.

Tiny limits:
- one draft prompt only
- no scorecard
- no long coaching
- no multiple variants
- no reference-file loading
- target under 180 Chinese characters or 120 English words when possible

## Tiny Frame

```text
I understand this as:
- Goal:
- Missing/assumed context:
- Best output:
- Mode:

Draft prompt:
{copyable prompt}

Say "expand" if you want the full collaboration frame.
```

## Compact Frame Fields

Use these fields when the user wants to inspect or adjust understanding:

- Intent
- Task Type
- Context Needed
- Constraints
- Output Shape
- Success Criteria
- Execution Mode

## Execution Modes

- `Answer Directly`
- `Clarify First`
- `Plan First`
- `Implement`
- `Verify`
- `Iterate`

## Feedback Loop

Use only during testing, calibration, or correction:

- useful -> keep structure
- too long -> reduce depth
- too shallow -> increase depth or quality criteria
- misunderstood -> rebuild frame
- needs verification -> raise verification level

Do not ask for feedback after every response.

## Habit Profile

Track only non-sensitive, useful thread-level preferences:

```text
User Prompt Habit Profile
- language:
- tone:
- answer_structure:
- depth:
- default_frame:
- common_domains:
- recurring_constraints:
- verification_level:
- dislikes:
```

Lifecycle:
- one occurrence: assumption only
- repeated occurrence: working thread preference
- explicit confirmation: stable thread preference
- user correction: override immediately

Do not claim long-term memory unless persistent storage exists and the user requests it.

## Guardrails

- Do not expose hidden chain-of-thought; show concise user-facing framing only.
- Do not invent preferences from one message unless marked as assumptions.
- Ask at most 3 clarifying questions.
- Add verification for current, technical, legal, medical, financial, or research claims.
- For coding tasks, include artifacts and validation.
- For creative/video tasks, include audience, message, format, style, script/structure, and publishing constraints.

## References

- `references/collaboration-frame.md`: templates, confidence, trigger table.
- `references/interactive-workflow.md`: user adjustments, habit updates, feedback menu.
- `references/prompt-pack-patterns.md`: full prompt pack patterns and domain adaptors.
- `references/golden-examples.md`: style anchors for validation/debugging only.
