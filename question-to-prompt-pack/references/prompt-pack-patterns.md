# Prompt Pack Patterns

Use the user's language in the final answer. This reference is written in ASCII for robust loading on Windows.

## Full Prompt Pack Template

```markdown
## Raw Question
> {user's original wording}

## Question Diagnosis
- Goal: {clear / vague; what is missing}
- Context: {available / missing}
- Constraints: {available / missing}
- Criteria: {available / missing}
- Verification: {whether fact-checking, counterexamples, risk checks, or tests are needed}

## Enhanced Prompt
{a complete prompt the user can paste into an AI}

## Context Slots
To improve the answer further, add:
1. {key missing detail 1}
2. {key missing detail 2}
3. {key missing detail 3}

## Follow-up Path
1. {make the answer more concrete}
2. {make the answer more actionable}
3. {surface assumptions or risks}
4. {ask for counterexamples or alternatives}
5. {compress into next actions}

## Quality Bar
A good answer should:
- {criterion 1}
- {criterion 2}
- {criterion 3}

## Prompt Fitness Score
Goal: {0-5}
Context: {0-5}
Constraints: {0-5}
Criteria: {0-5}
Verification: {0-5}
Main upgrade: {one sentence}

## Questioning Feedback
Your original question already had {strength}. The main thing to strengthen is {gap}. Next time, start by saying: {reusable reminder}.

## Why This Prompt Works
- Goal: {how the prompt clarifies the goal}
- Context: {what context is included or still missing}
- Constraints: {what narrows the answer}
- Criteria: {how the AI knows what good means}
- Verification: {how the answer should be checked}

## Next Rep
{one tiny exercise the user can do next time}

## Habit Note
{style or preference preserved; any habit that should be remembered in this thread}

## Reusable Template
{template with bracketed slots}
```

## Enhanced Prompt Skeleton

```text
I want you to help with this task/problem: {task}.

Background:
{identity, situation, available materials, audience, current progress}

Goal:
{what output or decision is needed}

Constraints:
{time, length, format, difficulty, style, tools, no-go areas}

Please output:
1. {output item 1}
2. {output item 2}
3. {output item 3}

Quality requirements:
- Be specific, not generic.
- Make each recommendation actionable.
- State assumptions and uncertainty.
- If key information is missing, ask up to 3 clarifying questions first.
- If my idea has problems, point them out directly and suggest corrections.
```

## Follow-up Prompt Bank

Use only the prompts that fit the task.

- "Which parts of this answer are still too generic? Rewrite them as concrete actions."
- "List the key assumptions behind your answer. What changes if they are false?"
- "Critique this from an opponent's point of view."
- "Give 3 alternative approaches and compare where each fits."
- "Compress this into 3 actions I can take today."
- "Separate facts, inferences, and recommendations."
- "Name the most likely failure point and give a fallback plan."
- "If I am a beginner, which step is easiest to misunderstand? Re-explain it."
- "Give me one example input and one example output."
- "Summarize the decision criteria in a table."

## Domain Adaptors

### Learning

Add:
- current level
- target skill
- available time
- preferred learning style
- measurable weekly output

Quality bar:
- has daily/weekly cadence
- has practice tasks
- has feedback loop
- has a minimum viable version for busy days

### Research

Add:
- research field
- current hypothesis
- available literature/data
- target venue or output
- novelty and validation criteria

Quality bar:
- distinguishes known work from speculation
- proposes testable questions
- includes evidence plan
- names failure modes

### Writing

Add:
- audience
- purpose
- tone
- length
- source material
- examples to imitate or avoid

Quality bar:
- has a clear thesis
- has coherent structure
- matches the audience
- avoids empty slogans

### Coding

Add:
- repo/file context
- observed behavior
- expected behavior
- constraints
- validation command

Quality bar:
- has scoped objective
- preserves behavior outside scope
- includes tests or verification path
- avoids unrelated refactor

### Decision / Strategy

Add:
- decision to make
- options already considered
- constraints
- risk tolerance
- time horizon
- success metric

Quality bar:
- compares options
- exposes assumptions
- includes risks and tradeoffs
- ends with recommendation and next step

### Content / Video

Add:
- target platform
- audience
- desired runtime
- tone
- visual style
- publishing constraints

Quality bar:
- has a concrete message
- has a shot or section structure
- has narration and subtitle rules
- ends with an action or memorable takeaway

### Prompt Co-Creation

Add:
- raw question
- visible interpretation
- adjustable assumptions
- user choices
- final prompt
- habit note

Quality bar:
- user can correct the AI's interpretation
- assumptions are visible
- final prompt preserves user style
- reusable preference is named

## Example Transformations

### Learning Example

Raw:

```text
I want to improve my research ability. What should I do?
```

Enhanced:

```text
I am a {level/role} in {field}. I want to improve my research ability over the next {time period}, especially {paper reading / topic selection / experiments / writing / submission}.

My current situation:
- Weekly available time: {time}
- Current foundation: {courses, papers, code, experiments}
- Biggest blocker: {blocker}

Design a 4-week training plan. Requirements:
1. Each week has a clear training objective.
2. Daily tasks fit within {daily time}.
3. Each week produces one checkable artifact.
4. Name the most likely failure point and fallback.
5. End with a weekly review template.

If key information is missing, ask me up to 3 clarifying questions first.
```

Feedback:

```text
The raw question has a clear direction: improve research ability. It lacks the exact ability dimension, current baseline, time constraint, and checkable output. Next time, say where you are, where you want to go, by when, and how success will be measured.
```

### Decision Example

Raw:

```text
Should I buy this tool?
```

Enhanced:

```text
Help me decide whether to buy {tool}. My goal is {goal}. My current alternatives are {alternatives}. My budget is {budget}, and I care most about {speed / quality / reliability / learning curve / privacy}.

Please compare:
1. Buy the tool now.
2. Use an alternative.
3. Wait and gather more evidence.

For each option, give benefits, risks, hidden costs, and a recommendation. Separate facts from assumptions. If current pricing or product details matter, tell me what needs to be verified.
```

### Coding Example

Raw:

```text
Fix this bug.
```

Enhanced:

```text
Help me debug this issue.

Observed behavior:
{what happens}

Expected behavior:
{what should happen}

Context:
- Repo/files involved: {paths}
- Error/logs: {logs}
- Recent changes: {changes}

Constraints:
- Keep the fix scoped.
- Do not refactor unrelated code.
- Preserve existing behavior outside this bug.

Please:
1. Identify the likely cause.
2. Propose a minimal fix.
3. List the files to inspect or edit.
4. Give a validation command or test plan.

If the reproduction is unclear, ask up to 3 clarifying questions first.
```
