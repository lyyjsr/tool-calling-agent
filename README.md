# Tool-Calling Agent

一个基于 Python 实现的最小工具调用型 Agent 项目。

## 项目目标
构建一个可以接收自然语言输入、识别用户意图，并在后续调用不同工具完成任务的 Agent 助手。

## 当前已实现
- CLI 输入输出
- 基于规则的意图识别（router）
- 响应生成模块
- 基础测试

## 当前支持的意图
- greet
- weather
- github
- calculate
- unknown

## 当前已实现
- CLI 输入输出
- 基于规则的意图识别（router）
- calculator tool
- GitHub user query tool
- 基础测试

## 当前支持的请求
- calculate 2 + 2
- 计算 5 * 6
- github openai
- 查询 github 用户 torvalds

## 项目能力
Agent 可根据用户输入识别意图，并路由到不同工具执行任务。目前已支持本地计算和 GitHub 用户公开信息查询。

## 项目结构
```bash
tool-calling-agent/
├─ src/
│  ├─ main.py
│  ├─ router.py
│  ├─ schemas.py
│  └─ responder.py
├─ tests/
│  └─ test_router.py
├─ README.md
├─ requirements.txt
└─ .gitignore