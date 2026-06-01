# Question to Prompt Pack

> 把大白话问题转成简洁的协作框架和可复制提示词。

Question to Prompt Pack 是一个 Codex 技能，用来提升用户和 AI 之间的沟通效率。它不是把提示词越写越长，而是帮助 AI 快速判断：应该直接执行、先问问题、展示简洁协作框架，还是生成完整提示词包。

English version: [README.md](README.md)

## 设计目标

这个技能的核心规则是：

```text
用最小的框架，避免最大的误解。
```

它解决的问题：

- 把自然语言问题转成结构化提示词
- 避免过度思考和 token 浪费
- 在执行前展示一个可编辑的理解框架
- 保留用户原本的大白话风格
- 根据用户反馈形成当前线程的工作偏好

## 核心模式

- `Tiny Frame`：默认模式，适合简单请求，省 token
- `Compact Frame`：用户想检查 AI 如何理解问题时使用
- `Full Frame`：复杂任务，需要假设、约束和质量标准时使用
- `Training Frame`：用户想训练提问能力时使用
- `Direct Execution`：用户明确说“直接做”时跳过框架

## 示例

用户输入：

```text
使用 $question-to-prompt-pack，省 token：
把这个问题变成更好的提示词：我想规划明天。
```

理想输出风格：

```text
我理解为：
- 目标：制定明天的可执行安排
- 缺失/假设：默认包含工作、学习和休息
- 最佳输出：时间块 + 优先级清单
- 模式：Tiny prompt rewrite

草稿提示词：
请帮我制定明天的一日计划，包括时间块、最重要的 3 件事、合理休息，以及如果当天被打断时的降级版本。如信息不足，最多先问 3 个问题。

如果想看完整协作框架，请说“展开”。
```

## 安装

把技能目录复制到 Codex 的 skills 目录：

```powershell
Copy-Item -LiteralPath .\question-to-prompt-pack -Destination "$env:USERPROFILE\.codex\skills\question-to-prompt-pack" -Recurse -Force
```

然后重启或刷新 Codex，让技能列表重新加载。

## 校验

运行内置规则检查：

```powershell
python .\question-to-prompt-pack\scripts\check_skill_rules.py
```

如果本机有系统技能创建器，也可以运行：

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .\question-to-prompt-pack
```

## 目录结构

```text
question-to-prompt-pack/
  SKILL.md
  agents/openai.yaml
  references/
    collaboration-frame.md
    golden-examples.md
    interactive-workflow.md
    prompt-pack-patterns.md
    test-cases.md
  scripts/
    check_skill_rules.py
```

## 使用建议

简单问题：

```text
使用 $question-to-prompt-pack，省 token：
把这个问题转成更好的提示词：我想安排明天。
```

需要检查理解：

```text
使用 $question-to-prompt-pack：
请先展示你如何理解我的问题框架，让我调整后再生成最终提示词。
```

直接执行：

```text
使用 $question-to-prompt-pack：
直接把下面的问题改成最终提示词，不要展示框架。
```

## 许可证

MIT。见 [LICENSE](LICENSE)。
