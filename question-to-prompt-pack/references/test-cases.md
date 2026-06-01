# Test Cases

These cases are for maintainers validating the skill. Do not load unless improving the skill.

## Case 1: Learning / Research

Raw:

```text
I want to improve my research ability. What should I do?
```

Expected behavior:
- Show an interpretation card first if the user asks to inspect the thinking.
- Ask or infer field, current level, available time, and target ability.
- Produce a training-plan prompt, not generic advice.
- Include weekly artifact and review loop.
- Feedback should teach: baseline + target + time + metric.

## Case 2: Content / Video

Raw:

```text
Help me make an explainer video.
```

Expected behavior:
- Show topic, audience, runtime, platform, tone, and asset assumptions.
- Let user choose style/depth before final prompt.
- Produce a prompt that separates script, storyboard, visuals, voiceover, subtitles, and publishing metadata.
- Include habit note if user prefers a repeatable video workflow.

## Case 3: Decision

Raw:

```text
Is this software worth buying?
```

Expected behavior:
- Request tool name, use case, alternatives, budget, privacy/security needs, and time horizon.
- Produce a decision prompt with options, tradeoffs, assumptions, and current-fact verification.
- Feedback should teach: decision question = options + criteria + constraints.

## Case 4: Coding

Raw:

```text
Fix this bug.
```

Expected behavior:
- Ask for observed behavior, expected behavior, repro steps, logs, changed files, and validation command.
- Produce a debugging prompt with scope and no unrelated refactor.
- Feedback should teach: bug request = observed vs expected + reproduction + validation.

## Case 5: High-Stakes / Freshness

Raw:

```text
Help me evaluate this investment opportunity.
```

Expected behavior:
- Do not produce financial advice as certainty.
- Require current sources, risk tolerance, time horizon, liquidity needs, and downside scenario.
- Include verification and "not financial advice" framing in the downstream prompt.

## Case 6: Habit-Aware Prompting

Raw:

```text
Use my usual style and turn this into a prompt: I want to build a skill that helps me ask better questions.
```

Expected behavior:
- Preserve known user style if available.
- If no profile exists, infer only low-risk style preferences and name them as assumptions.
- Produce a habit note and ask whether to remember it for the thread.

## Case 7: Collaboration Frame First

Raw:

```text
I need you to turn my rough question into a prompt, but first show me how you understand the whole question framework so I can adjust it.
```

Expected behavior:
- Do not jump straight to a final prompt.
- Produce a Collaboration Frame with intent, task type, context needed, constraints, output shape, success criteria, and execution mode.
- Show adjustable assumptions and an adjustment menu.
- Explain briefly how this improves communication and execution efficiency.
- Wait for user adjustment unless the user explicitly says to generate now.

## Case 8: Token-Saving Simple Request

Raw:

```text
Turn this into a better prompt: help me plan tomorrow.
```

Expected behavior:
- Use Tiny Frame, not Full Frame.
- Keep output under roughly 180 words unless user asks to expand.
- Include goal, missing/assumed context, best output, mode, and a draft prompt.
- End with "say expand" or equivalent.
- Do not include scorecards, long coaching, or many variants.

## Case 9: Direct Execution Override

Raw:

```text
Use this idea and directly write the final prompt. Do not show the frame.
```

Expected behavior:
- Do not show Collaboration Frame.
- State at most one short assumption if needed.
- Produce the final prompt directly.
- Do not add an adjustment menu.

## Case 10: Habit Profile Schema

Raw:

```text
Remember that I prefer concise Chinese outputs with a tiny frame first.
```

Expected behavior:
- Treat it as a thread-level working preference.
- Use the structured habit profile fields: language, tone, answer_structure, depth, default_frame, common_domains, recurring_constraints, verification_level, dislikes.
- Do not claim permanent memory unless persistent storage exists or the user asks for a file.

## Case 11: Understanding Confidence

Raw:

```text
Make this prompt better: summarize this article in 5 bullets.
```

Expected behavior:
- Treat confidence as high.
- Use Tiny Frame or direct prompt rewrite.
- Do not ask unnecessary clarification questions.
- Do not use Full Frame.

## Case 12: Low Confidence

Raw:

```text
Help me evaluate this.
```

Expected behavior:
- Treat confidence as low.
- Do not produce a polished prompt with hidden assumptions.
- Ask what "this" is or produce a compact frame with explicit missing context.

## Case 13: Result Feedback

Raw:

```text
The last prompt was directionally right, but too shallow.
```

Expected behavior:
- Acknowledge calibration.
- Increase depth or add quality criteria for the revised prompt.
- Do not treat it as a permanent preference unless repeated or confirmed.
