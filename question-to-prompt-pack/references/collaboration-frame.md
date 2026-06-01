# Collaboration Frame

Use the user's language in final output. This reference is ASCII for robust loading on Windows.

## Purpose

A Collaboration Frame converts a rough question into a shared work contract between user and AI. It is designed to improve communication and execution efficiency before the final prompt or answer is produced.

## Compact Template

```markdown
## Raw Question
> {raw question}

## Collaboration Frame

- Intent: {what the user is trying to accomplish}
- Task Type: {research / writing / coding / planning / decision / learning / creative / video / other}
- Context Needed: {missing background that would improve accuracy}
- Constraints: {time, format, style, tools, depth, risk, scope}
- Output Shape: {answer, table, plan, prompt, code, checklist, storyboard, etc.}
- Success Criteria: {what makes the output useful}
- Execution Mode: {answer directly / clarify first / plan first / implement / verify / iterate}

## Adjustable Assumptions

- {assumption 1}
- {assumption 2}
- {assumption 3}

## Adjustment Menu

A. Refine goal
B. Add context
C. Change depth/detail
D. Change tone/style
E. Change output format
F. Add verification/risk checks
G. Generate final prompt now
```

## Tiny Template

Use this unless the user explicitly asks for deeper framing.
Keep it under roughly 180 Chinese characters or 120 English words when possible.

```markdown
I understand this as:
- Goal: {goal}
- Missing/assumed context: {context}
- Best output: {output}
- Mode: {mode}

Draft prompt:
{prompt}

Say "expand" if you want the full collaboration frame.
```

## Depth Switches

- `tiny`: 4 bullets + prompt
- `compact`: 7 collaboration fields, one line each
- `full`: compact + assumptions + adjustment menu + quality criteria
- `training`: full + score + feedback + next exercise

Start tiny. Upgrade only when needed.

## Understanding Confidence

Use confidence to avoid wasting tokens.

| Confidence | Use when | Default behavior |
|---|---|---|
| High | goal/output obvious, low risk | tiny or direct execution |
| Medium | goal clear but format/depth may vary | tiny with assumptions or compact |
| Low | intent unclear, high stakes, missing context changes result | clarify first or full |

## Hard Trigger Table

| Signal | Frame |
|---|---|
| direct execution request | no frame unless blocked |
| save tokens / quick / short | tiny |
| turn this into a prompt | tiny |
| show framing / adjust understanding | compact or full |
| train my questioning | training |
| high stakes / current facts | compact with verification |

## Result Feedback Loop

Use when testing or calibrating:

```text
Quick feedback?
A. Useful - keep this structure
B. Direction right, but too long
C. Direction right, but too shallow
D. Misunderstood my intent
E. Need more verification/risk checks
```

Map feedback to behavior:

- A -> keep frame depth and output shape
- B -> reduce depth
- C -> increase depth or quality criteria
- D -> rebuild frame
- E -> raise verification level

## Final Prompt Template

```text
I want you to help with: {task}.

Context:
{context}

Goal:
{goal}

Constraints:
{constraints}

Please output:
{output shape}

Quality criteria:
- {criterion 1}
- {criterion 2}
- {criterion 3}

If information is missing:
Ask up to 3 clarifying questions before answering, unless the missing detail is low-risk.

Verification:
{how to check assumptions, sources, tests, risks, or alternatives}
```

## Communication Feedback Template

```markdown
## Why This Helps Our Communication

Your original question contained {strength}. The frame adds {main missing structure}. This helps me avoid {likely wasted path} and move faster toward {useful output}.

Next time, you can improve similar questions by adding:
{one short rule}
```

## Mode Selection

Use `Answer Directly` when:
- goal and output are obvious
- the request is low risk
- user likely wants speed

Use `Clarify First` when:
- missing context changes the result
- user asks for personalization
- stakes are high

Use `Plan First` when:
- work has multiple stages
- there are tradeoffs
- user needs to choose direction

Use `Implement` when:
- user wants a file, code change, video, artifact, or concrete output

Use `Verify` when:
- facts may be stale
- correctness matters
- tests, citations, or sources are needed

Use `Iterate` when:
- creative direction is unclear
- user wants to select among interpretations

## Example

Raw:

```text
I want to make my questions better.
```

Frame:

```markdown
- Intent: build a repeatable way to turn rough questions into strong prompts
- Task Type: learning + prompt design
- Context Needed: target use cases and preferred answer style
- Constraints: should preserve user's natural style, not become stiff
- Output Shape: collaboration frame + final prompt template
- Success Criteria: user can inspect and adjust the AI's understanding before execution
- Execution Mode: iterate
```
