# Golden Examples

Use these as style anchors when validating the skill. Keep outputs compact.

## Example 1: Tiny Frame

User:

```text
Save tokens. Turn this into a better prompt: help me plan tomorrow.
```

Expected:

```text
I understand this as:
- Goal: create a practical plan for tomorrow
- Missing/assumed context: assume work + personal tasks
- Best output: time blocks + top priorities
- Mode: tiny prompt rewrite

Draft prompt:
Help me plan tomorrow with time blocks, top 3 priorities, realistic breaks, and a fallback version if the day gets busy. Ask up to 3 questions first only if needed.

Say "expand" if you want the full collaboration frame.
```

## Example 2: Frame First

User:

```text
Before making the prompt, show how you understand my question framework.
```

Expected:

```text
Raw Question
> Before making the prompt, show how you understand my question framework.

Collaboration Frame
- Intent: inspect and adjust the AI's interpretation before prompt generation
- Task Type: prompt co-creation
- Context Needed: the actual rough question to transform
- Constraints: keep framing concise and editable
- Output Shape: collaboration frame, then final prompt after confirmation
- Success Criteria: user can correct intent, depth, tone, or output before generation
- Execution Mode: iterate

Adjustable Assumptions
- You want visible structure, not hidden reasoning.
- You prefer concise framing before final output.

Adjustment Menu
A. Refine goal
B. Add context
C. Change depth/detail
D. Change tone/style
E. Change output format
F. Add verification/risk checks
G. Generate final prompt now
```

## Example 3: Feedback Loop

User:

```text
This was useful, but too long.
```

Expected:

```text
Got it. I will treat this as local calibration: keep the same structure, but reduce depth and default to Tiny Frame for similar prompt-building tasks in this thread.

Revised version:
{shorter output}
```
