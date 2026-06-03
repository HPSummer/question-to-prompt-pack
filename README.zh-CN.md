# Question to Prompt Pack

> 一个统一入口：先理解大白话问题，生成简洁提示词包，再判断应该调用哪个 Codex skill。

Question to Prompt Pack 是一个 Codex 技能，用来提升用户和 AI 之间的沟通效率。它不是把提示词越写越长，而是帮助 AI 快速判断：应该直接执行、先问问题、展示简洁协作框架、生成完整提示词包，还是路由到最合适的 skill 执行。

English version: [README.md](README.md)

## 设计目标

这个技能的核心规则是：

```text
用最小的框架，避免最大的误解。
```

统一链路：

```text
用户大白话问题
-> question-to-prompt-pack 对齐意图
-> 内置 skill routing 选择 skill
-> 对应 skill 执行任务
-> 反馈结果回到用户偏好/路由策略
```

它解决的问题：

- 把自然语言问题转成结构化提示词
- 避免过度思考和 token 浪费
- 在执行前展示一个可编辑的理解框架
- 判断这件事应该调用哪个 skill
- 用一句可复用模式训练用户下次怎么问
- 用本地 profile 保留非敏感协作偏好
- 保留用户原本的大白话风格
- 根据用户反馈形成当前线程的工作偏好

## 核心模式

- `Tiny Frame`：默认模式，适合简单请求，省 token
- `Compact Frame`：用户想检查 AI 如何理解问题时使用
- `Full Frame`：复杂任务，需要假设、约束和质量标准时使用
- `Training Frame`：用户想训练提问能力时使用
- `Skill Route`：需要执行复杂任务时，选择最合适的 skill
- `Direct Execution`：用户明确说“直接做”时跳过框架

## 提问训练闭环

当用户想提升提问能力，或某个问题明显缺少关键上下文时，输出一个很短的训练块：

```text
提问升级：
- 缺失信息：
- 为什么重要：
- 下次复用模板：
```

默认模板：

```text
目标 + 背景 + 输出格式 + 约束 + 执行模式
```

普通执行请求不会强行教学，避免浪费 token。

## 示例

更多完整示例见：

- [Before / After Demos](examples/before-after.md)
- [科研用户 profile 示例](examples/researcher-profile.json)

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

路由：
- Task type: planning
- Best skill: none
- Confidence: high
- Next action: answer directly

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
    question-coaching.md
    skill-routing.md
    test-cases.md
    user-style-profile.md
  assets/
    user-style-profile.schema.json
  scripts/
    build_local_index.py
    check_skill_rules.py
    discover_skill_metadata.py
    eval_routes.py
    profile_manager.py
    search_skill_index.py
    validate_unified_cases.py
benchmarks/
  unified-cases.jsonl
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
请先展示你如何理解我的问题框架，让我调整后再生成最终提示词，并判断应该调用哪个 skill。
```

直接执行：

```text
使用 $question-to-prompt-pack：
直接把下面的问题改成最终提示词，不要展示框架。
```

统一执行入口：

```text
使用 $question-to-prompt-pack：
先理解我的需求，再判断应该调用哪个 skill，最后给出最小执行方案。

我想做一个个人科研效率工具 MVP。
```

初始化本地用户风格 profile：

```powershell
python .\question-to-prompt-pack\scripts\profile_manager.py --init --validate
```

验证统一链路 benchmark：

```powershell
python .\question-to-prompt-pack\scripts\validate_unified_cases.py --cases .\benchmarks\unified-cases.jsonl
```

当前 benchmark 包含 50 条真实用户风格问题，覆盖科研、代码、写作、PDF、图像、视频、自动化、决策和模糊输入。

## 许可证

MIT。见 [LICENSE](LICENSE)。
