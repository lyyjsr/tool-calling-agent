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
- CLI 多轮交互
- 基于规则的意图识别（router）
- calculator tool
- GitHub user query tool
- 基础会话历史（memory）
- 基础测试

## 项目能力
Agent 可根据用户输入识别意图，并路由到不同工具执行任务。目前已支持本地计算和 GitHub 用户公开信息查询。

## 新增能力
Agent 现在支持在单次运行中保留最近若干轮会话历史，并可通过 `history` 命令查看上下文记录。

## 当前架构
项目当前采用以下模块划分：

- `router.py`：负责用户输入的意图识别
- `dispatcher.py`：负责根据意图分发到不同工具或系统能力
- `tools.py`：封装具体工具逻辑
- `memory.py`：维护会话历史
- `responder.py`：统一生成用户可读响应

## 当前能力
- 多轮 CLI 交互
- 基于规则的意图识别
- calculator tool
- GitHub user query tool
- conversation memory
- dispatcher 调度层


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