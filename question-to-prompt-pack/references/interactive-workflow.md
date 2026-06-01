# Interactive Workflow

Use this only when the user wants to inspect or adjust the frame before final prompt generation.

## Selection Handling

Accept letter choices and natural language.

- A / refine goal: revise the intended outcome.
- B / add context: collect only the context that changes the result.
- C / depth: choose shorter, normal, deeper, or expert.
- D / tone: choose casual, direct, academic, persuasive, technical, etc.
- E / format: choose checklist, table, plan, prompt, code, storyboard, etc.
- F / verification: add sources, tests, risk checks, assumptions, or counterexamples.
- G / generate: produce the final prompt.

If the user gives several changes at once, apply them together.

## Minimal Clarification Rule

Ask at most 3 questions. Prefer fillable slots over open-ended interviews.

Bad:

```text
Tell me more about your background.
```

Better:

```text
Fill any that matter: audience={}; deadline={}; output format={}.
```

## Habit Detection

Treat a preference as a working habit only if:

1. the user explicitly states it, or
2. it appears repeatedly and is low-risk, or
3. the user accepts it after you name it.

Examples:

- prefers Chinese
- wants concise frames before execution
- likes direct implementation after alignment
- prefers structured bullets over long essays
- works often on research, AI tooling, video, skills, or code

## Feedback-Based Updates

When the user gives feedback on a generated prompt or result:

- "too long" -> lower default depth for similar tasks
- "too shallow" -> add depth or quality criteria for similar tasks
- "you misunderstood" -> rebuild the frame before generating again
- "this structure works" -> keep output shape as a working preference
- "needs verification" -> raise verification level for similar tasks

Do not treat frustration or one-off corrections as permanent preferences. Treat them as local calibration unless repeated or confirmed.

Detailed feedback menu:

```text
Quick feedback?
A. Useful - keep this structure
B. Direction right, but too long
C. Direction right, but too shallow
D. Misunderstood my intent
E. Need more verification/risk checks
```

Mapping:

- A -> keep frame depth and output shape as a working preference
- B -> reduce depth and default to Tiny Frame next time
- C -> increase depth or add quality criteria next time
- D -> rebuild the Collaboration Frame before rewriting
- E -> raise verification level for similar tasks

## Habit Note

Use one short sentence:

```text
I will treat this as a working preference in this thread: {preference}.
```

Do not persist to disk unless the user explicitly asks.

## Habit Profile Schema

Use this schema when a structured profile is needed:

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

Leave unknown fields blank. Do not infer sensitive fields.
